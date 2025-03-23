from discord.ext import commands

from src.application.use_cases.balance import BalanceUseCase
from src.presentation.messages.en.balance_messages import balance_embed_message, daily_reward_message, \
    daily_not_reward_message


class BalanceCommands(commands.Cog):
    def __init__(self, balance_use_case: BalanceUseCase):
        self.balance_use_case = balance_use_case

    @commands.command()
    async def balance(self, ctx: commands.Context):
        try:
            amount = self.balance_use_case.get_amount(ctx.author.id)
            embed = balance_embed_message(ctx.author.mention, amount)
            await ctx.send(embed=embed)
        except ValueError as e:
            await ctx.send(f"Error: {e}")

    @commands.command()
    async def daily(self, ctx: commands.Context):
        user_id = ctx.author.id

        success, reward = self.balance_use_case.get_daily(user_id)

        if success:
            embed = daily_reward_message(ctx.author.mention, reward)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("🎉")
        else:
            embed = daily_not_reward_message(ctx.author.mention)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("⏰")