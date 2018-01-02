from extensions.utils.importsfile import *


class LoopClass:
    """Loop commands"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_ready(self):
        await self.loopstorun()

    async def loopstorun(self):
        # pass
        self.bot.loop.create_task(self.awoo())
        # self.loop.create_task(self.servertakeover())

    async def awoo(self):
        timerange = list(range(7200, 28800, 2))
        awooarray = []
        awoopath = os.path.join("internalfiles", "images", "smallawoo", "**")
        fileexts = '.png', '.jpg', '.jpeg', '.gif'
        for filename in glob.glob(str(awoopath), recursive=False):
            if filename.endswith(fileexts):
                awooarray += [str(filename)]
        while not self.bot.is_closed():
            waittime = random.choice(timerange)
            for chan in self.bot.common.mainservergeneralchan:
                randomawoo = random.choice(awooarray)
                channel = self.bot.get_channel(id=int(chan))
                await channel.send(file=discord.File(fp=randomawoo, filename="awoo.png"), content="awoo~")
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

    # async def servertakeover(self):
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
