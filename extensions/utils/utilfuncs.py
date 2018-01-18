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


class MyErrors(commands.CommandError):
    """
    Subclassing error commands because why not.
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.errors = self
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    class DBotInternalError(commands.CommandError):
        pass

    class DBotExternalError(commands.CommandError):
        pass

    class BotNotWorking(commands.CommandError):
        pass

    class NotOwnerError(commands.CommandError):
        pass


def setup(dbot):
    dbot.add_cog(UtilFuncs(dbot))
    dbot.add_cog(MyErrors)
