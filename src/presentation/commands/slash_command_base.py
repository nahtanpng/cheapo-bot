from discord.ext import commands


class SlashCommandBase:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def setup(self):
        pass

    async def sync_commands(self):
        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(f"Error syncing commands: {e}")
