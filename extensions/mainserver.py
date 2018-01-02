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
