from extensions.utils.importsfile import *


class LoopClass:
    """Loop commands"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')
        self.awootask = self.bot.loop.create_task(self.awoo())
        self.pinger = self.bot.loop.create_task(self.ping_timer())

    def __unload(self):
        """Unloading the cog, cancel tasks"""
        self.pinger.cancel()
        self.awootask.cancel()

    async def awoo(self):
        await self.bot.wait_until_ready()
        timerange = list(range(7200, 28800, 2))
        while not self.bot.is_closed():
            curtime = datetime.datetime.now()
            waittime = random.choice(timerange)
            waittime1 = datetime.timedelta(seconds=int(waittime))
            projectedtime = curtime + waittime1
            key = "awootime"
            if await self.bot.misccache.exists(key=key):
                await self.bot.misccache.delete(key=key)
            await self.bot.misccache.add(key=key, value=projectedtime)
            sql_cmd = await self.bot.sql.statement_get_awoolist()
            async with self.bot.mysqlcon.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(sql_cmd)
                    chan_list = await cursor.fetchall()
            awoolist = []
            for server in self.bot.guilds:
                for emoji in server.emojis:
                    if "awoo" in emoji.name.lower():
                        awoolist.append(emoji)
            for item in chan_list:
                for key, chanid in item.items():
                    random_awoo = random.choice(awoolist)
                    send_chan = self.bot.get_channel(id=int(chanid))
                    await send_chan.send(content=random_awoo)
            await asyncio.sleep(waittime)

    async def ping_timer(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            curtime = datetime.datetime.now()
            latencytime = self.bot.latency
            sqlcmd = """
            INSERT INTO `{0}`.`_pinger` (`curtime`, `heartbeat`)
            VALUES (%s, %s)
            """
            newcmd = sqlcmd.format(self.bot.common.mysqldb).replace("\n", "")
            querydata = (curtime, latencytime)
            async with self.bot.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(newcmd, querydata)
            await asyncio.sleep(30)

    async def daychange(self):
        midnight = time.strftime("0000")
        while not self.bot.is_closed():
            curtime = time.strftime("%H%M")
            if curtime == midnight:
                for chan in self.bot.common.mainservergeneralchan:
                    channel = self.bot.get_channel(id=int(chan))
                    await channel.send(content="Day change")
                await asyncio.sleep(60)
            else:
                await asyncio.sleep(30)

    # async def mainguild_takeover(self):
    #     midnightutc = str(time.strftime("0000"))
    #     channel = self.get_channel(id=mainservergeneralchan)
    #     mainserverobj = self.get_guild(mainserver)
    #     jailrole = discord.utils.find(lambda m: m.name == 'jail', channel.guild.roles)
    #     while not self.is_closed():
    #         curtimeutc = datetime.datetime.utcnow().strftime("%H%M")
    #         if str(curtimeutc) == str(midnightutc):
    #             takeoverchoice = str(random.randrange(1, 200000000000000, 1))
    #             if str(takeoverchoice) == str("42"):
    #                 takeovermessage = 'ATTENTION\nATTENTION\nATTENTION\nTODAY IS THE DAY\nYOU ALL ARE GOING TO JAIL'
    #                 await channel.send(content=takeovermessage)
    #                 for memeber in mainserverobj.members:
    #                     await memeber.add_role(jailrole)
    #             else:
    #                 safemessage = str('You have been spared for another day...' + '\n' + 'The magic number is 42.'
    #                               + '\nThe overlord has chosen ' + str(takeoverchoice) + ' out of 200000000000000.')
    #                 await channel.send(content=safemessage)
    #             await asyncio.sleep(60)
    #         else:
    #             await asyncio.sleep(30)


def setup(dbot):
    dbot.add_cog(LoopClass(dbot))
