from extensions.utils.importsfile import *


class MainServer:
    """Internal Things for Boat's Main Server"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def on_guild_join(self, guild):
        await self.guild_logger(guild, str("join"))

    async def on_guild_remove(self, guild):
        await self.guild_logger(guild, str("leave"))

    async def guild_logger(self, guild, joinleave):
        if str(guild.id) in self.bot.common.mainserver:
            return
        else:
            mytime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            action = {"join": "was added to a new", "leave": "was removed from a"}
            mainservermessage = ("!!!! ALART !!!!\nBoat was {7} server\nDate: {0}\nGuild Name & ID: {1} --- {2}\n"
                                 "Guild Owner: {3} --- Owner ID: {4}\nGuild Info: Size: {5} Users; Created: {6}")
            content = mainservermessage.format(mytime, str(guild.name), str(guild.id), str(guild.owner),
                                               str(guild.owner.id), str(guild.member_count), str(guild.created_at),
                                               str(action[joinleave]))
            for channel in self.bot.common.mainserverlogchan:
                chan = self.bot.get_channel(id=int(channel))
                await chan.send(content)


def setup(dbot):
    dbot.add_cog(MainServer(dbot))
