import time
from interactions import Client, Intents, listen, slash_command, SlashContext, OptionType, slash_option, Embed
from datetime import datetime, timedelta
import storage
import requests
from requests_html import HTMLSession

ts_now = int(time.time())

ts_24 = ts_now - (24 * 60 * 60)

monems = "https://clearcutradio.app/api/v1/calls?system=us-ny-monroe&talkgroup=1077" + "&before_ts=" + str(ts_now) + "&after_ts=" + str(ts_24)
monfire = "https://clearcutradio.app/api/v1/calls?system=us-ny-monroe&talkgroup=1811" + "&before_ts=" + str(ts_now) + "&after_ts=" + str(ts_24)
henfire = "https://clearcutradio.app/api/v1/calls?system=us-ny-monroe&talkgroup=1654" + "&before_ts=" + str(ts_now) + "&after_ts=" + str(ts_24)
ritpub = "https://clearcutradio.app/api/v1/calls?system=us-ny-monroe&talkgroup=3070" + "&before_ts=" + str(ts_now) + "&after_ts=" + str(ts_24)
ritamb = "https://clearcutradio.app/api/v1/calls?system=us-ny-monroe&talkgroup=1894" + "&before_ts=" + str(ts_now) + "&after_ts=" + str(ts_24)
ritops = "https://clearcutradio.app/api/v1/calls?system=very-bad&talkgroup=100" + "&before_ts=" + str(ts_now) + "&after_ts=" + str(ts_24)

# ------------------ ClearCut Functions ------------------

def get_source_clearcut(url):
    try:
        data = requests.get(url=url)
        response = data.json()
        return response

    except requests.exceptions.RequestException as e:
        print(e)

# ------------------ End ClearCut Functions ------------------

# ------------------ RSS Functions ------------------

def get_source():
    try:
        session = HTMLSession()
        response = session.get("https://www.monroecounty.gov/incidents911.rss")
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_feed_monroe():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            if not title.startswith("PARKING INCIDENT"):
                description = item.find('description', first=True).text

                pubdate = item.find('pubDate', first=True).text

                out.append(title + " | " + description + " | " + pubdate)

    return out

def get_feed_roc():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            if not title.startswith("PARKING INCIDENT"):

                guid = item.find('guid', first=True).text

                if "ROCE" in guid:

                    description = item.find('description', first=True).text

                    pubdate = item.find('pubDate', first=True).text

                    out.append(title + " | " + description + " | " + pubdate)

    return out

def get_feed_hen():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            if not title.startswith("PARKING INCIDENT"):

                guid = item.find('guid', first=True).text

                if "HENE" in guid:

                    description = item.find('description', first=True).text

                    pubdate = item.find('pubDate', first=True).text

                    out.append(title + " | " + description + " | " + pubdate)

    return out

def get_unfiltered():
    response = get_source()

    out = list()

    with response as r:
        items = r.html.find("item", first=False)

        for item in items:        

            title = item.find('title', first=True).text

            description = item.find('description', first=True).text

            pubdate = item.find('pubDate', first=True).text

            out.append(title + " | " + description + " | " + pubdate)

    return out

# ------------------ End RSS Functions ------------------

bot = Client(intents=Intents.DEFAULT, token=storage.TOKEN)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine

@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print('Logged In!')
    print('------')

# ------------------ Help / Meta Commands ------------------

