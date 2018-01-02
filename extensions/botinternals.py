from extensions.utils.importsfile import *


class BotInternals:
    """Bot Internal Shit"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(hidden=True)
    async def help(self, ctx):
        return await ctx.send("Please see my help documentation at <https://personalwebsite.website/wiki/noodlebot>")

    @commands.command()
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.common.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        fmt = '{h} hours, {m} minutes, and {s} seconds'
        fmtnew = fmt.format(h=hours, m=minutes, s=seconds)
        return await ctx.send(fmtnew)

    async def on_command_error(self, ctx, exception):
        print(str(datetime.datetime.now()) + ': ' + str(exception))
        if isinstance(exception, commands.errors.NotOwner):
            return await ctx.send(content="You do not have the permissions to perform this command.")
        elif isinstance(exception, commands.errors.CheckFailure):
            return await ctx.send(content='You do not have the permissions to perform this command.')
        elif isinstance(exception, commands.errors.CommandNotFound):
            return await ctx.send(content="Command not recognized")
        elif isinstance(exception, commands.errors.BadArgument):
            return await ctx.send(content="You have provided an invalid argument for this command")
        elif isinstance(exception, commands.errors.UserInputError):
            return await ctx.send(content="You have provided an invalid input for this command")
        else:
            return await ctx.send(content='Command not recognized')

    async def memberbotmessage(self, member, secondaryargs):
        if str(member) == str(member.guild.me):
            return
        channel = member.guild.system_channel
        if not channel:
            return
        else:
            messages = {"join": "Welcome to {1}, {0}~", "leave": "ok bye {0}"}
            welcomemessage = messages[secondaryargs].format(member.mention, member.guild.name)
            return await channel.send(content=welcomemessage)

    async def on_member_join(self, member):
        await self.memberbotmessage(member, "join")

    async def on_member_remove(self, member):
        await self.memberbotmessage(member, "leave")


class BotInfo:
    """Bot Information and configuration"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_guild_join(self, guild):
        channel = guild.system_channel
        if channel is None:
            guildchans = guild.text_channels
            for chan in guildchans:
                sendperms = chan.permissions_for(guild.me).send_messages
                if sendperms:
                    initialchannel = chan
                    break
                else:
                    pass
        else:
            initialchannel = channel
        message = ("I am " + self.bot.common.botdescription + "\nThank you for joining me to this server, please run `"
                   + self.bot.common.discordbotcommandprefix + "bogconfig` to run my setup for this server.\nIn the " +
                   "setup we'll set things such as if and where you want welcome messages and other features.\n"
                   "**Please note, you will need `manage_guild` permissions on this guild in order to run `botconfig`")
        await initialchannel.send(message)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def botconfig(self, ctx):
        def checkauthor(m):
            return m.author == ctx.author

        yesanswerlist = ['yes', 'y', 'true', 'yeah', 'yup', '1', 't']
        noanswerlist = ['no', 'n', 'negative', 'false', 'nope', '0', 'f']
        configmessagelist = []
        startmsg = ('Beginning the bot configuration for server: ' + ctx.guild.name)
        sent_startmsg = await ctx.send(startmsg)
        configmessagelist.append(sent_startmsg)
        thischannelmsg = ("As a note, I am marking this channel as the 'initial' channel for this server\n"
                          "If my creator needs to send an announcement to all servers I am joined to, "
                          "I will send the message to this channel;\nNote: announcements are very rare, "
                          "I won't spam up your channel\nIs this acceptable? Please type 'yes' or 'no'")
        sent_thischannelmsg = await ctx.send(thischannelmsg)
        configmessagelist.append(sent_thischannelmsg)
        thischannelresp = await self.bot.wait_for('message', check=checkauthor)
        configmessagelist.append(thischannelresp)
        enablelogging = True
        thischannelresp1 = thischannelresp.content.lower()
        if thischannelresp1 in yesanswerlist:
            announcemsg1 = await ctx.send("Awesome, I'll mark this down as a good channel to send announcements to. "
                                          "Thanks!")
            configmessagelist.append(announcemsg1)
            initialchan = ctx.channel
        else:
            announcemsg1 = await ctx.send("Please enter the name of the channel you would like bot announcements sent "
                                          "to.\n(You can do this by typing a `#` and the channel name)")
            configmessagelist.append(announcemsg1)
            initialchanresp = await self.bot.wait_for('message', check=checkauthor)
            configmessagelist.append(initialchanresp)
            initialchan = initialchanresp.channel_mentions[0]
            myinitalresp = await ctx.send("You've selected " + str(initialchan.mention) +
                                          " as the channel I will send announcements to")
            configmessagelist.append(myinitalresp)

        await asyncio.sleep(0.5)
        usermsgs = ("Do you want to enable user join/part messages?\nPlease enter 'yes' or 'no'\n"
                    "Example: <https://personalwebsite.website/wiki/images/7/73/Bot_messages.png>")
        sent_usermsgs = await ctx.send(usermsgs)
        configmessagelist.append(sent_usermsgs)
        enableloggingresp = await self.bot.wait_for('message', check=checkauthor)
        configmessagelist.append(enableloggingresp)
        loggingresp = enableloggingresp.content.lower()
        if loggingresp in yesanswerlist:
            myloggingresp = await ctx.send("Please enter the name of the welcome channel\n"
                                           "(You can do this by typing a `#` and the channel name)")
            configmessagelist.append(myloggingresp)
            welcomechanmessage = await self.bot.wait_for('message', check=checkauthor)
            configmessagelist.append(welcomechanmessage)
            welcomechan = welcomechanmessage.channel_mentions[0]
            mywelcomeresp = await ctx.send("You've selected " + str(welcomechan.mention) + " as your new user welcome channel")
            configmessagelist.append(mywelcomeresp)
            welcomechanbool = 1
        else:
            mywelcomeresp = await ctx.send("You've selected to not enable welcome/part messages for this server.")
            configmessagelist.append(mywelcomeresp)
            welcomechan = None
            welcomechanbool = 0

        await asyncio.sleep(0.5)
        adminauditlogmsg = ("Do you want to enable an audit log which will be a log with timestamps, "
                            "of users who join and part this guild?\nPlease enter 'yes' or 'no'")
        sent_adminauditlogmsg = await ctx.send(adminauditlogmsg)
        configmessagelist.append(sent_adminauditlogmsg)
        adminauditlogresp = await self.bot.wait_for('message', check=checkauthor)
        configmessagelist.append(adminauditlogresp)
        auditresp = adminauditlogresp.content.lower()
        if auditresp in yesanswerlist:
            adminlogchanmsg = (
                "Please enter the name of the channel you would like to use as a user log audit channel\n"
                "This channel will be used to make a log of users who join and leave with timestamps.\n"
                "If you don't want to have a secondary channel of user joins/parts, please type 'None'\n"
                "(You can do this by typing a `#` and the channel name)\n"
                "Example: <https://personalwebsite.website/wiki/images/7/73/Bot_messages.png>"
            )
            sent_adminlogchanmsg = await ctx.send(adminlogchanmsg)
            configmessagelist.append(sent_adminlogchanmsg)
            adminlogchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(adminlogchanresp)
            adminlogchan = adminlogchanresp.channel_mentions[0]
            myresp = await ctx.send("You've selected " + str(adminlogchan.mention) + " as the user log channel")
            configmessagelist.append(myresp)
            adminlogchanbool = 1
        else:
            myresp = await ctx.send("You've selected to not enable user join/part messages for this server")
            configmessagelist.append(myresp)
            adminlogchan = None
            adminlogchanbool = 0

        await asyncio.sleep(0.5)
        voicelogmsg = ("Do you want to enable a voice audit log?\n"
                       "If enabled, with this function, I will send messages with timestamps of who "
                       "joined which voice channel\n"
                       "Please enter 'yes' or 'no'\n"
                       "**__Attention: the bot will not, and will never join voice channels, and thus, "
                       "conversations will never be recorded.__**\n"
                       "**__This feature will only send a message containing [time, who, joined/left, voicechannel__**"
                       "\nExample: <https://personalwebsite.website/wiki/images/0/05/Bot-voice_channel_message.png>"
                       )
        sent_voicelogmsg = await ctx.send(voicelogmsg)
        configmessagelist.append(sent_voicelogmsg)
        voicelogmsgresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        configmessagelist.append(voicelogmsgresp)
        voiceresp = voicelogmsgresp.content.lower()
        if voiceresp in yesanswerlist:
            voicelogchanmsg = (
                "Please enter the name of the channel you would like to use as a voice connection log channel\n"
                "(You can do this by typing a `#` and the channel name)"
            )
            sent_voicelogchanmsg = await ctx.send(voicelogchanmsg)
            configmessagelist.append(sent_voicelogchanmsg)
            voicelogchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(voicelogchanresp)
            voicelogchan = voicelogchanresp.channel_mentions[0]
            myresp1 = await ctx.send("You've selected " + str(voicelogchan.mention) + " as the voice log channel")
            configmessagelist.append(myresp1)
            voicelogchanbool = 1
        else:
            myresp1 = await ctx.send("You've selected to not enable user voice messages for this server")
            configmessagelist.append(myresp1)
            voicelogchan = None
            voicelogchanbool = 0

        await ctx.channel.delete_messages(configmessagelist)
        endconfigmsg = ("This concludes my configuration.\nThank you for adding me to this server;\n"
                        "You can view my help documentation at <https://personalwebsite.website/wiki/Noodlebot>\n"
                        "My creator is `noodle#4660`, and you can join my main server at "
                        "<https://discord.gg/9B8eVyx> if you need help with me.\n"
                        "You can also re-run this configuration command at any time to change your selections.")
        await ctx.send(endconfigmsg)
        channellist = [initialchan, welcomechan, adminlogchan, voicelogchan]
        responses = [enablelogging, welcomechanbool, adminlogchanbool, voicelogchanbool]
        sqlquery, tablename, querydata = await self.bot.sql.statement_insert_guildconfig(ctx, channellist, responses)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sqlquery, querydata)


    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Bot Information", description="Noodle Disco-Pybot", color=0x3347ff)
        embed.add_field(name="Web URL", value="[Boat Wiki](https://personalwebsite.website/wiki/noodlebot)")
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/app-icons/340802627887693825/f830b6257e434a56cab408ece5cf8fa8.png')
        embed.add_field(name="Creator", value="noodle#4660", inline=False)
        embed.add_field(name="Invite", value="[Invite URL]"
                                             "(https://discordapp.com/oauth2/authorize?client_id=340802627887693825"
                                             "&scope=bot&permissions=1610083543)", inline=False)
        embed.add_field(name="Bot Prefix", value="`,` (Comma)", inline=False)
        embed.add_field(name="Source", value="[Github](https://github.com/jwshields/discobot)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        t1 = time.perf_counter()
        await ctx.channel.trigger_typing()
        t2 = time.perf_counter()
        await ctx.channel.send("pseudo-ping: {}ms".format(round((t2-t1)*1000)))

    @commands.command(description="This command can be used to invite the bot to a server")
    async def invite(self, ctx):
        perms = discord.Permissions.none()
        perms.create_instant_invite = True
        perms.kick_members = True
        perms.ban_members = True
        perms.manage_channels = True
        perms.add_reactions = True
        perms.view_audit_log = True
        perms.read_messages = True
        perms.send_messages = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.attach_files = True
        perms.read_message_history = True
        perms.mention_everyone = True
        perms.external_emojis = True
        perms.connect = True
        perms.speak = True
        perms.mute_members = True
        perms.deafen_members = True
        perms.move_members = True
        perms.use_voice_activation = True
        perms.change_nickname = True
        perms.manage_nicknames = True
        perms.manage_roles = True
        perms.manage_emojis = True
        await ctx.send('Please click on this link to invite me to your server.\n'
                       + f'<{discord.utils.oauth_url(str(self.bot.common.botdiscordid), perms)}>')


def setup(dbot):
    dbot.remove_command("help")
    dbot.add_cog(BotInternals(dbot))
    dbot.add_cog(BotInfo(dbot))
