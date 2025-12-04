import discord
import random

GRADIENTS = [
    0x3498db, 0x2980b9, 0x8e44ad, 0x9b59b6,
    0xe74c3c, 0xc0392b, 0x2ecc71, 0x27ae60,
    0xf1c40f, 0xf39c12, 0x1abc9c, 0x16a085,
]

def fancy_embed(title, description=""):
    embed = discord.Embed(
        title=title,
        description=description,
        color=random.choice(GRADIENTS)
    )
    embed.set_thumbnail(url="https://i.imgur.com/bE2iHcJ.png")  # efekt görüntüsü
    embed.set_footer(text="SROEdgeBot • Dynamic UI System")
    return embed
