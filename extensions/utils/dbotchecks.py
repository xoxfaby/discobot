# from discord.ext import commands
# from extensions.utils.common import CommonParams
#
#
# class DBotChecks(None):
#     def check_trusted_user(self: None, ctx):
#         return str(ctx.message.author.id) in CommonParams.trustedusers
#
#     def check_main_server(self: None, ctx):
#         if str(ctx.guild.id) in CommonParams.mainserver:
#             return True
#         else:
#             raise commands.errors.CommandNotFound("A user attempted to run a command on a guild that is not the main guild")
#
#
# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)
