import discord
from discord.ext import commands

from src.application.use_cases.balance import BalanceUseCase
from src.presentation.messages.en.balance_messages import balance_embed_message


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