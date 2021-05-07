# discord-crypto-bot
A simple bot for discord that gets up to date crypto prices from https://coinranking.com/

# Requirements
* Python 3
* Python Packages:
  * Discord Py (https://discordpy.readthedocs.io/en/stable/intro.html)
  * Requests
  * Pandas

# Installation and Setup
* Go to https://coinranking.com/page/key-generator and create a new API key and save it for later(free version is limited to 200k uses per month)
* Go to https://discord.com/developers/applications and create a new bot, saving the bot token for later
* Download the repository
```bash
git clone https://github.com/JonatDenner/discord-crypto-bot.git
```
* Open the downloaded folder and create two files
  * ".login", where you will put the bot token
  * ".api", where you will put your coinranking api key
* Set the bot prefix to whatever you want it to be by changing the $ on line 11 of bot.py
```python
bot = commands.Bot(command_prefix='$',  intents=intents,  case_insensitive='true')
```
* Change the command to whatever you want it to be by changing the v on line 27 of bot.py
```python
async def v(ctx, crypto:str):
```

# Usage
Once the setup is complete, you just need to run bot.py file with Python 3. As long as the program is running the bot will be up. Then, create an invite link on https://discord.com/developers/applications and add it to your server.
