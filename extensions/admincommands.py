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
        try:
            await ctx.message.delete()
        except:
            pass
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
        try:
            await ctx.message.delete()
        except:
            pass
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
    # @commands.check(check_trusted_user)
    async def boatsay(self, ctx, *args):
        """
        Sekrit
        """
        mesg = ' '.join(args)
        try:
            await ctx.message.delete()
        except:
            pass
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

    @commands.group()
    @commands.has_permissions(manage_roles=True)
    async def managerole(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No subcommand was given")

    @managerole.command()
    async def color(self, ctx, *role):
        def checkresponse(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel) and \
                   (response.content == keys for keys in availablecolors)
        availablecolors = {
            'default': 0, 'teal': 0x1abc9c, 'dark_teal': 0x11806a, 'green': 0x2ecc71, 'dark_green': 0x1f8b4c,
            'blue': 0x3498db, 'dark_blue': 0x206694, 'purple': 0x9b59b6, 'dark_purple': 0x71368a, 'magenta': 0xe91e63,
            'dark_magenta': 0xad1457, 'gold': 0xf1c40f, 'dark_gold': 0xc27c0e, 'orange': 0xe67e22,
            'dark_orange': 0xa84300, 'red': 0xe74c3c, 'dark_red': 0x992d22, 'dark_grey': 0x607d8b,
            'light_grey': 0x979c9f, 'darker_grey': 0x546e7a, 'blurple': 0x7289da, 'greyple': 0x99aab5
        }
        messagelist = []
        colorlist = ''
        for key in availablecolors:
            colorlist += f'{key}, '
        mentioned_roles = ctx.message.role_mentions
        mymessage = await ctx.send(f'What color would you like to change the role {mentioned_roles[0].mention} to?\n'
                                   f'Available colors: {str(colorlist)}')
        response = await self.bot.wait_for('message', check=checkresponse, timeout=60)
        color = discord.Color(availablecolors[response.content])
        messagelist.append(response)
        messagelist.append(mymessage)
        for role in mentioned_roles:
            await role.edit(color=color)
            await ctx.message.add_reaction('✅')
            await ctx.channel.delete_messages(messagelist)
        return

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

    @commands.command()
    async def walkcommands(self, ctx):
        for cmd in self.bot.walk_commands():
            print(cmd)


def setup(dbot):
    dbot.add_cog(AdminCommands(dbot))
    dbot.add_cog(AdminTesting(dbot))
