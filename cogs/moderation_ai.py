import discord
from discord.ext import commands
from utils.storage import load, save
from utils.ai_analyzer import analyze_message
from utils.logger import log
from datetime import timedelta

WARN_PATH = "data/warnings.json"

class AIMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Bot mesajlarını yok say
        if message.author.bot:
            return
        
        guild_id = message.guild.id
        uid = str(message.author.id)

        # AI mesaj analizi (pozitif / negatif / nötr)
        score = await analyze_message(message.content)

        points_data = load("data/points.json", {})
        if uid not in points_data:
            points_data[uid] = {"positive": 0, "negative": 0}

        # Puan kaydı
        if score == 1:
            points_data[uid]["positive"] += 1
        elif score == -1:
            points_data[uid]["negative"] += 1

        save("data/points.json", points_data)

        # Sadece negatif mesajlarda moderasyon tetiklensin
        if score == -1:
            warnings = load(WARN_PATH, {})
            if uid not in warnings:
                warnings[uid] = {"warnings": 0}

            warnings[uid]["warnings"] += 1
            save(WARN_PATH, warnings)

            warn_count = warnings[uid]["warnings"]

            # Uyarı Seviyeleri
            if warn_count == 3:
                # İlk uyarı
                try:
                    await message.author.send("⚠️ **Uyarı:** Davranışların uygunsuz bulunuyor. Lütfen dikkatli ol.")
                except:
                    pass

                await log(self.bot, guild_id, "AI-MOD", f"{message.author} ilk uyarısını aldı.")

            elif warn_count == 5:
                # 60 saniye timeout
                await message.author.timeout(timedelta(seconds=60), reason="AI Moderasyon")
                await log(self.bot, guild_id, "AI-MOD", f"{message.author} 60 saniyelik timeout aldı.")

            elif warn_count == 7:
                # 5 dakika timeout
                await message.author.timeout(timedelta(minutes=5), reason="AI Moderasyon")
                await log(self.bot, guild_id, "AI-MOD", f"{message.author} 5 dakikalık timeout aldı.")

            elif warn_count >= 10:
                # 10 dakika timeout
                await message.author.timeout(timedelta(minutes=10), reason="AI Moderasyon (Ciddi Seviye)")
                await log(self.bot, guild_id, "AI-MOD", f"{message.author} ciddi seviyede davranışı nedeniyle 10 dakika timeout aldı.")

async def setup(bot):
    await bot.add_cog(AIMod(bot))
