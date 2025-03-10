import os
import sqlite3
from itertools import cycle

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Setting .env variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="c!", intents=intents)


# Database setup
def init_db():
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, 
                  balance INTEGER DEFAULT 0, 
                  last_daily TEXT)''')
    conn.commit()
    conn.close()

bot_statuses = cycle(["Use c!help 🎲", "You're up 🃏", "How about a game? 🎲"])

@tasks.loop(seconds=5)
async def change_bot_statuses():
    await bot.change_presence(activity=discord.CustomActivity(next(bot_statuses)))

@bot.event
async def on_ready():
    await bot.tree.sync()
    change_bot_statuses.start()
    await bot.change_presence(activity=discord.CustomActivity("Use c!help 🎲"))
    print(f'Logged in as {bot.user.name}')
    init_db()


# Slash Commands
from src.commands.balance import setup

setup(bot)

bot.run(TOKEN)
