## Monroe County NY Emergency Services Bot
#### Created by Aidan LeMay, https://aidanlemay.com/

***

### Setting Up the Project
*This Guide assumes you are operating on a standard Linux installation (written using Ubuntu 20.04 Server), have Sudo privelages, and have Python3.8.10 (Minimum!) installed.*

* Clone the project into the directory of your choice and `cd` into it
* Activate or install your Virtual Environment if needed
* Run `pip install -r requirements.txt`

-- THEN --

* Create a bot on the Discord Developer Portal using [This Tutorial](https://www.ionos.com/digitalguide/server/know-how/creating-discord-bot/)
* `nano storage.py` and add a variable called TOKEN="your-token-here"
* Add your bot to your server with `https://discordapp.com/api/oauth2/authorize?client_id=<CLIENT_ID_HERE>&permissions=8&scope=bot`
* `python3 bot.py` to run your bot

-- To Run Your Bot Headless / In The Background --

* Install NPM (Node.JS Package Manager)
* `sudo npm install pm2 -g`
* `pm2 ls`
* `pm2 start bot.py --watch` (Omit `--watch` if you don't want your project auto-served when the project files are changed)

### Command Definitions - Meta Commands
* `/help`: Displays Help command with these definitions
* `/pogle`: Don't worry about it
* `/ping`: Display API latency

### Command Definitions - RSS Feed
* `/m911 X#` [X#: Optional Quantity]: Returns X# of Monroe County 911 Events (Default 1) from https://www.monroecounty.gov/incidents911.rss with all 'Parking Incident's filtered out
* `/r911 X#` [X#: Optional Quantity]: Returns X# of Rochester Area 911 Events (Default 1) from https://www.monroecounty.gov/incidents911.rss with all 'Parking Incident's filtered out
* `/h911 X#` [X#: Optional Quantity]: Returns X# of Henrietta Area 911 Events (Default 1) from https://www.monroecounty.gov/incidents911.rss with all 'Parking Incident's filtered out
* `/a911 X#` [X#: Optional Quantity]: Returns X# of Monroe County 911 Events (Default 1) from https://www.monroecounty.gov/incidents911.rss unfiltered

### Command Definitions - ClearCut
* `/ems [keyword]`: Returns recent MC EMS ClearCut transcripts with optional matching keywords
* `/fire [keyword]`: Returns recent MC Fire ClearCut transcripts with optional matching keywords
* `/hfd [keyword]`: Returns recent Henrietta Fire ClearCut transcripts with optional matching keywords
* `/rit`: Returns recent RIT Fire and EMS ClearCut transcripts
* `/rite`: Returns recent RIT EMS ClearCut transcripts
* `/ritf`: Returns recent RIT Fire ClearCut transcripts
* `/rita`: Returns recent RIT Ambulance ClearCut transcripts
* `/ritp [keyword]`: Returns recent RIT Public Safety ClearCut transcripts with optional matching keywords
* `/ops [keyword]`: Returns recent RIT Campus Operations ClearCut transcripts with optional matching keywords
* `/tgs [keyword]`: Returns MONCON Talkgroups with optional matching keywords
* `/tg [tg] [keyword]`: Returns recent ClearCut transcripts from specified TG with optional matching keywords

