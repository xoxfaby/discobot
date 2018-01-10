from extensions.utils.importsfile import *


class UtilFuncs:
    """Utility Functions"""
    # Misc shit I guess idk
    # Mostly making this cog for small things like aiohttp downloads and file reading/writing
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def _retrieve_web_file(self, url: str, savelocation):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        with open(savelocation, "wb") as file:
                            file.write(data)
                        return data
                    else:
                        return None
        except:
            raise self.bot.myerrors.DBotExternalError("Failed to retreive requested file.")
