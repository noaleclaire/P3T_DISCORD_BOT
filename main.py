import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import aiohttp
import datetime

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class UserInfo:
    def __init__(self, memberInfo : discord.Member):
        self.memberInfo = memberInfo
        self.score : int

userList = []

# change this ID to your guild ID
guildID = 1054434525637267558

# channel where the bot talks
channelID = None

# start tasks
startWhoTakeCareOfBot = False

@bot.event
async def on_ready():
    global userList
    print("Bot is online")
    # try:
    #     synced = await bot.tree.sync()
    #     print(f"Synced {len(synced)} slash command(s)")
    # except Exception as e:
    #     print(e)
    for member in bot.get_all_members():
        if not member.bot:
            userList.append(UserInfo(member))

@bot.command(name="callMyP3T")
async def callTheBot(ctx):
    global channelID
    global startWhoTakeCareOfBot
    channelID = ctx.message.channel.id
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as resp:
            if resp.status == 200:
                js = await resp.json()
                await ctx.send("Hey! Did you call me?")
                await ctx.send(js['file'])
            else:
                await ctx.send("Hey! Did you call me?")
    if not startWhoTakeCareOfBot:
        whoTakeCareOfBot.start()
        startWhoTakeCareOfBot = True

@tasks.loop(seconds=5)
async def whoTakeCareOfBot():
    userOwner = random.choice(userList).memberInfo.mention
    try:
        if (datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour < 12):
            await bot.get_guild(guildID).get_channel(channelID).send(f"I want {userOwner} to take care of me this morning")
        else:
            await bot.get_guild(guildID).get_channel(channelID).send(f"I want {userOwner} to take care of me this afternoon")
    except:
        return


# @bot.tree.command(name="ping", description="test")
# async def ping(interaction: discord.Interaction):
#     await interaction.response.send_message(f"pong {interaction.user.mention}", ephemeral=True) #ephemeral -> only the user see the response

# @bot.tree.command(name="say", description="1224563")
# @app_commands.describe(thing_to_say="What should I say?")
# async def say(interaction: discord.Interaction, thing_to_say: str):
#     await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

# @bot.command()
# async def hello(ctx):
#     await ctx.send("Hey Bro!")

bot.run("")