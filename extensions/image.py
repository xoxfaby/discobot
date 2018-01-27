from extensions.utils.importsfile import *


class ImageManipulation:
    """Image Manipulation"""
    from extensions.utils import dbotchecks

    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def __local_check(self, ctx):
        result = bool(await self.bot.internals.cooldowncheck(ctx))
        return result

    async def _get_recent_images_links(self, ctx):
        msglist = []
        async for message in ctx.channel.history(limit=25, reverse=False):
            if message.attachments:
                download_list = list([at.url for at in message.attachments])
                for url in download_list:
                    msglist += [url]
            else:
                content = message.content
                fileexts = ['.png', '.jpg', '.jpeg', '.gif']
                if any(ext in content for ext in fileexts):
                    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                      content)
                    if len(urls) > 0:
                        for url in urls:
                            msglist += [url]
        return msglist

    def _moar_jpg(self, imglocation):
        file = os.path.split(imglocation)
        realfilepath = file[0]
        filename = file[1]
        convertname = (f'{time.strftime("%Y%m%d-%H%M%S")}-converted-{filename}.jpg')
        convertedfilepath = os.path.join(realfilepath, convertname)
        with Image(filename=imglocation) as original:
            with original.convert('jpg') as converted:
                with open(convertedfilepath, mode='wb+') as filepath:
                    compressionnum = random.randint(1, 25)
                    converted.compression_quality = int(compressionnum)
                    converted.save(filepath)
                    filepath.close()
        return convertedfilepath

    def _ok_doge(self, text):
        originalimage = os.path.join(os.curdir, "internalfiles", "images", "Doge.png")
        with Image(filename=originalimage) as original:
            with Drawing() as draw:
                fontlocation = os.path.join("internalfiles", "misc", "impact.ttf")
                draw.font = fontlocation
                black = Color("black")
                white = Color("white")
                draw.font_size = 90
                draw.stroke_color = white
                draw.text_alignment = 'center'
                draw.fill_color = white
                draw.text(x=int(300), y=int((560)), body=text)
                draw(original)
                image = original.make_blob('png')
                curtime = str(time.strftime("%Y_%m_%d %H_%M_%S", time.localtime()))
                filename = (f'{curtime}_okdoge.png')
                file = os.path.join("internalfiles", "temp", "okdoge", filename)
                with open(file, mode="wb+") as fp:
                    original.save(fp)
            return image

    def _sunnytask(self, words):
        if len(words) > 27:
            if " " in words:
                mesg = words.split(" ")
            else:
                mesg = list()
                mesg.append(words[0:27])
                mesg.append(words[27:])
            line1 = ""
            line2 = ""
            index = 0
            while len(line1) < 27:
                line1 += (mesg[index] + " ")
                index += 1
            while index < len(mesg):
                line2 += (mesg[index] + " ")
                index += 1
            multiline = True
        else:
            multiline = False
        W, H = (1920, 1080)
        black = Color("black")
        white = Color("white")
        fontlocation = os.path.join("internalfiles", "misc", "textile-webfont.ttf")
        with Image(width=W, height=H, background=black) as img:
            with Drawing() as draw:
                draw.font = fontlocation
                draw.font_size = 105
                draw.stroke_color = white
                draw.text_alignment = 'center'
                draw.fill_color = white
                if multiline:
                    draw.text(x=int(img.width / 2), y=int((img.height / 2) - 100), body=line1)
                    draw.text(x=int(img.width / 2), y=int((img.height / 2) + 100), body=line2)
                else:
                    draw.text(x=int(img.width / 2), y=int((img.height / 2)), body=words)
                draw(img)
                image = img.make_blob('png')
        return image

    def _corrupt_img(self, basedir, imglocation):
        # Majority of code absorbed from:
        # https://github.com/GlitchTools/batch_wordpad_glitch/blob/master/wordpad_glitch.py
        # Adaptions were made from the flow of the code, but the actual glitching was copied
        img_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp']
        wordpad_glitch = [
            (b'\x07', b'\x27'),
            (b'\x0B', b'\x0A\x0D'),
            (b'(?<!\x0A)(\x0D)', b'\x0A\x0D'),
            (b'(\x0A)(?<!\x0D)', b'\x0A\x0D'),
            (b'(\x0E)', b'(\x02)')]
        # Open image from imglocation, close image, save as bmp
        bmpdir = os.path.join(basedir, "bmp")
        origfilepath = os.path.split(imglocation)[0]
        filename = os.path.basename(imglocation).split('.')[0]
        ext = os.path.basename(imglocation).split('.')[-1]
        origfilename = f'{filename}.{ext}'
        fp = os.path.join(origfilepath, origfilename)
        if ext.lower() in img_formats:
            with Image(filename=fp) as img:
                with img.convert('bmp') as converted:
                    bmp_out = f'{filename}.bmp'
                    path_bmp_out = os.path.join(bmpdir, bmp_out)
                    converted.save(filename=path_bmp_out)
        else:
            return None
        with open(path_bmp_out, 'rb') as in_file:
            imgbytes = in_file.read()
        header = imgbytes[:140]
        core_data = imgbytes[140:]
        data_size = len(core_data)
        replacements = [(re.compile(sub), replacement) for (sub, replacement) in wordpad_glitch]
        for pattern, replacement in replacements:
            core_data = pattern.sub(replacement, core_data)
        letters = b'\x07', b'\x27', b'\x0b', b'\x0a', b'\x0d', b'\xce', b'\x0b', b'\xfa', b'\xd4', b'\x97', b'\x45', \
                  b'\x1a', b'\xfe', b'\xff', b'\xfd', b'\x01', b'\xcc', b'\xe9', b'\x95', b'\xe8', b'\xf9', b'\x95', \
                  b'\x3f', b'\x19', b'\x13', b'\x14', b'\x10', b'\x17', b'\xf8', b'\x9f', b'\x9e', b'\x93', b'\xa8', \
                  b'\xa6', b'\xab', b'\xa7', b'\xb1', b'\xac', b'\xa9', b'\xad', b'\xaa', b'\xae', b'\xaf', b'\xb0'
        outpath = None
        randrange = random.randint(1, 8)
        for xx in range(randrange):
            ii = random.randrange(0, data_size - 1, 1)
            temp_jj = ii + round(data_size / 8)
            jj = random.randrange(ii, temp_jj, 1)
            pre = core_data[:ii]
            post = core_data[jj:]
            sub_data = core_data[ii:jj]

            # inside sorts
            inside_ii = random.randrange(0, len(sub_data) - 1, 1)
            inside_temp_jj = inside_ii + round(len(sub_data) / 8)
            inside_jj = random.randrange(inside_ii, inside_temp_jj, 1)
            inside_pre = core_data[:inside_ii]
            inside_post = core_data[inside_jj:]
            inside_sub_data = sub_data[inside_ii:inside_jj]
            inside_sub_array = list(inside_sub_data)
            inside_sub_array.sort()
            inside_sub_data = bytes(inside_sub_array)
            sub_data = inside_pre + inside_sub_data + inside_post
            # done with inside sorts

            # replacements = [(re.compile(sub), replacement) for (sub, replacement) in wordpad_glitch]
            # for pattern, replacement in replacements:
            #     sub_data = pattern.sub(replacement, sub_data)

            sub_data = sub_data.replace(letters[random.randint(0, len(letters) - 1)],
                                        letters[random.randint(0, len(letters) - 1)])
            rand = random.randint(0, 5)
            datadict = [(pre + sub_data + post), (sub_data + pre + post), (post + pre + sub_data),
                        (pre + post + sub_data), (sub_data + post + pre), (post + sub_data + pre),
                        (pre[::1] + sub_data[::1] + post[::1]), (sub_data[::1] + pre[::1] + post[::1]),
                        (post[::1] + pre[::1] + sub_data[::1]), (pre[::1] + post[::1] + sub_data[::1]),
                        (sub_data[::1] + post[::1] + pre[::1]), (post[::1] + sub_data[::1] + pre[::1]),]
            core_data = random.choice(datadict)
        glitched = header + core_data
        outdir = os.path.join(basedir, "corrupt")
        corrupt_out_name = f'{filename}-corrupt.jpg'
        outpath = os.path.join(outdir, corrupt_out_name)
        with Image(blob=glitched) as img:
            img.format = 'jpg'
            img.compression_quality = 90
            img.save(filename=outpath)
        os.remove(path_bmp_out)
        if os.path.getsize(outpath) > 8000000:
            while os.path.getsize(outpath) > 8000000:
                with Image(filename=outpath) as img:
                    img.format = 'jpg'
                    img.compression_quality = 90
                    img.save(filename=outpath)
        return outpath

    def _deepfry(self, ctx, basedir, imagelocation):
        img_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp']
        frieddir = os.path.join(basedir, "fried")
        origfilepath = os.path.split(imagelocation)[0]
        filename = os.path.basename(imagelocation).split('.')[0]
        ext = os.path.basename(imagelocation).split('.')[-1]
        origfilename = f'{filename}.{ext}'
        fp = os.path.join(origfilepath, origfilename)
        if ext.lower() in img_formats:
            with Image(filename=fp) as img:
                with img.convert('jpg') as converted:
                    fried_out = f'{filename}.jpg'
                    path_fried_out = os.path.join(frieddir, fried_out)
                    frequency = 3
                    phase_shift = -90
                    amplitude = 0.2
                    bias = 0.7
                    converted.function('sinusoid', [frequency, phase_shift, amplitude, bias])
                    converted.level(0.3, 0.9, gamma=1.8)
                    converted.compression_quality = 5
                    converted.save(filename=path_fried_out)
                    return path_fried_out
        else:
            return None

    @commands.command(aliases=['alwayssunny', 'titlecard'])
    async def sunny(self, ctx, *, text: str):
        """Generates a titlecard from always sunny"""
        async with ctx.typing():
            pass
        partial_sunny = functools.partial(self._sunnytask, text)
        result = await self.bot.loop.run_in_executor(None, partial_sunny)
        if result is not None:
            file = io.BytesIO(result)
            await ctx.send(files=[discord.File(fp=file, filename="Sunny.png")])

    @commands.command()
    async def corrupt(self, ctx):
        """Corrupt an image"""
        if ctx.message.attachments:
            imglist = []
            download_list = list([at.url for at in ctx.message.attachments])
            for url in download_list:
                imglist += [url]
        else:
            imglist = await self._get_recent_images_links(ctx)
            if not imglist:
                raise self.bot.errors.DBotExternalError(f'No images have been posted in the last 25 messages that I '
                                                        f'could use.')
        imagefilename = (imglist[0]).split('/')[-1].strip().split(".")
        img_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp']
        if imagefilename[-1].lower() not in img_formats:
            raise self.bot.errors.DBotExternalError("The most recent attachment posted does not appear to be an image")
        filename = (f'{time.strftime("%Y%m%d-%H%M%S")}-{imagefilename[0]}-original.{imagefilename[-1]}')
        basedir = os.path.join(os.curdir, "internalfiles", "temp", "corrupt")
        origimglocation = os.path.join(os.curdir, "internalfiles", "temp", "corrupt", "original")
        fulllocation = os.path.join(origimglocation, filename)
        if not os.path.exists(origimglocation):
            os.makedirs(origimglocation)
        await self.bot.utils.retrieve_web_file(imglist[0], fulllocation)
        async with ctx.typing():
            pass
        partial_corrupt = functools.partial(self._corrupt_img, basedir, fulllocation)
        result = await self.bot.loop.run_in_executor(None, partial_corrupt)
        if result is not None:
            await ctx.send(file=discord.File(fp=result, filename="corrupt.jpg"))
        else:
            raise self.bot.errors.DBotExternalError(f"Sorry, there was an error on processing the image.")

    @commands.command(aliases=['needsmoarjpg', 'morejpg', 'moarjpg'])
    async def needsmorejpg(self, ctx):
        """Makes an image more jpg-y"""
        if ctx.message.attachments:
            imglist = []
            download_list = list([at.url for at in ctx.message.attachments])
            for url in download_list:
                imglist += [url]
        else:
            imglist = await self._get_recent_images_links(ctx)
            if not imglist:
                raise self.bot.errors.DBotExternalError(f'No images have been posted in the last 25 messages that I '
                                                        f'could use.')
        imagefilename = (imglist[0]).split('/')[-1].strip().split(".")
        img_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp']
        if imagefilename[-1].lower() not in img_formats:
            raise self.bot.errors.DBotExternalError("The most recent attachment posted does not appear to be an image")
        filename = (f'{time.strftime("%Y%m%d-%H%M%S")}-{imagefilename[0]}-original.{imagefilename[-1]}')
        imglocation = os.path.join(os.curdir, "internalfiles", "temp", "morejpg")
        if not os.path.exists(imglocation):
            os.makedirs(imglocation)
        fulllocation = os.path.join(imglocation, filename)
        await self.bot.utils.retrieve_web_file(imglist[0], fulllocation)
        async with ctx.typing():
            pass
        partial_jpg = functools.partial(self._moar_jpg, fulllocation)
        result = await self.bot.loop.run_in_executor(None, partial_jpg)
        if result is not None:
            await ctx.send(file=discord.File(fp=result, filename="moar.jpg"))
        else:
            raise self.bot.errors.DBotExternalError(f'Sorry, there was an error on processing the image.')

    @commands.command(aliases=['doge'])
    async def ok(self, ctx, *, text):
        """Ok"""
        imglocation = os.path.join(os.curdir, "internalfiles", "temp", "okdoge")
        if not os.path.exists(imglocation):
            os.makedirs(imglocation)
        async with ctx.typing():
            pass
        partial_doge = functools.partial(self._ok_doge, text)
        result = await self.bot.loop.run_in_executor(None, partial_doge)
        if result is not None:
            file = io.BytesIO(result)
            await ctx.send(files=[discord.File(fp=file, filename="ok.png")])

    @commands.command(aliases=['fried', 'fry', 'deep'])
    async def deepfry(self, ctx):
        """deepfry an image"""
        if ctx.message.attachments:
            imglist = []
            download_list = list([at.url for at in ctx.message.attachments])
            for url in download_list:
                imglist += [url]
        else:
            imglist = await self._get_recent_images_links(ctx)
            if not imglist:
                raise self.bot.errors.DBotExternalError(f'No images have been posted in the last 25 messages that I '
                                                        f'could use.')
        imagefilename = (imglist[0]).split('/')[-1].strip().split(".")
        img_formats = ['jpg', 'jpeg', 'png', 'tif', 'tiff', 'bmp']
        if imagefilename[-1].lower() not in img_formats:
            raise self.bot.errors.DBotExternalError("The most recent attachment posted does not appear to be an image")
        filename = (f'{time.strftime("%Y%m%d-%H%M%S")}-{imagefilename[0]}-original.{imagefilename[-1]}')
        basedir = os.path.join(os.curdir, "internalfiles", "temp", "fried")
        origimglocation = os.path.join(os.curdir, "internalfiles", "temp", "fried", "original")
        fulllocation = os.path.join(origimglocation, filename)
        if not os.path.exists(origimglocation):
            os.makedirs(origimglocation)
        await self.bot.utils.retrieve_web_file(imglist[0], fulllocation)

        async with ctx.typing():
            pass
        partial_fried = functools.partial(self._deepfry, ctx, basedir, fulllocation)
        result = await self.bot.loop.run_in_executor(None, partial_fried)
        if result is not None:
            await ctx.send(file=discord.File(fp=result, filename="fried.jpg"))
        else:
            raise self.bot.errors.DBotExternalError(f"Sorry, there was an error on processing the image.")

    # @commands.command()
    # async def hextest(self, ctx):
    #     imgpath = os.path.join("internalfiles", "temp", "test.bmp")
    #     bmpoffset = 0xA
    #     async with aiofiles.open(imgpath, mode="rb") as fp:
    #         await fp.seek(bmpoffset)
    #         offsetvalue = await fp.read(1)
    #         print(offsetvalue)
    #         await fp.seek(offsetvalue)
    #         header = fp[:offsetvalue]
    #         imgdata = fp[offsetvalue:]
    #         print(header)


def setup(dbot):
    dbot.add_cog(ImageManipulation(dbot))
