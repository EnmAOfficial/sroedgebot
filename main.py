import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import asyncio

# =============================
# ENV YÜKLE
# =============================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ DISCORD_TOKEN .env dosyasında bulunamadı!")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

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
# /sync SLASH KOMUTU
# =============================
@bot.tree.command(name="sync", description="Tüm slash komutlarını senkron eder.")
async def sync_commands(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

    synced = await bot.tree.sync()
    await interaction.response.send_message(
        f"✔ {len(synced)} komut başarıyla senkron edildi.",
        ephemeral=True
    )


# =============================
# ASYNC COG YÜKLEME SİSTEMİ
# =============================
async def load_all_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(f"cogs.{cog}")  # <── DOĞRU KULLANIM
            print(f"[OK] {cog} yüklendi.")
        except Exception as e:
            print(f"[HATA] {cog} → {e}")


# =============================
# BOT HAZIR OLDUĞUNDA
# =============================
@bot.event
async def on_ready():
    print(f"🔥 Bot giriş yaptı: {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"[SYNC] {len(synced)} komut senkron edildi.")
    except Exception as e:
        print(f"[SYNC HATASI] {e}")

    print("Bot tamamen hazır ✔")


# =============================
# MAIN (Render uyumlu)
# =============================
async def main():
    await load_all_cogs()  # <── ARTIK AWAIT EDİLİYOR
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
