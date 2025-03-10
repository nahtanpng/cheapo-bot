from discord.ext import commands

from .balance import balance_command, balance_slash, daily, daily_slash


def setup(bot: commands.Bot):
    bot.tree.command(name="balance", description="Check your coin balance. :coin:")(balance_slash)
    bot.command(name="balance")(balance_command)
    bot.tree.command(name="daily", description="Reward your daily reward!")(daily_slash)
    bot.command()(daily)
