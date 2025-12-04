import discord
from discord.ext import commands
from discord import app_commands

HELP_BANNER = "https://i.imgur.com/qM2wnIE.jpeg"  # İstersen değiştiririm

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Template", emoji="🧩", style=discord.ButtonStyle.primary)
    async def template(self, interaction, _):
        embed = discord.Embed(title="🧩 TEMPLATE KOMUTLARI", color=0x3498db)
        embed.add_field(name="/template_save", value="Sunucu şablonunu kaydeder.")
        embed.add_field(name="/template_apply", value="Şablonu uygular.")
        embed.set_image(url=HELP_BANNER)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="AutoMSG", emoji="⏰", style=discord.ButtonStyle.success)
    async def automsg(self, interaction, _):
        embed = discord.Embed(title="⏰ AUTOMSG", color=0x2ecc71)
        embed.add_field(name="/automsg_create", value="Zamanlanmış mesaj oluşturur.")
        embed.add_field(name="/automsg_list", value="Mesajları listeler.")
        embed.add_field(name="/automsg_delete", value="Silme işlemi.")
        embed.set_image(url=HELP_BANNER)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Delete", emoji="🧹", style=discord.ButtonStyle.danger)
    async def delete(self, interaction, _):
        embed = discord.Embed(title="🧹 DELETE", color=0xe74c3c)
        embed.add_field(name="/delete_last", value="Son X mesajı sil.")
        embed.add_field(name="/delete_user", value="Kullanıcı mesajları sil.")
        embed.set_image(url=HELP_BANNER)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Giveaway", emoji="🎉", style=discord.ButtonStyle.secondary)
    async def giveaway(self, interaction, _):
        embed = discord.Embed(title="🎉 GIVEAWAY", color=0x8e44ad)
        embed.add_field(name="/giveaway_start", value="Butonlu çekiliş başlatır.")
        embed.set_image(url=HELP_BANNER)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Stats", emoji="📊", style=discord.ButtonStyle.primary)
    async def stats(self, interaction, _):
        embed = discord.Embed(title="📊 STATS", color=0x1abc9c)
        embed.add_field(name="/stats", value="Kullanıcı istatistikleri.")
        embed.set_image(url=HELP_BANNER)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Tüm komutları kategori butonları ile gösterir.")
    async def help(self, interaction):
        embed = discord.Embed(
            title="📘 SROEDGE BOT YARDIM MENÜSÜ",
            description="Aşağıdaki butonlara tıklayarak komut kategorilerini görüntüleyebilirsin.",
            color=0x3498db
        )
        embed.set_image(url=HELP_BANNER)
        view = HelpView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
