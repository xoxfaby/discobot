from extensions.utils.importsfile import *


def check_trusted_user(ctx, common):
    if str(ctx.message.author.id) in common.trustedusers:
        return True
    else:
        return False


class DBotChecks:
    def __init__(self, common):
        self.common = common

    def check_trusted_user(self):
        async def predicate(ctx):
            return check_trusted_user(ctx, self.common)
        return commands.check(predicate)

    def check_main_server(self):
        async def predicate(ctx):
            if str(ctx.guild.id) in self.bot.common.mainserver:
                return True
            else:
                raise commands.errors.CommandNotFound("A user attempted to run a command on a guild that is not the "
                                                      "main guild")

#
# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)
