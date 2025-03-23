from datetime import datetime, timedelta

import discord
from discord.ext import commands

from src.infrastructure.db.balance import update_balance, get_last_daily, set_last_daily, verify_balance, pay, get_balance
from src.presentation.messages.en.balance_messages import balance_embed_message, daily_reward_message, \
    daily_not_reward_message
from src.presentation.messages.en.gambling_messages import user_can_not_pay

class a:
    def __init__(self, balance_repository):
# Command: Check current balance
async def balance_slash(interact: discord.Interaction):
    user_id = interact.user.id

    result = get_balance(user_id)

    embed = balance_embed_message(interact.user.mention, result)
    await interact.response.send_message(embed=embed)


async def balance_command(ctx: commands.Context):
    user_id = ctx.author.id

    result = get_balance(user_id)

    embed = balance_embed_message(ctx.author.mention, result)
    await ctx.send(embed=embed)

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
