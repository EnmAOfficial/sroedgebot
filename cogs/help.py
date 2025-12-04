# cogs/help.py

import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Tüm komutları kategori şeklinde gösterir.")
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📘 SROEDGE BOT YARDIM MENÜSÜ",
            description="Aşağıda tüm kullanılabilir komutlar kategorilere ayrılmış şekilde listelenmiştir.",
            color=0x3498db
        )

        # TEMPLATE
        embed.add_field(
            name="🧩 TEMPLATE (Şablon Sistemi)",
            value=(
                "**/template_save** – Sunucu şablonunu kaydeder.\n"
                "**/template_apply** – Kaydedilen şablonu uygular.\n"
            ),
            inline=False
        )

        # AUTOMSG
        embed.add_field(
            name="⏰ AUTOMSG (Zamanlanmış Mesaj)",
            value=(
                "**/automsg_create** – Zamanlanmış mesaj oluştur.\n"
                "**/automsg_list** – Tüm zamanlanmış mesajları görüntüle.\n"
                "**/automsg_delete** – ID’ye göre sil.\n"
            ),
            inline=False
        )

        # DELETE
        embed.add_field(
            name="🧹 DELETE (Mesaj Silme)",
            value=(
                "**/delete_last** – Son X mesajı sil.\n"
                "**/delete_user** – Bir kullanıcının mesajlarını sil.\n"
            ),
            inline=False
        )

        # GIVEAWAY
        embed.add_field(
            name="🎉 GIVEAWAY (Butonlu Çekiliş)",
            value=(
                "**/giveaway_start** – Süreli çekiliş başlat.\n"
            ),
            inline=False
        )

        # STATS
        embed.add_field(
            name="📊 STATS (Kullanıcı İstatistikleri)",
            value=(
                "**/stats** – Kullanıcı puanlarını ve sunucuya giriş tarihini gösterir.\n"
            ),
            inline=False
        )

        # HELP
        embed.add_field(
            name="ℹ️ HELP",
            value="**/help** – Bu menüyü görüntüler.",
            inline=False
        )

        embed.set_footer(text="SroEdge Community – EnmA tarafından geliştirildi.")
        embed.set_thumbnail(url="https://i.imgur.com/B6qV4KC.png")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
