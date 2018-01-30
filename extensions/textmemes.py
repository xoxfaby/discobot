from extensions.utils.importsfile import *


class TextMemes:
    """Meme commands"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        importlib.reload(self.dbotchecks)
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def __local_check(self, ctx):
        result = bool(await self.bot.internals.cooldowncheck(ctx))
        return result

    @commands.command()
    async def gface(self, ctx):
        """( ≖‿≖)"""
        await ctx.send("( ≖‿≖)")

    @commands.command()
    async def poop(self, ctx):
        """How can you say you love somebody"""
        await ctx.send("ＨＯＷ　ＣＡＮ　ＹＯＵ　ＳＡＹ　ＹＯＵ　ＬＯＶＥ　ＳＯＭＥＢＯＤＹ　ＩＦ　ＹＯＵ　ＷＯＮ’Ｔ　ＥＡＴ　ＴＨＥＩＲ　ＰＯＯＰ？")

    @commands.command()
    async def yay(self, ctx):
        """Happy emoji"""
        await ctx.send("( ⌒‿⌒)")

    @commands.command()
    async def derp(self, ctx):
        """Derp emoji"""
        await ctx.send("（ ｡∀ﾟ ）")

    @commands.command()
    async def idk(self, ctx):
        """idk emoji"""
        await ctx.send("┐('～`；)┌")

    @commands.command()
    async def ohgod(self, ctx):
        """Oh god"""
        await ctx.send("ヾ( ﾟДﾟ)ﾉ")

    @commands.command()
    async def hug(self, ctx):
        """
        Hugs somebody
        You can mention a user or not
        """
        if ctx.message.mentions:
            message = f'You need a huggu {ctx.message.mentions[0].mention}~ <3\n(づ｡◕‿‿◕｡)づ'
        else:
            message = "(づ｡◕‿‿◕｡)づ"
        await ctx.send(message)

    @commands.command()
    async def lenny(self, ctx):
        """Memes."""
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command(aliases=['gay'])
    async def determinegay(self, ctx, *args):
        """
        Determines the amount of gay that somebody is;
        Command is NSFW
        Accepts a user mention, a string of text, or no arguments
        If no arguments are specified, the bot selects a random user from the guild
        """
        with open(os.path.join("internalfiles", 'content', 'textshit', 'gayarray.txt'), mode='r') as infile:
            gayarray = infile.read().split("\n")
        if ctx.message.mentions:
            mesg = ctx.message.mentions
            for usermention in mesg:
                isgay = str(random.choice(gayarray))
                await ctx.send(usermention.mention + str(isgay))
        elif args is ():
            members = ctx.message.guild.members
            mentionarray = []
            for member in members:
                mentionarray += [member.mention]
            randomuser = random.choice(mentionarray)
            gayarraychoice = str(random.choice(gayarray))
            return await ctx.send(randomuser + gayarraychoice)
        else:
            mesg = ' '.join(args)
            gayarraychoice = str(random.choice(gayarray))
            return await ctx.send(mesg + gayarraychoice)

    @commands.command(aliases=['pasta', 'daddy'])
    async def emojipasta(self, ctx):
        """I will call you daddy"""
        pastafile = os.path.join("internalfiles", 'content', 'textshit', 'emojipasta.txt')
        result = []
        results = []
        with open(pastafile, encoding='utf-8') as fp:
            for line in fp:
                if line == '%\n':
                    results.append(result)
                    result = ''
                else:
                    result += line
        pastatosay = random.choice(results)
        return await ctx.send(pastatosay)

    @commands.command()
    async def thinking(self, ctx):
        """
        rly
        make
        u
        thonk
        """
        message = '```\n'
        message += "⠀⠀⠀⠀⠀⢀⣀⣀⣀\n"
        message += "⠀⠀⠀⠰⡿⠿⠛⠛⠻⠿⣷\n"
        message += "⠀⠀⠀⠀⠀⠀⣀⣄⡀⠀⠀⠀⠀⢀⣀⣀⣤⣄⣀⡀\n"
        message += "⠀⠀⠀⠀⠀⢸⣿⣿⣷⠀⠀⠀⠀⠛⠛⣿⣿⣿⡛⠿⠷\n"
        message += "⠀⠀⠀⠀⠀⠘⠿⠿⠋⠀⠀⠀⠀⠀⠀⣿⣿⣿⠇\n"
        message += "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁\n"
        message += "    \n"
        message += "⠀⠀⠀⠀⣿⣷⣄⠀⢶⣶⣷⣶⣶⣤⣀\n"
        message += "⠀⠀⠀⠀⣿⣿⣿⠀⠀⠀⠀⠀⠈⠙⠻⠗\n"
        message += "⠀⠀⠀⣰⣿⣿⣿⠀⠀⠀⠀⢀⣀⣠⣤⣴⣶⡄\n"
        message += "⠀⣠⣾⣿⣿⣿⣥⣶⣶⣿⣿⣿⣿⣿⠿⠿⠛⠃\n"
        message += "⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄\n"
        message += "⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁\n"
        message += "⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁\n"
        message += "⠀⠀⠛⢿⣿⣿⣿⣿⣿⣿⡿⠟\n"
        message += "⠀⠀⠀⠀⠀⠉⠉⠉\n"
        message += "```"
        await ctx.send(message)

    @commands.command()
    async def comrade(self, ctx):
        """Communism"""
        message = '```\n'
        message += '                 !#########       #\n'
        message += '               !########!          ##!\n'
        message += '            !########!               ###\n'
        message += '         !##########                  ####\n'
        message += '       ######### #####                ######\n'
        message += '        !###!      !####!              ######\n'
        message += '          !           #####            ######!\n'
        message += '                        !####!         #######\n'
        message += '                           #####       #######\n'
        message += '                             !####!   #######!\n'
        message += '                                ####!########\n'
        message += '             ##                   ##########\n'
        message += '           ,######!          !#############\n'
        message += '         ,#### ########################!####!\n'
        message += "       ,####      ##################!'    #####\n"
        message += "     ,####'           #######               !####!\n"
        message += "    ####'                                      #####\n"
        message += '    ~##                                          ##~\n'
        message += '```'
        await ctx.send(message)

    @commands.command()
    async def bigawoo(self, ctx):
        """AWOO"""
        message = '```\n'
        message += '⣿⣿⣿⣿⣿⣿⡷⣯⢿⣿⣷⣻⢯⣿⡽⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠸⣿⣿⣆⠹⣿⣿⢾⣟⣯⣿⣿⣿⣿⣿⣿⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣷⡌\n'
        message += '⣿⣿⣿⣿⣿⣿⣻⣽⡿⣿⣎⠙⣿⣞⣷⡌⢻⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⡄⠹⣿⣿⡆⠻⣿⣟⣯⡿⣽⡿⣿⣿⣿⣿⣽⡷⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣟⣷⣿⣿⣿⡀⠹⣟⣾⣟⣆⠹⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢠⡘⣿⣿⡄⠉⢿⣿⣽⡷⣿⣻⣿⣿⣿⣿⡝⣷⣯⢿⣿⣿⣿⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣯⢿⣾⢿⣿⡄⢄⠘⢿⣞⡿⣧⡈⢷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣧⠘⣿⣷⠈⣦⠙⢿⣽⣷⣻⣽⣿⣿⣿⣿⣌⢿⣯⢿⣿⣿⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣟⣯⣿⢿⣿⡆⢸⡷⡈⢻⡽⣷⡷⡄⠻⣽⣿⣿⡿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣏⢰⣯⢷⠈⣿⡆⢹⢷⡌⠻⡾⢋⣱⣯⣿⣿⣿⣿⡆⢻⡿⣿⣿⣿⣿⡟⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⡎⣿⢾⡿⣿⡆⢸⣽⢻⣄⠹⣷⣟⣿⣄⠹⣟⣿⣿⣟⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡇⢸⣯⣟⣧⠘⣷⠈⡯⠛⢀⡐⢾⣟⣷⣻⣿⣿⣿⡿⡌⢿⣻⣿⣿⣿⣿⡌\n'
        message += '⣿⣿⣿⣿⣿⣿⣧⢸⡿⣟⣿⡇⢸⣯⣟⣮⢧⡈⢿⣞⡿⣦⠘⠏⣹⣿⣽⢿⣿⣿⣿⣿⣯⣿⣿⣿⡇⢸⣿⣿⣾⡆⠹⢀⣠⣾⣟⣷⡈⢿⣞⣯⢿⣿⣿⣿⢷⠘⣯⣿⣿⣿⣿⣷\n'
        message += '⣿⣿⣿⣿⣿⣿⣿⡈⣿⢿⣽⡇⠘⠛⠛⠛⠓⠓⠈⠛⠛⠟⠇⢀⢿⣻⣿⣯⢿⣿⣿⣿⣷⢿⣿⣿⠁⣾⣿⣿⣿⣧⡄⠇⣹⣿⣾⣯⣿⡄⠻⣽⣯⢿⣻⣿⣿⡇⢹⣾⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⡽⡇⢸⣿⣿⣿⣿⣿⣞⣆⠰⣶⣶⡄⢀⢻⡿⣯⣿⡽⣿⣿⣿⢯⣟⡿⢀⣿⣿⣿⣿⣿⣧⠐⣸⣿⣿⣷⣿⣿⣆⠹⣯⣿⣻⣿⣿⣿⢀⣿⢿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣿⣿⠘⣯⡿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣧⡈⢿⣳⠘⡄⠻⣿⢾⣽⣟⡿⣿⢯⣿⡇⢸⣿⣿⣿⣿⣿⣿⡀⢾⣿⣿⣿⣿⣿⣿⣆⠹⣾⣷⣻⣿⡿⡇⢸⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣿⣿⡇⢹⣿⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠻⡇⢹⣆⠹⣟⣾⣽⣻⣟⣿⣽⠁⣾⣿⣿⣿⣿⣿⣿⣇⣿⣿⠿⠛⠛⠉⠙⠋⢀⠁⢘⣯⣿⣿⣧⠘⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣿⣿⣿⡈⣿⡃⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡙⠌⣿⣆⠘⣿⣞⡿⣞⡿⡞⢠⣿⣿⣿⣿⣿⡿⠛⠉⠁⢀⣀⣠⣤⣤⣶⣶⣶⡆⢻⣽⣞⡿⣷⠈⣿⣻⣿⣿\n'
        message += '⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠘⠁⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⢿⣄⢻⣿⣧⠘⢯⣟⡿⣽⠁⣾⣿⣿⣿⣿⣿⡃⢀⢀⠘⠛⠿⢿⣻⣟⣯⣽⣻⣵⡀⢿⣯⣟⣿⢀⣿⣽⣿⣿\n'
        message += '⣿⣿⣿⣟⣿⣿⣿⣿⣶⣶⡆⢀⣿⣾⣿⣾⣷⣿⣶⠿⠚⠉⢀⢀⣤⣿⣷⣿⣿⣷⡈⢿⣻⢃⣼⣿⣿⣿⣿⣻⣿⣿⣿⡶⣦⣤⣄⣀⡀⠉⠛⠛⠷⣯⣳⠈⣾⡽⣾⢀⣿⢾⣿⣿\n'
        message += '⣿⢿⣿⣿⣻⣿⣿⣿⣿⣿⡿⠐⣿⣿⣿⣿⠿⠋⠁⢀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣌⣥⣾⡿⣿⣿⣷⣿⣿⢿⣷⣿⣿⣟⣾⣽⣳⢯⣟⣶⣦⣤⡾⣟⣦⠘⣿⢾⡁⢺⣿⣿⣿\n'
        message += '⣿⣻⣿⣿⡷⣿⣿⣿⣿⣿⡗⣦⠸⡿⠋⠁⢀⢀⣠⣴⢿⣿⣽⣻⢽⣾⣟⣷⣿⣟⣿⣿⣿⣳⠿⣵⣧⣼⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣽⣳⣯⣿⣿⣿⣽⢀⢷⣻⠄⠘⣯⣿⣿\n'
        message += '⣿⢷⣻⣿⣿⣷⣻⣿⣿⣿⡷⠛⣁⢀⣀⣤⣶⣿⣛⡿⣿⣮⣽⡻⣿⣮⣽⣻⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢀⢸⣿⢀⡆⣿⣿⣿\n'
        message += '⠸⣟⣯⣿⣿⣷⢿⣽⣿⣿⣷⣿⣷⣆⠹⣿⣶⣯⠿⣿⣶⣟⣻⢿⣷⣽⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣯⣟⢀⡇⢼⣿⣿\n'
        message += '⣇⠹⣟⣾⣻⣿⣿⢾⡽⣿⣿⣿⣿⣿⣆⢹⣶⣿⣻⣷⣯⣟⣿⣿⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢀⡿⡇⢸⡇⢸⣿⡇\n'
        message += '⣿⣆⠹⣷⡻⣽⣿⣯⢿⣽⣻⣿⣿⣿⣿⣆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⠇⣼⡇⢸⡿⢠\n'
        message += '⡙⠾⣆⠹⣿⣦⠛⣿⢯⣷⢿⡽⣿⣿⣿⣿⣆⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠎⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⢀⣿⣾⣣⡿⡇⢸⢃⣾\n'
        message += '⣿⣷⡌⢦⠙⣿⣿⣌⠻⣽⢯⣿⣽⣻⣿⣿⣿⣧⠩⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⢰⢣⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⢀⢀⢿⣞⣷⢿⡇⠉⣼⣿\n'
        message += '⣿⣽⣆⠹⣧⠘⣿⣿⡷⣌⠙⢷⣯⡷⣟⣿⣿⣿⣷⡀⡹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣈⠃⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢀⣴⡧⢀⠸⣿⡽⣿⢀⣾⣿⣿\n'
        message += '⢻⣽⣿⡄⢻⣷⡈⢿⣿⣿⢧⢀⠙⢿⣻⡾⣽⣻⣿⣿⣄⠌⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⢁⣰⣾⣟⡿⢀⡄⢿⣟⣿⢀⣿⣿⣿\n'
        message += '⡄⢿⣿⣷⢀⠹⣟⣆⠻⣿⣿⣆⢀⣀⠉⠻⣿⡽⣯⣿⣿⣷⣈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⢀⣠⠘⣯⣷⣿⡟⢀⢆⠸⣿⡟⢸⣿⣿⣿\n'
        message += '⣷⡈⢿⣿⣇⢱⡘⢿⣷⣬⣙⠿⣧⠘⣆⢀⠈⠻⣷⣟⣾⢿⣿⣆⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⣠⡞⢡⣿⢀⣿⣿⣿⠇⡄⢸⡄⢻⡇⣼⣿⣿⣿\n'
        message += '⣿⣷⡈⢿⣿⡆⢣⡀⠙⢾⣟⣿⣿⣷⡈⠂⠘⣦⡈⠿⣯⣿⢾⣿⣆⠙⠻⠿⠿⠿⠿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢋⣠⣾⡟⢠⣿⣿⢀⣿⣿⡟⢠⣿⢈⣧⠘⢠⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣄⠻⣿⡄⢳⡄⢆⡙⠾⣽⣿⣿⣆⡀⢹⡷⣄⠙⢿⣿⡾⣿⣆⢀⡀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⢀⣀⣠⣴⡿⣯⠏⣠⣿⣿⡏⢸⣿⡿⢁⣿⣿⢀⣿⠆⢸⣿⣿⣿⣿\n'
        message += '⣿⣿⣿⣿⣦⡙⣿⣆⢻⡌⢿⣶⢤⣉⣙⣿⣷⡀⠙⠽⠷⠄⠹⣿⣟⣿⣆⢙⣋⣤⣤⣤⣄⣀⢀⢀⢀⢀⣾⣿⣟⡷⣯⡿⢃⣼⣿⣿⣿⠇⣼⡟⣡⣿⣿⣿⢀⡿⢠⠈⣿⣿⣿⡟\n'
        message += '⣿⣿⣿⣿⣿⣷⣮⣿⣿⣿⡌⠁⢤⣤⣤⣤⣬⣭⣴⣶⣶⣶⣆⠈⢻⣿⣿⣆⢻⣿⣿⣿⣿⣿⣿⣷⣶⣤⣌⣉⡘⠛⠻⠶⣿⣿⣿⣿⡟⣰⣫⣴⣿⣿⣿⣿⠄⣷⣿⠆⢻⣿⣿⡇﻿\n'
        message += '```'
        await ctx.send(message)

    @commands.command(usage="[the text you want to invoke the hivemind with]")
    async def zalgo(self, ctx, *args: str):
        """To invoke the hivemind"""
        try:
            await ctx.message.delete()
        except:
            pass
        partialurl = "https://zalgo.io/api?text="
        mesg = ' '.join(args)
        query = mesg.replace(" ", "+")
        fullurl = partialurl + query
        async with aiohttp.ClientSession() as session:
            async with session.get(fullurl) as r:
                if r.status == 200:
                    response = await r.text()
                    await ctx.send(response)
                else:
                    raise self.bot.errors.DBotExternalError("An error occurred when invoking the hivemind.")

    @commands.command()
    async def same(self, ctx):
        """Same"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send('```[✓] same\n[ ] unsame```')

    @commands.command()
    async def unsame(self, ctx):
        """Unsame"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send('```[ ] same\n[✓] unsame```')

    @commands.command()
    async def resame(self, ctx):
        """re:same"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send('```[✓] same\n[✓] re:same\n[ ] unsame```')

    @commands.command(aliases=['wide', 'fullwidth', 'aesthetic'])
    async def fullwidthtext(self, ctx, *, a_text):
        """Make your message ａｅｓｔｈｅｔｉｃ"""
        ascii_to_wide = dict((i, chr(i + 0xfee0)) for i in range(0x21, 0x7f))
        ascii_to_wide.update({0x20: u'\u3000', 0x2D: u'\u2212'})
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(f'{a_text.translate(ascii_to_wide)}')

    @commands.command()
    async def yee(self, ctx):
        """Yee"""
        message = "```\n"
        message += "░░░░░░░░░░░░░░░░░░░░░░░░░░░\n"
        message += "░░░░░░░░░░░░░▄███▄▄▄░░░░░░░\n"
        message += "░░░░░░░░░▄▄▄██▀▀▀▀███▄░░░░░\n"
        message += "░░░░░░░▄▀▀░░░░░░░░░░░▀█░░░░\n"
        message += "░░░░▄▄▀░░░░░░░░░░░░░░░▀█░░░\n"
        message += "░░░█░░░░░▀▄░░▄▀░░░░░░░░█░░░\n"
        message += "░░░▐██▄░░▀▄▀▀▄▀░░▄██▀░▐▌░░░\n"
        message += "░░░█▀█░▀░░░▀▀░░░▀░█▀░░▐▌░░░\n"
        message += "░░░█░░▀▐░░░░░░░░▌▀░░░░░█░░░\n"
        message += "░░░█░░░░░░░░░░░░░░░░░░░█░░░\n"
        message += "░░░░█░░▀▄░░░░▄▀░░░░░░░░█░░░\n"
        message += "░░░░█░░░░░░░░░░░▄▄░░░░█░░░░\n"
        message += "░░░░░█▀██▀▀▀▀██▀░░░░░░█░░░░\n"
        message += "░░░░░█░░▀████▀░░░░░░░█░░░░░\n"
        message += "░░░░░░█░░░░░░░░░░░░▄█░░░░░░\n"
        message += "░░░░░░░██░░░░░█▄▄▀▀░█░░░░░░\n"
        message += "░░░░░░░░▀▀█▀▀▀▀░░░░░░█░░░░░\n"
        message += "░░░░░░░░░█░░░░░░░░░░░░█░░░░\n"
        message += "```"
        return await ctx.send(message)


def setup(dbot):
    dbot.add_cog(TextMemes(dbot))
