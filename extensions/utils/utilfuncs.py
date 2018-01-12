from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class CommonParams:
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

    addons = ['extensions.botlogger',
              'extensions.botinternals',
              'extensions.mainserver',
              'extensions.admincommands',
              'extensions.load',
              'extensions.memecommands',
              'extensions.misc',
              'extensions.image',
              'extensions.loops'
              ]

    uptime = datetime.datetime.utcnow()

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


class UtilFuncs:
    """Utility Functions"""
    # Misc shit I guess idk
    # Mostly making this cog for small things like aiohttp downloads and file reading/writing
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__)}" loaded')

    async def retrieve_web_file(self, url: str, savelocation):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        with open(savelocation, "wb") as file:
                            file.write(data)
                        return data
                    else:
                        return None
        except:
            raise self.bot.errors.DBotExternalError("Failed to retreive requested file.")


class MyErrors(commands.CommandError):
    pass

    class DBotInternalError(commands.CommandError):
        pass

    class DBotExternalError(commands.CommandError):
        pass

    class BotNotWorking(commands.CommandError):
        pass
