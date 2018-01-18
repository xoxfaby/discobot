from extensions.utils.importsfile import *
from extensions.utils.common import CommonParams


class DBot(commands.Bot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description=CommonParams.botdescription,
                         command_prefix=commands.when_mentioned_or(CommonParams.discordbotcommandprefix))
        self.common = CommonParams()

    async def on_ready(self):
        curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f'\n{curtime}: Logged in as "{str(self.user)}" with the id of "{str(self.user.id)}"\n------\n')


class Main:
    bot = DBot()
    bot.starttime = datetime.datetime.utcnow()
    loaded_exts, total_exts = 0, len(bot.common.addons)
    for extension in bot.common.addons:
        try:
            bot.load_extension(extension)
            loaded_exts += 1
        except Exception as e:
            print(f'{extension} failed to load.\n{type(e).__name__}: {e}')
    curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(f'{bot.starttime}: {loaded_exts}/{total_exts} extensions and {len(bot.cogs.keys())} cogs have been loaded\n'
          f'Proceeding with login to Discord now...')
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
