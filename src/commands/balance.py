import sqlite3
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from src.db.balance import update_balance, get_last_daily, set_last_daily


# Command: Check current balance
async def balance_slash(interact: discord.Interaction):
    user_id = interact.user.id
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT balance from users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        await interact.response.send_message(f'{interact.user.mention}, your balance is {result[0]} coins.')
    else:
        c.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        await interact.response.send_message(f'{interact.user.name}, your balance is 0 coins. :coin:')
    conn.close()


async def balance_command(ctx: commands.Context):
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
        await ctx.send(f'{ctx.author.mention}, your balance is 0 coins. :coin:')
    conn.close()


# Command: daily reward
async def daily_slash(interact: discord.Interaction):
    user_id = interact.user.id
    reward = 100

    last_daily = get_last_daily(user_id)
    if last_daily:
        last_daily_date = datetime.fromisoformat(last_daily)
        now = datetime.now()
        if now - last_daily_date < timedelta(days=1):
            await interact.response.send_message(
                f'{interact.user.mention}, you can only claim your daily reward **once per day!**')
            return

    update_balance(user_id, reward)
    set_last_daily(user_id, datetime.now().isoformat())
    await interact.response.send_message(
        f'{interact.user.mention}, you **claimed** your daily reward of {reward} coins! :moneybag:')


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

