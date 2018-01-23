from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class Games:
    """A module for games within the bot."""
    def __init__(self, bot):
        self.bot = bot
        self.wwclass = self._ww_internals(self.bot)
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def __local_check(self, ctx):
        bucket = self.bot.cd.get_bucket(ctx.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            nice_retry_after = (f'{round(retry_after)}')
            mesg = f'You have been rate limited. Please wait for another {nice_retry_after} seconds.'
            await ctx.send(mesg)
            return False
        else:
            return True

    class _ww_internals:
        def __init__(self, bot):
            pass

    @commands.command()
    async def werewolf(self, ctx):
        """The classic werewolf game from IRC"""
        pass
