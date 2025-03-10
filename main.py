import discord
from discord.ext import commands
import sqlite3
from dotenv import load_dotenv
from src.db.balance import update_balance, get_last_daily, set_last_daily
from datetime import datetime, timedelta
import os

# Setting .env variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    init_db()

# Command: Check current balance
@bot.command()
async def balance(ctx: commands.Context):
    user_id = ctx.author.id
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT balance from users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        await ctx.send(f'{ctx.author.mention}, your balance is {result[0]} coins. :coin:')
    else:
        c.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        await ctx.send(f'{ctx.author.name}, your balance is 0 coins. :coin:')
    conn.close()

# Command: daily reward
@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    reward = 100

    last_daily = get_last_daily(user_id)
    if last_daily:
        last_daily_date = datetime.fromisoformat(last_daily)
        now = datetime.now()
        if now - last_daily_date < timedelta(days=1):
            await ctx.send(f'{ctx.author.mention}, you can only claim your daily reward **once per day!**')
            return

    update_balance(user_id, reward)
    set_last_daily(user_id, datetime.now().isoformat())
    await ctx.send(f'{ctx.author.mention}, you **claimed** your daily reward of {reward} coins! :moneybag:')

bot.run(TOKEN)
