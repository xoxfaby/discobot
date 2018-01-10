import os, configparser
from discord.ext import commands

internalfilesdir = os.path.join(os.curdir, "internalfiles")
configfile = os.path.join(internalfilesdir, "botconf.ini")
config = configparser.ConfigParser()
config.read(configfile)
botowner = int(config['dbot']['botowner'])
trustedusers = (config['dbot']['trustedusers']).split(',')
mainserver = (config['dbot']['mainserver']).split(',')


def check_trusted_user(ctx):
    return str(ctx.message.author.id) in trustedusers


def check_main_server(ctx):
    return str(ctx.guild.id) in mainserver


# def globalcooldown(ctx):
#     def predicate(ctx):
#         commands.cooldown(2, 60, commands.BucketType.user)
#     return commands.check(predicate=predicate)

