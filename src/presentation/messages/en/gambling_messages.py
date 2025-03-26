import discord

def user_can_not_pay(user_mention: str, balance: int) -> discord.Embed:
    embed = discord.Embed(
        color=0xFFA500,  # Orange for warning
        title="💸 BANKRUPT! 💸",
        description=(
            f"**{user_mention}**, your pockets are emptier than a desert saloon!\n\n"
            f"**Current Balance:** {balance} 💰\n\n"
            f"*\"No dough to show? Time to get workin', kiddo!\"*"
        )
    )

    return embed


def flip_reward_embed(user_mention: str, value: int) -> discord.Embed:
    embed = discord.Embed(
        color=0x00FF00,  # Green for success
        title=f"🎉 JACKPOT! 🎉",
        description=(
            f"**{user_mention}**, you nailed it!\n\n"
            f"{'💰'*2} **+{value} coins** {'💰'*2}\n\n"
            f"*\"Lady Luck's smiling on you today!\"*"
        )
    )
    embed.set_footer(text="Try your luck again?")
    return embed

def flip_loss_embed(user_mention: str, value: int) -> discord.Embed:
    embed = discord.Embed(
        color=0xFF0000,  # Red for loss
        title=f"💸 TOUGH LUCK! 💸",
        description=(
            f"**{user_mention}**, the house wins this round...\n\n"
            f"{'💨'*2} **-{value} coins** {'💨'*2}\n\n"
            f"*\"Better luck next time, champ!\"*"
        )
    )
    embed.set_footer(text="Feeling lucky for a rematch?")
    return embed


def flip_result_embed(side: str) -> discord.Embed:
    heads_emoji = "<:CoinFlipHeads:1354470047099130110>"
    tails_emoji = "<:CoinFlipTails:1354470023770542111>"

    embed = discord.Embed(color=0xFFD700)  # Gold color
    if side == "heads":
        embed.title = f"{heads_emoji} HEADS! {heads_emoji}"
        embed.description = "The coin spins through the air and lands..."
    else:
        embed.title = f"{tails_emoji} TAILS! {tails_emoji}"
        embed.description = "The coin tumbles before settling on..."
    embed.set_author(name="🎲 Coin Flip Result")

    return embed
