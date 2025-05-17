import discord
from discord import app_commands
from discord.ext import commands

from src.application.use_cases.balance import BalanceUseCase
from src.application.use_cases.gambling import GamblingUseCase
from src.application.use_cases.transfer_coins import TransferCoinsUseCase

from src.domain.exceptions import (
    InsufficientBalanceException,
    InvalidAmountException,
    SelfPaymentException
)

from src.presentation.messages.en.balance_messages import (
    balance_embed_message,
    daily_reward_message,
    daily_not_reward_message,
    payment_success_embed,
    create_error_embed
)
from src.presentation.messages.en.gambling_messages import (
    flip_reward_embed,
    flip_loss_embed,
    flip_result_embed,
    user_can_not_pay
)


async def setup_slash_commands(bot: commands.Bot):
    balance_use_case = None
    gambling_use_case = None
    transfer_coins_use_case = None

    def set_use_cases(balance_uc: BalanceUseCase, gambling_uc: GamblingUseCase,
                      transfer_us: TransferCoinsUseCase):
        nonlocal balance_use_case, gambling_use_case, transfer_coins_use_case
        balance_use_case = balance_uc
        gambling_use_case = gambling_uc
        transfer_coins_use_case = transfer_us

    @bot.tree.command(name="balance", description="Check your current coin balance")
    async def balance(interaction: discord.Interaction):
        try:
            amount = balance_use_case.get_amount(interaction.user.id)
            embed = balance_embed_message(interaction.user.mention, amount)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"Error in balance command: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @bot.tree.command(name="daily", description="Collect your daily coins reward")
    async def daily(interaction: discord.Interaction):
        try:
            user_id = interaction.user.id
            success, reward = balance_use_case.get_daily(user_id)

            if success:
                embed = daily_reward_message(interaction.user.mention, reward)
                await interaction.response.send_message(embed=embed)
            else:
                embed = daily_not_reward_message(interaction.user.mention)
                await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(f"Error in daily command: {e}")
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @bot.tree.command(name="pay", description="Send coins to another user")
    @app_commands.describe(
        receiver="The user to send coins to",
        amount="The amount of coins to send"
    )
    async def pay(interaction: discord.Interaction, receiver: discord.Member, amount: int):
        try:
            transfer_coins_use_case.execute(interaction.user.id, receiver.id, amount)
            await interaction.response.send_message(
                embed=payment_success_embed(interaction.user.mention, receiver.mention, amount)
            )
        except Exception as e:
            print(f"Error in pay command: {e}")

            if isinstance(e, InsufficientBalanceException):
                await interaction.response.send_message(
                    embed=create_error_embed(
                        title="💸 Insufficient Funds! 💸",
                        description=f"{interaction.user.mention}, you don't have enough coins!",
                        fields=[("Current Balance", f"{e.current_balance} coins", True)],
                        color=0xFF0000
                    ),
                    ephemeral=True
                )
            elif isinstance(e, InvalidAmountException):
                await interaction.response.send_message(
                    embed=create_error_embed(
                        title="❌ Invalid Amount! ❌",
                        description=f"{interaction.user.mention}, you must enter a positive number!",
                        color=0xFFA500
                    ),
                    ephemeral=True
                )
            elif isinstance(e, SelfPaymentException):
                await interaction.response.send_message(
                    embed=create_error_embed(
                        title="🤔 Self Payment? 🤔",
                        description=f"{interaction.user.mention}, you can't pay yourself!",
                        footer="Try paying someone else instead!",
                        color=0xFFFF00
                    ),
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    embed=create_error_embed(
                        title="⚠️ Unexpected Error! ⚠️",
                        description="Something went wrong with the payment",
                        footer=str(e),
                        color=0x000000
                    ),
                    ephemeral=True
                )

    @bot.tree.command(name="flip", description="Flip a coin and bet coins on the outcome")
    @app_commands.describe(
        side="Choose 'heads' or 'tails'",
        amount="Amount of coins to bet"
    )
    @app_commands.choices(side=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails")
    ])
    async def flip(interaction: discord.Interaction, side: str, amount: int):
        try:
            user_id = interaction.user.id
            success, chosen_face = gambling_use_case.flip(user_id, side, amount)

            # First respond with the result of the coin flip
            await interaction.response.send_message(embed=flip_result_embed(chosen_face))

            # Then follow up with win/loss message
            if success:
                await interaction.followup.send(embed=flip_reward_embed(interaction.user.mention, amount))
            else:
                await interaction.followup.send(embed=flip_loss_embed(interaction.user.mention, amount))
        except Exception as e:
            print(f"Error in flip command: {e}")

            if isinstance(e, ValueError):
                current_balance = int(e.args[0]) if e.args else 0
                await interaction.response.send_message(
                    embed=user_can_not_pay(interaction.user.mention, current_balance),
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(f"Error: {e}", ephemeral=True)

    @bot.tree.command(name="help", description="Shows all available commands")
    async def help(interaction: discord.Interaction):
        help_embed = discord.Embed(title="Cheapo Commands", color=discord.Color.yellow())

        help_embed.description = """
💰 **Economy Commands**:
- `/balance` - Peek at your coin stash. How much dough you got, hotshot?
- `/daily` - Grab your daily moolah! But don't get greedy—once a day, see?
- `/pay [user] [amount]` - Send some of your hard-earned cash to another user.

🎲 **Gambling Commands**:
- `/flip [heads/tails] [amount]` -  Flip a coin and bet your bottom dollar. Heads or tails, baby!
        """

        await interaction.response.send_message(embed=help_embed)

    # Return the setter function so we can set use cases from outside
    return set_use_cases
