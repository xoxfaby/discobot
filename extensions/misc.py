from extensions.utils.importsfile import *
from extensions.utils import dbotchecks


class Misc:
    """Miscellaneous commands for the bot."""
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def _internalfile(self, ctx, args: str):
        async with ctx.typing():
            file = os.path.join("internalfiles", "images", args)
            return await ctx.send(file=discord.File(fp=file, filename=args))

    @commands.group(hidden=True, aliases=['watch'])
    async def links(self, ctx):
        """
        This command allows you to set a list of links that are unique to your discord guild/server.
        This list can be as large or small as you want.
        You can invoke this command a number of ways.
        By calling `watch` by itself, I will print a list of registered links;
        By calling `watch add` and then listing a link or multiple links separated by spaces, I will add it to the stored list;
        By calling `watch remove` and then listing a link or multiple links separated by spaces, I will remove it from the stored list;
        """
        if ctx.invoked_subcommand is None:
            # check cache for media links per guild
            cache_key = f'{str(ctx.guild.id)}_links'
            guild_links_exists_in_cache = await self.bot.mysqlcache.exists(key=cache_key)
            if guild_links_exists_in_cache:
                linksvalue = await self.bot.mysqlcache.get(key=cache_key)
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
                async with self.bot.mysqlcon.acquire() as conn:
                    async with conn.cursor(aiomysql.DictCursor) as cursor:
                        await cursor.execute(sql_cmd)
                        num_rows = cursor.rowcount
                        if num_rows == 0:
                            raise self.bot.errors.DBotInternalError("Error: this server has no stored links.")
                        else:
                            linksvalue = await cursor.fetchall()
                            await self.bot.mysqlcache.add(key=cache_key, value=linksvalue)
            linktext = ""
            for row in linksvalue:
                linktext += str(row['links'] + "\n")
            embed = discord.Embed(title="Links:", colour=discord.Colour(0x17f705))
            embed.add_field(name="_\n_", value=linktext)
            await ctx.send(embed=embed)

    @links.command()
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
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.executemany(sql_cmd, querydata)
        await self.bot.mysqlcache.delete(key=cache_key)
        await ctx.send("Alright, I've added that to the database.")

    @links.command()
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
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.executemany(sql_cmd, querydata)
        await self.bot.mysqlcache.delete(key=cache_key)
        await ctx.send("Alright, I've removed the listed links from the database.")

    @links.command()
    async def removeall(self, ctx):
        cache_key = f'{str(ctx.guild.id)}_links'
        await self.bot.mysqlcache.delete(key=cache_key)
        guildid = str(ctx.guild.id)
        table_name = f'`{str(self.bot.common.mysqldb)}`.`_guild_links`'
        sqlquery = """
               DELETE FROM {0} 
               WHERE `guild-id` = '{1}'
               """
        sql_cmd = sqlquery.format(table_name, str(guildid))
        async with self.bot.mysqlcon.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(sql_cmd)
        await self.bot.mysqlcache.delete(key=cache_key)
        await ctx.send("Alright, I've removed all links from the database.")

    @commands.command()
    async def fakename(self, ctx):
        """Generates a fake name"""
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
        """Retrieves the weather"""
        if (zipcode is None) or ctx.message.mentions:
            if ctx.message.mentions:
                authorid = ctx.message.mentions[0].id
            else:
                authorid = ctx.author.id
            sqlcmd = await self.bot.sql.statement_get_weather_single_user(authorid)
            async with self.bot.mysqlcon.acquire() as conn:
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
                    raise self.bot.errors.DBotInternalError(message)
                else:
                    message = ('Please use a zip code when calling this function\n Example: `' +
                               self.bot.common.discordbotcommandprefix + 'weather 98104`\nYou could also set your '
                               'default weather by using the `' + self.bot.common.discordbotcommandprefix +
                               'weatherset zipcode` command')
                    raise self.bot.errors.DBotInternalError(message)
        elif zipcode.isdigit():
            getlocation = str(zipcode)
        else:
            raise self.bot.errors.DBotInternalError("A zipcode or user mention was not given")
        tempfull = "http://api.wunderground.com/api/{0}/geolookup/conditions/radar/q/{1}.json"
        fullurl = tempfull.format(self.bot.common.weatherapikey, str(getlocation))
        tempradar = ("http://api.wunderground.com/api/{0}/animatedradar/q/{1}.gif?newmaps=1&timelabel=1&timelabel.y=10"
                     "&num=8&delay=75")
        radarimageurl = tempradar.format(self.bot.common.weatherapikey, str(getlocation))
        weathercontent = discord.Embed()
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
                        wind = (f"{str(parsed_json['current_observation']['wind_dir'])} at "
                                f"{str(parsed_json['current_observation']['wind_mph'])}  MPH, gusting to "
                                f"{str(parsed_json['current_observation']['wind_gust_mph'])} MPH"
                                )
                        weathercontent.title = str(locationfull)
                        weathercontent.colour = discord.Color(0xd6f00c)
                        weathercontent.url = str(weburl)
                        weathercontent.add_field(name="Updated", value=str(lastupdated), inline=False)
                        weathercontent.add_field(name="Current Conditions", value=str(currentweather), inline=False)
                        weathercontent.add_field(name="Current Temperature", value=str(temp), inline=True)
                        weathercontent.add_field(name="Humidity", value=str(humidity), inline=True)
                        weathercontent.add_field(name="Wind", value=str(wind), inline=True)
                    else:
                        return
            tempfilename = (f'{str(getlocation)}-{time.strftime("%Y%m%d-%H%M%S")}-radar.gif')
            radargiflocation = os.path.join("internalfiles", "temp", tempfilename)
            async with aiohttp.ClientSession() as session:
                async with session.get(radarimageurl) as resp:
                    if resp.status == 200:
                        gifout = await resp.read()
                        with open(radargiflocation, "wb") as giffile:
                            giffile.write(gifout)
                    else:
                        radarimagetemp = parsed_json['radar']['image_url']
                        radarimageurl1 = radarimagetemp.replace(f'%26api_key={self.bot.common.weatherapikey}'
                                                                f'%26time1={time.strftime("%H%M%S")}')
                        async with session.get(radarimageurl1) as resp1:
                            if resp1.status == 200:
                                gifout1 = await resp.read()
                                with open(radargiflocation, "wb") as giffile:
                                    giffile.write(gifout1)
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
        """Set your default weather"""
        if zipcode is None:
            raise self.bot.errors.DBotInternalError(f'You did not pass a zipcode when calling this command.\nExample: '
                                                    f'`{self.bot.common.discordbotcommandprefix}weatherset 98104`')
        elif zipcode.isdigit():
            sqlquery, tablename, querydata = await self.bot.sql.statement_upsert_weathertable(str(ctx.author.id), str(zipcode))
            async with self.bot.mysqlcon.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(sqlquery, querydata)
            return await ctx.send(f'Your default weather has been set\nIn the future, you can run '
                                  f'`{self.bot.common.discordbotcommandprefix}w` to retrieve your local weather')
        else:
            raise self.bot.errors.DBotInternalError("A proper zip code was not specified")

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
        """V naisu"""
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        return await ctx.send("Nice")

    @commands.command()
    async def notnice(self, ctx):
        """Un-nice"""
        if str('Direct Message') not in str(ctx.channel):
            await ctx.message.delete()
        return await ctx.send("That wasn't very nice of you.")

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Roll a dice, use NdN format"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            return await ctx.send('Format has to be in NdN!')
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(description='To decide between multiple choices', aliases=['decide'])
    async def choose(self, ctx, *args: str):
        """Choose between multiple options, split by 'or' """
        options = (" ".join(args)).split(" or ")
        return await ctx.send(random.choice(options))

    @commands.command(description='No fighting', aliases=['preciousfriends', 'friends', 'nofight', 'nofite'])
    async def fight(self, ctx):
        """No fiting aloud"""
        return await self._internalfile(ctx, "V63Hv.jpg")

    @commands.command(description='sadpanda', aliases=['panda', 'fuckyou', 'exhentai', 'why'])
    async def sadpanda(self, ctx):
        """Fuck you why is there a sad panda"""
        return await self._internalfile(ctx, "sadpanda.png")

    @commands.command(description='sleep')
    async def sleep(self, ctx):
        """Awoo sleep"""
        return await self._internalfile(ctx, "awoosleep.png")

    @commands.command(aliases=['404'])
    async def fourzerofour(self, ctx):
        """File not found"""
        return await self._internalfile(ctx, "404.gif")

    @commands.command()
    async def cat(self, ctx):
        """Retreives a random cat image from http://random.cat/"""
        fullurl = "http://random.cat/meow"
        async with aiohttp.ClientSession() as session:
            async with session.get(fullurl) as r:
                if r.status == 200:
                    parsed_json = await r.json()
                    await ctx.send(parsed_json['file'])
                else:
                    raise self.bot.errors.DBotExternalError("An error occurred when calling random.cat")

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, args):
        """Search Youtube for a video"""
        mesg = ''.join(args)
        query = mesg.replace(" ", "+")
        myurl = (f'https://www.googleapis.com/youtube/v3/search?q={query}&type=video&maxResults=5&part=snippet&'
                 f'safeSearch=None&key={self.bot.common.youtubeapikey}')
        publicurl = (f'https://www.youtube.com/results?search_query={query}')
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
                    raise self.bot.errors.DBotExternalError("An error occurred when calling Youtube")
        contentslist = ",".join(itemcontents)
        newurl = (f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails'
                  f'&key={self.bot.common.youtubeapikey}&id={contentslist}')
        async with aiohttp.ClientSession() as session:
            async with session.get(newurl) as r:
                if r.status == 200:
                    parsed_json = await r.json()
                    items = parsed_json['items']
                    for result in items:
                        templength = (str(result['contentDetails']['duration']).strip("PT"))
                        if "H" in templength:
                            newlength = (templength.replace("H", " hours,").replace("M", " minutes, ").replace("S", " seconds" ))
                        elif "H" not in templength:
                            newlength = (templength.replace("M", " minutes, ").replace("S", " seconds"))
                        elif "M" not in templength:
                            newlength = (templength.replace("S", " seconds"))
                        else:
                            newlength = templength
                        length.append(str(newlength))
        incnum = 1
        for t, u, v, f, l in zip(title, uploaded, videoid, fullurl, length):
            videoinfo = (f'\nLength: {l}\nURL: {f}')
            valuedata = (t + videoinfo)
            embed.add_field(name=(f'Video #{incnum}'), value=valuedata, inline=False)
            incnum += 1

        def checknumber(m):
            return (m.author == ctx.author) and (int(m.content) < int(len(contentslist))) and \
                   (m.channel.id == ctx.channel.id)

        botmessage = await ctx.send(embed=embed)
        questionmesg = await ctx.send("Please say the video number you want")
        numberresponse = await self.bot.wait_for('message', check=checknumber, timeout=30)
        newcontent = fullurl[(int(numberresponse.content) - 1)]
        await questionmesg.delete()
        await numberresponse.delete()
        await botmessage.edit(content=newcontent, embed=None)

    @commands.command()
    async def avatar(self, ctx, target: discord.User=None):
        """Gets a user's avatar"""
        if target is None:
            target = ctx.message.author
        embed = discord.Embed(title="Avatar")
        embed.set_image(url=target.avatar_url_as(format='png'))
        await ctx.send(embed=embed)

    @commands.command(aliases=['bigmoji', 'bemoji', 'big'])
    async def bigemoji(self, ctx, emoji):
        """Attempts to make an emoji bigger"""
        # discord.PartialReactionEmoji()
        try:
            newemoji = await commands.EmojiConverter().convert(ctx, emoji)
        except commands.BadArgument:
            return await ctx.send("This is not a custom emoji, I cannot biggify it.")
        if type(newemoji) == discord.Emoji:
            emoji_cdn = newemoji.url
            embed = discord.Embed(title=f':{newemoji.name}: \N{EM DASH} `{newemoji.id}`')
            embed.set_image(url=emoji_cdn)
            await ctx.send(embed=embed)

    @commands.command()
    async def awootime(self, ctx):
        """Lists the time until the next awoo"""
        nextawoo = await self.bot.misccache.get(key="awoowaittime")
        curtime = datetime.datetime.now()
        delta = (nextawoo - curtime).total_seconds()
        hours, remainder = divmod(int(delta), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        temptime = f'{hours}H{minutes}M{seconds}S'
        if "0H" in temptime:
            fmt = temptime.replace("0H", "").replace("M", " minutes, and ").replace("S", " seconds")
        elif "0H0M" in temptime:
            fmt = temptime.replace("0H", "").replace("0M ", "").replace("S", " seconds")
        else:
            fmt = temptime.replace("H", " hours, ").replace("M", " minutes, and ").replace("S", " seconds")
        mesg = f'The next awoo~ will occur in {fmt}'
        return await ctx.send(mesg)

    @commands.command(aliases=['xmyy', 'thatreallyxmyy'])
    async def thatreally(self, ctx):
        """That really x my y"""
        # variables lifted from https://github.com/Chewsterchew/API
        # on 2018-01-18
        word1 = ["bites", "highs", "burns", "ruins", "humids", "leans", "quiets", "traffics", "homes", "crashes",
                 "trumps", "backs", "salts", "xboxs", "closes", "records", "stops", "sevens", "pollutes", "kills",
                 "rents", "cleans", "extras", "boggles", "Taylor's", "snaps", "questions", "coffee's", "clicks", "pops",
                 "ticks", "maintains", "stars", "ties", "nys", "bills", "defends", "opens", "airs", "Americans",
                 "steals", "drinks", "yous", "businesses", "teleys", "invents", "thanks", "students", "computers",
                 "frees", "weathers", "vends", "severs", "allergies", "silences", "fires", "ambers", "pushes", "screws",
                 "smokes", "mrs", "reds", "consumes", "let's", "classes", "makes", "draws", "lights", "butters",
                 "celebrates", "drives", "pulls", "toxics", "finds", "waters", "pets", "lags", "types", "environments",
                 "grows", "builds", "moos", "tunas", "confuses", "classifies", "births", "fails", "breaks",
                 "emotionals", "booms", "calls", "taxes", "burgers", "4s", "gases", "potatoes", "pre owns", "sends",
                 "mows", "tickles", "lefts", "Saharas", "nals", "unites", "camps", "roses", "shuts down", "macs",
                 "apples", "cheeses", "turns", "flexes", "moves", "trucks", "necks", "swallows", "Harry's", "flushes",
                 "pays", "eyes", "cities", "increases", "trains", "cooks", "i's", "cringes", "unders", "folds",
                 "enters", "speeds", "roads", "spends", "tacos", "pumps", "hearts", "Willows", "reads", "suhs", "dogs",
                 "rocks", "cookies"]
        word2 = ["bites", "voices", "rubber", "jokes", "weather", "dabs", "time", "jams", "depots", "parties",
                 "country", "Clinton", "fires", "grasses", "one", "door", "videos", "signs", "elevens", "air", "mood",
                 "movie", "rooms", "roads", "brain cells", "points", "mind", "Swifts", "chats", "vibe", "motives",
                 "mugs", "pens", "buttons", "sanity", "tocks", "office", "scouts", "shoes", "keys", "nyes", "freedom",
                 "will to live", "force", "flags", "Gatorade", "sprite", "tubes", "service", "phones", "wheel", "yous",
                 "services", "labs", "tuition", "ford", "machines", "warnings", "alert", "phone", "extinguishers",
                 "dexterious", "driver", "detector", "jos", "cross", "M&Ms", "goes", "days", "pictures", "poles",
                 "biscuit", "75 years", "cars", "levers", "waters", "ways out", "burgers", "dogs", "minecraft",
                 "emojis", "sciences", "trees", "legos", "buildings", "cows", "fish", "conversation", "animals",
                 "certificates", "science classes", "hearts", "issues", "roasted", "horns", "friends", "kings", "Gs",
                 "birthdays", "stations", "chips", "vehicles", "texts", "lawns", "pickles", "lanes", "deserts", "genes",
                 "rocks", "states", "outs", "coffee", "reds", "computers", "books", "watches", "milk", "steaks",
                 "teens", "wheels", "muscles", "homes", "stops", "self", "tattoos", "food", "Potters", "toilets",
                 "brows", "limits", "toasts", "towers", "volume", "tracks", "wears", "bones", "oragamies", "zones",
                 "kills", "money", "bells", "ups", "radios", "ways", "Donald's", "springs", "elections", "walls",
                 "corn", "dudes", "filters", "rolls", "tongues"]
        sentence = (f'That really {random.choice(word1)} my {random.choice(word2)}.')
        await ctx.send(sentence)

    # def _wolf(self, query):
    #     """ Non async WolframAlpha lib function """
    #     wolframclient = wolframalpha.Client(self.bot.common.wolframapikey)
    #     wolframquery = (" ".join(query))
    #     results = wolframclient.query(wolframquery)
    #     return results
    #
    # @commands.command(aliases=['wolfram', 'alpha', 'calculate'])
    # async def wolframalpha(self, ctx, *, args):
    #     if not args:
    #         raise self.bot.errors.DBotInternalError("You've not entered anything for Wolfram to calculate!")
    #     await ctx.trigger_typing()
    #     result = await self.bot.loop.run_in_executor(None, self._wolf, args)
    #     if result is not None:
    #         pass
    #         # do things with results
    #         # result.pods, result.info, result.assumptions, result.warnings, result.results
    #         # await ctx.send(result)
    #     else:
    #         raise self.bot.errors.DBotExternalError(f"Sorry, I couldn't calculate `{args}`.")


class EtcOnMessage:
    def __init__(self, bot):
        self.bot = bot
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Addon "{self.__class__.__name__}" loaded')

    async def on_message(self, message):
        if (message.content.startswith(self.bot.common.discordbotcommandprefix)) or \
                (str(message.author.id) == str(self.bot.common.botdiscordid)) or (message.author.bot is True):
            return
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
