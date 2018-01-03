from extensions.utils.importsfile import *


class BotLoggerDB:
    """Logger Class"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_command_completion(self, ctx):
        sqlcmd, querydata = await self.bot.sql.statement_insert_cmdtable(ctx)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sqlcmd, querydata)

    async def check_table(self, tabletype: str, tablename: str):
        tableexistsincache = await self.bot.botcache.mysqlcache.exists(key=tablename)
        if tableexistsincache:
            value = await self.bot.botcache.mysqlcache.get(key=tablename)
            if value:
                createtable = False
            else:
                createtable = True
        else:
            createtable = True
        if createtable:
            sqlcmd = await self.bot.sql.statement_check_table_exist(tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sqlcmd)
                    numtables = cursor.rowcount
                    if numtables:
                        pass
                    else:
                        createcmd = await self.bot.sql.statement_create_table(tabletype, tablename)
                        await cursor.execute(createcmd)
            addkv = await self.bot.botcache.mysqlcache.add(namespace="mysql", key=tablename, value=True)
            if addkv:
                nowexists = await self.bot.botcache.mysqlcache.exists(key=tablename)
                return nowexists


        # check cache first
        # if cache None, run sql
            # -> store new result in cache for later
        # if cache exists but false, run sql
            # -> store new result in cache for later
        # if cache exists & true, return
            # -> do nothing with sql nor cache





    async def download_attachment(self, ctx):
        if ctx.author.id == self.bot.common.botdiscordid:
            return
        else:
            downloadlist = list([at.url for at in ctx.attachments])
            filenames = list([at.filename for at in ctx.attachments])
            if str('Direct Message') in str(ctx.channel):
                folder = os.path.join(os.curdir, "internalfiles", "downloads", "DMs", str(ctx.author.id))
            else:
                folder = os.path.join(os.curdir, "internalfiles", "downloads", str(ctx.guild.id), str(ctx.channel.id))
            if not os.path.exists(folder):
                os.makedirs(folder)
            index = 0
            for url in downloadlist:
                filename = filenames[index]
                index += 1
                location = os.path.join(folder, str(time.strftime("%Y-%m-%d_%H%M%S_", time.localtime())) + filename)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            attachmentout = await resp.read()
                            with open(location, "wb") as file:
                                file.write(attachmentout)
                        else:
                            pass

    async def guildmemberlog(self, member, secondaryargs, guild):
        sqlcmd, tablename, querydata = await self.bot.sql.statement_insert_guild_member(member, secondaryargs, guild)
        await self.check_table("member-log", tablename)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sqlcmd, querydata)

    async def on_member_join(self, member):
        await self.logencounteredusers(member)
        await self.guildmemberlog(member, "join", member.guild)

    async def on_member_remove(self, member):
        await self.guildmemberlog(member, "leave", member.guild)

    async def on_member_ban(self, guild, member):
        await self.guildmemberlog(member, "ban", guild)

    async def on_member_unban(self, guild, member):
        await self.guildmemberlog(member, "unban", guild)

    async def on_voice_state_update(self, member, before, after):
        voicecommand, tablename, querydata = await self.bot.sql.statement_insert_voicetable(member, after)
        await self.check_table("voice", tablename)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(voicecommand, querydata)

    async def on_message(self, message):
        if str('Direct Message') in str(message.channel):
            dmsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_dm_new(message)
            await self.check_table("dm-new", tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(dmsqlcmd, querydata)
        else:
            channelsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_channel_new(message)
            await self.check_table("channel-new", tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query=channelsqlcmd, args=querydata)
        if message.attachments:
            await self.download_attachment(message)

    async def on_message_edit(self, beforemessage, aftermessage):
        if str('Direct Message') in str(aftermessage.channel):
            dmsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_dm_edit(beforemessage, aftermessage)
            await self.check_table("dm-edited", tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    return await cursor.execute(dmsqlcmd, querydata)
        else:
            channelsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_channel_edit(beforemessage,
                                                                                                   aftermessage)
            await self.check_table("channel-edited", tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    return await cursor.execute(channelsqlcmd, querydata)

    async def on_message_delete(self, message):
        if str('Direct Message') in str(message.channel):
            dmsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_dm_deleted(message)
            await self.check_table("dm-deleted", tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    return await cursor.execute(dmsqlcmd, querydata)
        else:
            channelsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_channel_deleted(message)
            await self.check_table("channel-deleted", tablename)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    return await cursor.execute(channelsqlcmd, querydata)

    async def on_guild_join(self, guild):
        members = guild.members
        await self.logencounteredusers(members)
        await self.logguild(guild, str("join"))

    async def on_guild_remove(self, guild):
        await self.logguild(guild, str("leave"))

    async def logencounteredusers(self, user):
        sqlquery = await self.bot.sql.statement_insert_encountered_users()
        msgtime = str(datetime.datetime.now())
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                if isinstance(user, list):
                    for member in user:
                        userid = str(member.id)
                        username = str(member)
                        findcmd = await self.bot.sql.statement_get_userlist_single_user(userid)
                        await cursor.execute(findcmd)
                        result = (await cursor.fetchone())
                        if not result:
                            querydata = (msgtime, userid, username)
                            await cursor.execute(sqlquery, querydata)
                        else:
                            pass
                elif isinstance(user, discord.member.Member):
                    userid = str(user.id)
                    username = str(user)
                    findcmd = await self.bot.sql.statement_get_userlist_single_user(userid)
                    await cursor.execute(findcmd)
                    result = (await cursor.fetchone())
                    if not result:
                        querydata = (msgtime, userid, username)
                        return await cursor.execute(sqlquery, querydata)
                    else:
                        return
                else:
                    return

    async def logguild(self, guild, joinleave):
        logguildcmd, tablename, querydata = await self.bot.sql.statement_insert_guild_log(guild, joinleave)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(logguildcmd, querydata)

    async def on_command_error(self, ctx, exception):
        errorsqlcmd, tablename, querydata = await self.bot.sql.statement_insert_errorlog(ctx, exception)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(errorsqlcmd, querydata)


def setup(dbot):
    if dbot.common.addloggercog:
        dbot.add_cog(BotLoggerDB(dbot))
    else:
        pass
