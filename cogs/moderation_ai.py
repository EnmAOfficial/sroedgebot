import discord
from discord.ext import commands
from utils.storage import load, save
from utils.ai_analyzer import analyze_message
from utils.logger import log
from config import AI_WARN_LEVELS
from datetime import timedelta

WARN_PATH = "data/warnings.json"

class AIMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        guild_id = message.guild.id
        uid = str(message.author.id)

        # AI ANALİZİ
        analysis = await analyze_message(message.content)
        toxicity = analysis["toxicity"]
        score = analysis["score"]
        category = analysis["category"]

        # PUAN KAYDI
        points = load("data/points.json", {})
        if uid not in points:
            points[uid] = {"positive": 0, "negative": 0}

        if score == 1:
            points[uid]["positive"] += 1
        elif score == -1:
            points[uid]["negative"] += 1

        save("data/points.json", points)

        # SADECE NEGATİF DURUMLARDA MODERASYON
        if score == -1:

            warnings = load(WARN_PATH, {})
            if uid not in warnings:
                warnings[uid] = {"warnings": 0}

            warnings[uid]["warnings"] += 1
            save(WARN_PATH, warnings)

            warn = warnings[uid]["warnings"]

            # LOG
            await log(
                self.bot,
                guild_id,
                "AI-MOD",
                f"❗ NEGATİF MESAJ ALGILANDI\n"
                f"Kullanıcı: {message.author}\n"
                f"Toxicity: {toxicity}%\n"
                f"Kategori: {category}\n"
                f"Uyarı seviyesi: {warn}\n"
                f"Mesaj: {message.content}"
            )

            # UYARI SEVİYELERİ
            if warn == AI_WARN_LEVELS["warn_1"]:
                try:
                    await message.author.send("⚠️ **Uyarı:** Davranışların uygunsuz. Lütfen dikkatli ol.")
                except:
                    pass

            elif warn == AI_WARN_LEVELS["timeout_60s"]:
                await message.author.timeout(timedelta(seconds=60))
                await log(self.bot, guild_id, "AI-MOD", f"{message.author} → 60 saniye timeout")

            elif warn == AI_WARN_LEVELS["timeout_5m"]:
                await message.author.timeout(timedelta(minutes=5))
                await log(self.bot, guild_id, "AI-MOD", f"{message.author} → 5 dakika timeout")

            elif warn >= AI_WARN_LEVELS["timeout_10m"]:
                await message.author.timeout(timedelta(minutes=10))
                await log(self.bot, guild_id, "AI-MOD", f"{message.author} → 10 dakika timeout")

async def setup(bot):
    await bot.add_cog(AIMod(bot))
