import discord

COIN = "<:coin:1354468542287839344>"

def payment_success_embed(sender: str, receiver: str, amount: int) -> discord.Embed:
    embed = discord.Embed(
        color=0x2ECC71,  # Green for success
        title="💰 Payment Processed! 💰",
        description=(
            f"**{sender}** just sent a payment to **{receiver}**\n\n"
            f"**Amount Transferred:** {'💸' * min(3, amount//100)} **{amount} coins** {'💸' * min(3, amount//100)}\n\n"
            f"*\"Money makes the world go 'round!\"*"
        ),
    )
    return embed

def balance_embed_message(user_mention: str, result: int):
    embed = discord.Embed(
        title="💰 Your Balance 💰",
        description=f"**{user_mention}, you’ve got a shiny pile of {result} coins!** {COIN}",
        color=0xFFD700
    )
    embed.set_footer(text="Keep stackin’ that dough, big shot—you’re on a roll! 🤑")
    return embed


def balance_embed_empty_message(user_mention: str):
    embed = discord.Embed(
        title="💔 Your Balance 💔",
        description=f"**{user_mention}, your pockets are empty... 0 coins to your name!** {COIN}",
        color=0xFF0000
    )
    embed.set_footer(text="Time to get to work, kiddo—those coins won’t earn themselves! 😅")
    return embed


def daily_reward_message(user_mention: str, reward: int):
    embed = discord.Embed(
        title="🎉 Daily Reward Claimed! 🎉",
        description=f"**{user_mention}, you just claimed your daily reward of {reward} coins!** :moneybag:\n\n*Keep stackin’ that dough, big shot—you’re on a roll!* 🤑",
        color=0xFFD700
    )
    return embed


def daily_not_reward_message(user_mention: str):
    embed = discord.Embed(
        title="⏰ Daily Cooldown ⏰",
        description=f"**{user_mention}, you’ve already claimed your daily reward today!**\n\n*Patience is a virtue, kiddo—come back tomorrow for more shiny coins!* 💰",
        color=0xFFA500
    )
    return embed


def create_error_embed(title: str, description: str, fields: list = None,
                       footer: str = None, color: int = 0xFF0000) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )

    if fields:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

    if footer:
        embed.set_footer(text=footer)

    return embed