from extensions.utils.importsfile import *


class AdminCommands:
    """Admin shit"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def deletebotmessages(self, ctx, num):
        await ctx.message.delete()
        limit = int(0)
        async for msg in ctx.history(limit=100, before=ctx.message):
            if msg.author == ctx.me:
                await msg.delete()
                limit += int(1)
                if limit == int(num):
                    break

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        mesg = ctx.message.content.split(" ")
        limit = mesg[1]
        await ctx.message.delete()
        await ctx.channel.purge(limit=int(limit))
        return await ctx.send(content='Deleted ' + str(limit) + ' message(s)')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def botkill(self, ctx):
        """
        This makes the bot shut itself down.
        """
        self.bot.common.logger.info('The botkill command was called at' +
                                    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                                    + ' in ' + str(ctx.guild) + '-' + str(ctx.channel))
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        await ctx.send('Proceeding with bot shutdown now...')
        await self.bot.close()
        await self.bot.sql.mysqlcon.close()
        return await self.bot.logout()

    @commands.command(hidden=True)
    async def boatsay(self, ctx, *args):
        """
        Sekrit
        """
        mesg = ' '.join(args)
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        return await ctx.send(mesg)

    @commands.command(hidden=True)
    async def adminbotsay(self, ctx, chanid, *args):
        """
        Sekrit
        """
        mesg = ' '.join(args)
        if (str('Direct Message') not in str(ctx.channel)) and \
                (str(ctx.channel.id) != str(self.bot.common.mainserverspamroom[0])):
            await ctx.message.delete()
        customchannel = self.bot.get_channel(id=int(chanid))
        return await customchannel.send(mesg)

    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def allguildbroadcast(self, ctx, *, message):
    #     if str(ctx.author.id) == str(self.bot.common.botowner):
    #         sqlcmd = await self.bot.sql.statement_get_initialchannel()
    #         async with self.bot.sql.mysqlcon.acquire() as conn:
    #             async with conn.cursor(aiomysql.DictCursor) as cursor:
    #                 await cursor.execute(sqlcmd)
    #                 rowcount = cursor.rowcount
    #                 guildconf = await cursor.fetchall()
    #                 dbguildlist = guildconf['guild-id']
    #                 botguildlist = []
    #                 for guild in self.bot.guilds:
    #                     botguildlist += guild
    #                 newlist = set(dbguildlist).symmetric_difference(botguildlist)
    #                 print(newlist)
    #
    #         count = 0
    #         for guild in self.bot.guilds:
    #             try:
    #                 await guild.owner.send(message)
    #             except:
    #                 pass
    #             else:
    #                 count += 1
    #         await say("Broadcast message sent to **{0}** users".format(count))
    #         await clear()
    #     else:
    #         return

    # @commands.command(hidden=True)
    # async def jail(self, ctx, *args):
    #     """Put a user in jail"""
    #     if str(ctx.author.id) in trustedusers:
    #         peepfile = os.path.join("internalfiles", "images", "peep.gif")
    #         afkchan = self.bot.get_channel(mainserverafkchan)
    #         for name in ctx.message.mentions:
    #             await self.bot.add_roles(name, mainserverjailrole)
    #             try:
    #                 await self.bot.move_member(name, afkchan)
    #             except:
    #                 pass
    #             await ctx.send(file=discord.File(fp=peepfile, filename="banhammer.gif"),
    #                                      content="Putting " + str(name.mention) + " in jail")
    #     else:
    #         await ctx.send("You are not authorized to use this command")

    # @commands.command(hidden=True)
    # async def unjail(self, ctx, *args):
    #     """Remove a user from jail"""
    #     if str(ctx.author.id) in trustedusers:
    #         unjailfile = os.path.join("internalfiles", "images", "2dll9My.png")
    #         for name in ctx.message.mentions:
    #             await self.bot.remove_roles(name, mainserverjailrole)
    #             await ctx.send(file=discord.File(fp=unjailfile, filename="snacksisback.png"),
    #                                      content="Removing " + str(name.mention) + " from jail!")
    #     else:
    #         await ctx.send("You are not authorized to use this command")


class AdminTesting:
    """Testing commands lol"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.group(hidden=True)
    @commands.is_owner()
    async def fake(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Command not recognized')

    # @commands.command(hidden=True)
    # async def guildchans(self, ctx):
    #     guildchannels = ctx.guild.channels
    #     allcategories = []
    #     nocategorychans = []
    #     mainlist = []
    #     for chan in guildchannels:
    #         if (chan.category is None) and type(chan) is not discord.CategoryChannel:
    #             nocategorychans += [chan]
    #         if type(chan) == discord.CategoryChannel:
    #             allcategories += dict(str(chan.position), str(chan.name), str(chan.id))
    #     print(allcategories)
    #     allcategories.sort()
    #     print("sorted")
    #     print("Categories:")
    #     for cat in allcategories:
    #         print(str(cat.position) + " - " + str(cat.name) + " - " + str(cat.id))
    #         chansincat = [cat.channels]
    #         for subchan in chansincat:
    #             print(subchan.name)
    #
    # @commands.command()
    # async def guildicon(self, ctx):
    #     icon = ctx.guild.icon_url
    #     print(icon)


def setup(dbot):
    dbot.add_cog(AdminCommands(dbot))
    dbot.add_cog(AdminTesting(dbot))
