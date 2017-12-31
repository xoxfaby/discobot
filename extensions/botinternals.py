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

    # async def on_guild_join(self, guild):
    #     guildchannels = guild.channels
    #     print(guildchannels)
    #     defaultchan.send("I am " + botdescription + "\nThank you for joining me to this server, please run `"
    #                      + discordbotcommandprefix + "bogconfig` to run my setup for this server.")
    #
    # async def getchans(self, ctx):
    #     textchans = ctx.guild.text_channels
    #     numofchans = len(textchans)
    #     nums = 1
    #     listofchans = "Text channels:\n"
    #     chanids = "Text Channels:\n"
    #     while nums != numofchans + 1:
    #         for chan in textchans:
    #             listofchans += str(nums) + ". " + str(chan.name) + "\n"
    #             chanids += str(nums) + ". " + str(chan.id) + "\n"
    #             nums += 1
    #     return listofchans, chanids
    #
    # @commands.command(hidden=True)
    # async def botconfig(self, ctx):
    #     if perms:
    #         perms = ctx.channel.permissions_for(ctx.author).administrator
    #         channelconverter = commands.TextChannelConverter()
    #         def checkchanid(m):
    #             return m.content.isdigit() and m.author == ctx.author
    #         def checkresponsebool(m):
    #             return m.author == ctx.author and m.content == "Yes"
    #         await ctx.send('Beginning the bot configuration for server: ' + ctx.guild.name)
    #         await asyncio.sleep(0.5)
    #         await ctx.send("Do you want to enable user join/part messages/logging?\nPlease type 'Yes' or 'No'")
    #         enableloggingresp = await self.bot.wait_for('message', check=checkresponsebool)
    #         await ctx.send("Please enter the channelid of the welcome channel")
    #
    #         welcomechanid = await self.bot.wait_for('message', check=checkchanid)
    #         welcomechanobj = await channelconverter.convert(ctx, welcomechanid.content)
    #         await ctx.send("You've selected " + str(welcomechanobj) + " as your new user welcome channel\n" +
    #                        "Please enter the channel id of the admin log/audit channel" +
    #                        "\nThis channel will be used to log users who join and leave with timestamps.\n"
    #                        "If you don't want to have a secondary channel of user joins/parts, please type 'None'")
    #         adminlogchanid = await self.bot.wait_for('message', check=checkchanid)
    #         adminlogchanobj = await channelconverter.convert(ctx, adminlogchanid.content)
    #         await ctx.send("Log channel defined.\n")
    #
    #         # answer = random.randint(1, 10)
    #         # if guess is None:
    #         #     fmt = 'Sorry, you took too long. It was {}.'
    #         #     await client.send_message(message.channel, fmt.format(answer))
    #         #     return
    #         # if int(guess.content) == answer:
    #         #     await client.send_message(message.channel, 'You are right!')
    #         # else:
    #         #     await client.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))
    #     else:
    #         ctx.send("You do not have 'manage_server' permissions on this guild." + "\n"
    #                  + "Permission denied to use this command")

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Bot Information", description="Noodle Disco-Pybot", color=0x3347ff)
        embed.add_field(name="Web URL", value="<https://personalwebsite.website/wiki/noodlebot>")
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/app-icons/340802627887693825/f830b6257e434a56cab408ece5cf8fa8.png')
        embed.add_field(name="Creator", value="noodle#4660", inline=False)
        embed.add_field(name="Invite", value="[Invite URL]"
                                             "(https://discordapp.com/oauth2/authorize?client_id=340802627887693825"
                                             "&scope=bot&permissions=1610083543)", inline=True)
        embed.add_field(name="Bot Prefix", value="`,` (Comma)")
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
