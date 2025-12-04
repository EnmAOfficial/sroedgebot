import discord
from discord.ext import commands
from utils.storage import load, save
from utils.ai_analyzer import analyze_message
from utils.logger import log

class AIMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        score = await analyze_message(message.content)

        path = f"data/points.json"
        data = load(path, {})

        uid = str(message.author.id)

        if uid not in data:
            data[uid] = {"positive": 0, "negative": 0}

        if score == 1:
            data[uid]["positive"] += 1
        elif score == -1:
            data[uid]["negative"] += 1

        save(path, data)

        await log(self.bot, message.guild.id, "AI", f"{message.author} puan aldı ({score})")

async def setup(bot):
    await bot.add_cog(AIMod(bot))
