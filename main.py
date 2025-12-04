import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# ENV YÜKLE
load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "automsg",
    "delete",
    "giveaway",
    "moderation_ai",
    "stats",
    "template",
    "help",
]

# =============================
# COG'LARI BOT BAŞLAMADAN ÖNCE YÜKLE
# =============================
async def load_all_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"[OK] {cog} yüklendi.")
        except Exception as e:
            print(f"[HATA] {cog} yüklenemedi → {e}")


# =============================
# BOT HAZIR OLDUĞUNDA
# =============================
@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

    # Slash komut sync
    try:
        synced = await bot.tree.sync()
        print(f"[SYNC] {len(synced)} komut senkron edildi.")
    except Exception as e:
        print(f"[SYNC HATASI] {e}")

    print("Bot tamamen hazır ✔")


# =============================
# BOTU BAŞLAT
# =============================
async def main():
    await load_all_cogs()
    await bot.start(os.getenv("DISCORD_TOKEN"))

import asyncio
asyncio.run(main())
