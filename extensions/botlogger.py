from extensions.utils.importsfile import *


class BotLoggerDB:
    """Logger Class"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        importlib.reload(self.dbotchecks)
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def on_command_completion(self, ctx):
        sql_cmd, query_data = await self.bot.sql.statement_insert_cmdtable(ctx)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql_cmd, query_data)

    async def download_attachment(self, ctx):
        if ctx.author.id == self.bot.common.botdiscordid:
            return
        else:
            download_list = list([at.url for at in ctx.attachments])
            file_names = list([at.filename for at in ctx.attachments])
            if str('Direct Message') in str(ctx.channel):
                folder = os.path.join(os.curdir, "internalfiles", "downloads", "DMs", str(ctx.author.id))
            else:
                folder = os.path.join(os.curdir, "internalfiles", "downloads", str(ctx.guild.id), str(ctx.channel.id))
            if not os.path.exists(folder):
                os.makedirs(folder)
            index = 0
            for url in download_list:
                filename = file_names[index]
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

    async def guild_member_log(self, member, secondaryargs, guild):
        sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_guild_member(member, secondaryargs, guild)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql_cmd, query_data)

    async def on_member_join(self, member):
        await self.log_encountered_users(member)
        await self.guild_member_log(member, "join", member.guild)

    async def on_member_remove(self, member):
        await self.guild_member_log(member, "leave", member.guild)

    async def on_member_ban(self, guild, member):
        await self.guild_member_log(member, "ban", guild)

    async def on_member_unban(self, guild, member):
        await self.guild_member_log(member, "unban", guild)

    async def on_voice_state_update(self, member, before, after):
        voice_command, table_name, query_data = await self.bot.sql.statement_insert_voicetable(member, after)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(voice_command, query_data)

    async def on_message(self, message):
        if str('Direct Message') in str(message.channel):
            sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_dm_new(message)
        else:
            sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_channel_new(message)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query=sql_cmd, args=query_data)
        if message.attachments:
            await self.download_attachment(message)

    async def on_message_edit(self, beforemessage, aftermessage):
        if str('Direct Message') in str(aftermessage.channel):
            sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_dm_edit(beforemessage, aftermessage)
        else:
            sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_channel_edit(beforemessage, aftermessage)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(sql_cmd, query_data)

    async def on_message_delete(self, message):
        if str('Direct Message') in str(message.channel):
            sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_dm_deleted(message)
        else:
            sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_channel_deleted(message)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(sql_cmd, query_data)

    async def on_guild_join(self, guild):
        members = guild.members
        await self.log_encountered_users(members)
        await self.log_guild(guild, str("join"))

    async def on_guild_remove(self, guild):
        await self.log_guild(guild, str("leave"))
        sql_cmd = await self.bot.sql.statement_remove_guild_config(guild)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(sql_cmd)

    async def log_encountered_users(self, user):
        sql_cmd = await self.bot.sql.statement_insert_encountered_users()
        msg_time = str(datetime.datetime.now())
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                if isinstance(user, list):
                    for member in user:
                        userid = str(member.id)
                        username = str(member)
                        find_cmd = await self.bot.sql.statement_get_userlist_single_user(userid)
                        await cursor.execute(find_cmd)
                        result = (await cursor.fetchone())
                        if not result:
                            query_data = (msg_time, userid, username)
                            await cursor.execute(sql_cmd, query_data)
                        else:
                            pass
                elif isinstance(user, discord.member.Member):
                    userid = str(user.id)
                    username = str(user)
                    find_cmd = await self.bot.sql.statement_get_userlist_single_user(userid)
                    await cursor.execute(find_cmd)
                    result = (await cursor.fetchone())
                    if not result:
                        query_data = (msg_time, userid, username)
                        return await cursor.execute(sql_cmd, query_data)
                    else:
                        return
                else:
                    return

    async def log_guild(self, guild, join_leave):
        sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_guild_log(guild, join_leave)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(sql_cmd, query_data)

    async def on_command_error(self, ctx, exception):
        sql_cmd, table_name, query_data = await self.bot.sql.statement_insert_errorlog(ctx, exception)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                return await cursor.execute(sql_cmd, query_data)


def setup(dbot):
    dbot.add_cog(BotLoggerDB(dbot))
