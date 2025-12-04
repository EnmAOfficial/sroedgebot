import discord
from discord import app_commands
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        # Load sırasında komutu zorla register ediyoruz
        self.bot.tree.add_command(self.help_cmd)

    @app_commands.command(name="help", description="Komut listesini gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📘 SROEdgeBot Yardım Menüsü",
            description="Aşağıda tüm komutlar listelenmiştir.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🕒 Otomatik Mesaj",
            value="`/automsg_create` - Tarihli mesaj oluştur\n"
                  "`/automsg_list` - Aktif mesajları göster\n"
                  "`/automsg_delete` - Mesaj sil",
            inline=False
        )

        embed.add_field(
            name="🎁 Çekiliş Sistemi",
            value="`/giveaway_start` – Çekiliş başlat",
            inline=False
        )

        embed.add_field(
            name="🧹 Mesaj Silme",
            value="`/delete_last` – Son mesajları sil\n"
                  "`/delete_user` – Kullanıcı mesajlarını sil",
            inline=False
        )

        embed.add_field(
            name="📊 AI Moderasyon",
            value="`/stats` – Kullanıcı puanlarını göster",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
