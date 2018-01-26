from extensions.utils.importsfile import *


class LevelSystem:
    """A level system for the bot"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def levelgoals(self):
        goaldict = dict()
        goaldict["images"] = int(50)
        goaldict['messages'] = int(100)
        goaldict['onlinetime'] = int(48)
        goaldict['voicetime'] = int(5)

    async def rewards(self):
        rewarddict = dict()
        rewarddict['imagemessage'] = int(2)
        rewarddict['textmessage'] = int(1)
        rewarddict['onlinetimeincrement'] = int(1)
        rewarddict['voicetime'] = int(1)

    async def levelup(self):
        pass

    async def randomchooser(self):
        pass

    async def levelstodb(self):
        pass

    async def on_message(self, ctx):
        pass

    @commands.command()
    @dbotchecks.check_server_admin_or_botowner()
    async def levelgoals(self, ctx, user):
        pass


def setup(dbot):
    dbot.add_cog(LevelSystem(dbot))
