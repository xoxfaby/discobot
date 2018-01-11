from extensions.utils.importsfile import *
from extensions.utils.sqlcommands import InternalSQL
from extensions.utils.utilfuncs import UtilFuncs, MyErrors, CommonParams


class DBot(commands.Bot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description=CommonParams.botdescription,
                         command_prefix=commands.when_mentioned_or(CommonParams.discordbotcommandprefix))
        self.common, self.sql, self.errors, self.utils = CommonParams(), InternalSQL(self), MyErrors(), UtilFuncs(self)

    async def on_ready(self):
        self.common.logger.info(f'\nLogged in as {str(self.user)}, id: {str(self.user.id)}')
        print(f'\nLogged in as: {str(self.user)}\nWith the id of: {str(self.user.id)}\n------\n')


class Main:
    bot = DBot()
    loaded_exts, total_exts = 0, len(bot.common.addons)
    for extension in bot.common.addons:
        try:
            bot.load_extension(extension)
            loaded_exts += 1
        except Exception as e:
            print(f'{extension} failed to load.\n{type(e).__name__}: {e}')
    curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    print(f'{curtime}: {loaded_exts}/{total_exts} extensions and {len(bot.cogs.keys())} cogs have been loaded')
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
