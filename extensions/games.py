from extensions.utils.importsfile import *


class Games:
    """A module for games within the bot."""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        self.wwclass = self._ww_internals(self.bot)
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def __local_check(self, ctx):
        result = bool(await self.bot.internals.cooldowncheck(ctx))
        return result

    class _ww_internals:
        def __init__(self, bot):
            pass

    @commands.command()
    async def werewolf(self, ctx):
        """The classic werewolf game from IRC"""
        pass
