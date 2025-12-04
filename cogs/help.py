import discord
from discord import app_commands
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Tüm komut kategorilerini gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📘 SROEdgeBot Yardım Menüsü",
            description="Aşağıdan istediğiniz kategoriye bakabilirsiniz:",
            color=0x3498db
        )

        embed.add_field(
            name="🕒 Otomatik Mesaj Sistemi",
            value=(
                "**/automsg_create** → Belirli tarih/saat için mesaj planla\n"
                "**/automsg_list** → Tüm planlı mesajları göster\n"
                "**/automsg_delete** → ID ile planlı mesaj sil"
            ),
            inline=False
        )

        embed.add_field(
            name="🎁 Giveaway Sistemi",
            value=(
                "**/giveaway_start** → Ödüllü çekiliş başlat\n"
                "**/giveaway_end** → Çekilişi bitir\n"
                "**/giveaway_list** → Aktif çekilişleri listele"
            ),
            inline=False
        )

        embed.add_field(
            name="🧹 Temizleme Komutları",
            value=(
                "**/delete_last** → Son X mesajı sil\n"
                "**/delete_user** → Belirli kullanıcının mesajlarını sil"
            ),
            inline=False
        )

        embed.add_field(
            name="🧠 AI Moderasyon Sistemi",
            value=(
                "Mesajları otomatik analiz eder, puanlar ve loglar.\n"
                "Uygunsuz mesaj → uyarı, timeout vb. yaptırımlar uygular."
            ),
            inline=False
        )

        embed.add_field(
            name="📦 Template / Sunucu Şablon Sistemi",
            value=(
                "**/template_save** → Sunucudaki kanal/rol düzenini kaydet\n"
                "**/template_apply** → Kayıtlı şablonu uygulayıp sunucuyu düzenle"
            ),
            inline=False
        )

        embed.add_field(
            name="📊 Kullanıcı İstatistikleri",
            value=(
                "**/stats** → Kullanıcının pozitif / negatif AI puanlarını göster\n"
            ),
            inline=False
        )

        embed.set_footer(text="SROEdgeBot • Geliştirici: EnmAOfficial", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
