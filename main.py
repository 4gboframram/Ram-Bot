########################################
#Original Author: RamRam #0001
########################################

import discord
import os
import requests
import re
import random
import asyncio
from dotenv import load_dotenv, find_dotenv
from replit import db 
TOKEN=load_dotenv(find_dotenv())
from discord.ext import commands
from discord.ext.commands import has_permissions,MissingPermissions
import numpy as np

os.system("pip install waifulabs") #replit likes to uninstall things installed with pip whenever it has to do package shit, so we have to install waifulabs again every time the bot is up
import waifulabs

class NotBotChannel(Exception): #exception used for when a command is not not used in a bot channel
	pass

spamlogger={} #logs how many messages a user has sent in the past minute

#randomized embed stuff
emoticons=["-_-", ":(", "o.o", "O.o", "^-^", "^.^", "( ͡° ͜ʖ ͡°)", r"¯\_(ツ)_/¯", "UwU", "OwO", ":{", ":}", ":\\", ":P"]
success=["Why do I even bother?", "Why am I still doing this?", "Hah!", "Barusu, your pride is disdainful."]
spam_logger={}

#virtualram functions for the different actions
killfunction=lambda x: -10*np.arctan(x/4)/(7*np.pi)+1
insultfunction=lambda x: -10*np.arctan(x/10)/(7*np.pi)+1
headpatfunction=lambda x: 4.5*np.arctan(x/40)/np.pi +0.75
complimentfunction=lambda x: 3.1*np.arctan(x/40)/np.pi +0.95
ram_encounters=["You are shopping at the market. It is a mildly warm summer day, and your eye catches a rather rare sight: Ram getting groceries for the Mathers estate instead of the usual Rem. She stands out among the crowd: the rays sunlight reflecting off her body in a almost beautiful way, and her hair rustling slowly in the gentle breeze. However, she caught your eyes for too long and she walks over to you, clearly mad.", ]

#regex shit
glare=open('glare.txt','r').read().splitlines()
def getGlarelist(glarelist):
	pattern=''
	for name in glarelist:
		pattern+=r'((^|\b)(?i)('+ name+r')(\b|$|[?.!,"]))|'
	return pattern[:-1] #remove annoying pipe-chan at the end of the final expression

Pattern=re.compile(getGlarelist(glare))

#getting server-based prefixes
def get_prefix(client, message):
	data=db['server '+str(message.guild.id)]
	try:
		return data[0] 
	except KeyError:
		db['server '+str(message.guild.id)]=['^ram ']
		return db['server '+str(message.guild.id)][0]

def disablecheck(ctx): #check for if the channel is a bot channel
	data=db["server "+str(ctx.guild.id)]
	if len(data)<2:
		for channel in ctx.guild.text_channels:
			data.append(channel.id)
	elif not ctx.channel.id in db["server "+str(ctx.guild.id)]:
			print("not a bot channel")
			raise NotBotChannel
			return
	else: pass

bot = commands.Bot(command_prefix=get_prefix,help_command=None)

@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Barusu make a fool of himself"))

@bot.event
async def on_guild_remove(guild):
	del db["server "+str(guild.id)] #free up database space when the bot is removed from a server

@bot.command()
async def help(ctx): #the most messy help command ever
	prefix=db[f"server {ctx.guild.id}"][0]
	embed=discord.Embed(title="Command Help", color=0xff99e4)
	embed.set_author(name="Ram Bot", icon_url="https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048")
	embed.add_field(name="Commands", value=f"{prefix}hah\nGo into a voice channel and use it to find out what it does. *Hah!*\n\n{prefix}clear [amount], *reason\n Clears [amount] amount of messages from the channel for optional [reason]\n\n{prefix}distort [attached image]\nDistorts the attached image.\n\n{prefix}virtualram\nGive Ram love. Or try to kill her. Your choice.\n\n{prefix}waifu\ngenerates a waifu with waifulabs api\n\n\nA **bot channel***: For this bot, a bot channel is a channel where every command can be used. Moderation commands can be used in any channel no matter if it is a bot channel or not. All other commands can only be used in bot channels\n\n {prefix}addbotchannel\nAdds the current channel to the list of bot channels\n\n{prefix}removebotchannel\Removes the current channel from the list of bot channels\n\n{prefix}allbotchannel\nAdds all channels in the server to the list of bot channels\n\n{prefix}removeallbotchannels\nRemoves all channels from the list of botchannels\n\n", inline=False)
	await ctx.send(embed=embed)

