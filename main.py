import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is online")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="ping", description="test")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"pong {interaction.user.mention}", ephemeral=True) #ephemeral -> only the user see the response

@bot.tree.command(name="say", description="1224563")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

@bot.command()
async def hello(ctx):
    await ctx.send("Hey Bro!")

bot.run("MTA1NDQzNTI5MjIzODU5ODE1NA.GwAkZw.YAV01wkPWVPVlzPQkroG-Q3XKX7ZDKWOa7WKTE")