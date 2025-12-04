import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_allowed
from utils.logger import log

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete_last", description="Son X mesajı sil.")
    async def delete_last(self, interaction: discord.Interaction, count: int):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("Yetkin yok.", ephemeral=True)

        deleted = await interaction.channel.purge(limit=count)
        await log(self.bot, interaction.guild_id, "DELETE", f"{len(deleted)} mesaj silindi.")

        await interaction.response.send_message(f"🧹 {len(deleted)} mesaj silindi.")

    @app_commands.command(name="delete_user", description="Belirli bir kişinin mesajlarını siler.")
    async def delete_user(self, interaction: discord.Interaction, user: discord.Member, limit: int = 100):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("Yetkin yok.", ephemeral=True)

        deleted = await interaction.channel.purge(limit=limit, check=lambda m: m.author.id == user.id)
        await log(self.bot, interaction.guild_id, "DELETE", f"{user} → {len(deleted)} mesajı silindi.")

        await interaction.response.send_message(f"{user} kullanıcısının {len(deleted)} mesajı silindi.")

async def setup(bot):
    await bot.add_cog(Delete(bot))
