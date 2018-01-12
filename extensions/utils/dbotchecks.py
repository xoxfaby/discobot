import os, configparser
from discord.ext import commands

internalfilesdir = os.path.join(os.curdir, "internalfiles")
configfile = os.path.join(internalfilesdir, "botconf.ini")
config = configparser.ConfigParser()
config.read(configfile)
botowner = int(config['dbot']['botowner'])
trustedusers = (config['dbot']['trustedusers']).split(',')
mainserver = (config['dbot']['mainserver']).split(',')


def check_trusted_user():
    async def predicate(ctx):
        return str(ctx.message.author.id) in trustedusers
    return commands.check(predicate)


def check_main_server():
    async def predicate(ctx):
        return str(ctx.guild.id) in mainserver
    return commands.check(predicate)


def globally_ignore_bots():
    async def predicate(ctx):
        return not ctx.author.bot


def check_server_admin_or_botowner():
    async def predicate(ctx):
        return ctx.channel.permissions_for(ctx.guild.me).manage_guild or (ctx.author.id in trustedusers)


# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)

