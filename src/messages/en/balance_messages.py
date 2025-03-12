import discord


def balance_embed_message(interaction: str, result):
    embed = discord.Embed(
        title="💰 Your Balance 💰",
        description=f"**{interaction}, you’ve got a shiny pile of {result[0]} coins!** :coin:",
        color=0xFFD700
    )
    embed.set_footer(text="Keep stackin’ that dough, big shot—you’re on a roll! 🤑")
    return embed


def balance_embed_empty_message(interaction: str):
    embed = discord.Embed(
        title="💔 Your Balance 💔",
        description=f"**{interaction}, your pockets are empty... 0 coins to your name!** :coin:",
        color=0xFF0000
    )
    embed.set_footer(text="Time to get to work, kiddo—those coins won’t earn themselves! 😅")
    return embed


def daily_reward_message(interaction: str, reward: int):
    embed = discord.Embed(
        title="🎉 Daily Reward Claimed! 🎉",
        description=f"**{interaction}, you just claimed your daily reward of {reward} coins!** :moneybag:\n\n*Keep stackin’ that dough, big shot—you’re on a roll!* 🤑",
        color=0xFFD700
    )
    return embed


def daily_not_reward_message(interaction: str):
    embed = discord.Embed(
        title="⏰ Daily Cooldown ⏰",
        description=f"**{interaction}, you’ve already claimed your daily reward today!**\n\n*Patience is a virtue, kiddo—come back tomorrow for more shiny coins!* 💰",
        color=0xFFA500
    )
    return embed
