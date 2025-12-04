import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_allowed
from utils.storage import load, save
from utils.logger import log

class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="template_save", description="Sunucunun şablonunu kaydeder.")
    async def template_save(self, interaction: discord.Interaction):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.")

        guild = interaction.guild

        data = {
            "roles": [r.name for r in guild.roles],
            "channels": [c.name for c in guild.channels]
        }

        save(f"data/templates/{guild.id}.json", data)

        await log(self.bot, guild.id, "TEMPLATE", "Şablon kaydedildi.")
        await interaction.response.send_message("✅ Şablon kaydedildi.")

    @app_commands.command(name="template_apply", description="Kayıtlı şablonu uygular.")
    async def template_apply(self, interaction: discord.Interaction):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("Yetkin yok.")

        guild = interaction.guild
        data = load(f"data/templates/{guild.id}.json", None)

        if not data:
            return await interaction.response.send_message("❌ Bu sunucu için şablon yok.")

        for ch in data["channels"]:
            await guild.create_text_channel(ch)

        await log(self.bot, guild.id, "TEMPLATE", "Şablon uygulandı.")
        await interaction.response.send_message("✨ Şablon uygulandı.")

async def setup(bot):
    await bot.add_cog(Template(bot))
