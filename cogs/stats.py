import discord
from discord.ext import commands
from discord import app_commands
from utils.storage import load

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="Kullanıcı istatistiklerini gösterir.")
    async def stats(self, interaction: discord.Interaction, user: discord.Member):
        data = load("data/points.json", {})

        u = data.get(str(user.id), {"positive": 0, "negative": 0})

        embed = discord.Embed(title=f"{user.name} İstatistikleri")
        embed.add_field(name="Sunucuya Katılım", value=user.joined_at.strftime("%Y-%m-%d"))
        embed.add_field(name="Pozitif", value=u["positive"])
        embed.add_field(name="Negatif", value=u["negative"])
        embed.add_field(name="Genel Puan", value=u["positive"] - u["negative"])

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Stats(bot))
