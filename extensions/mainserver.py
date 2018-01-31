from extensions.utils.importsfile import *


class MainServer:
    """Internal Things for Boat's Main Server"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        importlib.reload(self.dbotchecks)
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
            action = {"join": "was added to a new server", "leave": "was removed from a server"}
            try:
                invites = await guild.invites()
            except (discord.Forbidden, discord.HTTPException):
                invites = None
            mainservermessage = (f'!!!! ALART !!!!\nBoat was {str(action[joinleave])} \n'
                                 f'```Guild Name & ID: {str(guild.name)} --- {str(guild.id)}\n'
                                 f'Guild Owner: {str(guild.owner)} --- {str(guild.owner.id)}\n'
                                 f'Guild Misc Info:\n'
                                 f'    Users on join: {str(guild.member_count)}\n'
                                 f'    Created: {str(guild.created_at)}\n```')
            if invites:
                temp = [f'{x.code}, ' for x in invites]
                mainservermessage += (f'Invite list: {temp}')
            for channel in self.bot.common.mainserverlogchan:
                chan = self.bot.get_channel(id=int(channel))
                await chan.send(mainservermessage)


def setup(dbot):
    dbot.add_cog(MainServer(dbot))
