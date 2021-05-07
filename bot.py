import discord
import pandas as pd
import requests
from discord.ext import commands

#gets the bot token and coinranking api key
key = open('.login', 'r').read()
api = open('.api', 'r').read()

intents = discord.Intents.default()

#set prefix and other rules, full list of attributes at https://discordpy.readthedocs.io/en/stable/ext/commands/api.html?#bot
bot = commands.Bot(command_prefix='$',  intents=intents,  case_insensitive='true')

#opens the coins csv as a pandas dataframe
df = pd.read_csv('coins.csv', delimiter=',')

#sends the dataframe to a 2*x value list
coins = [[row[col] for col in df.columns] for row in df.to_dict('records')]

#actions to do when the bot successfully logs in
@bot.event
async def on_ready():
	print('\n------------------------------')
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------------------------------')
	await bot.change_presence(activity=discord.Game(name='$help for a list of available commands.'))

#defines one bot command
@bot.command()
async def v(ctx, crypto:str):
	'''Display given crypto value\nUsage: .v [crypto symbol], e.g. $v btc\nCase insensitive'''
	try:
		crypto = crypto.upper()
		match = [s for s in coins if crypto == s[1]]
		if match:
			#some cryptocurrencies share the same symbol, such as SOL, requiring loops
			for x in match:
				r=requests.get("https://api.coinranking.com/v2/coin/" + x[0], headers={"x-access-token":api})
				data = r.json()
				#firs catches unconfirmed coins, second catches dead/inactive ones
				if not data['data']['coin']['supply']['confirmed']:
					await ctx.send(data['data']['coin']['name'] + " supply is currently unconfirmed, so there is no price to display.")
				elif str(data['data']['coin']['price']) == "0":
					await ctx.send(data['data']['coin']['name'] + " is currently worth zero USD.")
				else:
					#displays a certain amount of digits depending on coing value, to avoid having large numbers every time
					if float(data['data']['coin']['price']) > 10000:
						output = data['data']['coin']['name'] + ': $' + (data['data']['coin']['price'])[:8] + ' | 24 Hour Change: ' + (data['data']['coin']['change'])[:6] + '%'
					elif float(data['data']['coin']['price']) > 0.00001:
						output = data['data']['coin']['name'] + ': $' + (data['data']['coin']['price'])[:10] + ' | 24 Hour Change: ' + (data['data']['coin']['change'])[:6] + '%'
					else:
						output = data['data']['coin']['name'] + ': $' + data['data']['coin']['price'] + ' | 24 Hour Change: ' + (data['data']['coin']['change'])[:6] + '%'

					await ctx.send(output)
					
		else:
			#if the symbol isn't in the csv file it most likely doesn't exist
			await ctx.send("Crypto doesn't exist.")

	#for other unknown errors
	except Exception as err:
		await ctx.send("An error occurred...")
		print(err)
#start the bot
bot.run(key)
