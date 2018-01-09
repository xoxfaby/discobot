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

    # async def _corrupt_img(self, ctx):
    #     async with aiohttp.ClientSession() as sess:
    #         async with sess.get(imglist[0]) as resp:
    #             if resp.status == 200:
    #                 filename, fileext = os.path.splitext(imglist[0])
    #                 if fileext != ".jpg":
    #                     raise self.bot.myerrors.BotNotWorking("Image needs to be a jpg\n"
    #                                                           "Currently other conversions are not working properly.")
    #                     # resp1 = await resp.read()
    #                     # im = await Image.open(resp1)
    #                     # print("after read")
    #                     # rgb_im = im.convert()
    #                     # print("before convert")
    #                     # imglocation = os.path.join("internalfiles", "temp",
    #                     #                            (time.strftime("%Y%m%d-%H%M%S") + "-new.jpg"))
    #                     # await rgb_im.save(imglocation)
    #                     # async with aiofiles.open(imglocation) as newread:
    #                     #     img_buff = await newread.read()
    #                 else:
    #                     imglocation = os.path.join("internalfiles", "temp",
    #                                                (time.strftime("%Y%m%d-%H%M%S") + "-original" + fileext))
    #                     img_buff = await resp.read()
    #                 async with aiofiles.open(imglocation, "wb") as img_file:
    #                     await img_file.write(img_buff)
    #                 imglocation1 = os.path.join("internalfiles", "temp",
    #                                             (time.strftime("%Y%m%d-%H%M%S") + "-corrupt.jpg"))
    #                 async with aiofiles.open(imglocation, 'rb') as input_image:
    #                     img = await input_image.read()
    #                     tobend = bndr.Bndr(img)
    #                     async with aiofiles.open(imglocation1, 'wb') as out_image:
    #                         outimage = tobend.process(bndr.ChrisBend())
    #                         await out_image.write(outimage)
    #                 await ctx.send(file=discord.File(fp=imglocation1, filename="bent.jpg"))
    #             else:
    #                 raise self.bot.myerrors.DBotExternalError("Bad image was given")
    #     # for i in range(random.randint(5, 25)):
    #     #     img_buff[random.randint(0, len(img_buff))] = random.randint(1, 254)
    #     # await ctx.send(file=discord.File(io.BytesIO(img_buff), filename="corrupt.jpg"))
    #
    # @commands.command()
    # async def corrupt(self, ctx, *args):
    #     """Corrupt an image"""
    #     imglist = await self._get_recent_images_links(ctx)
    #     if not imglist:
    #         raise self.bot.myerrors.DBotExternalError("No images have been posted in the last 25 messages that I "
    #                                                   "could use.")
    #     result = await self.bot.loop.run_in_executor(None, self._corrupt_img, args)
    #     # if result is not None:
    #     #     pass
    #     #     # do things with results
    #     #     # result.pods, result.info, result.assumptions, result.warnings, result.results
    #     #     # await ctx.send(result)
    #     # else:
    #     #     raise self.bot.myerrors.DBotExternalError(f"Sorry, I couldn't calculate `{args}`.")

def setup(dbot):
    dbot.add_cog(ImageManipulation(dbot))
