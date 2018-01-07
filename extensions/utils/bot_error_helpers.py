from extensions.utils.importsfile import *


class MyErrors(commands.CommandError):
    pass

    class DBotInternalError(commands.CommandError):
        pass

    class DBotExternalError(commands.CommandError):
        pass

    class BotNotWorking(commands.CommandError):
        pass
