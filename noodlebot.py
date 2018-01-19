from extensions.utils.importsfile import *
from extensions.utils.common import CommonParams, PrefixStuff
from extensions.utils.errors import MyErrors


class DBot(commands.Bot):
    """A modified discord.ext.commands.Bot class"""
    def __init__(self, *args, **kwargs):
        self.common, self.errors, self.prefixstuff = CommonParams(), MyErrors, PrefixStuff(self)
        # self.myprefix = commands.when_mentioned_or(self.prefixstuff.get_prefix)
        self.myprefix = self.common.discordbotcommandprefix
        super().__init__(*args, **kwargs, description=CommonParams.botdescription, command_prefix=self.myprefix)

    async def on_ready(self):
        curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(f'{curtime}: Logged in as "{str(self.user)}" with the id of "{str(self.user.id)}"\n------\n')


class Main:
    bot = DBot()
    loaded_exts, total_exts = 0, len(bot.common.addons)
    for extension in bot.common.addons:
        try:
            bot.load_extension(extension)
            loaded_exts += 1
        except Exception as e:
            print(f'{extension} failed to load.\n{type(e).__name__}: {e}')
    bot.starttime = datetime.datetime.utcnow()
    # time.sleep(2)
    # bot.loop.run_until_complete(bot.prefixstuff.load_all_prefixes())
    curtime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print(f'{curtime}: {loaded_exts}/{total_exts} extensions and {len(bot.cogs.keys())} cogs have been loaded\n\n'
          f'Proceeding with login to Discord now...\n')
    bot.run(bot.common.discordbottoken)
    exit(0)


if __name__ == '__main__':
    Main()