@slash_command(name="help", description="Bot Help!")
async def help(ctx: SlashContext):
    await ctx.send("""
    MC Emergency Services Discord Bot Help!
    \n\nCreated by Aidan LeMay using Discord.py
    \nhttps://github.com/aidan-lemay/MC-Emergency-Bot
    \n\nVisit the creator here! https://aidanlemay.com/
    """)

    await ctx.send("""
    ```\n\n/helpme: Display this help window
    \n/tg [TG ID] [Keyword (Optional)]: Returns calls from the specified TG with optional keywords (Case Sensitive) from the last 24 hours
    \n/tgs [X String: Optional Keyword Matching String]: Returns list of active talkgroups with optional keywords
    \n/rit: Returns both fire and ems calls from last 24 hours relating to RIT
    \n/rita [X String: Optional Keyword Matching String]: Returns calls from the last 24 hours from TG 1894
    \n/ems [X String: Optional Keyword Matching String]: Returns X# of Calls from TG 1077 (MC EMS Dispatch) with optional keywords (Case Sensitive)
    \n/fire [X String: Optional Keyword Matching String]: Returns X# of Calls from TG 1811 (MC FD Dispatch) with optional keywords (Case Sensitive)
    \n/rite: Returns all calls within the last 24 hours from TG 1077 that contain "RIT", "6359", or "DEFIB 63"
    \n/hfd [X String: Optional Keyword Matching String]: Returns X# of Calls from TG 1654 (HFD Dispatch) with optional keywords (Case Sensitive)
    \n/ritf: Returns all calls within the last 24 hours from TG 1654 that contain "RIT"
    \n/ops [X String: Optional Keyword Matching String]: Returns X# of Calls from RIT Campus Operations with optional keywords (Case Sensitive)```
    """)

    await ctx.send("""
    ```\n/m911 [X#: Optional Quantity]: Returns X# of Monroe County 911 Events from https://www.monroecounty.gov/incidents911.rss with all 'PARKING INCIDENT's filtered out
    \n/h911 [X#: Optional Quantity]: Returns X# of Henrietta area 911 Events from https://www.monroecounty.gov/incidents911.rss with all 'PARKING INCIDENT's filtered out
    \n/r911 [X#: Optional Quantity]: Returns X# of Rochester area 911 Events from https://www.monroecounty.gov/incidents911.rss with all 'PARKING INCIDENT's filtered out
    \n/a911 [X#: Optional Quantity]: Returns X# of Monroe County 911 Events from https://www.monroecounty.gov/incidents911.rss with no data filtered out
    \n/pogle or /polge: fun```
    """)

@slash_command(name="pogle", description="polge")
async def pogle(ctx: SlashContext):
    embed = Embed(color=0x06275c, description="pogle")
    embed.add_image("https://aidanlemay.com/pogle.jpg")
    await ctx.send(embed=embed)

@slash_command(name="ping", description="Get API Latency")
async def ping(ctx: SlashContext):
    await ctx.send(f"Command to Bot to API Latency: ({float(bot.latency)}ms)")
# ------------------ End Help / Meta Commands ------------------

# ------------------ RSS Commands ------------------

@slash_command(name="m911", description="Filtered Monroe County 911 Events")
@slash_option(
    name="events",
    description="Number of Events to Return",
    required=False,
    opt_type=OptionType.INTEGER
)
async def m911(ctx: SlashContext, events: int = 20):
    if events == None:
        events = 20

    df = get_feed_monroe()

    fSize = len(df)

    if fSize == 0:
        message = "```No Monroe County Events Found```"

    else:
        if events > fSize:
            events = fSize
        elif events < 1:
            events = 1

        message = "```\nMonroe County 911 Events:\n"

        # for i in df:
        j = 0
        while j < events:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message = message[ 0 : 1997 ]
        message += "```"

    await ctx.send(message)

@slash_command(name="r911", description="Filtered Rochester Area 911 Events")
@slash_option(
    name="events",
    description="Number of Events to Return",
    required=False,
    opt_type=OptionType.INTEGER
)
async def r911(ctx: SlashContext, events: int = 20):
    if events == None:
        events = 1
    df = get_feed_roc()

    fSize = len(df)

    if fSize == 0:
        message = "```No Rochester Area Events Found```"

    else:
        if events > fSize:
            events = fSize
        elif events < 1:
            events = 1

        message = "```\nRochester Area 911 Events:\n"

        # for i in df:
        j = 0
        while j < events:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message = message[ 0 : 1997 ]
        message += "```" 

    await ctx.send(message)

