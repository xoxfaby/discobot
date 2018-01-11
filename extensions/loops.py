from extensions.utils.importsfile import *


class LoopClass:
    """Loop commands"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__)}" loaded')

    async def on_ready(self):
        await self.loopstorun()

    async def loopstorun(self):
        # pass
        self.bot.loop.create_task(self.awoo())
        # self.loop.create_task(self.daychange())
        # self.loop.create_task(self.mainguild_takeover())

    async def awoo(self):
        timerange = list(range(7200, 28800, 2))
        awoo_array = []
        awoo_path = os.path.join("internalfiles", "images", "smallawoo", "**")
        file_exts = '.png', '.jpg', '.jpeg', '.gif'
        for filename in glob.glob(str(awoo_path), recursive=False):
            if filename.endswith(file_exts):
                awoo_array += [str(filename)]
        while not self.bot.is_closed():
            waittime = random.choice(timerange)
            sql_cmd = await self.bot.sql.statement_get_awoolist()
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(sql_cmd)
                    chan_list = await cursor.fetchall()
            for item in chan_list:
                for key, chanid in item.items():
                    random_awoo = random.choice(awoo_array)
                    send_chan = self.bot.get_channel(id=int(chanid))
                    await send_chan.send(file=discord.File(fp=random_awoo, filename="awoo.png"), content="awoo~")
            await asyncio.sleep(waittime)

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
