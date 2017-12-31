from extensions.utils.importsfile import *


class Load:
    """
    Load commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, botmodule: str):
        """Loads an addon."""
        try:
            fullmodule = ""
            if botmodule[0:11] != "extensions.":
                fullmodule = "extensions." + botmodule
            self.bot.load_extension(fullmodule)
            await ctx.send('✅ Extension loaded.')
        except Exception as e:
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, botmodule))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, botmodule: str):
        """Unloads an addon."""
        try:
            fullmodule = ""
            if botmodule[0:11] != "extensions.":
                fullmodule = "extensions." + botmodule
            if fullmodule == "extensions.load":
                await ctx.send("❌ I don't think you want to unload that!")
            else:
                self.bot.unload_extension(fullmodule)
                await ctx.send('✅ Extension unloaded.')
        except Exception as e:
            await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, botmodule))

    @commands.command(hidden=True, aliases=['reload'])
    @commands.is_owner()
    async def modulereload(self, ctx, dbotmodule):
        """Reloads an addon."""
        if dbotmodule is None:
            raise commands.errors.BadArgument("A reload command was given with no module name")
        elif dbotmodule == "all":
            modules = self.bot.extensions
            loadedmods = []
            for mod in modules:
                if mod[0:11] == "extensions.":
                    loadedmods += [mod]
            for mod in loadedmods:
                self.bot.unload_extension(mod)
                self.bot.load_extension(mod)
            await ctx.send('✅ All extensions have been reloaded.')
        else:
            try:
                fullmodule = ""
                if dbotmodule[0:11] != "extensions.":
                    fullmodule = "extensions." + dbotmodule
                self.bot.unload_extension(fullmodule)
                self.bot.load_extension(fullmodule)
                await ctx.send('✅ Extension reloaded.')
            except Exception as e:
                await ctx.send('💢 Failed!\n```\n{}: {}\n```'.format(type(e).__name__, dbotmodule))

    @commands.command(name='listextensions', hidden=True)
    @commands.is_owner()
    async def _listmods(self, ctx):
        modules = self.bot.extensions
        loadedmods = []
        for mod in modules:
            if mod[0:11] == "extensions.":
                loadedmods += [mod]
        await ctx.send("Loaded modules:" + '\n```' + ',\n'.join(loadedmods) + '```')


def setup(dbot):
    dbot.add_cog(Load(dbot))
