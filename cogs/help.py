import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Tüm komut listesini gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):
        
        embed = discord.Embed(
            title="📘 SROEdgeBot Yardım Menüsü",
            description="Aşağıda tüm kullanabileceğin komutlar listelenmiştir.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🕒 Otomatik Mesaj",
            value="`/automsg_create` → Belirlenen tarih/saatte mesaj gönderir\n"
                  "`/automsg_list` → Aktif otomatik mesajları gösterir\n"
                  "`/automsg_delete` → Bir otomatik mesajı siler",
            inline=False
        )

        embed.add_field(
            name="🎁 Çekiliş Sistemi",
            value="`/giveaway_start` → Çekiliş başlat",
            inline=False
        )

        embed.add_field(
            name="🧹 Silme Komutları",
            value="`/delete_last` → Son X mesajı siler\n"
                  "`/delete_user` → Kullanıcının mesajlarını siler",
            inline=False
        )

        embed.add_field(
            name="📊 İstatistik",
            value="`/stats` → Kullanıcının AI moderasyon puanlarını gösterir",
            inline=False
        )

        embed.add_field(
            name="📑 Sunucu Şablonu",
            value="`/template_save` → Şablon alır\n"
                  "`/template_apply` → Şablonu uygular",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
