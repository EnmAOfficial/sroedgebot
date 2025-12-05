import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_allowed
from utils.logger import log
import datetime


class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ================================
    #  /delete_last → Son X mesajı sil
    # ================================
    @app_commands.command(name="delete_last", description="Son X mesajı sil.")
    async def delete_last(self, interaction: discord.Interaction, count: int):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

        deleted = await interaction.channel.purge(limit=count)
        await log(self.bot, interaction.guild_id, "DELETE", f"{len(deleted)} mesaj silindi.")

        await interaction.response.send_message(f"🧹 {len(deleted)} mesaj silindi.")

    # ================================
    #  /delete_user → Belirli kişinin mesajlarını sil
    # ================================
    @app_commands.command(name="delete_user", description="Belirli bir kişinin mesajlarını siler.")
    async def delete_user(self, interaction: discord.Interaction, user: discord.Member, limit: int = 100):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

        deleted = await interaction.channel.purge(
            limit=limit,
            check=lambda m: m.author.id == user.id
        )

        await log(self.bot, interaction.guild_id, "DELETE", f"{user} → {len(deleted)} mesajı silindi.")
        await interaction.response.send_message(f"🧹 {user} kullanıcısının {len(deleted)} mesajı silindi.")

    # ===========================================
    #  /delete_all → KANALDAKİ TÜM MESAJLARI SİL
    # ===========================================
    @app_commands.command(name="delete_all", description="Bu kanaldaki TÜM mesajları siler.")
    async def delete_all(self, interaction: discord.Interaction):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

        channel = interaction.channel

        await interaction.response.defer()

        # Önce 14 günden eski mesaj olup olmadığını kontrol ediyoruz
        oldest = None
        async for msg in channel.history(limit=1, oldest_first=True):
            oldest = msg

        if oldest:
            msg_age = (discord.utils.utcnow() - oldest.created_at).days
        else:
            msg_age = 0

        # ============================
        #  MOD 1 → Normal Purge
        # ============================
        if msg_age < 14:
            deleted = await channel.purge(limit=None)
            await log(self.bot, interaction.guild_id, "DELETE", f"Kanal tamamen temizlendi. {len(deleted)} mesaj silindi.")

            return await interaction.followup.send(
                f"🧹 Kanal tamamen temizlendi. Toplam **{len(deleted)}** mesaj silindi."
            )

        # ============================
        #  MOD 2 → KANALI KLONLAMA
        # ============================
        new_channel = await channel.clone(reason="Tüm mesajları temizlemek için kanal sıfırlandı.")
        await new_channel.edit(position=channel.position)

        await channel.delete(reason="Tüm mesajlar temizleniyor.")

        await log(self.bot, interaction.guild_id, "DELETE", f"Kanal klonlama yöntemi ile sıfırlandı.")

        await new_channel.send("🧹 **Kanal tamamen sıfırlandı!** (14 günden eski mesajlar bulunduğu için klonlama yapıldı.)")

    # ===========================================
    async def setup(bot):
        await bot.add_cog(Delete(bot))
