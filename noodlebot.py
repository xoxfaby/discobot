from extensions.utils.importsfile import *
from extensions.utils.common import CommonParams
from extensions.utils.utilfuncs import UtilFuncs, MyErrors


class DBot(commands.Bot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description=CommonParams.botdescription,
                         command_prefix=commands.when_mentioned_or(CommonParams.discordbotcommandprefix))
        self.common = CommonParams()
        self.errors, self.utils = MyErrors(), UtilFuncs(self)

    async def on_ready(self):
        self.common.logger.info(f'\nLogged in as {str(self.user)}, id: {str(self.user.id)}')
        curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f'\n{curtime}:\nLogged in as: {str(self.user)}\nWith the id of: {str(self.user.id)}\n------\n')


class Main:
    bot = DBot()
    loaded_exts, total_exts = 0, len(bot.common.addons)
    for extension in bot.common.addons:
        try:
            bot.load_extension(extension)
            loaded_exts += 1
        except Exception as e:
            print(f'{extension} failed to load.\n{type(e).__name__}: {e}')
    curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(f'{curtime}: {loaded_exts}/{total_exts} extensions and {len(bot.cogs.keys())} cogs have been loaded')
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