@bot.command()
async def hah(ctx):
	guild = ctx.guild
	channel =ctx.author.voice.channel
	await channel.connect()
	voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
	audio_source = discord.FFmpegPCMAudio('hah.mp3')
	if not voice_client.is_playing():
		voice_client.play(audio_source, after=None)
	await asyncio.sleep(3) 
	await ctx.voice_client.disconnect()

from distort import randdistort
from deskew import deskew
@bot.command()
async def distort(ctx):
	try:
		url=ctx.message.attachments[0].url
		page = requests.get(url)

		f_ext = os.path.splitext(url)[-1]
		f_name = 'img{}'.format(f_ext)
		with open(f_name, 'wb') as f:
			f.write(page.content)
		randdistort(f'img{f_ext}')
		deskew(deskew('name.png')) 
		await ctx.send(file=discord.File('skew_corrected.png'))
	except NotBotChannel: pass

@bot.command()
@has_permissions(manage_messages=True)
async def clear(ctx,amount=5,**reason):
	await ctx.channel.purge(limit=amount+1)
	embed=discord.Embed(title=f"Cleared! {random.choice(emoticons)}", color=0xfd6d98)
	embed.set_author(name=f"Ram Bot {random.choice(emoticons)}", url="https://www.youtube.com/watch?v=hKNnuytioGA", icon_url="https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048")
	embed.add_field(name=f"Cleared {amount} messages from {ctx.channel.name}", value=f"{random.choice(success)} {random.choice(emoticons)}", inline=False)
	embed.add_field(name="This action was performed for the following reason:", value=f"{reason}", inline=False)
	botMessage=await ctx.send(embed=embed)
	await asyncio.sleep(10)
	await botMessage.delete()

@bot.command()
async def xp(ctx):
	try:
		disablecheck(ctx)
		userxp=db[str(ctx.author.id)]
		embed=discord.Embed(title='Level?',description=f"{ctx.author.mention}, you are level {userxp[1]}.\n You are {100+10*userxp[1]**2-userxp[0]} xp away from leveling up to level {userxp[1]+1}",colour=0xcc00ff)
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)
	except NotBotChannel: pass


@bot.command(name='rank')
async def rank(ctx):
	try:
		disablecheck()
		lists=[]
		for key in db.keys():
			lists.append(db[key])
		if key.startswith("server"):
			lists.remove(db[key])
		lists.sort(key=lambda k: (k[1], -k[0]),reverse=True)
		rank=lists.index(db[str(ctx.author.id)])
			
		embed=discord.Embed(title='Rank?',description=f"{ctx.author.mention}, you are in place {rank+1} of {len(lists)} people",colour=0xcc00ff)
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)
	except NotBotChannel: pass

#error handling
@bot.event
async def on_command_error(ctx, error):
		# if command has local error handler, return
		if hasattr(ctx.command, 'on_error'):
			return

		# get the original exception
		error = getattr(error, 'original', error)

		if isinstance(error, commands.CommandNotFound):
			embed = discord.Embed(title="You messed up",description="Command does not exist, you baka.\n ", colour=0xff0000)
			embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
			embed.add_field(name='Technical details for the nobody that cares', value='Error: `commands.CommandNotFound`')
			await ctx.send(embed=embed)
			return

		if isinstance(error, commands.BotMissingPermissions):
			missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
			if len(missing) > 2:
				fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
			else:
				fmt = ' and '.join(missing)
			_message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
			embed = discord.Embed(title="You or the moderators messed up",description=_message, colour=0xff0000)
			embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
			embed.add_field(name='Technical details for the nobody that cares:', value='Error: `commands.BotMissingPermissions`')
			await ctx.send(embed=embed)
			return

		if isinstance(error, commands.DisabledCommand):
			await ctx.send('This command has been disabled.')
			return

		if isinstance(error, commands.MissingPermissions):
			missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
			if len(missing) > 2:
				fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
			else:
				fmt = ' and '.join(missing)
			_message = 'You need the **{}** permission(s) to use this command, you baka.'.format(fmt)
			embed = discord.Embed(title="You or the moderators messed up",description=_message, colour=0xff0000)
			embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
			embed.add_field(name='Technical details for the nobody that cares:', value='Error: `commands.MissingPermissions`')
			await ctx.send(embed=embed)
			return

		if isinstance(error, commands.NoPrivateMessage):
			try:
				await ctx.author.send('This command cannot be used in direct messages.')
			except discord.Forbidden:
				pass
			return

		if isinstance(error, commands.CheckFailure):
			embed = discord.Embed(title="You or the moderators messed up",description="You do not have permission to use this command.", colour=0xff0000)
			embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
			embed.add_field(name='Technical details for the nobody that cares:', value='Error: `commands.CheckFailure`')
			await ctx.send(embed=embed)
			return 



