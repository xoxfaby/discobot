from extensions.utils.importsfile import *


class ImageMemes:
    """Image memes"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def _randomfilechoice(self, ctx, args: str):
        async with ctx.typing():
            memearray = []
            memepath = os.path.join("internalfiles", "content", args, "**")
            fileexts = '.png', '.jpg', '.jpeg', '.gif'
            for filename in glob.glob(str(memepath), recursive=True):
                if filename.endswith(fileexts):
                    memearray += [str(filename)]
            randomfile = random.choice(memearray)
            randomfilepath, randomfileext = os.path.splitext(randomfile)
            randomfilename = hashlib.md5(open(randomfile, 'rb').read()).hexdigest() + randomfileext
        return await ctx.send(file=discord.File(fp=randomfile, filename=str(randomfilename)))

    async def _internalfile(self, ctx, args: str):
        async with ctx.typing():
            file = os.path.join("internalfiles", "images", args)
            return await ctx.send(file=discord.File(fp=file, filename=args))

    @commands.command()
    async def memes(self, ctx):
        await self._randomfilechoice(ctx, "memes")

    @commands.command()
    async def pepes(self, ctx):
        await self._randomfilechoice(ctx, "pepes")

    @commands.command()
    async def mokou(self, ctx):
        await self._randomfilechoice(ctx, "mokou")

    @commands.command()
    async def grill(self, ctx):
        await self._randomfilechoice(ctx, "smug")

    @commands.command()
    async def rabbit(self, ctx):
        rabbitquestion = bool(random.getrandbits(1))
        if rabbitquestion:
            await self._randomfilechoice(ctx, "rabbit")
        else:
            await ctx.send("DO NOT FUCK THE RABBIT")

    @commands.command()
    async def animals(self, ctx):
        await self._randomfilechoice(ctx, "Animals")

    @commands.command()
    async def bestgirl(self, ctx):
        await self._randomfilechoice(ctx, "bestgirl")

    @commands.command()
    async def miku(self, ctx):
        await self._randomfilechoice(ctx, "miku")

    @commands.command()
    async def awoo(self, ctx):
        await self._internalfile(ctx, "3ae.png")

    @commands.command()
    async def doubt(self, ctx):
        await self._internalfile(ctx, "AbUWe1d.jpg")

    @commands.command()
    async def touhou(self, ctx):
        await self._internalfile(ctx, "touhou.png")

    @commands.command()
    async def awesome(self, ctx):
        await self._internalfile(ctx, "2dll9My.png")

    @commands.command()
    async def peep(self, ctx):
        await self._internalfile(ctx, "peep.gif")

    @commands.command()
    async def m(self, ctx):
        await self._internalfile(ctx, "m.jpg")

    @commands.command(hidden=True)
    async def superawoo(self, ctx):
        awoofile = os.path.join("internalfiles", "images", "3ae.png")
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        awoolist = [discord.File(fp=awoofile, filename="awoo.png"), discord.File(fp=awoofile, filename="awoo1.png"),
                    discord.File(fp=awoofile, filename="awoo2.png"), discord.File(fp=awoofile, filename="awoo3.png"),
                    discord.File(fp=awoofile, filename="awoo4.png"),
                    ]
        awoomessage = str("awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~\n"
                          "awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~\n"
                          "awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~\n"
                          "awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~\n"
                          "awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~ awoo~"
                          )
        async with ctx.typing():
            await ctx.send(files=awoolist, content="awoo~")
            await ctx.send(content=awoomessage)

    @commands.command()
    async def whatisgoingonhere(self, ctx):
        await ctx.send("http://i.imgur.com/tnWSXf7.png")

    @commands.command()
    async def inspire(self, ctx):
        fullurl = "http://inspirobot.me/api?generate=true"
        async with aiohttp.ClientSession() as session:
            async with session.get(fullurl) as r:
                if r.status == 200:
                    response = await r.text()
                    await ctx.send(response)
                else:
                    await ctx.send("An error occurred when calling Inspirobot")

    @commands.command(aliases=['genmeme', 'imgflip'])
    async def memegen(self, ctx, memetype, *args):
        if (str(memetype) == "help") or (str(memetype) == "list"):
            msg = "Please see this link for more information: " \
                  "<https://personalwebsite.website/wiki/index.php?title=ImageMemes#memegen>"
            return await ctx.send(msg)
        else:
            imgflipurl = str("https://api.imgflip.com/caption_image")
            imgflipdict = {}
            infile = csv.reader(open(os.path.join("internalfiles", "misc", "imgflip-ids.txt"), mode='r'), delimiter=':')
            for row in infile:
                key = row[0]
                imgflipdict[key] = row[1:]
            if memetype in imgflipdict:
                fullimgurl = str(str(imgflipurl) + '?template_id=' + str(imgflipdict[memetype]).strip("[]'")
                                 + '&username=' + str(self.bot.common.imgflipusername) + '&password=' +
                                 str(self.bot.common.imgflippassword) + '&text0=' + str(args[0]) + '&text1=' +
                                 str(args[1]))
                async with aiohttp.ClientSession() as session:
                    async with session.get(fullimgurl) as r:
                        if r.status == 200:
                            response = await r.json()
                            generatedmeme = response['data']['url']
                        else:
                            generatedmeme = str("Unable to create a meme")
                return await ctx.send(generatedmeme)
            else:
                raise commands.errors.UserInputError("User attempted to run memegen with an invalid meme type")

    # @commands.command(aliases=['sunny','titlecard'])
    # async def alwayssunny(self, ctx, *text: str):
    #     mesg = ' '.join(text)
    #     newmesg = mesg[17].replace()
    #     W, H = (1920, 1080)
    #     font = ImageFont.truetype(os.path.join("internalfiles", "misc", "textile-webfont.ttf"), 125)
    #     img = Image.new("RGBA", (W, H), (0, 0, 0))
    #     draw = ImageDraw.Draw(img)
    #     w, h = draw.multiline_textsize(mesg)
    #     draw.multiline_text(((W-w)/2,(H-h)/2), mesg, (255, 255, 255), font=font, align="center")
    #     savepath = os.path.join("internalfiles", "temp", time.strftime("%Y%m%d-%H%M%S_") + str(ctx.author.id) +
    #                             "_sunny.png")
    #     img.save(savepath)
    #     return await ctx.send(files=[discord.File(fp=savepath, filename="titlecard.png")])


class TextMemes:
    """Meme commands"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command()
    async def gface(self, ctx):
        await ctx.send("( ≖‿≖)")

    @commands.command()
    async def poop(self, ctx):
        await ctx.send("ＨＯＷ　ＣＡＮ　ＹＯＵ　ＳＡＹ　ＹＯＵ　ＬＯＶＥ　ＳＯＭＥＢＯＤＹ　ＩＦ　ＹＯＵ　ＷＯＮ’Ｔ　ＥＡＴ　ＴＨＥＩＲ　ＰＯＯＰ？")

    @commands.command()
    async def yay(self, ctx):
        await ctx.send("( ⌒‿⌒)")

    @commands.command()
    async def derp(self, ctx):
        await ctx.send("（ ｡∀ﾟ ）")

    @commands.command()
    async def idk(self, ctx):
        await ctx.send("┐('～`；)┌")

    @commands.command()
    async def ohgod(self, ctx):
        await ctx.send("ヾ( ﾟДﾟ)ﾉ")

    @commands.command()
    async def hug(self, ctx):
        await ctx.send("(づ｡◕‿‿◕｡)づ")

    @commands.command()
    async def lenny(self, ctx):
        """Memes."""
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command(aliases=['gay'])
    async def determinegay(self, ctx, *args):
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

    @commands.command(aliases=['pasta', 'emoji', 'daddy'])
    async def emojipasta(self, ctx):
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
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
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
                    await ctx.send("An error occurred when invoking the hivemind.")


def setup(dbot):
    dbot.add_cog(TextMemes(dbot))
    dbot.add_cog(ImageMemes(dbot))
