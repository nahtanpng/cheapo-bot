import discord
from discord.ext import commands
from src.application.use_cases.transfer_coins import TransferCoinsUseCase
from src.domain.exceptions import InsufficientBalanceException, InvalidAmountException, SelfPaymentException
from src.presentation.messages.en.balance_messages import payment_success_embed, create_error_embed


class PayCommand(commands.Cog):
    def __init__(self, transfer_coins_use_case: TransferCoinsUseCase):
        self.transfer_coins_use_case = transfer_coins_use_case

    @commands.command()
    async def pay(self, ctx: commands.Context, receiver: discord.Member, amount: int):
        try:
            self.transfer_coins_use_case.execute(ctx.author.id, receiver.id, amount)
            await ctx.send(embed=payment_success_embed(ctx.author.mention, receiver.mention, amount))

        except InsufficientBalanceException as e:
            await ctx.send(embed=create_error_embed(
                title="💸 Insufficient Funds! 💸",
                description=f"{ctx.author.mention}, you don't have enough coins!",
                fields=[("Current Balance", f"{e.current_balance} coins", True)],
                color=0xFF0000
            ))

        except InvalidAmountException:
            await ctx.send(embed=create_error_embed(
                title="❌ Invalid Amount! ❌",
                description=f"{ctx.author.mention}, you must enter a positive number!",
                color=0xFFA500
            ))

        except SelfPaymentException:
            await ctx.send(embed=create_error_embed(
                title="🤔 Self Payment? 🤔",
                description=f"{ctx.author.mention}, you can't pay yourself!",
                footer="Try paying someone else instead!",
                color=0xFFFF00
            ))

        except Exception as e:
            await ctx.send(embed=create_error_embed(
                title="⚠️ Unexpected Error! ⚠️",
                description="Something went wrong with the payment",
                footer=str(e),
                color=0x000000
            ))