@bot.command()
async def virtualram(ctx):
	
	try:
		disablecheck(ctx)
		embed=discord.Embed(title="A wild Ram appeared!", description=f"{random.choice(ram_encounters)}{ctx.author.mention}, You have 4 choices of action\n 1. Tell her she's cute.\n 2. Tell her she's a bitch.\n 3. Pat her head.\n 4. Draw your sword and attempt to kill her", colour=0xffbbdd)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
		message= await ctx.send(embed=embed)
		await message.add_reaction('1️⃣')
		await message.add_reaction('2️⃣')
		await message.add_reaction('3️⃣')
		await message.add_reaction('4️⃣')
		def check(reaction, user):
			return user == ctx.author and str(reaction.emoji) in ['1️⃣','2️⃣','3️⃣','4️⃣']
		try:
			userid=str(ctx.author.id)
			reaction, user=await bot.wait_for("reaction_add", timeout=10.0, check=check)
			print('worked?')
			if str(reaction.emoji)=='1️⃣':
				embed=discord.Embed()
				if db[userid][2]>1:
					print('1')
					embed=discord.Embed(title="Ram's Reaction", description=f"{ctx.author.mention}, Ram seems to have enjoyed the compliment.", colour=0xffbbdd)
					embed.set_image(url="https://static.wikia.nocookie.net/rezero/images/4/47/Ram_-_Re_Zero_Anime_BD_-_7.png")
					db[userid][2]+=1
					print(db[userid][2])
					await ctx.send(embed=embed)
					return
				else:
					print('1')
					embed=discord.Embed(title="Ram's Reaction", description=f"{ctx.author.mention}, Ram tells you to keep your perverted desires away from her.", colour=0xffbbdd)
					embed.set_image(url="https://static.wikia.nocookie.net/rezero/images/1/13/Ram_-_Re_Zero_Anime_BD_-_1.png")
					await ctx.send(embed=embed)
					db[userid][2]+=1
					print(db[userid][2])
					
			if str(reaction.emoji)=='2️⃣':
				print('2')
				embed=discord.Embed(title="Ram's Reaction", description=f"{ctx.author.mention}, Ram glares at you, confused why you would say such a thing.", colour=0xffbbdd)
				embed.set_image(url="https://static.wikia.nocookie.net/rezero/images/e/ee/Ram_-_Re_Zero_Anime_BD_-_6.png")
				db[userid][3]+=1
				print(db[userid][3])
			if str(reaction.emoji)=='3️⃣':
				embed=discord.Embed()
				if db[userid][4]>6:
					print('3')
					embed=discord.Embed(title="Ram's Reaction", description=f"{ctx.author.mention}, Ram seems to really enjoy the headpats.", colour=0xffbbdd)
					embed.set_image(url="https://cdn.discordapp.com/attachments/800920762131152957/831686121754460180/89058267_p0_master1200.jpg")
					db[userid][4]+=1
					print(db[userid][4])
				else:
					print('1')
					embed=discord.Embed(title="Ram's Reaction", description=f"{ctx.author.mention}, Ram says \"Such disdainful pride\"", colour=0xffbbdd)
					embed.set_image(url="https://cdn.discordapp.com/attachments/800920762131152957/831687011215736892/87551149_p0.jpg")
					db[userid][4]+=1
					print(db[userid][4])
			if str(reaction.emoji)=='4️⃣':
				print('4')
				embed=discord.Embed(title="Ram's Reaction", description=f"{ctx.author.mention}, Your attempt at assassinating Ram was futile. She fought back with a power not seen before and you almost died. You managed to escape somehow, but you still don't understand how.", colour=0xffbbdd)
				embed.set_image(url="https://cdn.discordapp.com/attachments/800920762131152957/831688418400403508/88392756_p0_master1200.jpg")
				db[userid][5]+=1
				print(db[userid][5])
			embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
			await ctx.send(embed=embed)
			return

		except asyncio.TimeoutError:await ctx.send('expired')
	except NotBotChannel: pass
@bot.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
	db["server "+str(ctx.guild.id)][0]=prefix
	embed=discord.Embed(title=f"Changed Server Prefix {random.choice(emoticons)}", description=f"My Prefix is now {prefix}", colour=0xffbbdd)	
	embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
	await ctx.send(embed=embed)
