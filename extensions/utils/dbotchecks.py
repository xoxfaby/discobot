# from discord.ext import commands
#
# def check_trusted_user(self, ctx):
#     return str(ctx.message.author.id) in CommonParams.trustedusers
#
#
# def check_main_server(self, ctx):
#     return str(ctx.guild.id) in CommonParams.mainserver
#
#
#
# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)
