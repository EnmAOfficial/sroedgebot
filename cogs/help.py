import discord
from discord import app_commands
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self, pages, active="main"):
        super().__init__(timeout=180)
        self.pages = pages
        self.active = active
        self.update_buttons()

    # ------------------------
    # BUTON RENKLERINI AYARLA
    # ------------------------
    def update_buttons(self):
        for child in self.children:
            if hasattr(child, "custom_id"):
                child.style = (
                    discord.ButtonStyle.success if child.custom_id == self.active 
                    else discord.ButtonStyle.secondary
                )

    # ------------------------
    # ANASAYFA
    # ------------------------
    @discord.ui.button(label="Ana Menü", style=discord.ButtonStyle.secondary, custom_id="main")
    async def main_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "main"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["main"], view=self)

    # ------------------------
    # KATEGORILER
    # ------------------------
    @discord.ui.button(label="Otomatik Mesaj", style=discord.ButtonStyle.secondary, custom_id="automsg")
    async def automsg_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "automsg"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["automsg"], view=self)

    @discord.ui.button(label="Giveaway", style=discord.ButtonStyle.secondary, custom_id="giveaway")
    async def giveaway_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "giveaway"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["giveaway"], view=self)

    @discord.ui.button(label="Temizleme", style=discord.ButtonStyle.secondary, custom_id="delete")
    async def delete_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "delete"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["delete"], view=self)

    @discord.ui.button(label="AI Moderasyon", style=discord.ButtonStyle.secondary, custom_id="ai")
    async def ai_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "ai"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["ai"], view=self)

    @discord.ui.button(label="Template", style=discord.ButtonStyle.secondary, custom_id="template")
    async def template_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "template"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["template"], view=self)

    @discord.ui.button(label="İstatistik", style=discord.ButtonStyle.secondary, custom_id="stats")
    async def stats_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.active = "stats"
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages["stats"], view=self)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Botun tüm kategorilerini gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):

        pages = {}

        # ---------------------
        # ANA SAYFA
        # ---------------------
        pages["main"] = discord.Embed(
            title="📘 SROEdgeBot — Ana Yardım Menüsü",
            description="Aşağıdaki kategorilerden birini seçebilirsin:",
            color=0x3498db
        )
        pages["main"].add_field(name="🕒 Otomatik Mesaj", value="Planlı mesaj sistemleri.", inline=False)
        pages["main"].add_field(name="🎁 Giveaway", value="Ödüllü çekiliş modülü.", inline=False)
        pages["main"].add_field(name="🧹 Temizleme", value="Mesaj silme işlemleri.", inline=False)
        pages["main"].add_field(name="🧠 AI Moderasyon", value="Uygunsuz mesaj analizi.", inline=False)
        pages["main"].add_field(name="📦 Template", value="Sunucu yapılandırma sistemi.", inline=False)
        pages["main"].add_field(name="📊 İstatistik", value="Pozitif/negatif puan sistemi.", inline=False)

        # ---------------------
        # OTOMATIK MESAJ
        # ---------------------
        pages["automsg"] = discord.Embed(
            title="🕒 Otomatik Mesaj Komutları",
            description="Planlı mesaj oluşturmak için kullanılır:",
            color=0x2980b9
        )
        pages["automsg"].add_field(name="/automsg_create", value="Belirli tarihte mesaj gönderir.", inline=False)
        pages["automsg"].add_field(name="/automsg_list", value="Planlı mesaj listesini gösterir.", inline=False)
        pages["automsg"].add_field(name="/automsg_delete", value="Mesaj ID'si ile siler.", inline=False)

        # ---------------------
        # GIVEAWAY
        # ---------------------
        pages["giveaway"] = discord.Embed(
            title="🎁 Giveaway Komutları",
            description="Sunucu çekilişlerini yönet:",
            color=0x2ecc71
        )
        pages["giveaway"].add_field(name="/giveaway_start", value="Çekiliş başlatır.", inline=False)
        pages["giveaway"].add_field(name="/giveaway_end", value="Çekilişi sonlandırır.", inline=False)

        # ---------------------
        # DELETE
        # ---------------------
        pages["delete"] = discord.Embed(
            title="🧹 Temizleme Komutları",
            description="Mesaj silmek için kullanılan komutlar:",
            color=0xe74c3c
        )
        pages["delete"].add_field(name="/delete_last", value="Son X mesajı siler.", inline=False)
        pages["delete"].add_field(name="/delete_user", value="Belirli kişinin mesajlarını temizler.", inline=False)

        # ---------------------
        # AI
        # ---------------------
        pages["ai"] = discord.Embed(
            title="🧠 AI Moderasyon",
            description="AI mesaj analizi ve ceza sistemi:",
            color=0x9b59b6
        )
        pages["ai"].add_field(name="Toxicity Analizi", value="Uygunsuz mesajı tespit eder.", inline=False)
        pages["ai"].add_field(name="Timeout Sistemi", value="Uyarı seviyesine göre ceza verir.", inline=False)

        # ---------------------
        # TEMPLATE
        # ---------------------
        pages["template"] = discord.Embed(
            title="📦 Template Sistemi",
            description="Sunucu yapısını kaydedip uygulama:",
            color=0xf1c40f
        )
        pages["template"].add_field(name="/template_save", value="Sunucu düzenini kaydeder.", inline=False)
        pages["template"].add_field(name="/template_apply", value="Kaydedilmiş düzeni uygular.", inline=False)

        # ---------------------
        # STATS
        # ---------------------
        pages["stats"] = discord.Embed(
            title="📊 Kullanıcı İstatistikleri",
            description="Pozitif / negatif AI puanlarını gösterir:",
            color=0x1abc9c
        )
        pages["stats"].add_field(name="/stats", value="Kullanıcı puanlarını görüntüler.", inline=False)

        view = HelpView(pages)

        await interaction.response.send_message(embed=pages["main"], view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))
