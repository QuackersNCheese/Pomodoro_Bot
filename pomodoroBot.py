import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from dataclasses import dataclass
import datetime

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
MAX_SESSION_TIME = 30
@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@tasks.loop(minutes=MAX_SESSION_TIME, count=2)
async def break_reminder():
    # Ignore the first execution of this command.
    if break_reminder.current_loop == 0:
        return
    
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME} minutes.")

@bot.event
async def on_ready():
    print("Hello! Pomodoro bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Pomodoro bot is ready!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)

    await ctx.send(f"Result: = {result}")

@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return
    
    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
    
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration =  end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration} seconds.")

@bot.command()
async def mlh(ctx):
    await ctx.send(f"https://mlh.io/")

@bot.command()
async def ghw(ctx):
    await ctx.send("https://ghw.mlh.io/")

@bot.command()
async def manual(ctx):
    await ctx.send(f"Hello! I am {bot.user.name}! I am here to help you study! Here are some of the commands you can use:\n\n"
                    "1. **!start** - Start a 30 min timer\n"
                    "2. **!end** - End the timer\n"
                    "3. **!add** - Add numbers\n"
                    "4. **!hello** - Say hello\n"
                    "5. **!mlh** - Get the MLH website\n"
                    "6. **!ghw** - Get the GHW website\n"
                    "7. **!help** - Get a list of commands\n")

bot.run(TOKEN)