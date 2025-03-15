import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        help_embed = discord.Embed(title="Cheapo Commands", color=discord.Color.yellow())

        image = discord.File("src/assets/images/bot_icon.png", "bot_icon.png")
        help_embed.set_thumbnail(url="attachment://bot_icon.png")

        help_embed.description = """
💰 **Economy Commands**:
- `c!balance` - Peek at your coin stash. How much dough you got, hotshot?
- `c!daily` - Grab your daily moolah! But don’t get greedy—once a day, see?

🎲 **Gambling Commands**:
- `c!flip <side> <amount> ` -  Flip a coin and bet your bottom dollar. Heads or tails, baby!
        """

        # Send the embed
        channel = self.get_destination()
        await channel.send(embed=help_embed, file=image)
