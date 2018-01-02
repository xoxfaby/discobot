from extensions.utils.importsfile import *


class DBotChecks:
    def __init__(self, common):
        self.common = common

    def check_trusted_user(self, ctx):
        return str(ctx.message.author.id) in self.common.trustedusers

    def check_main_server(self, ctx):
        return str(ctx.guild.id) in self.common.mainserver

#
# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)
