from extensions.utils.importsfile import *


class Load:
    """Load commands."""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, botmodule: str):
        """Loads an addon."""
        stdout = io.StringIO()
        try:
            fullmodule = ""
            if botmodule[0:11] != "extensions.":
                fullmodule = "extensions." + botmodule
            self.bot.load_extension(fullmodule)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'💢 Failed!\n```py\n{value}{traceback.format_exc()}\n```')
            await ctx.send(f'💢 Failed!\n```\n{type(e).__name__}: {fullmodule}\n```')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, botmodule: str):
        """Unloads an addon."""
        stdout = io.StringIO()
        try:
            fullmodule = ""
            if botmodule[0:11] != "extensions.":
                fullmodule = "extensions." + botmodule
            if fullmodule == "extensions.load":
                await ctx.send("❌ I don't think you want to unload that!")
            else:
                self.bot.unload_extension(fullmodule)
                await ctx.message.add_reaction('✅')
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'💢 Failed!\n```py\n{value}{traceback.format_exc()}\n```')
            await ctx.send(f'💢 Failed!\n```\n{type(e).__name__}: {fullmodule}\n```')

    @commands.command(hidden=True, aliases=['reload'])
    @commands.is_owner()
    async def modulereload(self, ctx, dbotmodule):
        """Reloads an addon."""
        stdout = io.StringIO()
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
            await ctx.message.add_reaction('✅')
        else:

            try:
                fullmodule = ""
                if dbotmodule[0:11] != "extensions.":
                    fullmodule = "extensions." + dbotmodule
                self.bot.unload_extension(fullmodule)
                self.bot.load_extension(fullmodule)
                await ctx.message.add_reaction('✅')
            except Exception as e:
                value = stdout.getvalue()
                await ctx.send(f'💢 Failed!\n```py\n{value}{traceback.format_exc()}\n```')
                await ctx.send(f'💢 Failed!\n```\n{type(e).__name__}: {fullmodule}\n```')

    @commands.command(name='listextensions', hidden=True)
    @commands.is_owner()
    async def _listmods(self, ctx):
        """List extensions"""
        stdout = io.StringIO()
        modules = self.bot.extensions
        loadedmods = []
        for mod in modules:
            if mod[0:11] == "extensions.":
                loadedmods += [mod]
        await ctx.send("Loaded modules:" + '\n```' + ',\n'.join(loadedmods) + '```')


def setup(dbot):
    dbot.add_cog(Load(dbot))
