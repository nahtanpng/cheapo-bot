from discord.ext import commands

from src.application.use_cases.gambling import GamblingUseCase
from src.presentation.messages.en.gambling_messages import flip_reward_message, flip_loss_message


class GamblingCommands(commands.Cog):
    def __init__(self, gambling_use_case: GamblingUseCase):
        self.gambling_use_case = gambling_use_case

    @commands.command()
    async def flip(self, ctx: commands.Context, side: str, amount: int):
        user_id = ctx.author.id

        success = self.gambling_use_case.flip(user_id, side, amount)

        if success:
            await ctx.send(flip_reward_message(ctx.author.mention, amount))
        else:
            await ctx.send(flip_loss_message(ctx.author.mention, amount))
