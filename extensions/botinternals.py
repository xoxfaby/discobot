from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class BotInternals:
    """Bot Internal Shit"""
    def __init__(self, bot):
        self.bot = bot
        self.bot.misccache = aiocache.SimpleMemoryCache(serializer=NullSerializer, namespace="misc")
        self.bot.ignore = aiocache.SimpleMemoryCache(serializer=NullSerializer, namespace="ignore")
        self.bot.cd = commands.CooldownMapping.from_cooldown(5, 30.0, commands.BucketType.user)
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def on_ready(self):
        game = discord.Game(name="https://personalwebsite.website/wiki/Noodlebot")
        await self.bot.change_presence(status=discord.Status.online, game=game)

    async def on_command_error(self, ctx, exception):
        if ctx.author.bot:
            return
        print(str(datetime.datetime.now()) + ': ' + str(exception))
        if isinstance(exception, self.bot.errors.DBotInternalError):
            return await ctx.send(content=exception)
        elif isinstance(exception, self.bot.errors.DBotExternalError):
            return await ctx.send(content=exception)
        elif isinstance(exception, self.bot.errors.DBotCooldownError):
            return
        elif isinstance(exception, commands.errors.NotOwner):
            return await ctx.send(content="You do not have the permissions to perform this command.")
        elif isinstance(exception, commands.errors.CheckFailure):
            return
        elif isinstance(exception, commands.errors.CommandNotFound):
            return
        elif isinstance(exception, commands.errors.BadArgument):
            return await ctx.send(content="You have provided an invalid argument for this command")
        elif isinstance(exception, commands.errors.UserInputError):
            return await ctx.send(content="You have provided an invalid input for this command")
        elif isinstance(exception, self.bot.errors.BotNotWorking):
            return await ctx.send(content=exception)
        else:
            return await ctx.send(content='An unknown error has occurred.')

    async def on_voice_state_update(self, member, before, after):
        if str(before.channel) == str(after.channel):
            return
        else:
            member_guild_config = str(f'{str(member.guild.id)}_guild_config')
            guild_config_exists_in_cache = await self.bot.mysqlcache.exists(key=member_guild_config)
            if guild_config_exists_in_cache:
                guild_conf = await self.bot.mysqlcache.get(key=member_guild_config)
                if bool(guild_conf['isconfigged']):
                    enable_voice_logs = bool(guild_conf['enablevoicelogs'])
                else:
                    return
            else:
                sql_cmd, table_name = await self.bot.sql.statement_get_server_config(member.guild)
                async with self.bot.mysqlcon.acquire() as conn:
                    async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(sql_cmd)
                        rowcount = cursor.rowcount
                        if rowcount == 1:
                            guild_conf = await cursor.fetchone()
                            await self.bot.mysqlcache.add(key=member_guild_config, value=guild_conf)
                            enable_voice_logs = bool(guild_conf['enablevoicelogs'])
                        else:
                            return
            if enable_voice_logs:
                content = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': ' + str(member) +
                           ' is in voice channel: ' + str(after.channel))
                voice_log_chan = self.bot.get_channel(id=int(guild_conf['voicelogchannel']))
                await voice_log_chan.send(content=content)
            else:
                return

    async def member_bot_message(self, member, secondaryargs, guild):
        if member == guild.me:
            return
        else:
            member_guild_config = str(f'{str(guild.id)}_guild_config')
            guild_config_exists_in_cache = await self.bot.mysqlcache.exists(key=member_guild_config)
            if guild_config_exists_in_cache:
                guild_conf = await self.bot.mysqlcache.get(key=member_guild_config)
                run_next = bool(guild_conf['isconfigged'])
            else:
                sql_cmd, table_name = await self.bot.sql.statement_get_server_config(guild)
                async with self.bot.mysqlcon.acquire() as conn:
                    async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(sql_cmd)
                        rowcount = cursor.rowcount
                        if rowcount == 1:
                            guild_conf = await cursor.fetchone()
                            await self.bot.mysqlcache.add(key=member_guild_config, value=guild_conf)
                            run_next = bool(guild_conf['isconfigged'])
                        else:
                            return
            if run_next:
                if bool(guild_conf['enableusewelcome']):
                    message_dict = {"join": guild_conf['welcomemessage'], "leave": guild_conf['partmessage'],
                                    "ban": "{0} was banned.", "unban": "{0} was unbanned"}
                    welcome_channel = self.bot.get_channel(id=int(guild_conf['welcomechannel']))
                    welcome_message = message_dict[secondaryargs].format(member.mention, guild.name)
                    if str(secondaryargs) is not "unban":
                        await welcome_channel.send(content=welcome_message)
                if bool(guild_conf['enableadminlogs']):
                    member_verb = {"join": " joined the server", "leave": " left the server",
                                   "ban": " was banned from the server", "unban": " was unbanned from the server"}
                    admin_msg = (str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ': ' + str(member) +
                                 str(member_verb[secondaryargs]))
                    admin_channel = self.bot.get_channel(id=int(guild_conf['adminchannel']))
                    await admin_channel.send(admin_msg)
            else:
                return

    async def on_member_join(self, member):
        await self.member_bot_message(member, "join", member.guild)

    async def on_member_remove(self, member):
        await self.member_bot_message(member, "leave", member.guild)

    async def on_member_ban(self, guild, member):
        await self.member_bot_message(member, "ban", guild)

    async def on_member_unban(self, guild, member):
        await self.member_bot_message(member, "unban", guild)


