import os
import sqlite3
from itertools import cycle

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from src.commands.help_command import CustomHelpCommand

# Setting .env variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="c!", intents=intents, help_command=CustomHelpCommand())


# Database setup
def init_db():
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, 
                  balance DECIMAL DEFAULT 0, 
                  last_daily TEXT,
                  message_counter INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()


bot_statuses = cycle(["Use c!help 🎲", "You're up 🃏", "How about a game? 🎲"])


@tasks.loop(seconds=5)
async def change_bot_statuses():
    await bot.change_presence(activity=discord.CustomActivity(next(bot_statuses)))


@bot.event
async def on_ready():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://media.discordapp.net/attachments/1350148775196233759/1350148879034744904/cheapo.png?ex=67d5afa1&is=67d45e21&hm=2106493561e93b006c81f6a888274e35613e00a38b8b7cd4735e918f3849bdc1&=&format=webp&quality=lossless&width=704&height=704") as response:
            if response.status == 200:
                img = await response.read()
                await bot.user.edit(avatar=img)
                print("Avatar uploaded!")
            else:
                print(f"Failed to fetch image: HTTP {response.status}")

    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://media.discordapp.net/attachments/1350148775196233759/1350148879957626922/banner.png?ex=67d5afa1&is=67d45e21&hm=fc9ff4d92d0039b743222e8456fa622e6af5c4a59f33ec59ff8d3ffa145f969c&=&format=webp&quality=lossless&width=748&height=264") as response:
            if response.status == 200:
                img = await response.read()
                await bot.user.edit(banner=img)
                print("Banner uploaded!")
            else:
                print(f"Failed to fetch image: HTTP {response.status}")

    await bot.tree.sync()
    change_bot_statuses.start()
    await bot.change_presence(activity=discord.CustomActivity("Use c!help 🎲"))
    print(f'Logged in as {bot.user.name}')
    init_db()


# Commands
from src.commands.commands_setup import commands_setup

commands_setup(bot)

# Events
from src.events.events_setup import events_setup

events_setup(bot)

bot.run(TOKEN)
