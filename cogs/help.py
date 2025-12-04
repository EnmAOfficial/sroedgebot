import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        # BOT AÇILIR AÇILMAZ ZORLA REGISTER ET
        try:
            self.bot.tree.add_command(self.help_cmd)
        except:
            pass

    @app_commands.command(name="help", description="Tüm komutların listesini gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📘 SROEdgeBot Yardım Menüsü",
            description="Aşağıdaki komutları kullanabilirsiniz:",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="🕒 Otomatik Mesaj",
            value=(
                "`/automsg_create` — Zamanlı mesaj oluştur\n"
                "`/automsg_list` — Zamanlı mesajları listele\n"
                "`/automsg_delete` — Mesajı sil"
            ),
            inline=False
        )

        embed.add_field(
            name="🧹 Temizlik",
            value=(
                "`/delete_last` — Son mesajları sil\n"
                "`/delete_user` — Kullanıcıya ait mesajları sil"
            ),
            inline=False
        )

        embed.add_field(
            name="🎁 Çekiliş",
            value="`/giveaway_start` — Çekiliş başlat",
            inline=False
        )

        embed.add_field(
            name="📊 İstatistik",
            value="`/stats` — Pozitif/Negatif puanlar",
            inline=False
        )

        embed.set_footer(text="SROEdgeBot © EnmA")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))
