import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        help_embed = discord.Embed(title="Cheapo Commands", color=discord.Color.yellow())

        image = discord.File("src/assets/bot_icon.png", "bot_icon.png")
        help_embed.set_thumbnail(url="attachment://bot_icon.png")

        help_embed.description = """
💰 **Economy Commands**:
- `c!balance` - Check your coin balance.
- `c!daily` - Claim your daily reward (once per day).
        """

        # Send the embed
        channel = self.get_destination()
        await channel.send(embed=help_embed, file=image)
