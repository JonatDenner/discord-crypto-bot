import discord
import pandas as pd
import requests
from discord.ext import commands

key = open('.login', 'r').read()
api = open('.api', 'r').read()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='$',  intents=intents,  case_insensitive='true')

df = pd.read_csv('coins.csv', delimiter=',')

coins = [[row[col] for col in df.columns] for row in df.to_dict('records')]

@bot.event
async def on_ready():
	print('\n------------------------------')
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------------------------------')
	await bot.change_presence(activity=discord.Game(name='$help for a list of available commands.'))

@bot.command()
async def v(ctx, crypto:str):
	'''Display given crypto value'''
	try:
		crypto = crypto.upper()
		match = [s for s in coins if crypto == s[1]]
		if match:
			for x in match:
				r=requests.get("https://api.coinranking.com/v2/coin/" + x[0], headers={"x-access-token":api})
				data = r.json()
				if not data['data']['coin']['supply']['confirmed']:
					await ctx.send(data['data']['coin']['name'] + " supply is currently unconfirmed, so there is no price to display.")
				elif str(data['data']['coin']['price']) == "0":
					await ctx.send(data['data']['coin']['name'] + " is currently worth zero USD.")
				else:
					if float(data['data']['coin']['price']) > 10000:
						output = data['data']['coin']['name'] + ': $' + (data['data']['coin']['price'])[:8] + ' | 24 Hour Change: ' + (data['data']['coin']['change'])[:6] + '%'
					elif float(data['data']['coin']['price']) > 0.00001:
						output = data['data']['coin']['name'] + ': $' + (data['data']['coin']['price'])[:10] + ' | 24 Hour Change: ' + (data['data']['coin']['change'])[:6] + '%'
					else:
						output = data['data']['coin']['name'] + ': $' + data['data']['coin']['price'] + ' | 24 Hour Change: ' + (data['data']['coin']['change'])[:6] + '%'

					await ctx.send(output)
					
		else:
			await ctx.send("Crypto doesn't exist.")
			
	except Exception as err:
		await ctx.send("An error occurred...")
		print(err)

bot.run(key)