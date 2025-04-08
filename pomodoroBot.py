import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello! Pomodoro bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Pomodoro bot is ready!")

bot.run(TOKEN)