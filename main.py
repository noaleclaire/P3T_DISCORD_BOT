import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
import aiohttp
import datetime
import asyncio

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(HungryBotSelectMenuView())

bot = PersistentViewBot()

class UserInfo:
    def __init__(self, memberInfo : discord.Member):
        self.memberInfo = memberInfo
        self.score = 0
        self.scoreHungryBot = 0

memberList = []

currentOwner = None
oldOwner = None

def getMemberByID(memberID : int) -> UserInfo:
    for member in memberList:
        if member.memberInfo.id == memberID:
            return (member)
    return None

# change this ID to your guild ID
guildID = 1054434525637267558

# channel where the bot talks
channelID = None

hungryGifs = ["https://media.tenor.com/sCsJ0l1gxHUAAAAd/cat-meme.gif", "https://media.tenor.com/fTTVgygGDh8AAAAd/kitty-cat-sandwich.gif"]
hungryFoods = [["Poultry, Leg", '\N{POULTRY LEG}'], ["Cookie", '\N{COOKIE}'], ["Bacon", '\N{BACON}'], ["Fried Shrimp", '\N{FRIED SHRIMP}']]

@bot.event
async def on_ready():
    global memberList
    print("Bot is online")
    # try:
    #     synced = await bot.tree.sync()
    #     print(f"Synced {len(synced)} slash command(s)")
    # except Exception as e:
    #     print(e)
    for member in bot.get_all_members():
        if not member.bot:
            memberList.append(UserInfo(member))
        # if member.id == 444171484085223424:
        #     memberList.append(UserInfo(member))

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
    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    try:
        await bot.wait_for("message", timeout=10, check=checkMessage)
        await ctx.reply(f"{ctx.message.author.mention} can you take care of me please")
        await ctx.send("https://media.tenor.com/DZmldC3h2oMAAAAS/cute-face-puss.gif")
    except Exception:
        await ctx.send(f"I'm wondering why **{ctx.message.author.display_name}** called me...")
    await asyncio.sleep(5)
    if not hungryBot.is_running():
        hungryBot.start()
    # if not responseToCall.is_running():
    #     responseToCall.start()

def keySortByScore(member):
    return member.score

@bot.command()
async def ranking(ctx):
    embed = discord.Embed(title="Ranking of MyP3T's Favorite Members",
    description="Those are the members that take care of me most of the time :heart_eyes_cat:",
    colour=discord.Colour.brand_red())
    memberList.sort(key=keySortByScore, reverse=True)
    members = ""
    scores = ""
    emoji = ""
    count = 0
    for i in range (0, len(memberList)):
        if i == 11 or memberList[i].score <= 0:
            break
        if i == 0:
            emoji = ":crown:"
            embed.set_thumbnail(url=f"{memberList[i].memberInfo.display_avatar}")
            members += "**" + memberList[i].memberInfo.display_name + "**" + " " + emoji + "\n"
        elif i == 1:
            emoji = ":heart_on_fire:"
            members += "**" + memberList[i].memberInfo.display_name + "**" + " " + emoji + "\n"
        elif i == 2:
            emoji = ":heart_eyes_cat:"
            members += "**" + memberList[i].memberInfo.display_name + "**" + " " + emoji + "\n"
        else:
            emoji = ":star2:"
            members += memberList[i].memberInfo.display_name + " " + emoji + "\n"
        scores += str(memberList[i].score) + "\n"
        count += 1
    if members == "":
        members = "No One Take Care of Me :crying_cat_face:"
    embed.add_field(name="RANKING:", value=members)
    if scores != "":
        embed.add_field(name="SCORES:", value=scores)
    if count < 10:
        embed.set_footer(text="Why are there so few people taking care of me...")
    await ctx.send(embed=embed)

class HungryBotSelectMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HungryBotSelectMenu())

class HungryBotSelectMenu(discord.ui.Select):
    def __init__(self):
        options = []
        for food in hungryFoods:
            options.append(discord.SelectOption(label=food[0], emoji=food[1]))
        super().__init__(placeholder="What food do you want to give him?", options=options, custom_id="HungrySelectMenu")
        self.reaction = random.choice(hungryFoods)[0]

    async def callback(self, interaction : discord.Interaction):
        if self.reaction == self.values[0]:
            getMemberByID(interaction.user.id).scoreHungryBot = 1
        else:
            getMemberByID(interaction.user.id).scoreHungryBot = -1
        await interaction.response.send_message("Thanks! I'm waiting for more food from the others :cat:", ephemeral=True)

