from extensions.utils.importsfile import *


class CommonParams:
    """Things for common parameters"""
    def __init__(self):
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    config = configparser.ConfigParser()
    internalfilesdir = os.path.join(os.curdir, "internalfiles")
    configfile = os.path.join(internalfilesdir, "botconf.ini")
    if not os.path.isfile(configfile):
        print("!!!!!!\nbotconf.ini does not exist in the internalfiles directory\n!!!!!!")
        time.sleep(0.1)
        sys.exit("The file 'botconf.ini' does not exist\nPlease copy 'botconf.ini.example' in the "
                 "'internalfiles' directory to 'botconf.ini' and set the configuration options listed.")
    config.read(configfile)
    botdescription = str(config['dbot']['botdescription'])
    botdiscordid = int(config['dbot']['botdiscordid'])
    discordbottoken = str(config['dbot']['discordbottoken'])
    discordbotcommandprefix = str(config['dbot']['discordbotcommandprefix'])
    botowner = int(config['dbot']['botowner'])
    trustedusers = (config['dbot']['trustedusers']).split(',')
    mainserver = (config['dbot']['mainserver']).split(',')
    mainserverlogchan = (config['dbot']['mainserverlogchan']).split(',')
    mainserverjailrole = int(config['dbot']['mainserverjailrole'])
    mainserverafkchan = int(config['dbot']['mainserverafkchan'])
    mysqlserver = str(config['script']['mysqlserver'])
    mysqlport = int(config['script']['mysqlport'])
    mysqluser = str(config['script']['mysqluser'])
    mysqlpw = str(config['script']['mysqlpw'])
    mysqldb = str(config['script']['mysqldb'])
    weatherapikey = str(config['wunderground']['weatherapikey'])
    wolframapikey = str(config['wolfram']['wolframalphaapikey'])
    youtubeapikey = str(config['youtube']['youtubeapikey'])
    imgflipusername = str(config['imgflip']['imgusername'])
    imgflippassword = str(config['imgflip']['imgpassword'])
    addons = ['extensions.utils.sqlcommands',
              'extensions.utils.utilfuncs',
              'extensions.botlogger',
              'extensions.botinternals',
              'extensions.mainserver',
              'extensions.admincommands',
              'extensions.load',
              'extensions.memecommands',
              'extensions.misc',
              'extensions.etconmessage',
              'extensions.image',
              'extensions.loops'
              ]
    if not botdescription:
        botdescription = 'discord pybot'
    if not discordbotcommandprefix:
        discordbotcommandprefix = "!!"
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logpath = os.path.join(os.curdir, 'internalfiles', 'logger')
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    logname = 'discordapi.log'
    fulllog = os.path.join(logpath, logname)
    archivepath = os.path.join(logpath, 'oldlogs')
    if not os.path.exists(archivepath):
        os.makedirs(archivepath)
    rotatelog = None
    if os.path.isfile(fulllog):
        logtogz = open(fulllog, 'rb')
        logtogz1 = logtogz.read()
        logtogz.close()
        gzdfile = gzip.GzipFile(fulllog + '.gz', 'wb')
        gzdfile.write(logtogz1)
        gzdfile.close()
        gzfilename = fulllog + '.gz'
        if os.path.isfile(gzfilename):
            os.remove(fulllog)
        i = 0
        archivepathname = os.path.join(archivepath, logname)
        while os.path.isfile(archivepathname + '_' + time.strftime('%Y-%m-%d') + '_' + str(i) + '.log.gz'):
            i += 1
        rotatelog = os.path.join(archivepath, logname) + '_' + time.strftime('%Y-%m-%d') + '_' + str(i) + '.log.gz'
        os.rename(gzfilename, rotatelog)
    handler = logging.FileHandler(filename=fulllog, encoding='utf-8', mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


class PrefixStuff:
    """Things for custom prefixes"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def load_all_prefixes(self):
        mysqlconnected = await self.bot.mysqlcache.exists(key="mysqlcon")
        while not mysqlconnected:
            await asyncio.sleep(0.2)
            mysqlconnected = await self.bot.mysqlcache.exists(key="mysqlcon")
        prefixdictexist = await self.bot.mysqlcache.exists(key="prefixes")
        if prefixdictexist:
            await self.bot.mysqlcache.delete(key="prefixes")
        sqlcmd = await self.bot.sql.statement_get_prefixes()
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sqlcmd)
                results = await cursor.fetchall()
                self.bot.prefixdict = {}
                for item in results:
                    self.bot.prefixdict[item['guildid']] = item['prefix']
                await self.bot.mysqlcache.add(key="prefixes", value=self.bot.prefixdict)

    async def reload_prefix_cache(self):
        prefixdictexist = await self.bot.mysqlcache.exists(key="prefixes")
        if prefixdictexist:
            await self.bot.mysqlcache.delete(key="prefixes")
        sqlcmd = await self.bot.sql.statement_get_prefixes()
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sqlcmd)
                results = await cursor.fetchall()
                self.bot.prefixdict = {}
                for item in results:
                    self.bot.prefixdict[item['guildid']] = item['prefix']
                await self.bot.mysqlcache.add(key="prefixes", value=self.bot.prefixdict)

    async def prefix_for(self, guildid):
        prefixdict = await self.bot.mysqlcache.get(key="prefixes")
        try:
            prefix = prefixdict[str(guildid)]
        except (KeyError, AttributeError, TypeError):
            prefix = self.bot.common.discordbotcommandprefix
        return prefix

    async def get_prefix(self, bot, message):
        try:
            # if message.guild is None:
            #     return commands.when_mentioned_or()(bot,message)
            # else:
                prefix = [await self.prefix_for(message.guild.id)]
                return commands.when_mentioned_or(*prefix)(bot, message)
        except (KeyError, AttributeError):
            return self.bot.common.discordbotcommandprefix


class MyErrors(commands.CommandError):
    pass

    class DBotInternalError(commands.CommandError):
        pass

    class DBotExternalError(commands.CommandError):
        pass

    class BotNotWorking(commands.CommandError):
        pass

    class NotOwnerError(commands.CommandError):
        pass

    class DBotCooldownError(commands.CommandError):
        pass
