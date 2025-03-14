import sqlite3
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from src.db.balance import update_balance, get_last_daily, set_last_daily, verify_balance, pay
from src.messages.en.balance_messages import balance_embed_message, balance_embed_empty_message, daily_reward_message, \
    daily_not_reward_message
from src.messages.en.gambling_messages import user_can_not_pay


# Command: Check current balance
async def balance_slash(interact: discord.Interaction):
    user_id = interact.user.id
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT balance from users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        embed = balance_embed_message(interact.user.mention, result)
        await interact.response.send_message(embed=embed)
    else:
        c.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        embed = balance_embed_empty_message(interact.user.mention)
        await interact.response.send_message(embed=embed)
    conn.close()


async def balance_command(ctx: commands.Context):
    user_id = ctx.author.id
    conn = sqlite3.connect('economy.db')
    c = conn.cursor()
    c.execute('SELECT balance from users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        embed = balance_embed_message(ctx.author.mention, result)
        await ctx.send(embed=embed)
    else:
        c.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        embed = balance_embed_empty_message(ctx.author.mention)
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
            embed = daily_not_reward_message(interact.user.mention)
            await interact.response.send_message(embed=embed)
            await interact.message.add_reaction("⏰")
            return

    update_balance(user_id, reward)
    set_last_daily(user_id, datetime.now().isoformat())

    embed = daily_reward_message(interact.user.mention, reward)
    await interact.response.send_message(embe=embed)
    await interact.message.add_reaction("🎉")


async def daily(ctx: commands.Context):
    user_id = ctx.author.id
    reward = 100

    last_daily = get_last_daily(user_id)
    if last_daily:
        last_daily_date = datetime.fromisoformat(last_daily)
        now = datetime.now()
        if now - last_daily_date < timedelta(days=1):
            embed = daily_not_reward_message(ctx.author.mention)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("⏰")
            return

    update_balance(user_id, reward)
    set_last_daily(user_id, datetime.now().isoformat())

    embed = daily_reward_message(ctx.author.mention, reward)
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("🎉")


# Commands: pay
async def pay_command(ctx: commands.Context, receiver: discord.Member, value: int):
    sender_id = ctx.author.id

    user_can_pay, user_balance = verify_balance(sender_id, value)

    if not user_can_pay:
        await ctx.send(user_can_not_pay(ctx.author.mention, user_balance))
        return

    receiver_id = receiver.id

    pay(sender_id, receiver_id, value)

    await ctx.send(f"{ctx.author.mention} successfully paid {receiver.mention} **{value} coins**! 💸")
