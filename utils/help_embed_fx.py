import discord

EMBED_COLOR = 0x2F3136  # Discord koyu arka plan rengi

def fancy_embed(title, description=""):
    embed = discord.Embed(
        title=title,
        description=description,
        color=EMBED_COLOR
    )
    
    # Thumbnail koymuyoruz → mesaj temiz kalıyor.
    embed.set_footer(text="SROEdgeBot • Yardım Sistemi")
    return embed
