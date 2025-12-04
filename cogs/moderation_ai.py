import discord
from discord.ext import commands
from utils.storage import load, save
from utils.ai_analyzer import analyze_message
from config import AI_WARN_LEVELS, LOG_CHANNEL_ID
from datetime import timedelta

WARN_PATH = "data/warnings.json"


# ---------------------------------------------------
# EMBED RENK SEÇİCİ
# ---------------------------------------------------
def get_embed_color(category, toxicity):

    category = category.lower()

    if toxicity >= 75:
        return 0xff0000  # 🔥 çok agresif – kırmızı

    if category in ["hakaret", "kufur", "taciz", "tehdit"]:
        return 0xff6a00  # 🟧 agresif – turuncu

    if toxicity >= 35:
        return 0xffc800  # 🟨 hafif tehdit – sarı

    if toxicity <= 0:
        return 0x2ecc71  # 🟩 pozitif – yeşil

    return 0x3498db  # 🟦 nötr – mavi


# ---------------------------------------------------
# AI MOD COG
# ---------------------------------------------------
class AIMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # ---------------------------------------------------
    # LOG EMBED SİSTEMİ
    # ---------------------------------------------------
    async def send_embed_log(self, message, toxicity, category, warn_count, action):

        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        embed = discord.Embed(
            title="🛡️ AI Moderasyon Sistemi – Uygunsuz Mesaj Tespit Edildi",
            color=get_embed_color(category, toxicity)
        )

        embed.set_thumbnail(url=message.author.display_avatar.url)

        embed.add_field(name="👤 Kullanıcı", value=f"{message.author.mention}", inline=False)
        embed.add_field(name="🔥 Toxicity", value=f"%{toxicity}", inline=True)
        embed.add_field(name="🏷️ Kategori", value=category.capitalize(), inline=True)
        embed.add_field(name="⚠️ Uyarı Seviyesi", value=str(warn_count), inline=True)

        embed.add_field(name="🛠️ Uygulanan İşlem", value=action, inline=False)
        embed.add_field(name="💬 Mesaj İçeriği", value=f"```{message.content}```", inline=False)

        embed.set_footer(text="SroEdge AI Moderasyon • EnmAOfficial")
        
        await channel.send(embed=embed)


    # ---------------------------------------------------
    # MESAJ LİSTEYİCİ (ANA MODERASYON)
    # ---------------------------------------------------
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        guild_id = message.guild.id
        uid = str(message.author.id)

        # ---------------------------
        # 1) AI ANALİZ
        # ---------------------------
        analysis = await analyze_message(message.content)
        toxicity = analysis["toxicity"]
        score = analysis["score"]
        category = analysis["category"]

        # ---------------------------
        # 2) PUAN SİSTEMİ
        # ---------------------------
        points = load("data/points.json", {})
        if uid not in points:
            points[uid] = {"positive": 0, "negative": 0}

        if score == 1:
            points[uid]["positive"] += 1
        elif score == -1:
            points[uid]["negative"] += 1

        save("data/points.json", points)

        # ---------------------------
        # 3) NEGATİF DEĞİLSE ÇIK
        # ---------------------------
        if score != -1:
            return

        # ---------------------------
        # 4) UYARI SİSTEMİ
        # ---------------------------
        warnings = load(WARN_PATH, {})
        if uid not in warnings:
            warnings[uid] = {"warnings": 0}

        warnings[uid]["warnings"] += 1
        save(WARN_PATH, warnings)

        warn = warnings[uid]["warnings"]

        action = "📌 Uyarı kaydedildi (şimdilik işlem uygulanmadı)"  # default


        # ---------------------------
        # 5) CEZA SİSTEMİ (ORTA SEVİYE)
        # ---------------------------
        if warn == AI_WARN_LEVELS["warn_1"]:
            try:
                await message.author.send("⚠️ **Uyarı:** Davranışlarınız uygunsuz bulunmuştur. Lütfen dikkatli olun.")
            except:
                pass
            action = "⚠️ 1. Uyarı gönderildi"

        elif warn == AI_WARN_LEVELS["timeout_60s"]:
            await message.author.timeout(timedelta(seconds=60), reason="AI Moderasyon (Orta Seviye)")
            action = "⏳ 60 saniyelik timeout uygulandı"

        elif warn == AI_WARN_LEVELS["timeout_5m"]:
            await message.author.timeout(timedelta(minutes=5), reason="AI Moderasyon (Orta Seviye)")
            action = "⏳ 5 dakikalık timeout uygulandı"

        elif warn >= AI_WARN_LEVELS["timeout_10m"]:
            await message.author.timeout(timedelta(minutes=10), reason="AI Moderasyon (Ciddi Seviye)")
            action = "⏳ 10 dakikalık timeout uygulandı"


        # ---------------------------
        # 6) RENKLİ EMBED LOG GÖNDERME
        # ---------------------------
        await self.send_embed_log(
            message=message,
            toxicity=toxicity,
            category=category,
            warn_count=warn,
            action=action
        )


async def setup(bot):
    await bot.add_cog(AIMod(bot))
