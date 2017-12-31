from extensions.utils.importsfile import *


class MainServer:
    """Internal Things for Boat's Main Server"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(hidden=True)
    async def watch(self, ctx):
        if str(ctx.guild.id) == str(self.bot.common.mainserver[0]):
            return await ctx.send('Media Links:' + '\n<' + self.bot.common.mainservermedialinks[0] + '>\n<' +
                                  self.bot.common.mainservermedialinks[1] + '>')
        else:
            return

    async def on_voice_state_update(self, member, before, after):
        if str(member.guild.id) in self.bot.common.mainserver:
            if str(before.channel) == str(after.channel):
                pass
            else:
                if str(member.guild.id) == str(self.bot.common.mainserver[0]):
                    voicelogchan = self.bot.get_channel(id=int(self.bot.common.mainservervoicelogchan[0]))
                elif str(member.guild.id) == str(self.bot.common.mainserver[1]):
                    voicelogchan = self.bot.get_channel(id=int(self.bot.common.mainservervoicelogchan[1]))
                else:
                    voicelogchan = None
                content = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ': ' + str(member) +
                           ' is in voice channel: ' + str(after.channel))
                await voicelogchan.send(content=content)
        else:
            return

    async def memberbotlog(self, member, secondaryargs, guild):
        if str(guild.id) in self.bot.common.mainserver:
            if str(member) == str(guild.me):
                return
            memberverb = {"join": " joined the server", "leave": " left the server",
                          "ban": " was banned from the server", "unban": " was unbanned from the server"}
            messages = {"join": "Welcome to {1}, {0}~", "leave": "ok bye {0}",
                        "ban": "{0} was banned.", "unban": "{0} was unbanned"}
            adminlogchan = None
            welcomechannel = None
            welcomemessage = messages[secondaryargs].format(member.mention, guild.name)
            adminmsg = (str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ': ' + str(member) +
                        str(memberverb[secondaryargs]))
            if str(guild.id) == str(self.bot.common.mainserver[0]):
                adminlogchan = self.bot.get_channel(id=int(self.bot.common.mainserverlogchan[0]))
                welcomechannel = self.bot.get_channel(id=int(self.bot.common.mainserverwelcomechan[0]))
            if str(guild.id) == str(self.bot.common.mainserver[1]):
                adminlogchan = self.bot.get_channel(id=int(self.bot.common.mainserverlogchan[1]))
                welcomechannel = self.bot.get_channel(id=int(self.bot.common.mainserverwelcomechan[1]))
            if str(secondaryargs) is not "unban":
                await welcomechannel.send(content=welcomemessage)
            await adminlogchan.send(content=str(adminmsg))
        else:
            return

    async def on_member_join(self, member):
        await self.memberbotlog(member, "join", member.guild)

    async def on_member_remove(self, member):
        await self.memberbotlog(member, "leave", member.guild)

    async def on_member_ban(self, guild, member):
        await self.memberbotlog(member, "ban", guild)

    async def on_member_unban(self, guild, member):
        await self.memberbotlog(member, "unban", guild)

    async def on_guild_join(self, guild):
        await self.guildlogger(guild, str("join"))

    async def on_guild_remove(self, guild):
        await self.guildlogger(guild, str("leave"))

    async def guildlogger(self, guild, joinleave):
        if str(guild.id) in self.bot.common.mainserver:
            return
        else:
            if str(joinleave) == "join":
                action = "was added to a new"
            elif str(joinleave) == "leave":
                action = "was removed from a"
            else:
                action = None
            mainservermessage = ("!!!! ALART !!!!\nBoat was {7} server\nDate: {0}\n"
                                 "Guild Name & ID: {1} --- {2}\nGuild Owner: {3} --- Owner ID: {4}\n"
                                 "Guild Info: Size: {5} Users; Created: {6}")
            content = mainservermessage.format(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
                                               str(guild.name), str(guild.id), str(guild.owner), str(guild.owner.id),
                                               str(guild.member_count), str(guild.created_at), str(action))
            for channel in self.bot.common.mainserverlogchan:
                chan = self.bot.get_channel(id=int(channel))
                await chan.send(content)


def setup(dbot):
    dbot.add_cog(MainServer(dbot))
