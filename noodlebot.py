import extensions.utils.common as common
from extensions.utils.importsfile import *
from extensions.utils.sqlcommands import InternalSQL
from extensions.utils.cache import BotCache


class DBot(commands.Bot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description=common.CommonParams.botdescription, pm_help=True,
                         command_prefix=commands.when_mentioned_or(common.CommonParams.discordbotcommandprefix))
        self.common = common.CommonParams()
        self.sql = InternalSQL(self)
        self.botcache = BotCache(self)

    async def on_ready(self):
        self.common.logger.info('\nLogged in as %s, id: %s', str(self.user.name), str(self.user.id))
        print('')
        print('Logged in as: ' + str(self.user.name))
        print('With the id of: ' + str(self.user.id))
        print('------\n')


class Main:
    bot = DBot()
    for extension in bot.common.addons:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
