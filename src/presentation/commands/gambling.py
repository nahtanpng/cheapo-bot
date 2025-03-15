import random

from discord.ext import commands

from src.infrastructure.db.balance_repository_impl import verify_balance
from src.infrastructure.db.gambling import flip_reward
from src.presentation.messages.en.gambling_messages import user_can_not_pay, flip_reward_message, flip_loss_message


async def flip(ctx: commands.Context, side: str, value: int):
    user_id = ctx.author.id

    user_can_pay, user_balance = verify_balance(user_id, value)

    if not user_can_pay:
        await ctx.send(user_can_not_pay(ctx.author.mention, user_balance))
        return

    coin_faces = ["heads", "tails"]
    chosen_face = random.choice(coin_faces)

    if side == chosen_face:
        flip_reward(user_id, value, is_winner=True)
        await ctx.send(flip_reward_message(ctx.author.mention, value))
    else:
        flip_reward(user_id, value, is_winner=False)
        await ctx.send(flip_loss_message(ctx.author.mention, value))