@slash_command(name="h911", description="Filtered Henrietta Area 911 Events")
@slash_option(
    name="events",
    description="Number of Events to Return",
    required=False,
    opt_type=OptionType.INTEGER
)
async def h911(ctx: SlashContext, events: int = 20):
    if events == None:
        events = 1
    df = get_feed_hen()

    fSize = len(df)

    if fSize == 0:
        message = "```No Henrietta Area Events Found```"

    else:
        if events > fSize:
            events = fSize
        elif events < 1:
            events = 1

        message = "```\nHenrietta Area 911 Events:\n"

        # for i in df:
        j = 0
        while j < events:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message = message[ 0 : 1997 ]
        message += "```"    

    await ctx.send(message)

@slash_command(name="a911", description="Unfiltered Monroe County 911 Events")
@slash_option(
    name="events",
    description="Number of Events to Return",
    required=False,
    opt_type=OptionType.INTEGER
)
async def a911(ctx: SlashContext, events: int = 20):
    if events == None:
        events = 1
    df = get_unfiltered()

    fSize = len(df)

    if fSize == 0:
        message = "```No Monroe County Events Found```"

    else:
        if events > fSize:
            events = fSize
        elif events < 1:
            events = 1

        message = "```ALL Monroe County 911 Events:\n"

        # for i in df:
        j = 0
        while j < events:
            message += "-> " + df[j] + "\n\n"
            j+=1

        message = message[ 0 : 1997 ]
        message += "```"   

    await ctx.send(message)

# ------------------ End RSS Commands ------------------

# ------------------ ClearCut Commands ------------------
match = ["RIT", "rit", "R I T", "r i t", "6359", "6 3 5 9", "6-3-5-9", "Defib 63", "DEFIB 63", "defib 63", "Defib 6-3", "DEFIB 6-3", "defib 6-3", "601", "6 0 1", "Andrews", "Andrews Memorial", "Andrews Memorial Drive", "Lomb", "Lomb Memorial", "Lomb Memorial Drive", "Lowenthall", "Perkins", "Riverknoll", "University Commons", "John", "John Street", "Wiltsie", "Greenleaf", "Greenleaf Court", "Gleason", "Reynolds", "Kimball", "Farnum", "Charters"]

def matching(sentence, words):
    # Convert both the sentence and words to lowercase for case-insensitive comparison
    lowercase_sentence = sentence.lower()
    lowercase_words = [word.lower() for word in words]

    # Check if any word in the array is present in the sentence
    return any(word in lowercase_sentence for word in lowercase_words)

