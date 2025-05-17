# main.py
import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.application.use_cases.balance import BalanceUseCase
from src.application.use_cases.gambling import GamblingUseCase
from src.application.use_cases.transfer_coins import TransferCoinsUseCase
from src.domain.services.balance_service import BalanceService
from src.domain.services.gambling_service import GamblingService
from src.domain.services.payment_service import PaymentService
from src.infrastructure.db.balance_repository_impl import BalanceRepositoryImpl
from src.infrastructure.db.gambling_repository_impl import GamblingRepositoryImpl
# Import your repositories and services
from src.infrastructure.db.init_db import Database
from src.infrastructure.db.user_repository_impl import UserRepositoryImpl
from src.presentation.commands.balance.balance_commands import BalanceCommands
from src.presentation.events.events_setup import events_setup
from src.presentation.setup_slash_commands import setup_slash_commands

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv('TOKEN')

# Create the bot instance
bot = commands.Bot(command_prefix="c!", intents=intents)

# Store use cases at global level
balance_use_case = None
gambling_use_case = None
transfer_coins_use_case = None
set_slash_command_use_cases = None


async def setup_bot():
    global balance_use_case, gambling_use_case, transfer_coins_use_case, set_slash_command_use_cases

    # Initialize database
    database = Database()
    database.init_db()
    conn = database.conn

    # Initialize repositories
    balance_repository = BalanceRepositoryImpl(conn)
    user_repository = UserRepositoryImpl(conn)
    gambling_repository = GamblingRepositoryImpl(conn)

    # Initialize services
    balance_service = BalanceService(balance_repository, user_repository)
    gambling_service = GamblingService(balance_repository, gambling_repository)
    payment_service = PaymentService(balance_repository)

    # Initialize use cases
    balance_use_case = BalanceUseCase(balance_service)
    gambling_use_case = GamblingUseCase(gambling_service)
    transfer_coins_use_case = TransferCoinsUseCase(payment_service)

    # Set up events
    events_setup(bot)

    # Initialize slash commands and get the setter function
    set_slash_command_use_cases = await setup_slash_commands(bot)

    # Traditional commands can still be registered for backward compatibility
    await bot.add_cog(BalanceCommands(balance_use_case))

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')
        print(f'Bot is connected to {len(bot.guilds)} guilds.')

        # Now that the bot is ready, we can set the use cases for the slash commands
        if set_slash_command_use_cases:
            set_slash_command_use_cases(balance_use_case, gambling_use_case, transfer_coins_use_case)
            print("Use cases have been set for slash commands")

        def print_welcome_message():
            gold = "\033[38;2;255;189;48m"
            yellow = "\033[33;1m"
            reset = "\033[0m"

            welcome_message = f"""
            {gold}╔════════════════════════════════════════════════════════════════╗
            ║                     @                            @             ║
            ║    @	 @@@@@@                                                @ ║
            ║      	@@       @     @  @@@@@@   @@@@@    @@@@@    @@@@        ║
            ║       @@       @@   @@   @@     @@   @@  @@   @@  @@  @@       ║
            ║       @@       @@@@@@@   @@@@   @@   @@  @@   @@  @@  @@       ║
            ║       @@       @@   @@   @@     @@@@@@@  @@@@@@   @@  @@       ║
            ║ @      @@@@@@	 @     @  @@@@@@  @@   @@  @@	     @@@@        ║
            ║                                                            @   ║
            ╚════════════════════════════════════════════════════════════════╝
                                  Welcome to Cheapo Bot!                       
            {reset}"""

            print(welcome_message)

        print_welcome_message()

        # Sync commands with Discord after setting use cases
        try:
            print("Syncing commands with Discord...")
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")


# Run the bot
async def main():
    try:
        async with bot:
            await setup_bot()
            await bot.start(TOKEN)
    finally:
        # Clean up resources if needed
        print("Bot has shut down.")


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())