@tasks.loop(hours=1, count=1)
async def noMoreHungryBot():
    messageID = 0
    async for message in bot.get_guild(guildID).get_channel(channelID).history():
        if message.author == bot.user:
            messageID = message.id
            break
    await asyncio.sleep(20)
    try:
        message = await bot.get_guild(guildID).get_channel(channelID).fetch_message(messageID)
        await message.delete()
    except:
        pass
    msg = "Thanks to "
    for member in memberList:
        if member.scoreHungryBot == 1:
            msg += "**" + member.memberInfo.display_name + "**" + ", "
        member.score += member.scoreHungryBot
        member.scoreHungryBot = 0
    if msg != "Thanks to ":
        msg = msg[0:len(msg) - 2] + " this food was **INCREDIBLE** :heart_eyes_cat:"
    else:
        msg = "Thanks everyone, but no one gave me the **Extraordinary** food I expected :crying_cat_face:"
    await bot.get_guild(guildID).get_channel(channelID).send(msg)
    noMoreHungryBot.stop()

@tasks.loop(minutes=30)
async def hungryBot():
    embed = discord.Embed(title="I'm hungry!",
    description="@everyone Can someone give me some food? Choose right please!",
    colour=discord.Colour.random())
    embed.set_image(url=random.choice(hungryGifs))
    await bot.get_guild(guildID).get_channel(channelID).send(embed=embed, view=HungryBotSelectMenuView())
    noMoreHungryBot.start()





def removeCurrentOwnerFromList():
    global oldOwner
    if currentOwner != None:
        for member in memberList:
            if member.memberInfo.mention == currentOwner:
                oldOwner = currentOwner
                memberList.remove(member)
                break

def addOldOwnerToList():
    if oldOwner != None:
        for member in bot.get_all_members():
            if member.mention == oldOwner:
                memberList.append(UserInfo(member))
                break

async def checkOwnerPresence(interaction : discord.Interaction, choice : str):
    if currentOwner != None:
        if interaction.user.mention == currentOwner:
            if (choice == "yes"):
                await interaction.message.delete()
                await interaction.channel.send("Thank you! :heart_eyes_cat:")
                getMemberByID(interaction.user.id).score += 1
                noAnswerOfTheMentionOwner.cancel()
            if (choice == "no"):
                await interaction.message.delete()
                await interaction.channel.send("You fall in my esteem :crying_cat_face:")
                removeCurrentOwnerFromList()
                noAnswerOfTheMentionOwner.cancel()
                await asyncio.sleep(5)
                whoTakeCareOfBot.restart()
        else:
            await interaction.response.send_message(f"I'm waiting for the response of {currentOwner}... :crying_cat_face:", ephemeral=True)
    else:
        await interaction.response.send_message("There is no one to take care of me :crying_cat_face: :crying_cat_face: :crying_cat_face:")

class OwnerPresence(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Yes no problem!", style=discord.ButtonStyle.primary, custom_id="YesCare")
    async def yes(self, interaction : discord.Interaction, button : discord.ui.Button):
        await checkOwnerPresence(interaction, "yes")

    @discord.ui.button(label="Sorry I haven't the time", style=discord.ButtonStyle.red, custom_id="NoCare")
    async def no(self, interaction : discord.Interaction, button : discord.ui.Button):
        await checkOwnerPresence(interaction, "no")

@tasks.loop(hours=1, count=1)
async def noAnswerOfTheMentionOwner():
    messageID = 0
    async for message in bot.get_guild(guildID).get_channel(channelID).history():
        if message.author == bot.user:
            messageID = message.id
            break
    await asyncio.sleep(10)
    message = await bot.get_guild(guildID).get_channel(channelID).fetch_message(messageID)
    await message.delete()
    await bot.get_guild(guildID).get_channel(channelID).send(f"Where are you {currentOwner}... I'm waiting for you... :crying_cat_face:\n\
        You missed the opportunity, I'm sad...")
    await asyncio.sleep(5)
    removeCurrentOwnerFromList()
    whoTakeCareOfBot.restart()
    noAnswerOfTheMentionOwner.stop()

@tasks.loop(hours=6)
async def whoTakeCareOfBot():
    global currentOwner
    currentOwner = random.choice(memberList).memberInfo.mention
    addOldOwnerToList()
    try:
        if datetime.datetime.now().hour >= 0 and datetime.datetime.now().hour < 12:
            await bot.get_guild(guildID).get_channel(channelID).send(f"I want {currentOwner} to take care of me this morning :cat:", view=OwnerPresence())
        else:
            await bot.get_guild(guildID).get_channel(channelID).send(f"I want {currentOwner} to take care of me this afternoon :cat:", view=OwnerPresence())
        noAnswerOfTheMentionOwner.start()
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