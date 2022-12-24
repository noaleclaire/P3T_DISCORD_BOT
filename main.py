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
        self.add_view(StrokeBotButtons())

bot = PersistentViewBot()

class UserInfo:
    def __init__(self, memberInfo : discord.Member):
        self.memberInfo = memberInfo
        self.score = 0
        self.scoreHungryBot = 0

memberList = {}
currentMemberCalled = None

guildID = None
# channel where the bot talks
channelID = None

def getMemberByID(memberID : int) -> UserInfo:
    for member in memberList[guildID]:
        if member.memberInfo.id == memberID:
            return (member)
    return None

hungryGifs = ["https://media.tenor.com/sCsJ0l1gxHUAAAAd/cat-meme.gif", "https://media.tenor.com/fTTVgygGDh8AAAAd/kitty-cat-sandwich.gif"]
hungryFoods = [["Poultry, Leg", '\N{POULTRY LEG}'], ["Cookie", '\N{COOKIE}'], ["Bacon", '\N{BACON}'], ["Fried Shrimp", '\N{FRIED SHRIMP}']]

strokeGifs = ["https://media.tenor.com/762byUjvxi8AAAAS/dr-evil-stroke.gif", "https://media.tenor.com/HRFQ9DcDq6gAAAAS/stroking-cat-viralhog.gif",
            "https://media.tenor.com/uFX64bs0eIUAAAAd/stroking-cat.gif", "https://media.tenor.com/i-htVw82J7wAAAAS/cat-leek.gif"]

toysToPlayWithGifs = ["https://media.tenor.com/pq2tWPMudLgAAAAS/playful-kitten-cute.gif", "https://media.tenor.com/t9YX6fymF_AAAAAS/lola-cat.gif",
                    "https://media.tenor.com/peSEPfmGL6MAAAAS/kitty-music.gif", "https://media.tenor.com/hvVwrpDdjSAAAAAd/whack-a-finger-cat.gif"]
toysToPlayWith = ["🪢", "🧶", "🧵", "🐁", "🐭", "🐛", "🪱", "🪲", "🥒", "🥎", "🎾", "🎈", "📦"]

