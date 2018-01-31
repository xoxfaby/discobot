from extensions.utils.importsfile import *


class AdminCommands:
    """Admin shit"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        importlib.reload(self.dbotchecks)
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    @commands.command()
    @dbotchecks.check_server_admin_or_botowner()
    async def deletebotmessages(self, ctx, num: int):
        """Gets the last few messages from the channel history, and if they are from myself, I will delete the amount you specify"""
        try:
            await ctx.message.delete()
        except:
            pass
        messages_list = []
        async for msg in ctx.history(limit=num, before=ctx.message):
            if msg.author == ctx.me:
                messages_list.append(msg)
        await ctx.channel.delete_messages(messages_list)

    @commands.command()
    @dbotchecks.check_server_admin_or_botowner()
    async def purge(self, ctx, *, num: int):
        """Purges the last x number of messages from the channel"""
        try:
            await ctx.message.delete()
        except Exception as e:
            pass
        await ctx.channel.purge(limit=int(num))
        return await ctx.send(content='Deleted ' + str(num) + ' message(s)')

    @commands.command(hidden=True, aliases=['die'])
    @commands.is_owner()
    async def botkill(self, ctx):
        """This makes the bot shut itself down."""
        mesg = (f'The botkill command was called at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} in '
                f'{str(ctx.guild)} -{str(ctx.channel)}')
        self.bot.common.logger.info(mesg)
        print(mesg)
        if str('Direct Message') not in str(ctx.channel):
            try:
                await ctx.message.delete()
            except Exception as e:
                pass
        await ctx.send('Proceeding with bot shutdown now...')
        return await self.bot.logout()

    @commands.command(hidden=True)
    async def boatsay(self, ctx, *, args):
        """Sekrit"""
        mesg = args
        try:
            await ctx.message.delete()
        except:
            pass
        return await ctx.send(mesg)

    @commands.command(hidden=True)
    @dbotchecks.check_trusted_user()
    async def adminbotsay(self, ctx, chanid, *, args):
        """Sekrit"""
        mesg = args
        try:
            await ctx.message.delete()
        except:
            pass
        customchannel = self.bot.get_channel(id=int(chanid))
        return await customchannel.send(mesg)

    @commands.command()
    async def feedback(self, ctx, *, feedback: str):
        feedbackuserid = str(ctx.author.id)
        feedbackusername = str(ctx.author)
        sendtime = f'{datetime.datetime.now()}'
        if str('Direct Message') in str(ctx.channel):
            channelid = str(ctx.channel.id)
            channelname = f"DM"
            guildid = f"DM"
            guildname = f"DM"
        else:
            guildid = str(ctx.guild.id)
            guildname = str(ctx.guild.name)
            channelid = str(ctx.channel.id)
            channelname = str(ctx.channel.name)
        mesg = f"Alright, I've sent this feedback to my owner; thank you!"
        await ctx.send(mesg)
        sql_query = """
        INSERT INTO `{0}`.`_feedback`
        (`time`, `user-id`, `user-name`, `guild-id`, `guild-name`, `channel-id`, `channel-name`, `content`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        new_query = sql_query.format(str(self.bot.common.mysqldb))
        query_data = (str(sendtime), str(feedbackuserid), str(feedbackusername), str(guildid), str(guildname),
                      str(channelid), str(channelname), str(feedback))
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(new_query, query_data)
        mesg1 = f"I've recieved feedback from somebody! See below:\n"
        mesg1 += f"```\n"
        mesg1 += f"Username: {feedbackusername} - UserID: {feedbackuserid}\n"
        if str('Direct Message') in str(ctx.channel):
            mesg1 += f'Location: DM\n'
        else:
            mesg1 += f'Location: \n    Guild: {guildname} - {guildid}\n'
            mesg1 += f'    Channel: {channelname} - {channelid}\n\n'
        mesg1 += f'Feedback Message:\n{feedback}\n'
        mesg1 += f'```'
        for channel in self.bot.common.mainserverlogchan:
            chan = self.bot.get_channel(id=int(channel))
            await chan.send(mesg1)

    async def _role_getter(self, ctx, role):
        if not ctx.message.role_mentions:
            role = role.replace("@", "")
            mentioned_roles = await commands.RoleConverter().convert(ctx, role)
        else:
            mentioned_roles = ctx.message.role_mentions
        return mentioned_roles

    async def _user_getter(self, ctx, user):
        if not ctx.message.mentions:
            mentioned_users = await commands.MemberConverter().convert(ctx, user)
        else:
            mentioned_users = ctx.message.mentions
        return mentioned_users

    @commands.command()
    async def guildinfo(self, ctx):
        """Info about the discord guild/server"""
        guild = ctx.guild
        embed = discord.Embed(title="Guild Information")
        embed.add_field(name="Guild Name", value=f'{guild.name}', inline=True)
        embed.add_field(name="Guild ID", value=f'{guild.id}', inline=True)
        embed.add_field(name="Guild Region", value=f'{guild.region}', inline=True)
        embed.add_field(name="Number of Users", value=f'{guild.member_count}', inline=True)
        guildicon = ctx.guild.icon_url_as(format='png', size=1024)
        embed.add_field(name="Guild Icon", value="_\n_", inline=False)
        embed.set_image(url=guildicon)
        return await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user=None):
        """lists info about a mentioned user"""
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
        elif isinstance(mentioned_users, discord.Member) or isinstance(mentioned_users, discord.User):
            membername = mentioned_users.display_name
            memberid = mentioned_users.id
            if isinstance(mentioned_users, discord.Member):
                userrole = mentioned_users.top_role
                userjoinedguild = mentioned_users.joined_at
            else:
                userrole = "None"
                userjoinedguild = "None"
            useravatar = mentioned_users.avatar_url_as(format='jpg', size=1024)
            userjoineddisco = mentioned_users.created_at

        else:
            return
        embed.add_field(name="Member Name", value=str(membername))
        embed.add_field(name="Member ID", value=str(memberid))
        if isinstance(mentioned_users, discord.Member):
            embed.add_field(name="Top Role of User", value=f'`{str(userrole.name)}`')
        embed.add_field(name="Joined Discord", value=str(userjoineddisco), inline=False)
        if isinstance(mentioned_users, discord.Member):
            embed.add_field(name="Joined this Guild/Server", value=str(userjoinedguild), inline=False)
        embed.add_field(name="_\n_", value="_\n_", inline=False)
        embed.add_field(name="User Avatar", value="_\n_", inline=False)
        embed.set_image(url=useravatar)
        return await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx, role):
        """Subcommand to guildinfo, lists info about a mentioned role"""
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
        """Used to manage the server"""
        if ctx.invoked_subcommand is None:
            raise self.bot.errors.DBotExternalError("No subcommand was given")

    @manage.group(aliases=['roles'])
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx):
        """Subcommand to manage, can be used to manage a role"""
        if ctx.invoked_subcommand is None:
            raise self.bot.errors.DBotExternalError("No subcommand was given")

    @role.command()
    async def rolename(self, ctx, role, *rolename):
        """Subcommand to `manage role`, can be used to edit a role name"""
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
        """Subcommand to `manage role`, can be used to edit a role's color"""
        mentioned_roles = await self._role_getter(ctx, role)
        if not color:
            mesg = ''
            if isinstance(mentioned_roles, list):
                for role in mentioned_roles:
                    mesg += f"Current color for {role.mention}: {role.color}\n"
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

    @commands.group(aliases=['getprefix', 'showprefix'])
    async def prefix(self, ctx):
        """A group command to manage the prefix for the bot."""
        if ctx.invoked_subcommand is None:
            return await ctx.send("Available subcommands are `set` or `show`")

    @prefix.command()
    @dbotchecks.check_server_admin_or_botowner()
    async def set(self, ctx, *, newprefix):
        """Set a new prefix for the bot, unique to this server"""
        newcmd, querydata = await self.bot.sql.statement_insert_prefix(str(ctx.guild.id), str(newprefix))
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(newcmd, querydata)
        mesg = (f'Alright, I have set the custom prefix for this guild to be `{newprefix}`.\nPlease use that to use me'
                f' from now on. You can also view my prefix at any time by mentioning me and using the `showprefix`'
                f' command')
        await self.bot.pref.reload_prefix_cache()
        await ctx.send(mesg)

    @prefix.command()
    async def show(self, ctx):
        """The bot will retrieve and show the prefix listed for this server"""
        await self.bot.pref.reload_prefix_cache()
        sqlcmd = await self.bot.sql.statement_get_single_prefix()
        newcmd = sqlcmd.format(self.bot.common.mysqldb, ctx.guild.id)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(newcmd)
                num_rows = cursor.rowcount
                if num_rows:
                    prefix = (await cursor.fetchone())['prefix']
                else:
                    prefix = None
        if prefix is None:
            mesg = (f'You have not set a custom prefix on this server.\nMy default command prefix is `'
                    f'{self.bot.common.discordbotcommandprefix}` (Comma)\nYou can use '
                    f'`{self.bot.common.discordbotcommandprefix}prefix set mynewprefixhere` to set a new custom '
                    f'prefix.')
        else:
            mesg = (f'The prefix for this server is `{prefix}`\nTo run a command, you must either '
                    f'prepend this to the command, or mention me.\nTo set a new custom prefix, please use '
                    f'`{prefix}prefix set mynewprefixhere`')
        await ctx.send(mesg)

    @commands.command()
    async def feedbackreply(self, ctx, userid, *, text):
        member = await self._user_getter(ctx, str(userid))
        pass

    # @commands.group()
    # @dbotchecks.check_server_admin_or_botowner()
    # async def ignore(self, ctx):
    #     if ctx.invoked_subcommand is None:
    #         return await ctx.send("No subcommand was given; Please try `ignore`, `checkignore`, or `unignore`.")
    #
    # @ignore.command()
    # @dbotchecks.check_server_admin_or_botowner()
    # async def ignore(self, ctx, ignoretype, user):
    #     if ignoretype == "global":
    #         botowner = bool(ctx.author.id == self.bot.common.botowner)
    #         if botowner:
    #             pass
    #         else:
    #             return
    #     if ignoretype == "server":
    #         key = str(ctx.guild.id)
    #     elif ignoretype == "global":
    #         key = "global"
    #     else:
    #         return
    #     user_object = await self._user_getter(ctx, user)
    #     keyexist = await self.bot.ignorecache.exists(key)
    #     if keyexist:
    #         ignorelist = await self.bot.ignorecache.get(key)
    #         print(ignorelist)
    #         ignorelist.append(user_object.id)
    #         print(ignorelist)
    #         await self.bot.ignorecache.set(key=key, value=ignorelist)
    #
    # @ignore.command()
    # @dbotchecks.check_server_admin_or_botowner()
    # async def unignore(self, ctx, ignoretype, user):
    #     pass
    #
    # @ignore.command()
    # async def checkignore(self, ctx):
    #     listexists = await self.bot.ignorecache.exists(key=)
    #     if listexists:
    #         userlist = await self.bot.ignorecache.get()

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, text):
        """evaluate a python expression"""
        # Code lifted from Robodanny on 2018-01-23
        # Some adaptions have been made as to not completely copy Danny's code.
        # Sauce: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py
        if (text.startswith('```') or text.startswith('```py')) and text.endswith('```'):
            env = {'bot': self.bot, 'ctx': ctx, 'channel': ctx.channel, 'author': ctx.author, 'guild': ctx.guild,
                   'message': ctx.message, 'mysqlcon': self.bot.mysqlcon, 'mysqlcache': self.bot.mysqlcache,
                   'misccache': self.bot.misccache, }
            env.update(globals())
            newtext = '\n'.join(text.split('\n')[1:-1])
            stdout = io.StringIO()
            compiled = f'async def func():\n{textwrap.indent(newtext, "  ")}'
            try:
                exec(compiled, env)
            except Exception as e:
                await ctx.message.add_reaction('\u274C')
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            func = env['func']
            try:
                with contextlib.redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await ctx.message.add_reaction('\u274C')
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n{e}\n```')
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction('\u2705')
                except Exception as e:
                    pass
                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    await ctx.send(f'```py\n{value}{ret}\n```')
        else:
            return await ctx.send("You did not send a valid code block for me to run")

    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def allguildbroadcast(self, ctx, *, message):
    #     if str(ctx.author.id) == str(self.bot.common.botowner):
    #         sqlcmd = await self.bot.sql.statement_get_initialchannel()
    #         async with self.bot.mysqlcon.acquire() as conn:
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
    #
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
    #
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
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        importlib.reload(self.dbotchecks)
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    @commands.group(hidden=True)
    @commands.is_owner()
    async def fake(self, ctx):
        """Fake dispatch command"""
        if ctx.invoked_subcommand is None:
            return

    @fake.command()
    async def join(self, ctx):
        user = ctx.author
        self.bot.dispatch('member_join', user)

    @fake.command()
    async def guild_join(self, ctx):
        guild = ctx.guild
        self.bot.dispatch('guild_join', guild)

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx):
        """Echos a command to the console"""
        mesg = ctx.message.content
        print(mesg)
        return await ctx.send("Printed to PyCharm console.")

    @commands.command()
    async def testperms(self, ctx):
        print(ctx.author)
        print(any([ctx.channel.permissions_for(ctx.author).manage_guild, (str(ctx.author.id) in self.bot.common.trustedusers)]))
        print(str(ctx.author.id) in self.bot.common.trustedusers)
        print(type(self.bot.common.trustedusers[0]))
        print(ctx.channel.permissions_for(ctx.author).manage_guild)

    @commands.command()
    async def testcache(self, ctx):
        timerange = list(range(14400, 43200, 2))
        waittime = random.choice(timerange)
        curtime = datetime.datetime.now()
        waittime1 = datetime.timedelta(seconds=int(waittime))
        projectedtime = curtime + waittime1
        key = "testawootime"
        if await self.bot.misccache.exists(key=key):
            print("in exists")
            print(projectedtime)
            await self.bot.misccache.set(key=key, value=projectedtime)
        else:
            print("in else")
            await self.bot.misccache.add(key=key, value=projectedtime)
        print("out")
        keyout = await self.bot.misccache.get(key=key)
        print(keyout)

    @commands.command()
    async def printchan(self, ctx):
        print(ctx.message.channel)

    # @commands.command()
    # async def showprefix(self, ctx):
    #     prefixdict = await self.bot.mysqlcache.get(key="prefixes")
    #     print(type(prefixdict))
    #     print(prefixdict['guildid'])

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
    #
    # @commands.command()
    # async def tasks(self, ctx):
    #     tasks = asyncio.Task.all_tasks()
    #     print(tasks)

    @commands.command()
    async def plshalp(self, ctx):
        return await ctx.send("My bot is broken")
    #
    # @commands.command()
    # async def emojitest(self, ctx):
    #     awoolist = []
    #     for server in self.bot.guilds:
    #         for emoji in server.emojis:
    #             if "awoo12" in emoji.name.lower():
    #                 awoolist.append(emoji)
    #     mesg = ''
    #     for emote in awoolist:
    #         newemote = await commands.EmojiConverter().convert(ctx, str(emote))
    #         print(emote)
    #         print(type(emote))
    #     await ctx.send(emote)



def setup(dbot):
    dbot.add_cog(AdminCommands(dbot))
    dbot.add_cog(AdminTesting(dbot))
