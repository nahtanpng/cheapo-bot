import random

import discord
from discord.ext import commands

from src.db.balance import verify_balance
from src.db.gambling import flip_reward


async def flip(ctx: commands.Context, side: str, value: int):
    user_id = ctx.author.id

    user_can_pay, user_balance = verify_balance(user_id, value)

    if not user_can_pay:
        await ctx.send(f'''
🎩 **Yikes, {ctx.author.mention}!** 🎩

You’re flat broke, kiddo! Can’t make it rain without the dough. 💸  
Your current balance is **{user_balance} coins** :moneybag:.  

*"Better get back to work, champ—those coins won’t earn themselves!"* 😅
        ''')
        return

    coin_faces = ["heads", "tails"]
    chosen_face = random.choice(coin_faces)

    if side == chosen_face:
        flip_reward(user_id, value, is_winner=True)
        await ctx.send(f'''
🎉 **Hot diggity dog, {ctx.author.mention}!** 🎉

You hit the jackpot! 🎰  
**{value} coins** are now yours to keep! :money_mouth:  

*"Keep throwing those coin, big shot—you’re on a winning streak!"* 🤑
        ''')
    else:
        flip_reward(user_id, value, is_winner=False)
        await ctx.send(f'''
💔 **Oh no, {ctx.author.mention}!** 💔

The house always wins, kiddo. 🎰  
**{value} coins** just flew outta your pocket! :money_with_wings:  
        ''')