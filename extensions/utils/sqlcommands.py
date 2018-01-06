from extensions.utils.importsfile import *


class InternalSQL:
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))
        self.mysqlcache = aiocache.SimpleMemoryCache(serializer=NullSerializer, namespace="mysql")
        self.bot.loop.create_task(self.mysqlstart())

    async def mysqlstart(self):
        mysqlconfigured = self.bot.common.config.getboolean('DONOTTOUCH', 'mysqlconfigured')
        schema = self.bot.common.mysqldb
        if not mysqlconfigured:
            await self.schemacreate()
        else:
            pass
        self.mysqlcon = await aiomysql.create_pool(host=self.bot.common.mysqlserver, port=self.bot.common.mysqlport,
                                                   user=self.bot.common.mysqluser, minsize=5, maxsize=100,
                                                   use_unicode=True, password=self.bot.common.mysqlpw, db=schema,
                                                   autocommit=True, charset='utf8mb4')

    async def schemacreate(self):
        print("MySQL isn't configured yet...\nCreating tables in the Database now...")
        schemacommands = await self.bot.sql.statement_create_bot_schema()
        temp_con = await aiomysql.connect(host=self.bot.common.mysqlserver, port=self.bot.common.mysqlport,
                                          user=self.bot.common.mysqluser, password=self.bot.common.mysqlpw,
                                          charset='utf8mb4', use_unicode=True, autocommit=True)
        async with temp_con.cursor() as cursor:
            for command in schemacommands:
                await cursor.execute(command)
            await cursor.close()
        temp_con.close()
        self.bot.common.config.set('DONOTTOUCH', 'mysqlconfigured', 'True')
        with open(self.bot.common.configfile, 'w') as towrite:
            self.bot.common.config.write(towrite)

    async def statement_create_bot_schema(self):
        infile = open(os.path.join("extensions", "db", "CREATE-bot-schema.sql"), 'r')
        sql_file = infile.read()
        infile.close()
        sql_file1 = sql_file.replace("mysqldb", self.bot.common.mysqldb)
        sql_commands = sql_file1.strip('\n').split(';')[:-1]
        return sql_commands

    async def statement_upsert_weathertable(self, authorid, zipcode):
        sql_query = """REPLACE INTO `{0}`.`_weathertable` (`user-id`, `zipcode`) VALUES ('{1}', '{2}');"""
        new_query = sql_query.format(self.bot.common.mysqldb, str(authorid), str(zipcode))
        return new_query

    async def statement_get_weather_single_user(self, authorid):
        sql_query = """SELECT `zipcode` FROM `{0}`.`_weathertable` WHERE `user-id` = '{1}';"""
        new_query = sql_query.format(self.bot.common.mysqldb, authorid)
        return new_query

    async def statement_insert_channel_new(self, ctx):
        msgtime = str(datetime.datetime.now())
        guildid = str(ctx.guild.id)
        guildname = str(ctx.guild.name)
        channelid = str(ctx.channel.id)
        channelname = str(ctx.channel.name)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            attachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sql_query = """
        INSERT INTO `{0}`.`{1}_{2}_messages` (`time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `content`, `attachmenturl`, `attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sql_query.format(self.bot.common.mysqldb, guildid, channelid)
        query_data = (msgtime, guildid, guildname, channelid, channelname, userid, username, messageid, content,
                      attachmenturl, attachmentfilename)
        table_name = str(guildid + "_" + channelid + "_messages")
        return new_query, table_name, query_data

    async def statement_insert_channel_edit(self, ctx, aftermessage):
        msgtime = str(datetime.datetime.now())
        guildid = str(ctx.guild.id)
        guildname = str(ctx.guild.name)
        channelid = str(ctx.channel.id)
        channelname = str(ctx.channel.name)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        beforecontent = str(ctx.content)
        aftercontent = str(aftermessage.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            beforeattachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            beforeattachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
            afterattachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            afterattachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
        else:
            beforeattachmenturl = "None"
            beforeattachmentfilename = "None"
            afterattachmentfilename = "None"
            afterattachmenturl = "None"
        sqlquery = """
        INSERT INTO `{0}`.`{1}_{2}_edited` (`time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `before-content`, `before-attachmenturl`, `before-attachmentfilename`,
        `after-content`, `after-attachmenturl`, `after-attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        newquery = sqlquery.format(self.bot.common.mysqldb, guildid, channelid)
        querydata = (msgtime, guildid, guildname, channelid, channelname, userid, username, messageid, beforecontent,
                     beforeattachmenturl, beforeattachmentfilename, aftercontent, afterattachmenturl,
                     afterattachmentfilename)
        tablename = str(guildid + "_" + channelid + "_edited")
        return newquery, tablename, querydata

    async def statement_insert_channel_deleted(self, ctx):
        msgtime = str(datetime.datetime.now())
        guildid = str(ctx.guild.id)
        guildname = str(ctx.guild.name)
        channelid = str(ctx.channel.id)
        channelname = str(ctx.channel.name)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        messageid = str(ctx.id)
        originalcreate = str(ctx.created_at)
        if ctx.attachments:
            attachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sqlquery = """
        INSERT INTO `{0}`.`{1}_{2}_deleted` (`time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `original-send-time`, `content`, `attachmenturl`, `attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        newquery = sqlquery.format(self.bot.common.mysqldb, guildid, channelid)
        querydata = (msgtime, guildid, guildname, channelid, channelname, userid, username, messageid, originalcreate,
                     content, str(attachmenturl), str(attachmentfilename))
        tablename = str(guildid + "_" + channelid + "_deleted")
        return newquery, tablename, querydata

    async def statement_insert_dm_new(self, ctx):
        msgtime = str(datetime.datetime.now())
        channelid = str(ctx.channel.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            attachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sqlquery = """
        INSERT INTO `{0}`.`dm_{1}_messages` (`time`, `dm_channel-id`, `user-id`, `user-name`, `message-id`,
        `content`, `attachmenturl`, `attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        newquery = sqlquery.format(self.bot.common.mysqldb, userid)
        querydata = (msgtime, channelid, userid, username, messageid, content, attachmenturl, attachmentfilename)
        tablename = str("dm_" + userid + "_messages")
        return newquery, tablename, querydata

    async def statement_insert_dm_edit(self, ctx, aftermessage):
        msgtime = str(datetime.datetime.now())
        channelid = str(ctx.channel.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        beforecontent = str(ctx.content)
        aftercontent = str(aftermessage.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            beforeattachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            beforeattachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
            afterattachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            afterattachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
        else:
            beforeattachmenturl = "None"
            beforeattachmentfilename = "None"
            afterattachmentfilename = "None"
            afterattachmenturl = "None"
        sqlquery = """
        INSERT INTO `{0}`.`dm_{1}_edited` (`time`, `dm_channel-id`, `user-id`, `user-name`, `message-id`, 
        `before-content`, `before-attachmenturl`, `before-attachmentfilename`, `after-content`, `after-attachmenturl`, 
        `after-attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        newquery = sqlquery.format(self.bot.common.mysqldb, userid)
        querydata = (msgtime, channelid, userid, username, messageid, beforecontent, beforeattachmenturl,
                     beforeattachmentfilename, aftercontent, afterattachmenturl, afterattachmentfilename)
        tablename = str("dm_" + userid + "_edited")
        return newquery, tablename, querydata

    async def statement_insert_dm_deleted(self, ctx):
        msgtime = str(datetime.datetime.now())
        channelid = str(ctx.channel.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        originalsendtime = str(ctx.created_at)
        messageid = str(ctx.id)
        if ctx.attachments:
            attachmenturl = ','.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ','.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sqlquery = """
        INSERT INTO `{0}`.`dm_{1}_deleted` (`time`, `dm_channel-id`, `user-id`, `user-name`, `message-id`, 
        `original-send-time`, `content`, `attachmenturl`, `attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        newquery = sqlquery.format(self.bot.common.mysqldb, userid)
        querydata = (msgtime, channelid, userid, username, messageid, originalsendtime, content, attachmenturl,
                     attachmentfilename)
        tablename = str("dm_" + userid + "_deleted")
        return newquery, tablename, querydata

    async def statement_insert_errorlog(self, ctx, exception):
        msgtime = str(datetime.datetime.now())
        if str('Direct Message') in str(ctx.channel):
            guildid = str("DM")
        else:
            guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.message.content)
        messageid = str(ctx.message.id)
        errormessage = str(exception)
        sqlquery = """
        INSERT INTO `{0}`.`_errorlog` (`time`, `guild-id`, `user-id`, `user-name`, `message-id`, `content`, 
        `errormessage`)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        newquery = sqlquery.format(self.bot.common.mysqldb)
        querydata = (msgtime, guildid, userid, username, messageid, content, errormessage)
        tablename = str(guildid + "_errorlog")
        return newquery, tablename, querydata

    async def statement_insert_voicetable(self, member, after):
        if after.deaf is True:
            serverdeaf = int("1")
        else:
            serverdeaf = int("0")
        if after.mute is True:
            servermute = int("1")
        else:
            servermute = int("0")
        if after.self_deaf is True:
            selfdeaf = int("1")
        else:
            selfdeaf = int("0")
        if after.self_mute is True:
            selfmute = int("1")
        else:
            selfmute = int("0")
        msgtime = str(datetime.datetime.now())
        guildid = str(member.guild.id)
        guildname = str(member.guild.name)
        memberid = str(member.id)
        membername = str(member)
        if after.channel is None:
            voicechannelname = str("None")
            voicechannelid = str("None")
        else:
            voicechannelname = str(after.channel)
            voicechannelid = str(after.channel.id)
        SQLQuery = """INSERT INTO `{0}`.`{1}_voice` (`time`, `guild-id`, `guild-name`, `user-id`, `user-name`,
        `voicechannel-id`, `voicechannel-name`, `selfdeaf`, `selfmute`, `serverdeaf`, `servermute`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        NewQuery = SQLQuery.format(self.bot.common.mysqldb, guildid)
        QueryData = (msgtime, guildid, guildname, memberid, membername, voicechannelid, voicechannelname, selfdeaf,
                     selfmute, serverdeaf, servermute)
        tablename = str(guildid + "_voice")
        return NewQuery, tablename, QueryData

    async def statement_insert_guild_member(self, member, secondaryargs, guild):
        msgtime = str(datetime.datetime.now())
        guildid = str(guild.id)
        guildname = str(guild.name)
        userid = str(member.id)
        username = str(member)
        action = str(secondaryargs)
        SQLQuery = """
        INSERT INTO `{0}`.`{1}_memberlog` (`time`, `guild-id`, `guild-name`, `user-id`, `user-name`, `action`)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        NewQuery = SQLQuery.format(self.bot.common.mysqldb, guildid)
        QueryData = (msgtime, guildid, guildname, userid, username, action)
        tablename = str(guildid + "_memberlog")
        return NewQuery, tablename, QueryData

    async def statement_insert_guild_log(self, guild, joinleave):
        msgtime = str(datetime.datetime.now())
        guildid = str(guild.id)
        guildname = str(guild.name)
        largeguild = int(guild.large)
        guildownername = str(guild.owner)
        guildownerid = str(guild.owner.id)
        numusersonjoin = str(guild.member_count)
        guildcreatedUTC = str(guild.created_at)
        NewQuery = ''
        QueryData = ()
        leavetime = None
        if joinleave == str("join"):
            guildquery = """
            REPLACE INTO `{0}`.`_guildlog` (`firstseen`, `guildid`, `guildname`, `largeguild`, `guild-owner-name`,
            `guild-owner-id`, `number-users-on-join`, `guild-created-date-UTC`, `leavetime`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            NewQuery = guildquery.format(self.bot.common.mysqldb)
            QueryData = (msgtime, guildid, guildname, largeguild, guildownername, guildownerid,
                         numusersonjoin, guildcreatedUTC, leavetime)
        elif joinleave == str("leave"):
            leavetime = str(datetime.datetime.now())
            guildquery = """
            UPDATE `{0}`.`_guildlog` SET `leavetime` = %s WHERE `guildid` = %s
            """
            NewQuery = guildquery.format(self.bot.common.mysqldb)
            QueryData = (leavetime, guildid)
        tablename = str("_guildlog")
        return NewQuery, tablename, QueryData

    async def statement_create_table(self, table_type, table_name):
        if table_type == "voice":
            sqlFilename = "CREATE-voice.sql"
        elif table_type == "member-list":
            sqlFilename = "CREATE-member-list.sql"
        elif table_type == "member-log":
            sqlFilename = "CREATE-member-log.sql"
        elif table_type == "dm-new":
            sqlFilename = "CREATE-dm-message.sql"
        elif table_type == "dm-edited":
            sqlFilename = "CREATE-dm-edited.sql"
        elif table_type == "dm-deleted":
            sqlFilename = "CREATE-dm-deleted.sql"
        elif table_type == "channel-new":
            sqlFilename = "CREATE-messages.sql"
        elif table_type == "channel-edited":
            sqlFilename = "CREATE-edited.sql"
        elif table_type == "channel-deleted":
            sqlFilename = "CREATE-deleted.sql"
        else:
            sqlFilename = None
        if sqlFilename is None:
            pass
        else:
            infile = open(os.path.join("extensions", "db", sqlFilename), 'r')
            sqlFile = infile.read()
            infile.close()
            sqlCommands1 = sqlFile.replace("tablename", table_name)
            sqlCommands = sqlCommands1.replace("mysqldb", self.bot.common.mysqldb)
            return sqlCommands

    async def statement_insert_encountered_users(self):
        sql_query = """
        INSERT INTO `{0}`.`_encountered-users` (`firstseen`, `user-id`, `user-name`)
        VALUES (%s, %s, %s);
        """
        new_query = sql_query.format(self.bot.common.mysqldb)
        return new_query

    async def statement_get_userlist_single_user(self, authorid):
        sql_query = """SELECT `user-id` FROM `{0}`.`_encountered-users` WHERE `user-id` = '{1}';"""
        new_query = sql_query.format(self.bot.common.mysqldb, authorid)
        return new_query

    async def statement_insert_cmdtable(self, ctx):
        msgtime = str(datetime.datetime.now())
        if str("Direct Message") in str(ctx.channel):
            channelid = "DM"
            channelname = "DM"
            guildid = "DM"
            guildname = "DM"
        else:
            channelid = str(ctx.channel.id)
            channelname = str(ctx.channel.name)
            guildid = str(ctx.guild.id)
            guildname = str(ctx.guild.name)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.message.content)
        messageid = str(ctx.message.id)
        sqlquery = """INSERT INTO `{0}`.`_commandtable` (`time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `content`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sqlquery.format(self.bot.common.mysqldb)
        query_data = (msgtime, guildid, guildname, channelid, channelname, userid, username, messageid, content)
        return new_query, query_data

    async def statement_insert_guildconfig(self, ctx, channellist: list, responses: list, joinpartmsgs: list):
        with open(os.path.join("extensions", "utils", "botconfig-lines.txt"), encoding='utf-8', mode='r') as infile:
            botconfigscript = infile.read().split("%%\n")
        if (str(joinpartmsgs[0]) == str(botconfigscript[25])) and (str(joinpartmsgs[1]) == str(botconfigscript[26])):
            joinmessage = str(botconfigscript[25])
            partmessage = str(botconfigscript[26])
        else:
            joinmessage = str(joinpartmsgs[0])
            partmessage = str(joinpartmsgs[1])
        configtime = str(datetime.datetime.now())
        guildid = str(ctx.guild.id)
        whoconfiged = str(ctx.author)
        initialchan = str(channellist[0].id)
        welcomechan = str(channellist[1].id)
        adminlogchan = str(channellist[2].id)
        voicelogchan = str(channellist[3].id)
        awoochan = str(channellist[4].id)
        enableawoos = bool(responses[4])
        enablelogging = bool(responses[0])
        welcomechanbool = bool(responses[1])
        adminlogchanbool = bool(responses[2])
        voicelogchanbool = bool(responses[3])
        isconfigged = 1
        configquery = """
        REPLACE INTO `{0}`.`_serverconfig` (`guild-id`, `isconfigged`, `initialchannel`, `whoconfiged`, `lastconfiged`, 
        `enablelogging`, `enableusewelcome`, `enableadminlogs`, `enablevoicelogs`, `welcomechannel`, `adminchannel`,
        `voicelogchannel`, `awoochannel`, `enableawoo`, `partmessage`, `welcomemessage`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        new_query = configquery.format(self.bot.common.mysqldb)
        query_data = (guildid, isconfigged, initialchan, whoconfiged, configtime, enablelogging, welcomechanbool,
                     adminlogchanbool, voicelogchanbool, welcomechan, adminlogchan, voicelogchan, awoochan, enableawoos,
                     partmessage, joinmessage)
        return new_query, query_data

    async def statement_get_server_config(self, guild):
        guildid = str(guild.id)
        sql_query = """
        SELECT * 
        FROM `{0}`.`_serverconfig`
        WHERE `guild-id` = {1};
        """
        new_query = sql_query.format(self.bot.common.mysqldb, guildid)
        table_name = str("_serverconfig")
        return new_query, table_name

    async def statement_get_initialchannel(self):
        sql_query = """
        SELECT `guild-id`, `initialchannel`
        FROM `{0}`.`_serverconfig`
        """
        new_query = sql_query.format(self.bot.common.mysqldb)
        return new_query

    async def statement_get_awoolist(self):
        sql_query = """
        SELECT `awoochannel` 
        FROM `{0}`.`_serverconfig`
        WHERE `enableawoo` = '1';
        """
        new_query = sql_query.format(self.bot.common.mysqldb)
        return new_query


# beginning framework for dynamic table, row, column, and statement generator
# this is going to be messy
# no promises lollllllll
# class MySQLFramework:
#     def __init__(self, bot):
#         self.bot = bot
#         print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
#               + ': Addon "{}" loaded'.format(self.__class__.__name__))
#
#     async def tablecreate(self):
#         pass
#
#     async def columns(self):
#         pass
#
#     async def statement_generator(self):
#         pass
