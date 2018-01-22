from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class InternalSQL:
    def __init__(self, bot):
        self.bot = bot
        self.bot.sql = self
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')
        self.bot.mysqlcache = aiocache.SimpleMemoryCache(serializer=NullSerializer, namespace="mysql")
        self.bot.mysqltask = self.bot.loop.create_task(self.mysqlstart())

    def __unload(self):
        """cleans up sql connections"""
        self.bot.loop.run_until_complete(self.mysqlclose())

    async def mysqlclose(self):
        await self.bot.mysqlcon.close()

    async def mysqlstart(self):
        mysqlconfigured = self.bot.common.config.getboolean('DONOTTOUCH', 'mysqlconfigured')
        schema = self.bot.common.mysqldb
        if not mysqlconfigured:
            await self.schemacreate()
        else:
            pass
        self.bot.mysqlcon = await aiomysql.create_pool(host=self.bot.common.mysqlserver, port=self.bot.common.mysqlport,
                                                       user=self.bot.common.mysqluser, minsize=10, maxsize=250,
                                                       use_unicode=True, password=self.bot.common.mysqlpw, db=schema,
                                                       autocommit=True, charset='utf8mb4')

    async def statement_get_prefixes(self):
        sqlcmd = """SELECT `guildid`, `prefix` FROM `{0}`.`prefixes` """
        newcmd = sqlcmd.format(self.bot.common.mysqldb)
        return newcmd

    async def statement_get_single_prefix(self):
        sqlcmd = """SELECT `prefix` FROM `{0}`.`prefixes` WHERE `guildid` = '{1}'"""
        return sqlcmd

    async def statement_insert_prefix(self, guildid, prefix):
        sqlcmd = """INSERT INTO `{0}`.`prefixes` (`guildid`, `prefix`)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE    
        `guildid` = %s, `prefix` = %s;
        """
        newcmd = sqlcmd.format(self.bot.common.mysqldb).replace("\n", "")
        querydata = (str(guildid), str(prefix), str(guildid), str(prefix))
        return newcmd, querydata

    async def schemacreate(self):
        schemacommands = await self.bot.sql.statement_create_bot_schema()
        temp_con = await aiomysql.connect(host=self.bot.common.mysqlserver, port=self.bot.common.mysqlport,
                                          user=self.bot.common.mysqluser, password=self.bot.common.mysqlpw,
                                          charset='utf8mb4', use_unicode=True, autocommit=True)
        for command in schemacommands:
            async with temp_con.cursor() as cursor:
                await cursor.execute(command)
        self.bot.common.config.set('DONOTTOUCH', 'mysqlconfigured', 'True')
        with open(self.bot.common.configfile, 'w') as towrite:
            self.bot.common.config.write(towrite)

    async def statement_create_bot_schema(self):
        infile = open(os.path.join("extensions", "utils", "bot-schema.sql"), 'r')
        sql_file = infile.read()
        infile.close()
        sql_file1 = sql_file.replace("mysqldb", self.bot.common.mysqldb)
        sql_commands = sql_file1.strip('\n').split(';')[:-1]
        newsql = []
        for line in sql_commands:
            newsql += [line.replace("\n", "")]
        return sql_commands

    async def statement_upsert_weathertable(self, authorid, zipcode):
        sqlquery = """
                INSERT INTO `{0}`.`_weathertable` (`user-id`, `zipcode`)
                VALUES(%s, %s)
                ON DUPLICATE KEY UPDATE    
                `zipcode` = %s
                """
        newquery = sqlquery.format(self.bot.common.mysqldb)
        querydata = (authorid, zipcode, zipcode)
        return newquery, querydata

    async def statement_get_weather_single_user(self, authorid):
        sql_query = """SELECT `zipcode` FROM `{0}`.`_weathertable` WHERE `user-id` = '{1}';"""
        new_query = sql_query.format(self.bot.common.mysqldb, authorid)
        return new_query

    async def statement_insert_channel_new(self, ctx):
        createtime = str(ctx.created_at)
        guildid = str(ctx.guild.id)
        guildname = str(ctx.guild.name)
        channelid = str(ctx.channel.id)
        channelname = str(ctx.channel.name)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            attachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sql_query = """
        INSERT INTO `{0}`.`_messages` (`create-time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `content`, `attachmenturl`, `attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sql_query.format(self.bot.common.mysqldb, guildid, channelid)
        query_data = (createtime, guildid, guildname, channelid, channelname, userid, username, messageid, content,
                      attachmenturl, attachmentfilename)
        table_name = str("_messages")
        return new_query, table_name, query_data

    async def statement_insert_channel_edit(self, ctx, aftermessage):
        createtime = str(ctx.created_at)
        isedited = 1
        guildid = str(ctx.guild.id)
        edittime = str(aftermessage.edited_at)
        guildname = str(ctx.guild.name)
        channelid = str(ctx.channel.id)
        channelname = str(ctx.channel.name)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        beforecontent = str(ctx.content)
        aftercontent = str(aftermessage.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            beforeattachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            beforeattachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
            afterattachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            afterattachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
        else:
            beforeattachmenturl = "None"
            beforeattachmentfilename = "None"
            afterattachmentfilename = "None"
            afterattachmenturl = "None"
        sqlquery = """
        INSERT INTO `{0}`.`_messages` (`create-time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `content`, `attachmenturl`, `attachmentfilename`, `isedited`, 
        `edit-time`, `edit-before-content`, `edit-after-content`, `edit-before-attachmenturl`,
        `edit-before-attachmentfilename`, `edit-after-attachmenturl`, `edit-after-attachmentfilename`) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE    
        `isedited` = %s, `edit-time` = %s, `edit-before-content` = %s, `edit-after-content` = %s,
        `edit-before-attachmenturl` = %s, `edit-before-attachmentfilename` = %s, 
        `edit-after-attachmenturl` = %s, `edit-after-attachmentfilename` = %s;
        """
        newquery = sqlquery.format(self.bot.common.mysqldb)
        querydata = (createtime, guildid, guildname, channelid, channelname, userid, username, messageid,
                     beforecontent, beforeattachmenturl, beforeattachmentfilename, isedited, edittime, beforecontent,
                     aftercontent, beforeattachmenturl, beforeattachmentfilename, afterattachmenturl,
                     afterattachmentfilename, isedited, edittime, beforecontent, aftercontent, beforeattachmenturl,
                     beforeattachmentfilename, afterattachmenturl, afterattachmentfilename)
        tablename = str("_messages")
        return newquery, tablename, querydata

    async def statement_insert_channel_deleted(self, ctx):
        createtime = str(ctx.created_at)
        isdeleted = 1
        deletetime = str(datetime.datetime.now())
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
            attachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sqlquery = """
        INSERT INTO `{0}`.`_messages` (`create-time`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, 
        `user-id`, `user-name`, `message-id`, `content`, `attachmenturl`, `attachmentfilename`, `isdeleted`, 
        `delete-time`) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE    
        `isdeleted` = %s, `delete-time` = %s;
        """
        newquery = sqlquery.format(self.bot.common.mysqldb)
        querydata = (createtime, guildid, guildname, channelid, channelname, userid, username, messageid, content,
                     str(attachmenturl), str(attachmentfilename), isdeleted, deletetime, isdeleted, deletetime)
        tablename = str("_messages")
        return newquery, tablename, querydata

    async def statement_insert_dm_new(self, ctx):
        createtime = str(ctx.created_at)
        channelid = str(ctx.channel.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            attachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sql_query = """
        INSERT INTO `{0}`.`_dm_messages` (`create-time`, `dm_channel-id`, `user-id`, `user-name`, `message-id`, `content`, 
        `attachmenturl`, `attachmentfilename`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sql_query.format(self.bot.common.mysqldb)
        query_data = (createtime, channelid, userid, username, messageid, content, attachmenturl, attachmentfilename)
        table_name = str("_dm_messages")
        return new_query, table_name, query_data

    async def statement_insert_dm_edit(self, ctx, aftermessage):
        createtime = str(ctx.created_at)
        isedited = 1
        channelid = str(ctx.channel.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        beforecontent = str(ctx.content)
        aftercontent = str(aftermessage.content)
        messageid = str(ctx.id)
        edittime = str(aftermessage.edited_at)
        if ctx.attachments:
            beforeattachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            beforeattachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
            afterattachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            afterattachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
        else:
            beforeattachmenturl = "None"
            beforeattachmentfilename = "None"
            afterattachmentfilename = "None"
            afterattachmenturl = "None"
        sqlquery = """
        INSERT INTO `{0}`.`_dm_messages` (`create-time`, `dm_channel-id`, `user-id`, `user-name`, `message-id`, `content`,
        `attachmenturl`, `attachmentfilename`, `isedited`, `edit-time`, `edit-before-content`, `edit-after-content`,
        `edit-before-attachmenturl`,`edit-before-attachmentfilename`, `edit-after-attachmenturl`,
        `edit-after-attachmentfilename`) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE    
        `isedited` = %s, `edit-time` = %s, `edit-before-content` = %s, `edit-after-content` = %s,
        `edit-before-attachmenturl` = %s, `edit-before-attachmentfilename` = %s, 
        `edit-after-attachmenturl` = %s, `edit-after-attachmentfilename` = %s
        """
        newquery = sqlquery.format(self.bot.common.mysqldb)
        querydata = (createtime, channelid, userid, username, messageid, beforecontent, beforeattachmenturl,
                     beforeattachmentfilename, isedited, edittime, beforecontent, aftercontent, beforeattachmenturl,
                     beforeattachmentfilename, afterattachmenturl, afterattachmentfilename, isedited, edittime,
                     beforecontent, aftercontent, beforeattachmenturl, beforeattachmentfilename, afterattachmenturl,
                     afterattachmentfilename)
        tablename = str("_dm_messages")
        return newquery, tablename, querydata

    async def statement_insert_dm_deleted(self, ctx):
        createtime = str(ctx.created_at)
        isdeleted = 1
        deletetime = str(datetime.datetime.now())
        channelid = str(ctx.channel.id)
        userid = str(ctx.author.id)
        username = str(ctx.author)
        content = str(ctx.content)
        messageid = str(ctx.id)
        if ctx.attachments:
            attachmenturl = ', '.join([str(at.url) for at in ctx.attachments])
            attachmentfilename = ', '.join([str(at.filename) for at in ctx.attachments])
        else:
            attachmenturl = "None"
            attachmentfilename = "None"
        sqlquery = """
        INSERT INTO `{0}`.`_dm_messages` (`create-time`, `dm_channel-id`, `user-id`, `user-name`, `message-id`, `content`,
        `attachmenturl`, `attachmentfilename`, `isdeleted`, `delete-time`) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE    
        `isdeleted` = %s, `delete-time` = %s;
        """
        newquery = sqlquery.format(self.bot.common.mysqldb)
        querydata = (createtime, channelid, userid, username, messageid, content, str(attachmenturl),
                     str(attachmentfilename), isdeleted, deletetime, isdeleted, deletetime)
        tablename = str("_dm_messages")
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
        tablename = str("_errorlog")
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
        sql_query = """INSERT INTO `{0}`.`_voice` (`time`, `guild-id`, `guild-name`, `user-id`, `user-name`,
        `voicechannel-id`, `voicechannel-name`, `selfdeaf`, `selfmute`, `serverdeaf`, `servermute`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sql_query.format(self.bot.common.mysqldb, guildid)
        query_data = (msgtime, guildid, guildname, memberid, membername, voicechannelid, voicechannelname, selfdeaf,
                      selfmute, serverdeaf, servermute)
        tablename = str("_voice")
        return new_query, tablename, query_data

    async def statement_insert_guild_member(self, member, secondaryargs, guild):
        msgtime = str(datetime.datetime.now())
        guildid = str(guild.id)
        guildname = str(guild.name)
        userid = str(member.id)
        username = str(member)
        action = str(secondaryargs)
        sql_query = """
        INSERT INTO `{0}`.`_memberlog` (`time`, `guild-id`, `guild-name`, `user-id`, `user-name`, `action`)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        new_query = sql_query.format(self.bot.common.mysqldb, guildid)
        query_data = (msgtime, guildid, guildname, userid, username, action)
        tablename = str("_memberlog")
        return new_query, tablename, query_data

    async def statement_insert_guild_log(self, guild, joinleave):
        msgtime = str(datetime.datetime.now())
        guildid = str(guild.id)
        guildname = str(guild.name)
        largeguild = int(guild.large)
        guildownername = str(guild.owner)
        guildownerid = str(guild.owner.id)
        numusersonjoin = str(guild.member_count)
        guildcreatedutc = str(guild.created_at)
        leavetime = None
        if joinleave == str("join"):
            guildquery = """
            REPLACE INTO `{0}`.`_guildlog` (`firstseen`, `guildid`, `guildname`, `largeguild`, `guild-owner-name`,
            `guild-owner-id`, `number-users-on-join`, `guild-created-date-UTC`, `leavetime`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            new_query = guildquery.format(self.bot.common.mysqldb)
            query_data = (msgtime, guildid, guildname, largeguild, guildownername, guildownerid, numusersonjoin,
                          guildcreatedutc, leavetime)
        elif joinleave == str("leave"):
            leavetime = str(datetime.datetime.now())
            guildquery = """
            INSERT  INTO `{0}`.`_guildlog` (`firstseen`, `guildid`, `guildname`, `largeguild`, `guild-owner-name`,
            `guild-owner-id`, `number-users-on-join`, `guild-created-date-UTC`, `leavetime`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE    
            `leavetime` = %s;
            """
            new_query = guildquery.format(self.bot.common.mysqldb)
            query_data = (msgtime, guildid, guildname, largeguild, guildownername, guildownerid, numusersonjoin,
                          guildcreatedutc, leavetime, leavetime)
        else:
            return
        tablename = str("_guildlog")
        return new_query, tablename, query_data

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
        command = ctx.invoked_with
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
        `user-id`, `user-name`, `message-id`, `command`, `content`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sqlquery.format(self.bot.common.mysqldb)
        query_data = (msgtime, guildid, guildname, channelid, channelname, userid, username, messageid, command, content)
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
        enableawoos = bool(responses[4])
        enablelogging = bool(responses[0])
        welcomechanbool = bool(responses[1])
        adminlogchanbool = bool(responses[2])
        voicelogchanbool = bool(responses[3])
        if enableawoos:
            awoochan = str(channellist[4].id)
        else:
            awoochan = None
        if welcomechanbool:
            welcomechan = str(channellist[1].id)
        else:
            welcomechan = None
        if adminlogchanbool:
            adminlogchan = str(channellist[2].id)
        else:
            adminlogchan = None
        if voicelogchanbool:
            voicelogchan = str(channellist[3].id)
        else:
            voicelogchan = None
        isconfigged = 1
        configquery = """
        INSERT INTO `{0}`.`_serverconfig` (`guild-id`, `isconfigged`, `initialchannel`, `whoconfiged`, `lastconfiged`, 
        `enablelogging`, `enableusewelcome`, `enableadminlogs`, `enablevoicelogs`, `welcomechannel`, `adminchannel`,
        `voicelogchannel`, `awoochannel`, `enableawoo`, `partmessage`, `welcomemessage`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        `initialchannel` = %s, `whoconfiged` = %s, `lastconfiged` = %s, `enablelogging` = %s, `enableusewelcome` = %s,
        `enableadminlogs` = %s, `enablevoicelogs` = %s, `welcomechannel` = %s, `adminchannel` = %s,
        `voicelogchannel` = %s, `awoochannel` = %s, `enableawoo` = %s, `partmessage` = %s, `welcomemessage` = %s
        """
        new_query = configquery.format(self.bot.common.mysqldb)
        query_data = (guildid, isconfigged, initialchan, whoconfiged, configtime, enablelogging, welcomechanbool,
                      adminlogchanbool, voicelogchanbool, welcomechan, adminlogchan, voicelogchan, awoochan,
                      enableawoos, partmessage, joinmessage, initialchan, whoconfiged, configtime, enablelogging,
                      welcomechanbool, adminlogchanbool, voicelogchanbool, welcomechan, adminlogchan, voicelogchan,
                      awoochan, enableawoos, partmessage, joinmessage)
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

    async def statement_remove_guild_config(self, guild):
        guildid = str(guild.id)
        sql_query = """
        DELETE FROM `{0}`.`_serverconfig`
        WHERE `guild-id` = {1};
        """
        new_query = sql_query.format(self.bot.common.mysqldb, str(guildid))
        return new_query


# beginning framework for dynamic table, row, column, and statement generator
# this is going to be messy
# no promises lollllllll
# class MySQLFramework:
#     def __init__(self, bot):
#         self.bot = bot
#         print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')
#
#     async def tablecreate(self):
#         pass
#
#     async def columns(self):
#         pass
#
#     async def statement_generator(self):
#         pass


def setup(dbot):
    dbot.add_cog(InternalSQL(dbot))
