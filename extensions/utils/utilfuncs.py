from extensions.utils.importsfile import *


class UtilFuncs:
    """Utility Functions"""
    # Misc shit I guess idk
    # Mostly making this cog for small things like aiohttp downloads and file reading/writing
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def _bytes_download(self, url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        b = io.BytesIO(data)
                        b.seek(0)
                        return b
                    else:
                        return None
        except:
            raise self.bot.myerrors.DBotExternalError("Failed to retreive requested file.")
