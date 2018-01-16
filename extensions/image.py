from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class ImageManipulation:
    """Image Manipulation"""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

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

    # def _corrupt_img(self, imglocation):
    #     # Majority of code absorbed from:
    #     # https://github.com/GlitchTools/batch_wordpad_glitch/blob/master/wordpad_glitch.py
    #     # Adaptions were made from the flow of the code, but the actual glitching was copied
    #
    #    img_formats = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']
    #     wordpad_glitch = [
    #         # (b'\x07', b'\x27'),
    #         # (b'\x0B', b'\x0A\x0D'),
    #         (b'(?<!\x0A)(\x0D)', b'\x0A\x0D'),
    #         (b'(\x0A)(?<!\x0D)', b'\x0A\x0D')]
    #
    #     _wordpad_glitch = [
    #         (re.compile(sub), replacement) for (sub, replacement) in wordpad_glitch]
    #
    #     def _replace(img, replacements=()):
    #         for pattern, replacement in replacements:
    #             img = pattern.sub(replacement, img)
    #         return img
    #     wordpad_replacer = functools.partial(_replace, replacements=_wordpad_glitch)
    #
    #     # Open image from imglocation, close image, save as bmp
    #     realfilepath = os.path.split(imglocation)[0]
    #     filename = os.path.basename(imglocation).split('.')[0]
    #     if os.path.splitext(imglocation)[1].lower() in img_formats:
    #         img = Image.open(imglocation)
    #         bmp_out = f'{filename}.bmp'
    #         path_bmp_out = os.path.join(realfilepath, bmp_out)
    #         img.save(path_bmp_out)
    #     else:
    #         return None
    #     # open bmp
    #     with open(path_bmp_out, 'rb') as in_file:
    #         imgbytes = in_file.read()
    #     header = imgbytes[:1000]
    #     core_data = imgbytes[1000:]
    #     data_size = len(core_data)
    #     letters = b'a', b'b', b'c', b'd', b'e'
    #     for xx in range(5):
    #         ii = random.randint(0, data_size - 1)
    #         jj = random.randint(ii, ii + random.randint(100, 10000))
    #         pre = core_data[:ii]
    #         post = core_data[jj:]
    #         sub_data = core_data[ii:jj]
    #         sub_data = sub_data.replace(letters[random.randint(0, 4)],
    #                                     letters[random.randint(0, 4)])
    #         core_data = pre + sub_data + post
    #
    #     glitched = header + core_data
    #     print(len(glitched))
    #     corrupt_out_name = f'{filename}-corrupt.jpg'
    #     out_path = os.path.join(os.path.dirname(realfilepath), corrupt_out_name)
    #     with open(out_path, 'wb') as wh:
    #         wh.write(glitched)
    #     wh.close()
    #     return out_path
    #
    # @commands.command()
    # async def corrupt(self, ctx):
    #     """Corrupt an image"""
    #     imglist = await self._get_recent_images_links(ctx)
    #     if not imglist:
    #         raise self.bot.errors.DBotExternalError(f'No images have been posted in the last 25 messages that I could'
    #                                                 f' use.')
    #     imagefilename = (imglist[0]).split('/')[-1].strip().split(".")
    #     filename = (f'{time.strftime("%Y%m%d-%H%M%S")}-{imagefilename[0]}-original.{imagefilename[1]}')
    #     imglocation = os.path.join(os.curdir, "internalfiles", "temp", "corrupt")
    #     fulllocation = os.path.join(imglocation, filename)
    #     imglocation = os.path.join(os.curdir, "internalfiles", "temp", "morejpg")
    #     if not os.path.exists(imglocation):
    #         os.makedirs(imglocation)
    #     await self.bot.utils.retrieve_web_file(imglist[0], fulllocation)
    #     async with ctx.typing():
    #         result = await self.bot.loop.run_in_executor(None, self._corrupt_img, fulllocation)
    #     if result is not None:
    #         await ctx.send(file=discord.File(fp=result, filename="corrupt.jpg"))
    #     else:
    #         raise self.bot.errors.DBotExternalError(f"Sorry, there was an error on processing the image.")

    @commands.command(aliases=['needsmoarjpg', 'morejpg', 'moarjpg'])
    async def needsmorejpg(self, ctx):
        """Makes an image more jpg-y"""
        imglist = await self._get_recent_images_links(ctx)
        if not imglist:
            raise self.bot.errors.DBotExternalError(f'No images have been posted in the last 25 messages that I could'
                                                    f' use.')
        imagefilename = (imglist[0]).split('/')[-1].strip()
        filename = (f'{time.strftime("%Y%m%d-%H%M%S")}-original-{imagefilename}')
        imglocation = os.path.join(os.curdir, "internalfiles", "temp", "morejpg")
        if not os.path.exists(imglocation):
            os.makedirs(imglocation)
        fulllocation = os.path.join(imglocation, filename)
        await self.bot.utils.retrieve_web_file(imglist[0], fulllocation)
        async with ctx.typing():
            convertedfilepath = await self.bot.loop.run_in_executor(None, self._moar_jpg, fulllocation)
        if convertedfilepath is not None:
            newfn = str("moarjpg" + filename)
            await ctx.send(file=discord.File(fp=convertedfilepath, filename=newfn))
        else:
            raise self.bot.errors.DBotExternalError(f'Sorry, there was an error on processing the image.')


def setup(dbot):
    dbot.add_cog(ImageManipulation(dbot))
