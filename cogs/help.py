import discord
from discord.ext import commands
from discord import app_commands

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # TEMPLATE
    @discord.ui.button(label="Template", style=discord.ButtonStyle.primary)
    async def template(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🧩 TEMPLATE KOMUTLARI", color=0x3498db)
        embed.add_field(name="/template_save", value="Sunucu şablonunu kaydeder.", inline=False)
        embed.add_field(name="/template_apply", value="Kayıtlı şablonu uygular.", inline=False)
        embed.set_footer(text="SroEdge Community – EnmA")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # AUTOMSG
    @discord.ui.button(label="AutoMSG", style=discord.ButtonStyle.success)
    async def automsg(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="⏰ AUTOMSG KOMUTLARI", color=0x2ecc71)
        embed.add_field(name="/automsg_create", value="Zamanlanmış mesaj oluştur.", inline=False)
        embed.add_field(name="/automsg_list", value="Zamanlanmış mesajları listeler.", inline=False)
        embed.add_field(name="/automsg_delete", value="Zamanlanmış mesajı siler.", inline=False)
        embed.set_footer(text="SroEdge Community – EnmA")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # DELETE
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🧹 DELETE KOMUTLARI", color=0xe74c3c)
        embed.add_field(name="/delete_last", value="Son X mesajı siler.", inline=False)
        embed.add_field(name="/delete_user", value="Belirli kişinin mesajlarını siler.", inline=False)
        embed.set_footer(text="SroEdge Community – EnmA")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # GIVEAWAY
    @discord.ui.button(label="Giveaway", style=discord.ButtonStyle.secondary)
    async def giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="🎉 GIVEAWAY", color=0x8e44ad)
        embed.add_field(name="/giveaway_start", value="Butonlu çekiliş başlatır.", inline=False)
        embed.set_footer(text="SroEdge Community – EnmA")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # STATS
    @discord.ui.button(label="Stats", style=discord.ButtonStyle.primary)
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="📊 STATS", color=0x1abc9c)
        embed.add_field(name="/stats", value="Kullanıcı istatistiklerini gösterir.", inline=False)
        embed.set_footer(text="SroEdge Community – EnmA")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Tüm komutları kategori butonları ile gösterir.")
    async def help(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="📘 SROEDGE BOT YARDIM MENÜSÜ",
            description="Aşağıdaki butonlara tıklayarak komut kategorilerini görüntüleyebilirsin.",
            color=0x3498db
        )

        view = HelpView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))
