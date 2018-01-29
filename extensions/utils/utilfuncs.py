from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class UtilFuncs:
    """Utility Functions"""
    # Misc shit I guess idk
    # Mostly making this cog for small things like aiohttp downloads and file reading/writing
    def __init__(self, bot):
        self.bot = bot
        self.bot.utils = self
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def retrieve_web_file(self, url: str, savelocation=None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        if savelocation is not None:
                            with open(savelocation, "wb") as file:
                                file.write(data)
                        return data
                    else:
                        return None
        except:
            raise self.bot.errors.DBotExternalError("Failed to retreive requested file.")


class Startup:
    """Bot init thingers"""
    def __init__(self, bot):
        self.bot = bot
        self.bot.utils = self
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def on_ready(self):
        curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        mesg = f'{0}: Logged in as "{1}" with the id of "{2}"\n------\n'
        mesg = mesg.format(curtime, str(self.bot.user), str(self.bot.user.id))
        print(mesg)

    async def on_shard_ready(self, shardid):
        curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        mesg = f'{0}: Shard {1} logged in as "{2}" with the id of "{3}"\n------\n'
        mesg = mesg.format(curtime, str(shardid), str(self.bot.user), str(self.bot.user.id))
        print(mesg)


def setup(dbot):
    dbot.add_cog(UtilFuncs(dbot))
    dbot.add_cog(Startup(dbot))
