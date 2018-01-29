from extensions.utils.importsfile import *
from extensions.utils.common import CommonParams, PrefixStuff, MyErrors, Loading


class DBot(commands.AutoShardedBot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        self.common, self.errors = CommonParams, MyErrors
        self.pref, self.loading = PrefixStuff(self), Loading(self)
        super().__init__(*args, **kwargs, description=self.common.botdescription, command_prefix=self.pref.get_prefix)


class Main:
    bot = DBot()
    bot.loading.load()
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