@bot.event
async def on_ready():
    global memberList
    print("Bot is online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(e)
    for guild in bot.guilds:
        memberList[guild.id] = []
        for member in guild.members:
            if not member.bot:
                memberList[guild.id].append(UserInfo(member))

@bot.event
async def on_message(message):
    global guildID
    global channelID
    if message.guild != None:
        guildID = message.guild.id
        channelID = message.channel.id
        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return

# Call Bot Command
@bot.command(name="callMyP3T")
@commands.cooldown(1, 30, commands.BucketType.user)
async def callTheBot(ctx):
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
    if not hungryBot.is_running():
        await asyncio.sleep(5)
        hungryBot.start()
    if not strokeBot.is_running():
        await asyncio.sleep(15)
        strokeBot.start()
    callTheBot.cooldown.per = 10

# Ranking Members Command
def keySortByScore(member):
    return member.score

@bot.command()
async def ranking(ctx):
    embed = discord.Embed(title="Ranking of MyP3T's Favorite Members",
    description="Those are the members that take care of me most of the time :heart_eyes_cat:",
    colour=discord.Colour.brand_red())
    memberList[guildID].sort(key=keySortByScore, reverse=True)
    members = ""
    scores = ""
    emoji = ""
    count = 0
    for i in range (0, len(memberList[guildID])):
        if i == 11 or memberList[guildID][i].score <= 0:
            break
        if i == 0:
            emoji = ":crown:"
            embed.set_thumbnail(url=f"{memberList[guildID][i].memberInfo.display_avatar}")
            members += "**" + memberList[guildID][i].memberInfo.display_name + "**" + " " + emoji + "\n"
        elif i == 1:
            emoji = ":heart_on_fire:"
            members += "**" + memberList[guildID][i].memberInfo.display_name + "**" + " " + emoji + "\n"
        elif i == 2:
            emoji = ":heart_eyes_cat:"
            members += "**" + memberList[guildID][i].memberInfo.display_name + "**" + " " + emoji + "\n"
        else:
            emoji = ":star2:"
            members += memberList[guildID][i].memberInfo.display_name + " " + emoji + "\n"
        scores += str(memberList[guildID][i].score) + "\n"
        count += 1
    if members == "":
        members = "No One Take Care of Me :crying_cat_face:"
    embed.add_field(name="RANKING:", value=members)
    if scores != "":
        embed.add_field(name="SCORES:", value=scores)
    if count < 10:
        embed.set_footer(text="Why are there so few people taking care of me...")
    await ctx.send(embed=embed)

# Guess Toy To Play With Slash Command
@bot.tree.command(name="toyGame", description="What kind of toy MyP3T would like to play with?")
async def say(interaction: discord.Interaction):
    embed = discord.Embed(title="Find the good toy!",
    description="Hey @everyone! I would like a new toy to play with!\n\
React to this message to find which toy would make me happy :smiley_cat:",
    colour=discord.Colour.random())
    embed.set_thumbnail(url=random.choice(toysToPlayWithGifs))
    await interaction.response.send_message(embed=embed)
    react = random.choice(toysToPlayWith)
    message = await interaction.original_response()
    def checkReactions(reaction, user):
        return reaction.message.id == message.id and str(reaction.emoji) == react
    try:
        reaction, user = await bot.wait_for("reaction_add", timeout=60, check=checkReactions)
        await interaction.followup.send(f"Yeah! Thank you {user.mention} the toy was obviously a {reaction.emoji}")
        getMemberByID(user.id).score += 2
    except Exception:
        await interaction.followup.send(f"Unfortunately no one found the toy I wanted\nNext time maybe...")

# Hungry Bot Task
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
        await interaction.response.send_message("Thanks! I'm waiting more food from the others :cat:", ephemeral=True)

@tasks.loop(hours=1, count=1)
async def noMoreHungryBot():
    messageID = 0
    async for message in bot.get_guild(guildID).get_channel(channelID).history(limit=200):
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
    for member in memberList[guildID]:
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

# Stroke Bot Task
async def checkResponseStroke(interaction : discord.Interaction, choice : str):
    if currentMemberCalled != None:
        if interaction.user.id == currentMemberCalled.memberInfo.id:
            if (choice == "yes"):
                await interaction.message.delete()
                await interaction.channel.send(random.choice(strokeGifs))
                getMemberByID(interaction.user.id).score += 5
                noResponseForStroking.cancel()
            if (choice == "no"):
                await interaction.message.delete()
                await interaction.channel.send(":crying_cat_face: Why...")
                getMemberByID(interaction.user.id).score -= 1
                noResponseForStroking.cancel()
        else:
            await interaction.response.send_message(f"I'm waiting for **{currentMemberCalled.memberInfo.display_name}** :cat:", ephemeral=True)
    else:
        await interaction.response.send_message("There is no one to take care of me :crying_cat_face:")

class StrokeBotButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="Come here!", style=discord.ButtonStyle.primary, custom_id="YesStroke", emoji="🐈")
    async def yes(self, interaction : discord.Interaction, button : discord.ui.Button):
        await checkResponseStroke(interaction, "yes")

    @discord.ui.button(label="Sorry I haven't the time", style=discord.ButtonStyle.red, custom_id="NoStroke")
    async def no(self, interaction : discord.Interaction, button : discord.ui.Button):
        await checkResponseStroke(interaction, "no")

@tasks.loop(hours=1, count=1)
async def noResponseForStroking():
    messageID = 0
    async for message in bot.get_guild(guildID).get_channel(channelID).history(limit=200):
        if message.author == bot.user:
            messageID = message.id
            break
    await asyncio.sleep(30)
    try:
        message = await bot.get_guild(guildID).get_channel(channelID).fetch_message(messageID)
        await message.delete()
    except:
        pass
    await bot.get_guild(guildID).get_channel(channelID).send(f"Where are you **{currentMemberCalled.memberInfo.display_name}**... I'm waiting for you... :crying_cat_face:\n\
        You missed the opportunity, I'm sad...")
    getMemberByID(currentMemberCalled.memberInfo.id).score -= 2
    noResponseForStroking.stop()

@tasks.loop(minutes=20)
async def strokeBot():
    global currentMemberCalled
    currentMemberCalled = random.choice(memberList[guildID])
    try:
        await bot.get_guild(guildID).get_channel(channelID).send(f"Is {currentMemberCalled.memberInfo.mention} here? I want to be stroked", view=StrokeBotButtons())
        noResponseForStroking.start()
    except:
        return

bot.run("BOT TOKEN")