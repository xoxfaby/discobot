from extensions.utils.importsfile import *


class EtcOnMessage:
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def etc_message_check(self, message):
        member_guild_config = str(f'{str(message.guild.id)}_guild_config')
        guild_config_exists_in_cache = await self.bot.mysqlcache.exists(key=member_guild_config)
        if guild_config_exists_in_cache:
            guild_conf = await self.bot.mysqlcache.get(key=member_guild_config)
            if bool(guild_conf['isconfigged']):
                enable_etc = bool(guild_conf['etc_on_message'])
            else:
                return False
        else:
            sql_cmd, table_name = await self.bot.sql.statement_get_server_config(message.guild)
            async with self.bot.mysqlcon.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(sql_cmd)
                    rowcount = cursor.rowcount
                    if rowcount == 1:
                        guild_conf = await cursor.fetchone()
                        await self.bot.mysqlcache.add(key=member_guild_config, value=guild_conf)
                        enable_etc = bool(guild_conf['etc_on_message'])
                    else:
                        return False
        if enable_etc:
            return True
        else:
            return False

    async def on_message(self, message):
        if (message.content.startswith(self.bot.common.discordbotcommandprefix)) or \
                (str(message.author.id) == str(self.bot.common.botdiscordid)) or (message.author.bot is True) or \
                (message.guild is None):
            return
        alphabet = {"bmoji": u"\U0001f171", "oksymbol": str("👌"), "fire": str("🔥")}
        msg = message.content
        etc_on_message = await self.etc_message_check(message)
        if not etc_on_message:
            return
        if msg.lower().startswith('ok google') or msg.lower().startswith('okay google'):
            if msg.lower().startswith('ok google'):
                subreplace = re.compile('ok google ', re.IGNORECASE)
                newmsg = subreplace.sub("", msg)
            elif msg.lower().startswith('okay google'):
                subreplace = re.compile('okay google ', re.IGNORECASE)
                newmsg = subreplace.sub("", msg)
            else:
                return
            newmesg1 = newmsg.replace(" ", "+")
            googleurl = (str("https://www.google.com/search?q=") + str(newmesg1))
            await message.add_reaction('✅')
            await message.channel.send(str(googleurl))
        if alphabet["oksymbol"] in msg:
            numberoffire = random.randrange(0, 5)
            if numberoffire != 0:
                await message.add_reaction('🔥')
        if "Don't say Hello" in msg:
            await message.channel.send("Hello")
        # if :
        #     for char in alphabet.keys():
        #         if char in msg:
        #             bmsg = msg.replace(char, alphabet[char])
        #         elif char.upper() in msg:
        #             bmsg = msg.replace(char.upper(), alphabet[char])
        #         if msg != message.content:
        #             await message.send(content=bmsg)


def setup(dbot):
    dbot.add_cog(EtcOnMessage(dbot))