@slash_command(name="ems", description="ClearCut EMS Transcripts")
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Messages With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def ems(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut(monems)
    message = "```Monroe County EMS Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
        
    message = message[ 0 : 1997 ]

    message += "```"

    await ctx.send(message)

@slash_command(name="fire", description="ClearCut Monroe County Fire Transcripts")
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Messages With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def fire(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut(monfire)
    message = "```Monroe County Fire Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
        
    message = message[ 0 : 1997 ]

    message += "```"

    await ctx.send(message)

@slash_command(name="hfd", description="ClearCut Henrietta Fire Transcripts")
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Messages With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def hfd(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut(henfire)
    message = "```Henrietta Fire Department Call Transcripts:\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
        
    message = message[ 0 : 1997 ]

    message += "```"

    await ctx.send(message)

@slash_command(name="rit", description="ClearCut RIT Related County Transcripts")
async def rit(ctx: SlashContext):
    response = get_source_clearcut(monems)
    message = "RIT EMS Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            text = data['transcript']['text']

            # Get all calls within num range with matching keywords
            if (matching(text, match)):
                message += str(timestamp) + " | " + text + "\n\n"

    response = get_source_clearcut(henfire)
    message += "\n\nRIT Fire Related Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            text = data['transcript']['text']

            # Get all calls within num range with matching keywords
            if (matching(text, match)):
                message += str(timestamp) + " | " + text + "\n\n"

    n = 1994 # chunk length
    chunks = [message[i:i+n] for i in range(0, len(message), n)]

    for c in chunks:
        await ctx.send("```" + c + "```")

@slash_command(name="rite", description="ClearCut RIT EMS Transcripts")
async def rite(ctx: SlashContext):
    response = get_source_clearcut(monems)
    message = "```RIT EMS Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            text = data['transcript']['text']

            # Get all calls within num range with matching keywords
            if (matching(text, match)):
                message += str(timestamp) + " | " + text + "\n\n"

    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@slash_command(name="ritf", description="ClearCut RIT Fire Transcripts")
async def ritf(ctx: SlashContext):
    response = get_source_clearcut(henfire)
    message = "```RIT Fire Related Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            text = data['transcript']['text']

            # Get all calls within num range with matching keywords
            if (matching(text, match)):
                message += str(timestamp) + " | " + text + "\n\n"

    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@slash_command(name="rita", description="ClearCut RIT Ambulance Transcripts")
async def rita(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut(ritamb)
    message = "```RIT Ambulance Call Transcripts:\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
        
    message = message[ 0 : 1997 ]

    message += "```"

    await ctx.send(message)

@slash_command(name="ritp", description="ClearCut RIT Public Safety Transcripts")
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Messages With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def ritp(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut(ritpub)
    message = "```RIT Public Safety Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            
            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
    
    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@slash_command(name="ops", description="ClearCut RIT Campus Operations Transcripts")
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Messages With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def ops(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut(ritops)
    message = "```RIT Campus Operations Call Transcripts:\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            
            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
    
    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@slash_command(name="tgs", description="ClearCut Talkgroup List")
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Talkgroups With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def tgs(ctx: SlashContext, keyword: str = ""):
    response = get_source_clearcut("https://clearcutradio.app/api/v1/talkgroups?system=us-ny-monroe")
    message = "```List of Active Monroe County Talkgroups:\n------------------------\n\n"

    for data in response:
        tg = data['id']
        category = data['category']
        name = data['name']
        transcribed = data['transcribe']

        if (keyword is not None):
            if (keyword in category or keyword in name):
                message += "TGID: " + str(tg) + " | Name: " + name + " | Transcribed: " + str(transcribed) + "\n\n"
        elif (keyword is None and transcribed == True):
            message += "TGID: " + str(tg) + " | Name: " + name + " | Transcribed: " + str(transcribed) + "\n\n"

    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

@slash_command(name="tg", description="ClearCut Custom TG Transcripts")
@slash_option(
    name="talkgroup",
    description="Talkgroup ID",
    required=True,
    opt_type=OptionType.INTEGER
)
@slash_option(
    name="keyword",
    description="(Case Sensitive) Return Messages With Keyword",
    required=False,
    opt_type=OptionType.STRING
)
async def tg(ctx: SlashContext, talkgroup: int, keyword: str = ""):
    response = get_source_clearcut("https://clearcutradio.app/api/v1/calls?system=us-ny-monroe&talkgroup=" + str(talkgroup).strip())
    message = "```Custom Call Data from TG" + str(talkgroup).strip() + ":\n\n"

    for data in response:
        if (data is not None and data['transcript'] is not None and data['transcript']['text'] is not None):
            curtime = datetime.today() - timedelta(hours = 4)
            timestamp = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            calltime = datetime.fromtimestamp(data['startTime']) - timedelta(hours = 4)
            mintime = curtime - timedelta(hours = 24)
            text = data['transcript']['text']

            if (keyword is not None):
                # Get all calls within num range with matching keywords
                if (calltime > mintime and keyword in text):
                    message += str(timestamp) + " | " + text + "\n\n"
            else:
                # Get all calls within num range
                if (calltime > mintime):
                    message += str(timestamp) + " | " + text + "\n\n"
    
    message = message[ 0 : 1997 ]
    message += "```"

    await ctx.send(message)

# ------------------ End ClearCut Commands ------------------

bot.start()