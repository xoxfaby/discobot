from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class AdminCommands:
    """Admin shit"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def deletebotmessages(self, ctx, num: int):
        try:
            await ctx.message.delete()
        except:
            pass
        limit = int(num)
        messages_list = []
        messages_list += (x for x in await ctx.history(limit=limit, before=ctx.message).flatten() if x.author == ctx.me)
        await ctx.channel.delete_messages(messages_list)

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
        """This makes the bot shut itself down."""
        mesg = (f'The botkill command was called at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} in '
                f'{str(ctx.guild)} -{str(ctx.channel)}')
        self.bot.common.logger.info(mesg)
        print(mesg)
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        await ctx.send('Proceeding with bot shutdown now...')
        await self.bot.sql.mysqlcon.close()
        return await self.bot.logout()

    @commands.command(hidden=True)
    @commands.check(dbotchecks.check_trusted_user)
    async def boatsay(self, ctx, *args):
        """Sekrit"""
        mesg = ' '.join(args)
        try:
            await ctx.message.delete()
        except:
            pass
        return await ctx.send(mesg)

    @commands.command(hidden=True)
    @commands.check(dbotchecks.check_trusted_user)
    async def adminbotsay(self, ctx, chanid, *args):
        """Sekrit"""
        mesg = ' '.join(args)
        try:
            await ctx.message.delete()
        except:
            pass
        customchannel = self.bot.get_channel(id=int(chanid))
        return await customchannel.send(mesg)

    async def _role_getter(self, ctx, role):
        if not ctx.message.role_mentions:
            role = role.replace("@", "")
            mentioned_roles = await commands.RoleConverter().convert(ctx, role)
        else:
            mentioned_roles = ctx.message.role_mentions
        return mentioned_roles

    async def _user_getter(self, ctx, user):
        if not ctx.message.mentions:
            mentioned_users = await commands.UserConverter().convert(ctx, user)
        else:
            mentioned_users = ctx.message.mentions
        return mentioned_users

    @commands.group()
    async def guildinfo(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Guild Information")
            embed.add_field(name="Guild Name", value=f'{ctx.guild.name}', inline=True)
            embed.add_field(name="Guild ID", value=f'{ctx.guild.id}', inline=True)
            embed.add_field(name="Guild Region", value=f'{ctx.guild.region}', inline=True)
            embed.add_field(name="Number of Users", value=f'{len(ctx.guild.members)}', inline=True)
            guildicon = ctx.guild.icon_url_as(format='png', size=1024)
            embed.add_field(name="Guild Icon", value="_\n_", inline=False)
            embed.set_image(url=guildicon)
            return await ctx.send(embed=embed)
        else:
            return

    @guildinfo.command()
    async def userinfo(self, ctx, user=None):
        if user is None:
            mentioned_users = ctx.author
        else:
            mentioned_users = await self._user_getter(ctx, user)
        embed = discord.Embed(Title="User Information")
        if isinstance(mentioned_users, list):
            membername = mentioned_users[0].display_name
            memberid = mentioned_users[0].id
            userrole = mentioned_users[0].top_role
            useravatar = mentioned_users[0].avatar_url_as(format='jpg', size=1024)
            userjoineddisco = mentioned_users[0].created_at
            userjoinedguild = mentioned_users[0].joined_at
        elif isinstance(mentioned_users, discord.Member):
            membername = mentioned_users.display_name
            memberid = mentioned_users.id
            userrole = mentioned_users.top_role
            useravatar = mentioned_users.avatar_url_as(format='jpg', size=1024)
            userjoineddisco = mentioned_users.created_at
            userjoinedguild = mentioned_users.joined_at
        else:
            return
        embed.add_field(name="Member Name", value=str(membername))
        embed.add_field(name="Member ID", value=str(memberid))
        embed.add_field(name="Top Role of User", value=str(userrole.name))
        embed.add_field(name="Joined Discord", value=str(userjoineddisco), inline=False)
        embed.add_field(name="Joined this Guild/Server", value=str(userjoinedguild), inline=False)
        embed.add_field(name="_\n_", value="_\n_", inline=False)
        embed.add_field(name="User Avatar", value="_\n_", inline=False)
        embed.set_image(url=useravatar)
        return await ctx.send(embed=embed)

    @guildinfo.command()
    async def roleinfo(self, ctx, role):
        mentioned_roles = await self._role_getter(ctx, role)
        embed = discord.Embed(title="Role Information")
        if isinstance(mentioned_roles, list):
            rolecolor = mentioned_roles[0].color
            numusers = len(mentioned_roles[0].members)
            roleid = str(mentioned_roles[0].id)
            rolename = str(mentioned_roles[0].name)
            rolecreated = str(mentioned_roles[0].created_at)
        elif isinstance(mentioned_roles, discord.Role):
            rolecolor = mentioned_roles.color
            numusers = len(mentioned_roles.members)
            roleid = str(mentioned_roles.id)
            rolename = str(mentioned_roles.name)
            rolecreated = str(mentioned_roles.created_at)
        else:
            return
        embed.add_field(name="Role Name", value=str(rolename), inline=True)
        embed.add_field(name="Role ID", value=str(roleid), inline=True)
        embed.add_field(name="Numer of users with role", value=str(numusers), inline=False)
        embed.add_field(name="Role Color", value=str(rolecolor), inline=False)
        embed.add_field(name="Created at", value=str(rolecreated), inline=False)
        await ctx.send(embed=embed)

    @commands.group(aliases=['server'])
    async def manage(self, ctx):
        if ctx.invoked_subcommand is None:
            raise self.bot.errors.DBotExternalError("No subcommand was given")

    @manage.group(aliases=['roles'])
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            raise self.bot.errors.DBotExternalError("No subcommand was given")

    @role.command()
    async def rolename(self, ctx, role, *rolename):
        mentioned_roles = await self._role_getter(ctx, role)
        if not rolename:
            mesg = f'No new name was submitted for role: {0}'
            if isinstance(mentioned_roles, list):
                mesg = mesg.format(mentioned_roles[0].mention)
            elif isinstance(mentioned_roles, discord.Role):
                mesg = mesg.format(mentioned_roles.mention)
            raise self.bot.errors.DBotExternalError(mesg)
        else:
            newname = ''.join(rolename)
            if isinstance(mentioned_roles, list):
                for role in mentioned_roles:
                    await role.edit(name=newname)
                    return await ctx.message.add_reaction('✅')
            elif isinstance(mentioned_roles, discord.Role):
                await mentioned_roles.edit(name=newname)
                return await ctx.message.add_reaction('✅')

    @role.command()
    async def color(self, ctx, role, *color):
        mentioned_roles = await self._role_getter(ctx, role)
        if not color:
            mesg = ''
            if isinstance(mentioned_roles, list):
                for role in mentioned_roles:
                    mesg += f"Current color for {role.mention}: {role.color}\n"
                return await ctx.send(mesg)
            elif isinstance(mentioned_roles, discord.Role):
                mesg = f"Current color for {mentioned_roles.mention}: {mentioned_roles.color}\n"
                return await ctx.send(mesg)
        else:
            color1 = ''.join(color)
            color1 = color1.replace("#", "")
            newcolor = discord.Color(int(color1, 16))
            if type(newcolor) == discord.Color:
                if isinstance(mentioned_roles, list):
                    for role in mentioned_roles:
                        await role.edit(color=newcolor)
                        return await ctx.message.add_reaction('✅')
                elif isinstance(mentioned_roles, discord.Role):
                    await mentioned_roles.edit(color=newcolor)
                    return await ctx.message.add_reaction('✅')

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
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    @commands.group(hidden=True)
    @commands.is_owner()
    async def fake(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx):
        """Echos a command to the console"""
        mesg = ctx.message.content
        print(mesg)
        return await ctx.send("Printed to PyCharm console.")

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
    #
    # @commands.command()
    # async def walkcommands(self, ctx):
    #     for cmd in self.bot.walk_commands():
    #         print(cmd)
    #
    # @commands.command()
    # async def showtasks(self, ctx):
    #     awoo = self.bot.bg_awoo()
    #     print(awoo)


def setup(dbot):
    dbot.add_cog(AdminCommands(dbot))
    dbot.add_cog(AdminTesting(dbot))
