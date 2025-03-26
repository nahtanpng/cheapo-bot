from discord.ext import commands

from src.application.use_cases.gambling import GamblingUseCase
from src.presentation.messages.en.gambling_messages import flip_reward_embed, flip_loss_embed, flip_result_embed, \
    user_can_not_pay


class GamblingCommands(commands.Cog):
    def __init__(self, gambling_use_case: GamblingUseCase):
        self.gambling_use_case = gambling_use_case

    @commands.command()
    async def flip(self, ctx: commands.Context, side: str, amount: int):
        user_id = ctx.author.id

        try:
            success, chosen_face = self.gambling_use_case.flip(user_id, side, amount)

            await ctx.send(embed=flip_result_embed(chosen_face))

            if success:
                await ctx.send(embed=flip_reward_embed(ctx.author.mention, amount))
            else:
                await ctx.send(embed=flip_loss_embed(ctx.author.mention, amount))
        except ValueError as e:
            current_balance = int(e.args[0]) if e.args else 0
            await ctx.send(embed=user_can_not_pay(ctx.author.mention, current_balance))
