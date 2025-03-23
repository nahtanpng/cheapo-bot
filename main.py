import os
from itertools import cycle

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from src.application.use_cases.balance import BalanceUseCase
from src.application.use_cases.transfer_coins import TransferCoinsUseCase
from src.domain.services.balance_service import BalanceService
from src.domain.services.payment_service import PaymentService
from src.infrastructure.db.balance_repository_impl import BalanceRepositoryImpl
from src.infrastructure.db.init_db import Database
from src.infrastructure.db.user_repository_impl import UserRepositoryImpl
from src.presentation.commands.balance.balance_commands import BalanceCommands
from src.presentation.commands.help_command import CustomHelpCommand
from src.presentation.commands.pay_command import PayCommand

# Setting .env variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="c!", intents=intents, help_command=CustomHelpCommand())

db = Database()
db.init_db()
balance_repository = BalanceRepositoryImpl(db.conn)
user_repository = UserRepositoryImpl(db.conn)
payment_service = PaymentService(balance_repository)
balance_service = BalanceService(balance_repository, user_repository)
balance_use_case = BalanceUseCase(balance_service)
transfer_coins_use_case = TransferCoinsUseCase(payment_service)

bot_statuses = cycle(["Use c!help 🎲", "You're up 🃏", "How about a game? 🎲"])


@tasks.loop(seconds=5)
async def change_bot_statuses():
    await bot.change_presence(activity=discord.CustomActivity(next(bot_statuses)))


@bot.event
async def on_ready():
    # async with aiohttp.ClientSession() as session:
    #     async with session.get("https://cdn.discordapp.com/attachments/1350148775196233759/1350165015411429508/bot_icon_1.png?ex=67d5bea8&is=67d46d28&hm=b033124e3bdbbf5d3bd41d98eb876b205a2dc23db215603e630ce11ea1e3eb57&") as response:
    #         if response.status == 200:
    #             img = await response.read()
    #             await bot.user.edit(avatar=img)
    #             print("Avatar uploaded!")
    #         else:
    #             print(f"Failed to fetch image: HTTP {response.status}")
    #
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(
    #             "https://cdn.discordapp.com/attachments/1350148775196233759/1350164631766962186/Teste_3.png?ex=67d5be4d&is=67d46ccd&hm=dbe0e69324ca6adb05495dd52ce32956268e436f409d564475a8a785b9a269eb&") as response:
    #         if response.status == 200:
    #             img = await response.read()
    #             await bot.user.edit(banner=img)
    #             print("Banner uploaded!")
    #         else:
    #             print(f"Failed to fetch image: HTTP {response.status}")

    await bot.tree.sync()
    change_bot_statuses.start()
    await bot.change_presence(activity=discord.CustomActivity("Use c!help 🎲"))
    print(f'Logged in as {bot.user.name}')

    await bot.add_cog(PayCommand(transfer_coins_use_case))
    await bot.add_cog(BalanceCommands(balance_use_case))


bot.run(TOKEN)
