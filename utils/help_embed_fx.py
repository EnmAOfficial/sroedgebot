import discord

def fancy_embed(title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blurple()
    )
    embed.set_footer(text="SROEdge Bot • by EnmAOfficial")
    return embed
