from extensions.utils.importsfile import *


class ImageManipulation:
    """Image memes"""

    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

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

    def _corrupt_img(self, fileext, imagebytes):
        if fileext != ".jpg":
            raise self.bot.myerrors.BotNotWorking("Image needs to be a jpg\nCurrently other conversions are not "
                                                  "working properly.\nMy apologies for the inconvenience.")
    #         # resp1 = await resp.read()
    #         # im = await Image.open(resp1)
    #         # print("after read")
    #         # rgb_im = im.convert()
    #         # print("before convert")
    #         # imglocation = os.path.join("internalfiles", "temp",
    #         #                            (time.strftime("%Y%m%d-%H%M%S") + "-new.jpg"))
    #         # await rgb_im.save(imglocation)
    #         # async with aiofiles.open(imglocation) as newread:
    #         #     img_buff = yield from resp.content.read()
        else:
            imglocation = os.path.join("internalfiles", "temp",
                                       (time.strftime("%Y%m%d-%H%M%S") + "-original" + fileext))
        with open(imglocation, "wb") as img_file:
            img_file.write(imagebytes)
        imglocation1 = os.path.join("internalfiles", "temp",
                                    (time.strftime("%Y%m%d-%H%M%S") + "-corrupt.jpg"))
    #     test_img_to_str = str(img_buff)
    #     tobend = bndr.Bndr(test_img_to_str)
    #     with open(imglocation1, 'w') as out_image:
    #         outimage = tobend.process(bndr.ChrisBend())
    #         out_image.write(outimage)
    #     return imglocation1
    #     # await ctx.send(file=discord.File(fp=imglocation1, filename="bent.jpg"))
    #     # for i in range(random.randint(5, 25)):
    #     #     img_buff[random.randint(0, len(img_buff))] = random.randint(1, 254)
    #     # await ctx.send(file=discord.File(io.BytesIO(img_buff), filename="corrupt.jpg"))

    @commands.command()
    async def corrupt(self, ctx):
        """Corrupt an image"""
        imglist = await self._get_recent_images_links(ctx)
        if not imglist:
            raise self.bot.myerrors.DBotExternalError("No images have been posted in the last 25 messages that I "
                                                      "could use.")
        filename, fileext = os.path.splitext(imglist[0])
        imgbytes = await self.bot.utils._bytes_download(imglist[0])
        result = await self.bot.loop.run_in_executor(None, self._corrupt_img, fileext, imgbytes)
        if result is not None:
            print(result)
            # do things with results
            # result.pods, result.info, result.assumptions, result.warnings, result.results
            # await ctx.send(result)
        else:
            raise self.bot.myerrors.DBotExternalError(f"Sorry, the resulting image had an error.")

def setup(dbot):
    dbot.add_cog(ImageManipulation(dbot))
