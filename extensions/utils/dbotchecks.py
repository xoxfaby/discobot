from extensions.utils.importsfile import *


class DBotChecks:
    def __init__(self, bot):
        self.bot = bot

    def check_trusted_user(self, ctx):
        return str(ctx.message.author.id) in self.bot.common.trustedusers

    def check_main_server(self, ctx):
        if str(ctx.guild.id) in self.bot.common.mainserver:
            return True
        else:
            raise commands.errors.CommandNotFound("A user attempted to run a command on a guild that is not the main guild")



#
# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)
