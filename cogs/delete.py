import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from utils.permissions import is_allowed
from utils.logger import log
from datetime import timedelta


class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =====================================================
    # /delete_last → Son X mesajı sil
    # =====================================================
    @app_commands.command(
        name="delete_last",
        description="Belirtilen sayıda son mesajı siler."
    )
    async def delete_last(self, interaction: discord.Interaction, count: int):

        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )

        deleted = await interaction.channel.purge(limit=count)
        await log(self.bot, interaction.guild_id, "DELETE", f"{len(deleted)} mesaj silindi.")

        await interaction.response.send_message(
            f"🧹 **{len(deleted)} mesaj silindi.**",
            ephemeral=False
        )

    # =====================================================
    # /delete_user → Bir kullanıcının mesajlarını sil
    # =====================================================
    @app_commands.command(
        name="delete_user",
        description="Belirlenen üyenin mesajlarını siler."
    )
    async def delete_user(self, interaction: discord.Interaction,
                          user: discord.Member,
                          limit: int = 100):

        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )

        deleted = await interaction.channel.purge(
            limit=limit,
            check=lambda m: m.author.id == user.id
        )

        await log(self.bot, interaction.guild_id, "DELETE",
                  f"{user} → {len(deleted)} mesajı silindi.")

        await interaction.response.send_message(
            f"🧹 **{user} kullanıcısına ait {len(deleted)} mesaj silindi.**"
        )

    # =====================================================
    # /delete_all → Kanaldaki TÜM mesajları sil
    # =====================================================
    @app_commands.command(
        name="delete_all",
        description="Bu kanaldaki TÜM mesajları siler."
    )
    async def delete_all(self, interaction: discord.Interaction):

        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message(
                "❌ Bu komutu kullanma yetkin yok.",
                ephemeral=True
            )

        channel = interaction.channel

        await interaction.response.defer(ephemeral=True)

        # Kanaldaki en eski mesaja bakıyoruz
        async for msg in channel.history(limit=1, oldest_first=True):
            oldest_msg = msg
            break
        else:
            return await interaction.followup.send("Kanal zaten boş.")

        msg_age = (discord.utils.utcnow() - oldest_msg.created_at).days

        # ============================
        #   MOD 1 → Normal Purge (14 günden küçükse)
        # ============================
        if msg_age < 14:
            deleted = await channel.purge(limit=None)
            await log(self.bot, interaction.guild_id, "DELETE",
                      f"Kanal purge yöntemiyle temizlendi. {len(deleted)} mesaj silindi.")

            return await interaction.followup.send(
                f"🧹 **Kanal tamamen temizlendi! ({len(deleted)} mesaj silindi)**"
            )

        # ============================
        #   MOD 2 → Klonlama Yöntemi (14 günden eski mesaj varsa)
        # ============================
        new_channel = await channel.clone(reason="Kanal tamamen sıfırlandı.")
        await new_channel.edit(position=channel.position)

        await channel.delete(reason="Kanal sıfırlandı (14+ gün mesaj).")
        await log(self.bot, new_channel.guild.id, "DELETE", "Kanal klonlama yöntemi ile sıfırlandı.")

        await new_channel.send("🧹 **Kanal tamamen sıfırlandı!** (14 günden eski mesaj bulunduğu için klonlama yapıldı.)")

        return

# =====================================================
# COG SETUP (EN KRİTİK KISIM)
# Bu olmazsa komutlar ASLA görünmez!!!
# =====================================================
async def setup(bot):
    await bot.add_cog(Delete(bot))
