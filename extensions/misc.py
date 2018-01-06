from extensions.utils.importsfile import *


class Misc:
    """Miscellaneous commands for the bot."""
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def _internalfile(self, ctx, args: str):
        async with ctx.typing():
            file = os.path.join("internalfiles", "images", args)
            return await ctx.send(file=discord.File(fp=file, filename=args))

    @commands.group(hidden=True)
    async def watch(self, ctx):
        """
        This command allows you to set a list of links that are unique to your discord guild/server.
        This list can be as large or small as you want.
        You can invoke this command a number of ways.
        By calling `watch` by itself, I will print a list of registered links;
        By calling `watch add` and then listing a link or multiple links separated by spaces, I will add it to the stored list;
        By calling `watch remove` and then listing a link or multiple links separated by spaces, I will remove it from the stored list;
        By calling `watch removeall` I will remove all stored links;
        """
        if ctx.invoked_subcommand is None:
            # check cache for media links per guild
            cache_key = f'{str(ctx.guild.id)}_links'
            guild_links_exists_in_cache = await self.bot.sql.mysqlcache.exists(key=cache_key)
            if guild_links_exists_in_cache:
                linksvalue = await self.bot.sql.mysqlcache.get(key=cache_key)
                get_from_db = False
            else:
                linksvalue = None
                get_from_db = True
            # if not in cache, check db for links
            if get_from_db:
                table_name = f'`{self.bot.common.mysqldb}`.`_guild_links`'
                sqlquery = """
                SELECT `links` FROM {0} WHERE `guild-id` = '{1}'
                """
                sql_cmd = sqlquery.format(table_name, ctx.guild.id)
                async with self.bot.sql.mysqlcon.acquire() as conn:
                    async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(sql_cmd)
                        num_rows = cursor.rowcount
                        if num_rows == 0:
                            raise self.bot.myerrors.DBotInternalError("Error: this server has no stored links.")
                        else:
                            linksvalue = await cursor.fetchall()
                            await self.bot.sql.mysqlcache.add(key=cache_key, value=linksvalue)
            linktext = ""
            for row in linksvalue:
                linktext += str(row['links'] + "\n")
            embed = discord.Embed(title="Links:", colour=discord.Colour(0x17f705))
            embed.add_field(name="_\n_", value=linktext)
            await ctx.send(embed=embed)

    @watch.command()
    async def add(self, ctx, *args):
        cache_key = f'{str(ctx.guild.id)}_links'
        links = (" ".join(args)).split(" ")
        guildid = str(ctx.guild.id)
        table_name = f'`{str(self.bot.common.mysqldb)}`.`_guild_links`'
        sqlquery = """
        INSERT INTO {0} (`guild-id`, `links`)
        VALUES (%s, %s);
        """
        sql_cmd = sqlquery.format(table_name)
        querydata = []
        for link in links:
            data = (str(guildid), str(link))
            querydata.append(data)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.executemany(sql_cmd, querydata)
        await self.bot.sql.mysqlcache.delete(key=cache_key)
        await ctx.send("Alright, I've added that to the database.")

    @watch.command()
    async def remove(self, ctx, *args):
        cache_key = f'{str(ctx.guild.id)}_links'
        links = (" ".join(args)).split(" ")
        guildid = str(ctx.guild.id)
        table_name = f'`{str(self.bot.common.mysqldb)}`.`_guild_links`'
        sqlquery = """
        DELETE FROM {0} 
        WHERE `guild-id` = '{1}'
        AND `links` = %s
        """
        sql_cmd = sqlquery.format(table_name, str(guildid))
        querydata = []
        for link in links:
            data = (str(link))
            querydata.append(data)
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.executemany(sql_cmd, querydata)
        await self.bot.sql.mysqlcache.delete(key=cache_key)
        await ctx.send("Alright, I've removed the listed links from the database.")

    @watch.command()
    async def removeall(self, ctx, *args):
        cache_key = f'{str(ctx.guild.id)}_links'
        await self.bot.sql.mysqlcache.delete(key=cache_key)
        guildid = str(ctx.guild.id)
        table_name = f'`{str(self.bot.common.mysqldb)}`.`_guild_links`'
        sqlquery = """
               DELETE FROM {0} 
               WHERE `guild-id` = '{1}'
               """
        sql_cmd = sqlquery.format(table_name, str(guildid))
        async with self.bot.sql.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql_cmd)
        await self.bot.sql.mysqlcache.delete(key=cache_key)
        await ctx.send("Alright, I've removed all links from the database.")

    @commands.command()
    async def fakename(self, ctx):
        apiurl = "https://uinames.com/api/?ext"
        async with aiohttp.ClientSession() as session:
            async with session.get(apiurl) as r:
                if r.status == 200:
                    parsed_json = await r.json()
                    fullname = (parsed_json['name'] + ' ' + parsed_json['surname'])
                    gender = parsed_json['gender']
                    location = parsed_json['region']
                    age = parsed_json['age']
                    birthday = parsed_json['birthday']['dmy']
                    email = parsed_json['email']
                    photo = parsed_json['photo']
                    fakeperson = discord.Embed(title=str(fullname), colour=discord.Colour(0xd6f00c))
                    fakeperson.add_field(name="Gender", value=str(gender), inline=True)
                    fakeperson.add_field(name="Location", value=str(location), inline=True)
                    fakeperson.add_field(name="Age", value=str(age), inline=True)
                    fakeperson.add_field(name="Birthdate", value=str(birthday), inline=True)
                    fakeperson.add_field(name="Email Address", value=str(email), inline=True)
                    fakeperson.set_image(url=photo)
                    return await ctx.send(embed=fakeperson)

    @commands.command(aliases=['w', 'W'], usage="[zipcode]")
    async def weather(self, ctx, zipcode=None):
        authorid = ''
        if (zipcode is None) or ctx.message.mentions:
            if ctx.message.mentions:
                mesg = ctx.message.mentions
                for usermention in mesg:
                    authorid = usermention.id
            else:
                authorid = ctx.author.id
            sqlcmd = await self.bot.sql.statement_get_weather_single_user(authorid)
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sqlcmd)
                    num_rows = cursor.rowcount
                    if num_rows:
                        getlocation = (await cursor.fetchone())[0]
                    else:
                        getlocation = None
            if getlocation is None:
                if ctx.message.mentions:
                    message = "The mentioned user has not set their default weather;\nplease try again."
                    raise self.bot.myerrors.DBotInternalError(message)
                else:
                    message = ('Please use a zip code when calling this function\n Example: `' +
                               self.bot.common.discordbotcommandprefix + 'weather 98104`\nYou could also set your '
                               'default weather by using the `' + self.bot.common.discordbotcommandprefix +
                               'weatherset zipcode` command')
                    raise self.bot.myerrors.DBotInternalError(message)
            else:
                getlocation = str(getlocation)
        elif zipcode.isdigit():
            getlocation = str(zipcode)
        else:
            raise self.bot.myerrors.DBotInternalError("A zipcode or user mention was not given")
        if getlocation:
            tempfull = "http://api.wunderground.com/api/{0}/geolookup/conditions/radar/q/{1}.json"
            fullurl = tempfull.format(self.bot.common.weatherapikey, getlocation)
            tempradar = ("http://api.wunderground.com/api/{0}/animatedradar/q/{1}.gif"
                         "?newmaps=1&timelabel=1&timelabel.y=10&num=8&delay=75")
            radarimageurl = tempradar.format(self.bot.common.weatherapikey, getlocation)
            weathercontent = discord.Embed()
            parsed_json = {}
            currentweather = ""
            async with ctx.typing():
                async with aiohttp.ClientSession() as session:
                    async with session.get(fullurl) as r:
                        if r.status == 200:
                            parsed_json = await r.json()
                            location1 = str(parsed_json['current_observation']['display_location']['full'])
                            location2 = str(parsed_json['current_observation']['display_location']['country_iso3166'])
                            locationfull = str(f'{location1}, {location2}')
                            temp = parsed_json['current_observation']['temperature_string']
                            weburl = parsed_json['current_observation']['ob_url']
                            currentweather = parsed_json['current_observation']['weather']
                            lastupdated = (parsed_json['current_observation']['observation_time'] + " (Local time)")
                            humidity = parsed_json['current_observation']['relative_humidity']
                            wind = (str(parsed_json['current_observation']['wind_dir']) + ' at ' +
                                    str(parsed_json['current_observation']['wind_mph']) + ' MPH, gusting to ' +
                                    str(parsed_json['current_observation']['wind_gust_mph']) + ' MPH')
                            weathercontent.title = str(locationfull)
                            weathercontent.colour = discord.Color(0xd6f00c)
                            weathercontent.url = str(weburl)
                            weathercontent.add_field(name="Updated", value=str(lastupdated), inline=False)
                            weathercontent.add_field(name="Current Conditions", value=str(currentweather), inline=False)
                            weathercontent.add_field(name="Current Temperature", value=str(temp), inline=True)
                            weathercontent.add_field(name="Humidity", value=str(humidity), inline=True)
                            weathercontent.add_field(name="Wind", value=str(wind), inline=True)
                radargiflocation = os.path.join("internalfiles", "temp",
                                                (getlocation + "-" + time.strftime("%Y%m%d-%H%M%S") + "-radar.gif"))
                async with aiohttp.ClientSession() as session:
                    async with session.get(radarimageurl) as resp:
                        if resp.status == 200:
                            gifout = await resp.read()
                            with open(radargiflocation, "wb") as giffile:
                                giffile.write(gifout)
                        else:
                            radarimagetemp = parsed_json['radar']['image_url']
                            radarimageurl1 = radarimagetemp.replace("%26api_key=" + self.bot.common.weatherapikey,
                                                                    "%26time1=" + time.strftime("%H%M%S"))
                            async with session.get(radarimageurl1) as resp:
                                if resp.status == 200:
                                    gifout = await resp.read()
                                    with open(radargiflocation, "wb") as giffile:
                                        giffile.write(gifout)
                    weathercontent.set_image(url='attachment://radar.gif')
            if "fog" in currentweather.lower():
                await ctx.send("```IT IS FOG```")
                await asyncio.sleep(4)
            elif "snow" in currentweather.lower():
                await ctx.send("```FUCK SNOW```")
                await asyncio.sleep(4)
            await ctx.send(embed=weathercontent, file=discord.File(radargiflocation, 'radar.gif'))

    @commands.command(aliases=['ws'], usage=['[zipcode]'])
    async def weatherset(self, ctx, zipcode=None):
        if zipcode is None:
            raise self.bot.myerrors.DBotInternalError("You did not pass a zipcode when calling this command.\nExample: "
                                                      "`" + self.bot.common.discordbotcommandprefix +
                                                      "weatherset 98104`")
        elif zipcode.isdigit():
            sqlquery = await self.bot.sql.statement_upsert_weathertable(str(ctx.author.id), str(zipcode))
            async with self.bot.sql.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sqlquery)
            return await ctx.send('Your default weather has been set\nIn the future, you can run `'
                                  + self.bot.common.discordbotcommandprefix + 'w` to retrieve your local weather')
        else:
            raise self.bot.myerrors.DBotInternalError("A proper zip code was not specified")

    @commands.command(aliases=['poll'])
    async def straw(self, ctx, *args):
        """
        Creates a poll on strawpoll.
        Usage:
        - Enter all parameters with double quotes
        poll "my poll title" "first option" "second option" "third option" etc...
        """
        spoll_api = strawpoll.API()
        title = args[0]
        arglist = list(args)
        arglist.pop(0)
        topoll = strawpoll.Poll(title, arglist, multi=False)
        return_poll = await spoll_api.submit_poll(poll=topoll)
        return await ctx.send(return_poll.url)

    @commands.command()
    async def nice(self, ctx):
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        return await ctx.send("Nice")

    @commands.command()
    async def notnice(self, ctx):
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        return await ctx.send("That wasn't very nice of you.")

    @commands.command()
    async def roll(self, ctx, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            return await ctx.send('Format has to be in NdN!')
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='To decide between multiple choices', aliases=['decide'])
    async def choose(self, ctx, *args: str):
        options = (" ".join(args)).split(" or ")
        return await ctx.send(random.choice(options))

    @commands.command(description='No fighting', aliases=['preciousfriends', 'friends', 'nofight', 'nofite'])
    async def fight(self, ctx):
        """
        No fiting aloud
        """
        return await self._internalfile(ctx, "V63Hv.jpg")

    @commands.command(description='sadpanda', aliases=['panda', 'fuckyou', 'exhentai', 'why'])
    async def sadpanda(self, ctx):
        """
        Fuck you why is there a sad panda
        """
        return await self._internalfile(ctx, "sadpanda.png")

    @commands.command(description='sleep')
    async def sleep(self, ctx):
        """
        Awoo sleep
        """
        return await self._internalfile(ctx, "awoosleep.png")

    @commands.command(aliases=['404'])
    async def fourzerofour(self, ctx):
        """
        File not found
        """
        return await self._internalfile(ctx, "404.gif")

    @commands.command()
    async def cat(self, ctx):
        """
        Retreives a random cat image from http://random.cat/
        """
        fullurl = "http://random.cat/meow"
        async with aiohttp.ClientSession() as session:
            async with session.get(fullurl) as r:
                if r.status == 200:
                    parsed_json = await r.json()
                    await ctx.send(parsed_json['file'])
                else:
                    raise self.bot.myerrors.DBotExternalError("An error occurred when calling random.cat")

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *args):
        mesg = ' '.join(args)
        query = mesg.replace(" ", "+")
        myurl = f'https://www.googleapis.com/youtube/v3/search?q={query}&type=video&maxResults=5&' \
                f'part=snippet&safeSearch=None&key={self.bot.common.youtubeapikey}'
        publicurl = f'https://www.youtube.com/results?search_query={query}'
        embed = discord.Embed(title=("Youtube search results for " + mesg), url=publicurl, color=0xff0000)
        itemcontents = []
        title = []
        uploaded = []
        videoid = []
        fullurl = []
        length = []
        async with aiohttp.ClientSession() as session:
            async with session.get(myurl) as r:
                if r.status == 200:
                    parsed_json = await r.json()
                    items = parsed_json['items']
                    for result in items:
                        title.append(str(result['snippet']['title']))
                        uploaded.append(str(result['snippet']['publishedAt']))
                        videoid.append(str(result['id']['videoId']))
                        fullurl.append("https://youtu.be/" + result['id']['videoId'])
                        itemcontents.append(str(result['id']['videoId']))
                else:
                    raise self.bot.myerrors.DBotExternalError("An error occurred when calling Youtube")
        contentslist = ",".join(itemcontents)
        newurl = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&' \
                 f'key={self.bot.common.youtubeapikey}&id={contentslist}'
        async with aiohttp.ClientSession() as session:
            async with session.get(newurl) as r:
                if r.status == 200:
                    parsed_json = await r.json()
                    items = parsed_json['items']
                    for result in items:
                        templength = (str(result['contentDetails']['duration']).strip("PT"))
                        if "H" in templength:
                            newlength = templength.replace("H"," hours,").replace("M", " minutes, ").replace("S",
                                                                                                             " seconds")
                        elif "H" not in templength:
                            newlength = templength.replace("M", " minutes, ").replace("S", " seconds")
                        elif "M" not in templength:
                            newlength = templength.replace("S", " seconds")
                        else:
                            newlength = templength
                        length.append(str(newlength))
        incnum = 1
        for t, u, v, f, l in zip(title, uploaded, videoid, fullurl, length):
            videoinfo = f'Length: {l}\nURL: {f}'
            embed.add_field(name="Title", value=t, inline=False)
            embed.add_field(name="_\n_", value=videoinfo, inline=False)
            incnum += 1

        def checknumber(m):
            return (m.author == ctx.author) and (int(m.content) < int(len(contentslist)))

        botmessage = await ctx.send(embed=embed)
        questionmesg = await ctx.send("Please say the video number you want")
        numberresponse = await self.bot.wait_for('message', check=checknumber)
        newcontent = fullurl[(int(numberresponse.content) - 1)]
        await questionmesg.delete()
        await numberresponse.delete()
        await botmessage.edit(content=newcontent, embed=None)

    @commands.command()
    async def avatar(self, ctx, target: discord.User=None):
        if target is None:
            target = ctx.message.author
        embed = discord.Embed(title="Avatar")
        embed.set_image(url=target.avatar_url_as(format='png'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['bigmoji', 'bemoji', 'big'])
    async def bigemoji(self, ctx, emoji):
        try:
            newemoji = await commands.EmojiConverter().convert(ctx, emoji)
        except commands.BadArgument:
            return await ctx.send("This is not a custom emoji, I cannot biggify it.")
        if type(newemoji) == discord.Emoji:
            emoji_cdn = newemoji.url
            embed = discord.Embed(title=f':{newemoji.name}: \N{EM DASH} `{newemoji.id}`')
            embed.set_image(url=emoji_cdn)
            await ctx.send(embed=embed)


class EtcOnMessage:
    def __init__(self, bot):
        self.bot = bot
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
              + ': Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_message(self, message):
        if (message.content.startswith(self.bot.common.discordbotcommandprefix)) or \
                (str(message.author.id) == str(self.bot.common.botdiscordid)):
            return
        else:
            alphabet = {"bmoji": u"\U0001f171", "oksymbol": str("👌"), "fire": str("🔥")}
            msg = message.content
            if msg.lower().startswith('ok google') or msg.lower().startswith('okay google'):
                if msg.lower().startswith('ok google'):
                    subreplace = re.compile('ok google ', re.IGNORECASE)
                    newmsg = subreplace.sub("", msg)
                elif msg.lower().startswith('okay google'):
                    subreplace = re.compile('okay google ', re.IGNORECASE)
                    newmsg = subreplace.sub("", msg)
                else:
                    newmsg = msg
                newmesg1 = newmsg.replace(" ", "+")
                googleurl = (str("https://www.google.com/search?q=") + str(newmesg1))
                await message.channel.send(str(googleurl))
            if alphabet["oksymbol"] in msg:
                firemsg = ""
                numberoffire = random.randrange(0, 5)
                if numberoffire == 0:
                    await message.channel.send("That was not fire at all")
                else:
                    for _ in range(numberoffire):
                        firemsg += alphabet["fire"]
                    await message.channel.send(firemsg)
            # if :
            #     for char in alphabet.keys():
            #         if char in msg:
            #             bmsg = msg.replace(char, alphabet[char])
            #         elif char.upper() in msg:
            #             bmsg = msg.replace(char.upper(), alphabet[char])
            #         if msg != message.content:
            #             await message.send(content=bmsg)


def setup(dbot):
    dbot.add_cog(Misc(dbot))
    dbot.add_cog(EtcOnMessage(dbot))
