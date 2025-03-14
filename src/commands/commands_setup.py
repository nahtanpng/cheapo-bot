from discord.ext import commands

from .balance_commands_impl import balance_command, balance_slash, daily, daily_slash, pay_command
from .gambling import flip


def commands_setup(bot: commands.Bot):
    bot.tree.command(name="balance", description="Check your coin balance. :coin:")(balance_slash)
    bot.command(name="balance")(balance_command)
    bot.tree.command(name="daily", description="Reward your daily reward!")(daily_slash)
    bot.command()(daily)
    bot.command()(flip)
    bot.command(name="pay")(pay_command)
