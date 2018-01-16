from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class LevelSystem:
    """A level system for the bot"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')
