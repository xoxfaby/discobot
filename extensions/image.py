from extensions.utils.importsfile import *


class ImageManipulation:
    """Image memes"""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    # async def _get_recent_images_links(self, ctx):
    #     msglist = []
    #     async for message in ctx.channel.history(limit=25, reverse=False):
    #         if message.attachments:
    #             download_list = list([at.url for at in message.attachments])
    #             for url in download_list:
    #                 msglist += [url]
    #         else:
    #             content = message.content
    #             fileexts = ['.png', '.jpg', '.jpeg', '.gif']
    #             if any(ext in content for ext in fileexts):
    #                 urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    #                                   content)
    #                 if len(urls) > 0:
    #                     for url in urls:
    #                         msglist += [url]
    #     return msglist

    # def _corrupt_img(self, imglocation):
    #     # Majority of code absorbed from:
    #     # https://github.com/GlitchTools/batch_wordpad_glitch/blob/master/wordpad_glitch.py
    #
    #     img_formats = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']
    #
    #     wordpad_glitch = [
    #         (b'\x07', b'\x27'),
    #         (b'\x0B', b'\x0A\x0D'),
    #         (b'(?<!\x0A)(\x0D)', b'\x0A\x0D'),
    #         (b'(\x0A)(?<!\x0D)', b'\x0A\x0D')]
    #
    #     _wordpad_glitch = [
    #         (re.compile(sub), replacement) for (sub, replacement) in wordpad_glitch]
    #
    #     def replace(img, replacements=()):
    #         for pattern, replacement in replacements:
    #             img = pattern.sub(replacement, img)
    #         return img
    #     wordpad_replacer = functools.partial(replace, replacements=_wordpad_glitch)
    #
    #     if os.path.splitext(imglocation)[1].lower() in img_formats:
    #         img = Image.open(imglocation)
    #         filename = os.path.basename(imglocation).split('.')[0]
    #
    #     with open(imglocation) as in_file:
    #         imgbytes = io.BytesIO(in_file.read())
    #         imgbytes.seek(0)
    #
    #     imagebytes.seek(0)
    #     header = imagebytes.read(16 + 24)
    #     glitched = io.BytesIO(header + wordpad_replacer(imagebytes.read()))
    #     glitched.seek(0)
    #     output = io.BytesIO(glitched.read())
    #     with open(output_image, 'wb') as wh:
    #         wh.write(output.read())
    #     print("saved image {0}".format(output_image))
    #     wh.close()
    #
    #
    #     with open(imglocation, "wb") as img_file:
    #         img_file.write(imagebytes)
    #         imglocation1 = os.path.join("internalfiles", "temp",
    #                                     (time.strftime("%Y%m%d-%H%M%S") + "-corrupt.jpg"))
    #         # test_img_to_str = str(imagebytes)
    #         tobend = bndr.Bndr(imagebytes)
    #         with open(imglocation1, 'w') as out_image:
    #             outimage = tobend.process(bndr.ChrisBend())
    #             out_image.write(outimage)
    #     return imglocation1


    # @commands.command()
    # async def corrupt(self, ctx):
    #     """Corrupt an image"""
    #     imglist = await self._get_recent_images_links(ctx)
    #     if not imglist:
    #         raise self.bot.myerrors.DBotExternalError("No images have been posted in the last 25 messages that I "
    #                                                   "could use.")
    #     filename, fileext = os.path.splitext(imglist[0])
    #     imglocation = os.path.join("internalfiles", "temp", (time.strftime("%Y%m%d-%H%M%S") +
    #                                filename + "-original" + fileext))
    #     await self.bot.utils._retrieve_web_file(imglist[0], imglocation)
    #     result = await self.bot.loop.run_in_executor(None, self._corrupt_img, imglocation)
    #     if result is not None:
    #         print(result)
    #         await ctx.send(file=discord.File(fp=result, filename="corrupt.jpg"))
    #     else:
    #         raise self.bot.myerrors.DBotExternalError(f"Sorry, the resulting image had an error.")


def setup(dbot):
    dbot.add_cog(ImageManipulation(dbot))
