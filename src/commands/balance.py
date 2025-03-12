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
        embed = discord.Embed(
            title="💰 Your Balance 💰",
            description=f"**{interact.user.mention}, you’ve got a shiny pile of {result[0]} coins!** :coin:",
            color=0xFFD700  # Gold color
        )
        embed.set_footer(text="Keep stackin’ that dough, big shot—you’re on a roll! 🤑")
        await interact.response.send_message(embed=embed)
    else:
        c.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        embed = discord.Embed(
            title="💔 Your Balance 💔",
            description=f"**{interact.user.mention}, your pockets are empty... 0 coins to your name!** :coin:",
            color=0xFF0000  # Red color
        )
        embed.set_footer(text="Time to get to work, kiddo—those coins won’t earn themselves! 😅")
        await interact.response.send_message(embed=embed)
    conn.close()


async def balance_command(ctx: commands.Context):
    user_id = ctx.author.id
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT balance from users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        embed = discord.Embed(
            title="💰 Your Balance 💰",
            description=f"**{ctx.author.mention}, you’ve got a shiny pile of {result[0]} coins!** :coin:",
            color=0xFFD700  # Gold color
        )
        embed.set_footer(text="Keep stackin’ that dough, big shot—you’re on a roll! 🤑")
        await ctx.send(embed=embed)
    else:
        c.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        embed = discord.Embed(
            title="💔 Your Balance 💔",
            description=f"**{ctx.author.mention}, your pockets are empty... 0 coins to your name!** :coin:",
            color=0xFF0000  # Red color
        )
        embed.set_footer(text="Time to get to work, kiddo—those coins won’t earn themselves! 😅")
        await ctx.send(embed=embed)
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
            embed = discord.Embed(
                title="⏰ Daily Cooldown ⏰",
                description=f"**{ctx.author.mention}, you’ve already claimed your daily reward today!**\n\n*Patience is a virtue, kiddo—come back tomorrow for more shiny coins!* 💰",
                color=0xFFA500  # Orange color
            )
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("⏰")
            return

    update_balance(user_id, reward)
    set_last_daily(user_id, datetime.now().isoformat())
    embed = discord.Embed(
        title="🎉 Daily Reward Claimed! 🎉",
        description=f"**{ctx.author.mention}, you just claimed your daily reward of {reward} coins!** :moneybag:\n\n*Keep stackin’ that dough, big shot—you’re on a roll!* 🤑",
        color=0xFFD700  # Gold color
    )
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("🎉")


