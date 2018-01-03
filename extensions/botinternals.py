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

    async def on_voice_state_update(self, member, before, after):
        if str(before.channel) == str(after.channel):
            return
        else:
            sqlcmd, tablename = await self.bot.sql.statement_get_server_config(member.guild)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(sqlcmd)
                    rowcount = cursor.rowcount
                    if rowcount == 1:
                        guildconf = await cursor.fetchone()
                    else:
                        guildconf = {}
            if 'isconfigged' in guildconf:
                if guildconf['enablevoicelogs']:
                    content = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': ' + str(member) +
                               ' is in voice channel: ' + str(after.channel))
                    voicelogchan = self.bot.get_channel(id=int(guildconf['voicelogchannel']))
                    await voicelogchan.send(content=content)
                else:
                    return
            else:
                return

    async def memberbotmessage(self, member, secondaryargs, guild):
        if str(member) == str(member.guild.me):
            return
        sqlcmd, tablename = await self.bot.sql.statement_get_server_config(guild)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sqlcmd)
                rowcount = cursor.rowcount
                if rowcount == 1:
                    guildconf = await cursor.fetchone()
                else:
                    guildconf = {}
        if 'isconfigged' in guildconf:
            messagedict = {"join": guildconf['welcomemessage'], "leave": guildconf['partmessage'],
                           "ban": "{0} was banned.", "unban": "{0} was unbanned"}
            memberverb = {"join": " joined the server", "leave": " left the server",
                          "ban": " was banned from the server", "unban": " was unbanned from the server"}
            if guildconf['enableusewelcome']:
                welcomechannel = self.bot.get_channel(id=int(guildconf['welcomechannel']))
                welcomemessage = messagedict[secondaryargs].format(member.mention, guild.name)
                if str(secondaryargs) is not "unban":
                    await welcomechannel.send(content=welcomemessage)
            if guildconf['enableadminlogs']:
                adminmsg = (str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ': ' + str(member) +
                            str(memberverb[secondaryargs]))
                adminchannel = self.bot.get_channel(id=int(guildconf['adminchannel']))
                await adminchannel.send(adminmsg)
        else:
            return

    async def on_member_join(self, member):
        await self.memberbotmessage(member, "join", member.guild)

    async def on_member_remove(self, member):
        await self.memberbotmessage(member, "leave", member.guild)

    async def on_member_ban(self, guild, member):
        await self.memberbotmessage(member, "ban", guild)

    async def on_member_unban(self, guild, member):
        await self.memberbotmessage(member, "unban", guild)

    @commands.command(hidden=True)
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def botconfig(self, ctx):
        def checkauthor(m):
            return m.author == ctx.author
        botconfigscript = []
        with open(os.path.join("extensions", "utils", "botconfig-lines.txt"), encoding='utf-8', mode='r') as infile:
            botconfigscript = infile.read().split("%%\n")
        yesanswerlist = ['yes', 'y', 'true', 'yeah', 'yup', '1', 't']
        noanswerlist = ['no', 'n', 'negative', 'false', 'nope', '0', 'f']
        configmessagelist = []
        configmessagelist1 = []
        sent_startmsg = await ctx.send(str(botconfigscript[0]).format(str(ctx.guild.name)))
        configmessagelist1.append(sent_startmsg)
        sent_thischannelmsg = await ctx.send(botconfigscript[1])
        configmessagelist.append(sent_thischannelmsg)
        thischannelresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        configmessagelist.append(thischannelresp)
        enablelogging = 1
        thischannelresp1 = thischannelresp.content.lower()
        if thischannelresp1 in yesanswerlist:
            announcemsg1 = await ctx.send(botconfigscript[2])
            configmessagelist.append(announcemsg1)
            initialchan = ctx.channel
        else:
            announcemsg1 = await ctx.send(botconfigscript[3])
            configmessagelist.append(announcemsg1)
            initialchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(initialchanresp)
            initialchan = initialchanresp.channel_mentions[0]
            myinitalresp = await ctx.send(botconfigscript[4].format(str(initialchan.mention)))
            configmessagelist.append(myinitalresp)
        async with ctx.typing():
            await ctx.channel.delete_messages(configmessagelist)
        configmessagelist = None
        configmessagelist = []

        await asyncio.sleep(0.5)
        sent_usermsgs = await ctx.send(botconfigscript[5])
        configmessagelist.append(sent_usermsgs)
        enableloggingresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        configmessagelist.append(enableloggingresp)
        loggingresp = enableloggingresp.content.lower()
        if loggingresp in yesanswerlist:
            myloggingresp = await ctx.send(botconfigscript[6])
            configmessagelist.append(myloggingresp)
            welcomechanmessage = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(welcomechanmessage)
            welcomechan = welcomechanmessage.channel_mentions[0]
            mywelcomeresp = await ctx.send(botconfigscript[7].format(str(welcomechan.mention)))
            configmessagelist.append(mywelcomeresp)
            welcomechanbool = 1
            sent_defaultmessages = await ctx.send(botconfigscript[18])
            configmessagelist.append(sent_defaultmessages)
            defaultmessagesresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(defaultmessagesresp)
            secondresp = defaultmessagesresp.content.lower()
            if secondresp in yesanswerlist:
                sent_asknewwelcome = await ctx.send(botconfigscript[19])
                configmessagelist.append(sent_asknewwelcome)
                newwelcomeresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
                configmessagelist.append(newwelcomeresp)
                welcomemessage = newwelcomeresp.content
                sent_asknewpart = await ctx.send(botconfigscript[20])
                configmessagelist.append(sent_asknewpart)
                newleaveresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
                configmessagelist.append(newleaveresp)
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
        async with ctx.typing():
            await ctx.channel.delete_messages(configmessagelist)
        configmessagelist = None
        configmessagelist = []

        await asyncio.sleep(0.5)
        sent_adminauditlogmsg = await ctx.send(botconfigscript[9])
        configmessagelist.append(sent_adminauditlogmsg)
        adminauditlogresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        configmessagelist.append(adminauditlogresp)
        auditresp = adminauditlogresp.content.lower()
        if auditresp in yesanswerlist:
            sent_adminlogchanmsg = await ctx.send(botconfigscript[10])
            configmessagelist.append(sent_adminlogchanmsg)
            adminlogchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(adminlogchanresp)
            adminlogchan = adminlogchanresp.channel_mentions[0]
            myresp = await ctx.send(botconfigscript[11].format(str(adminlogchan.mention)))
            configmessagelist.append(myresp)
            adminlogchanbool = 1
        else:
            myresp = await ctx.send(botconfigscript[12])
            configmessagelist.append(myresp)
            adminlogchan = None
            adminlogchanbool = 0
        async with ctx.typing():
            await ctx.channel.delete_messages(configmessagelist)
        configmessagelist = None
        configmessagelist = []

        await asyncio.sleep(0.5)
        sent_voicelogmsg = await ctx.send(botconfigscript[13])
        configmessagelist.append(sent_voicelogmsg)
        voicelogmsgresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        configmessagelist.append(voicelogmsgresp)
        voiceresp = voicelogmsgresp.content.lower()
        if voiceresp in yesanswerlist:
            sent_voicelogchanmsg = await ctx.send(botconfigscript[14])
            configmessagelist.append(sent_voicelogchanmsg)
            voicelogchanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(voicelogchanresp)
            voicelogchan = voicelogchanresp.channel_mentions[0]
            myresp1 = await ctx.send(botconfigscript[15].format(str(voicelogchan.mention)))
            configmessagelist.append(myresp1)
            voicelogchanbool = 1
        else:
            myresp1 = await ctx.send(botconfigscript[16])
            configmessagelist.append(myresp1)
            voicelogchan = None
            voicelogchanbool = 0
        async with ctx.typing():
            await ctx.channel.delete_messages(configmessagelist)
        configmessagelist = None
        configmessagelist = []

        await asyncio.sleep(0.5)
        sent_awooquestion = await ctx.send(botconfigscript[22])
        configmessagelist.append(sent_awooquestion)
        awooresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
        configmessagelist.append(awooresp)
        awoorespcontent = awooresp.content.lower()
        if awoorespcontent in yesanswerlist:
            sent_awoochanquestion = await ctx.send(botconfigscript[23])
            configmessagelist.append(sent_awoochanquestion)
            awoochanresp = await self.bot.wait_for('message', check=checkauthor, timeout=60)
            configmessagelist.append(awoochanresp)
            awoochan = awoochanresp.channel_mentions[0]
            enableawoos = 1
        else:
            sent_awoochanquestion = await ctx.send(botconfigscript[24])
            configmessagelist.append(sent_awoochanquestion)
            enableawoos = 0
            awoochan = None

        # add config option to choose what prefix to use
        await ctx.send(botconfigscript[17])
        channellist = [initialchan, welcomechan, adminlogchan, voicelogchan, awoochan]
        responses = [enablelogging, welcomechanbool, adminlogchanbool, voicelogchanbool, enableawoos]
        joinpartmsgs = [welcomemessage, leavemessage]
        sqlquery, querydata = await self.bot.sql.statement_insert_guildconfig(ctx, channellist, responses, joinpartmsgs)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sqlquery, querydata)
        await asyncio.sleep(2)
        async with ctx.typing():
            await ctx.channel.delete_messages(configmessagelist1)
            await ctx.channel.delete_messages(configmessagelist)


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
                   "**Please note, you will need `manage_guild` permissions on this guild in order to run `botconfig`**")
        await initialchannel.send(message)

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
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.common.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        fmt = '{h} hours, {m} minutes, and {s} seconds'
        fmtnew = fmt.format(h=hours, m=minutes, s=seconds)
        return await ctx.send(fmtnew)

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
