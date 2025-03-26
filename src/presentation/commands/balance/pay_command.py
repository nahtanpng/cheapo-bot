import discord
from discord.ext import commands
from src.application.use_cases.transfer_coins import TransferCoinsUseCase
from src.presentation.messages.en.balance_messages import payment_success_embed


class PayCommand(commands.Cog):
    def __init__(self, transfer_coins_use_case: TransferCoinsUseCase):
        self.transfer_coins_use_case = transfer_coins_use_case

    @commands.command()
    async def pay(self, ctx: commands.Context, receiver: discord.Member, amount: int):
        try:
            self.transfer_coins_use_case.execute(ctx.author.id, receiver.id, amount)
            await ctx.send(embed=payment_success_embed(ctx.author.mention, receiver.mention, amount))
        except ValueError as e:
            await ctx.send(f"Error: {e}")