class BotInfo:
    """Bot Information and configuration"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

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
        message = (f'Hello! I am {self.bot.common.botdescription}\nThank you for joining me to this server, please run '
                   f'`{self.bot.common.discordbotcommandprefix}botconfig` to run my setup for this server.\nIn the '
                   f'setup we\'ll set things such as if and where you want welcome messages and other features.\n'
                   f'**Please note, you will need `manage_guild` permissions on this guild in order to run`'
                   f'{self.bot.common.discordbotcommandprefix}botconfig`**')
        try:
            await initialchannel.send(message)
        except Exception:
            return
            # fmt = f'On guild {guild.id} - {guild.name} - I was unable to send an initial message.'
            # raise self.bot.errors.DBotExternalError()

    @commands.command()
    async def info(self, ctx):
        """This command shows various information about the bot."""
        embed = discord.Embed(title="Bot Information", description="Noodle Disco-Pybot", color=0x3347ff)
        embed.add_field(name="Web URL", value="[Boat Wiki](https://personalwebsite.website/wiki/noodlebot)")
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/app-icons/340802627887693825/f830b6257e434a56cab408ece5cf8fa8.png')
        embed.add_field(name="Creator", value="`noodle#4660`")
        embed.add_field(name="Invite", value="[Invite URL]"
                                             "(https://discordapp.com/oauth2/authorize?client_id=340802627887693825&"
                                             "scope=bot&permissions=365030599)")
        embed.add_field(name="Bot Prefix", value="`,` (Comma)")
        embed.add_field(name="Source", value="[Github](https://github.com/jwshields/discobot)")
        now = datetime.datetime.utcnow()
        delta = now - self.bot.starttime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        fmt = '{h} hours, {m} minutes, and {s} seconds'
        fmt_new = fmt.format(h=hours, m=minutes, s=seconds)
        embed.add_field(name="Uptime", value=fmt_new)
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """This command shows the uptime of the bot."""
        now = datetime.datetime.utcnow()
        delta = now - self.bot.starttime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        fmt = '{h} hours, {m} minutes, and {s} seconds'
        fmt_new = fmt.format(h=hours, m=minutes, s=seconds)
        return await ctx.send(fmt_new)

    @commands.command()
    async def ping(self, ctx):
        """
        This command takes no arguments
        It will give you a pseudo-ping time, counting the amount of time it takes to send a "typing" signal to discord.
        """
        t1 = time.perf_counter()
        await ctx.channel.trigger_typing()
        t2 = time.perf_counter()
        await ctx.channel.send(f'pseudo-ping: {round((t2-t1)*1000)}ms')

    @commands.command(description="This command can be used to invite the bot to a server")
    async def invite(self, ctx):
        """
        This command takes no arguments.
        It can be used to generate an invite URL for me to join your server.
        """
        perms = discord.Permissions.none()
        perms.create_instant_invite = True
        perms.kick_members = True
        perms.ban_members = True
        perms.add_reactions = True
        perms.view_audit_log = True
        perms.read_messages = True
        perms.send_messages = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.attach_files = True
        perms.read_message_history = True
        perms.mute_members = True
        perms.deafen_members = True
        perms.move_members = True
        perms.change_nickname = True
        perms.manage_roles = True
        # URL should come out to be this:
        # https://discordapp.com/oauth2/authorize?client_id=340802627887693825&scope=bot&permissions=365030599
        await ctx.send('Please click on this link to invite me to your server.\n'
                       + f'<{discord.utils.oauth_url(str(self.bot.common.botdiscordid), perms)}>')

    # Yes, I know this command is a mess. I need to rewrite it.
    @commands.command(hidden=True, aliases=['botconfig', 'config'])
    @dbotchecks.check_server_admin_or_botowner()
    @commands.guild_only()
    async def bot_config(self, ctx):
        """
        This command can only be used by users with the `manage_guild` permission or higher.
        This command accepts no arguments when calling it;
        Calling this command will begin the bot into a prompt with you about how to configure various options on this server.
        At the end of the configuration, I will delete messages relating to the config as to not clog up the room with messages.
        """
        def checkauthor(m):
            return (m.author == ctx.author) and (m.channel == ctx.channel) and (m.content != "cancel")
        with open(os.path.join("extensions", "utils", "botconfig-lines.txt"), encoding='utf-8', mode='r') as infile:
            botconfigscript = infile.read().split("%%\n")
        yesanswerlist = ['yes', 'y', 'true', 'yeah', 'yup', '1', 't']
        configmessagelist = []
        userresp = []
        configmessagelist1 = []
        sent_startmsg = await ctx.send(str(botconfigscript[0]).format(str(ctx.guild.name)))
        configmessagelist1.append(sent_startmsg)
        sent_thischannelmsg = await ctx.send(botconfigscript[1])
        configmessagelist.append(sent_thischannelmsg)
        thischannelresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        userresp.append(thischannelresp)
        thischannelresp1 = thischannelresp.content.lower()
        if thischannelresp1 in yesanswerlist:
            announcemsg1 = await ctx.send(botconfigscript[2])
            configmessagelist.append(announcemsg1)
            initialchan = ctx.channel
        else:
            announcemsg1 = await ctx.send(botconfigscript[3])
            configmessagelist.append(announcemsg1)
            initialchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            userresp.append(initialchanresp)
            initialchan = initialchanresp.channel_mentions[0]
            myinitalresp = await ctx.send(botconfigscript[4].format(str(initialchan.mention)))
            configmessagelist.append(myinitalresp)
        await asyncio.sleep(0.5)
        sent_usermsgs = await ctx.send(botconfigscript[5])
        configmessagelist.append(sent_usermsgs)
        enableloggingresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        userresp.append(enableloggingresp)
        loggingresp = enableloggingresp.content.lower()
        if loggingresp in yesanswerlist:
            myloggingresp = await ctx.send(botconfigscript[6])
            configmessagelist.append(myloggingresp)
            welcomechanmessage = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            userresp.append(welcomechanmessage)
            welcomechan = welcomechanmessage.channel_mentions[0]
            mywelcomeresp = await ctx.send(botconfigscript[7].format(str(welcomechan.mention)))
            configmessagelist.append(mywelcomeresp)
            welcomechanbool = 1
            sent_defaultmessages = await ctx.send(botconfigscript[18])
            configmessagelist.append(sent_defaultmessages)
            defaultmessagesresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            userresp.append(defaultmessagesresp)
            secondresp = defaultmessagesresp.content.lower()
            if secondresp in yesanswerlist:
                sent_asknewwelcome = await ctx.send(botconfigscript[19])
                configmessagelist.append(sent_asknewwelcome)
                newwelcomeresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
                userresp.append(newwelcomeresp)
                welcomemessage = newwelcomeresp.content
                sent_asknewpart = await ctx.send(botconfigscript[20])
                configmessagelist.append(sent_asknewpart)
                newleaveresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
                userresp.append(newleaveresp)
                leavemessage = newleaveresp.content
            else:
                sent_nochangemessages = await ctx.send(botconfigscript[21])
                configmessagelist.append(sent_nochangemessages)
                welcomemessage = botconfigscript[25]
                leavemessage = botconfigscript[26]
        else:
            mywelcomeresp = await ctx.send(botconfigscript[8])
            configmessagelist.append(mywelcomeresp)
            welcomechan = None
            welcomechanbool = 0
            welcomemessage = None
            leavemessage = None
        await asyncio.sleep(0.5)
        sent_adminauditlogmsg = await ctx.send(botconfigscript[9])
        configmessagelist.append(sent_adminauditlogmsg)
        adminauditlogresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        userresp.append(adminauditlogresp)
        auditresp = adminauditlogresp.content.lower()
        if auditresp in yesanswerlist:
            sent_adminlogchanmsg = await ctx.send(botconfigscript[10])
            configmessagelist.append(sent_adminlogchanmsg)
            adminlogchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            userresp.append(adminlogchanresp)
            adminlogchan = adminlogchanresp.channel_mentions[0]
            myresp = await ctx.send(botconfigscript[11].format(str(adminlogchan.mention)))
            configmessagelist.append(myresp)
            adminlogchanbool = 1
        else:
            myresp = await ctx.send(botconfigscript[12])
            configmessagelist.append(myresp)
            adminlogchan = None
            adminlogchanbool = 0
        await asyncio.sleep(0.5)
        sent_voicelogmsg = await ctx.send(botconfigscript[13])
        configmessagelist.append(sent_voicelogmsg)
        voicelogmsgresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        userresp.append(voicelogmsgresp)
        voiceresp = voicelogmsgresp.content.lower()
        if voiceresp in yesanswerlist:
            sent_voicelogchanmsg = await ctx.send(botconfigscript[14])
            configmessagelist.append(sent_voicelogchanmsg)
            voicelogchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            userresp.append(voicelogchanresp)
            voicelogchan = voicelogchanresp.channel_mentions[0]
            myresp1 = await ctx.send(botconfigscript[15].format(str(voicelogchan.mention)))
            configmessagelist.append(myresp1)
            voicelogchanbool = 1
        else:
            myresp1 = await ctx.send(botconfigscript[16])
            configmessagelist.append(myresp1)
            voicelogchan = None
            voicelogchanbool = 0
        await asyncio.sleep(0.5)
        sent_awooquestion = await ctx.send(botconfigscript[22])
        configmessagelist.append(sent_awooquestion)
        awooresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        userresp.append(awooresp)
        awoorespcontent = awooresp.content.lower()
        if awoorespcontent in yesanswerlist:
            sent_awoochanquestion = await ctx.send(botconfigscript[23])
            configmessagelist.append(sent_awoochanquestion)
            awoochanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            userresp.append(awoochanresp)
            awoochan = awoochanresp.channel_mentions[0]
            myresp1 = await ctx.send(botconfigscript[27].format(str(awoochan.mention)))
            configmessagelist.append(myresp1)
            enableawoos = 1
        else:
            sent_awoochanquestion = await ctx.send(botconfigscript[24])
            configmessagelist.append(sent_awoochanquestion)
            enableawoos = 0
            awoochan = None
        # add config option to choose what prefix to use
        await ctx.send(botconfigscript[17])
        enablelogging = any([welcomechanbool, adminlogchanbool, voicelogchanbool, enableawoos])
        channellist = [initialchan, welcomechan, adminlogchan, voicelogchan, awoochan]
        responses = [enablelogging, welcomechanbool, adminlogchanbool, voicelogchanbool, enableawoos]
        joinpartmsgs = [welcomemessage, leavemessage]
        sqlquery, querydata = await self.bot.sql.statement_insert_guildconfig(ctx, channellist, responses, joinpartmsgs)
        member_guild_config = str(f'{str(ctx.guild.id)}_guild_config')
        await self.bot.mysqlcache.delete(key=member_guild_config)
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sqlquery, querydata)
        await asyncio.sleep(1)
        async with ctx.typing():
            await ctx.channel.delete_messages(configmessagelist1)
            await ctx.channel.delete_messages(configmessagelist)
            try:
                await ctx.channel.delete_messages(userresp)
            except Exception as e:
                pass


class DBotHelp:
    """Bot help replacement"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    @commands.command(hidden=True)
    async def help(self, ctx, cmd=None, subcmd=None):
        """Help command"""
        if str(cmd) == "help":
            return await ctx.send("Why are you trying to get help for help?")
        elif cmd is None and subcmd is None:
            return await ctx.send("No command was specified.\nYou can see my overall help documentation at "
                                  "<https://personalwebsite.website/wiki/noodlebot>")
        elif cmd and not subcmd:
            mycmd = self.bot.get_command(cmd)
            if mycmd is not None:
                url = f'https://personalwebsite.website/wiki/{mycmd.cog_name}#{mycmd.name}'
                if mycmd.help is not None:
                    helptext = mycmd.help
                else:
                    helptext = "I do not have built-in help text for this command, please see my website"
            else:
                return
        elif cmd and subcmd:
            mycmd = self.bot.get_command(cmd)
            if mycmd is not None:
                url = f'https://personalwebsite.website/wiki/{mycmd.cog_name}#{mycmd.name}'
                if mycmd.help is not None:
                    helptext = mycmd.help
                else:
                    helptext = "I do not have built-in help text for this command, please see my website"
            else:
                return
        else:
            return
        embed = discord.Embed(title="Bot Help", colour=discord.Colour(0x3ba6c9))
        # embed.set_thumbnail(
        #     url="https://cdn.discordapp.com/avatars/340802627887693825/f830b6257e434a56cab408ece5cf8fa8.png?size=1024")
        embed.add_field(name=f'Command: `{mycmd}`', value=helptext)
        embed.add_field(name="URL", value=f'<{url}>')
        await ctx.send(embed=embed)


def setup(dbot):
    dbot.remove_command("help")
    dbot.check(dbotchecks.globally_ignore_bots())
    dbot.add_cog(DBotHelp(dbot))
    dbot.add_cog(BotInternals(dbot))
    dbot.add_cog(BotInfo(dbot))
