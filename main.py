import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import aiohttp
import datetime

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(OwnerPresence())

bot = PersistentViewBot()

class UserInfo:
    def __init__(self, memberInfo : discord.Member):
        self.memberInfo = memberInfo
        self.score : int

userList = []
currentUserOwner : str

# change this ID to your guild ID
guildID = 1054434525637267558

# channel where the bot talks
channelID = None

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
        # if member.id == 444171484085223424:
        #     userList.append(UserInfo(member))

@bot.command(name="callMyP3T")
async def callTheBot(ctx):
    global channelID
    channelID = ctx.message.channel.id
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as resp:
            if resp.status == 200:
                js = await resp.json()
                await ctx.send("Hey! Did you call me?")
                await ctx.send(js['file'])
            else:
                await ctx.send("Hey! Did you call me?")
    if not whoTakeCareOfBot.is_running():
        whoTakeCareOfBot.start()

async def checkOwnerPresence(interaction : discord.Interaction, choice : str):
    if (interaction.user.mention == currentUserOwner):
        if (choice == "yes"):
            await interaction.message.delete()
            await interaction.channel.send("Thank you! :heart_eyes_cat:")
        if (choice == "no"):
            await interaction.message.delete()
            await interaction.channel.send("You fall in my esteem :crying_cat_face:")
            whoTakeCareOfBot.restart()
    else:
        await interaction.response.send_message(f"I'm waiting for the response of {currentUserOwner}... :crying_cat_face:", ephemeral=True)

class OwnerPresence(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Yes no problem!", style=discord.ButtonStyle.primary, custom_id="YesCare")
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await checkOwnerPresence(interaction, "yes")

    @discord.ui.button(label="Sorry I haven't the time", style=discord.ButtonStyle.red, custom_id="NoCare")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await checkOwnerPresence(interaction, "no")

@tasks.loop(hours=6)
async def whoTakeCareOfBot():
    global currentUserOwner
    currentUserOwner = random.choice(userList).memberInfo.mention
    try:
        if (datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour < 12):
            await bot.get_guild(guildID).get_channel(channelID).send(f"I want {currentUserOwner} to take care of me this morning", view=OwnerPresence())
        else:
            await bot.get_guild(guildID).get_channel(channelID).send(f"I want {currentUserOwner} to take care of me this afternoon", view=OwnerPresence())
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