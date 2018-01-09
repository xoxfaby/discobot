import extensions.utils.common as common
# from extensions.utils.common import check_trusted_user, check_main_server
from extensions.utils.importsfile import *
from extensions.utils.sqlcommands import InternalSQL
from extensions.utils.bot_error_helpers import MyErrors
from extensions.utils.utilfuncs import UtilFuncs


class DBot(commands.Bot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description=common.CommonParams.botdescription,
                         command_prefix=commands.when_mentioned_or(common.CommonParams.discordbotcommandprefix))
        self.common = common.CommonParams()
        self.sql = InternalSQL(self)
        self.myerrors = MyErrors()
        self.utils = UtilFuncs(self)

    async def on_ready(self):
        self.common.logger.info('\nLogged in as %s, id: %s', str(self.user.name), str(self.user.id))
        print('')
        print('Logged in as: ' + str(self.user.name))
        print('With the id of: ' + str(self.user.id))
        print('------\n')


class Main:
    bot = DBot()
    loaded_exts = 0
    total_exts = len(bot.common.addons)
    for extension in bot.common.addons:
        try:
            bot.load_extension(extension)
            loaded_exts += 1
        except Exception as e:
            print('{} failed to load.\n{}: {}'.format(extension, type(e).__name__, e))
    curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    print(curtime + f': {loaded_exts}/{total_exts} extensions and {len(bot.cogs.keys())} cogs have been loaded')
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
