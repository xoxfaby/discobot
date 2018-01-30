from extensions.utils.importsfile import *


class ImageMemes:
    """Image memes"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        importlib.reload(self.dbotchecks)
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def __local_check(self, ctx):
        result = bool(await self.bot.internals.cooldowncheck(ctx))
        return result

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
        """Posts a nice meme"""
        await self._randomfilechoice(ctx, "memes")

    @commands.command()
    async def pepes(self, ctx):
        """Posts a rare pepe"""
        await self._randomfilechoice(ctx, "pepes")

    @commands.command()
    async def mokou(self, ctx):
        """Posts a mokou"""
        await self._randomfilechoice(ctx, "mokou")

    @commands.command()
    async def grill(self, ctx):
        """Posts a smug anime girl"""
        await self._randomfilechoice(ctx, "smug")

    @commands.command()
    async def rabbit(self, ctx):
        """
        DO
        NOT
        """
        rabbitquestion = bool(random.getrandbits(1))
        if rabbitquestion:
            await self._randomfilechoice(ctx, "rabbit")
        else:
            await ctx.send("DO NOT FUCK THE RABBIT")

    @commands.command()
    async def animals(self, ctx):
        """Posts a cute animal"""
        await self._randomfilechoice(ctx, "Animals")

    @commands.command()
    async def bestgirl(self, ctx):
        """Posts a nice girl"""
        await self._randomfilechoice(ctx, "bestgirl")

    @commands.command()
    async def miku(self, ctx):
        """Posts from a selection of Miku images"""
        await self._randomfilechoice(ctx, "miku")

    @commands.command()
    async def awoo(self, ctx):
        """Awoo~~~"""
        await self._internalfile(ctx, "3ae.png")

    @commands.command()
    async def doubt(self, ctx):
        """Press x"""
        await self._internalfile(ctx, "AbUWe1d.jpg")

    @commands.command()
    async def touhou(self, ctx):
        """2hu"""
        await self._internalfile(ctx, "touhou.png")

    @commands.command()
    async def awesome(self, ctx):
        """Cool"""
        await self._internalfile(ctx, "2dll9My.png")

    @commands.command()
    async def peep(self, ctx):
        """A rare animated peep"""
        await self._internalfile(ctx, "peep.gif")

    @commands.command()
    async def m(self, ctx):
        """m"""
        await self._internalfile(ctx, "m.jpg")

    @commands.command(hidden=True)
    async def superawoo(self, ctx):
        """Sekrit"""
        awoofile = os.path.join("internalfiles", "images", "3ae.png")
        if str('Direct Message') not in str(ctx.channel):
            try:
                await ctx.message.delete()
            except Exception as e:
                pass
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
        """Oh no"""
        await ctx.send("http://i.imgur.com/tnWSXf7.png")

    @commands.command()
    async def inspire(self, ctx):
        """Generates an image from inspirobot"""
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
        """
        Generates a meme from imgflip
        Please see this webpage for more information:
        https://personalwebsite.website/wiki/index.php?title=ImageMemes#memegen
        """
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


def setup(dbot):
    dbot.add_cog(ImageMemes(dbot))
