import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

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

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"[OK] {cog} yüklendi.")
        except Exception as e:
            print(f"[HATA] {cog} yüklenemedi → {e}")

    try:
        synced = await bot.tree.sync()
        print(f"Slash komutlar senkron edildi ({len(synced)})")
    except Exception as e:
        print("Slash sync hatası:", str(e))

bot.run(os.getenv("DISCORD_TOKEN"))
