import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# =============================
# ENV YÜKLE
# =============================
load_dotenv()

# =============================
# BOT AYARLARI
# =============================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Yüklenecek tüm COG dosyaları
COGS = [
    "automsg",
    "delete",
    "giveaway",
    "moderation_ai",
    "stats",
    "template",
    "help",        # /help çalışması için gerekli
]

# =============================
# BOT BAŞLATILDIĞINDA ÇALIŞIR
# =============================
@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

    # COG'LARI YÜKLE
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"[OK] {cog} yüklendi.")
        except Exception as e:
            print(f"[HATA] {cog} yüklenemedi → {e}")

    # SLASH KOMUT SENKRON
    try:
        synced = await bot.tree.sync()
        print(f"[SYNC] {len(synced)} komut başarıyla senkron edildi.")
    except Exception as e:
        print(f"[SYNC HATASI] Slash komutlar senkron edilemedi → {e}")

    print("Bot tamamen hazır! ✔")


# =============================
# BOTU ÇALIŞTIR
# =============================
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("❌ DISCORD_TOKEN .env dosyasında bulunamadı!")

bot.run(token)