@bot.command()
async def waifu(ctx):
	try:
		disablecheck(ctx)
		waifu = waifulabs.GenerateWaifu()
		bigwaifu = waifu.GenerateBigWaifu()

		bigwaifu.save("waifus/mybigwaifu.png")
		await ctx.send("Ram is still best girl, but since you can't have her, here you go")
		await ctx.send(file=discord.File("waifus/mybigwaifu.png"))
	except NotBotChannel: pass

		
@bot.command()
@commands.has_permissions(administrator=True)
async def addbotchannel(ctx):
	if not ctx.channel.id in db['server '+str(ctx.guild.id)]:
		db['server '+str(ctx.guild.id)].append(ctx.channel.id)
		embed=discord.Embed(title=f"Bot Channel {random.choice(emoticons)}", description=f"Channel {ctx.channel.mention} is now a bot channel. If you had no bot channels before, then this is the only channel where this bot's commands can be used", colour=0xffbbdd)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)

	else: 
		embed=discord.Embed(title=f"Error {random.choice(emoticons)}", description=f"Channel {ctx.channel.mention} is already a bot channel", colour=0xff0000)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def removebotchannel(ctx):
	server_data=db['server '+str(ctx.guild.id)]
	try:
		server_data.remove(ctx.channel.id)
		embed=discord.Embed(title=f"Bot Channel {random.choice(emoticons)}", description=f"Channel {ctx.channel.mention} is no longer a bot channel.", colour=0xffbbdd)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)
	except ValueError: 
		embed=discord.Embed(title=f"Bot Channel Error {random.choice(emoticons)}", description=f"Could not remove this channel from the list of bot channels because it is not a bot channel to begin with, baka.", colour=0xff0000)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)
	
	


@bot.command()
@commands.has_permissions(administrator=True)
async def allbotchannel(ctx):
	server_data=db['server '+str(ctx.guild.id)]
	server_data = [x for x in server_data if not isinstance(x, int)]
	for channel in ctx.guild.text_channels:
			server_data.append(channel.id)
	embed=discord.Embed(title=f"Bot Channel {random.choice(emoticons)}", description=f"All channels are now  bot channels", colour=0xffbbdd)	
	embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
	await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def removeallbotchannels(ctx):
	try:
		for i in range(len(db['server '+str(ctx.guild.id)])-1):
			db['server '+str(ctx.guild.id)].pop()
		db['server '+str(ctx.guild.id)].append(None)
		embed=discord.Embed(title=f"Bot Channel {random.choice(emoticons)}", description=f"All bot channels have been removed", colour=0xffbbdd)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)
	except ValueError: 
		embed=discord.Embed(title=f"Bot Channel Error {random.choice(emoticons)}", description=f"Something went wrong removing all bot channels?", colour=0xff0000)	
		embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')	
		await ctx.send(embed=embed)





@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	if Pattern.search(message.content)!=None:
		await message.channel.send(file=discord.File('glare.png'))
	userid=message.author.id
	global spam_logger	
	try:
		try:
			if db[str(userid)][2]==0 and db[str(userid)][3]==0 and db[str(userid)][4]==0 and db[str(userid)][5]==0:
				db[str(userid)][0]+=round((10/spam_logger[str(userid)]))
			else: 
				db[str(userid)][0]+=round((10/spam_logger[str(userid)])*(complimentfunction(db[str(userid)][2])+insultfunction(db[str(userid)][3])+headpatfunction(db[str(userid)][4])+killfunction(db[str(userid)][5]))/4)
		except KeyError:
			db[str(userid)][0]+=10
		if db[str(userid)][0]>=100+10*db[str(userid)][1]**2:
			db[str(userid)][1]+=1
			db[str(userid)][0]=0
			embed=discord.Embed(title=f"Level Up? {random.choice(emoticons)}", description=f"{message.author.mention}, you have leveled up to level {db[str(userid)][1]}. You still have some work to do. Hah! {random.choice(emoticons)}", colour=0xffbbdd)	
			embed.set_author(name="Ram Bot", icon_url='https://cdn.discordapp.com/avatars/828806563023159306/ab71416d358f662caf39fd83d32e5047.webp?size=2048')
			await message.channel.send(embed=embed)
	except KeyError: db[str(userid)]=[0,0,0,0,0,0]
	await bot.process_commands(message)




from keep_alive import keep_alive
keep_alive()
client=discord.Client()
bot.run(os.getenv('TOKEN'))
