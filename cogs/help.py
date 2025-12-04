import discord
from discord import app_commands
from discord.ext import commands

class HelpView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=180)
        self.pages = pages

    @discord.ui.button(label="Otomatik Mesaj", style=discord.ButtonStyle.blurple)
    async def automsg(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["automsg"])

    @discord.ui.button(label="Giveaway", style=discord.ButtonStyle.green)
    async def giveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["giveaway"])

    @discord.ui.button(label="Temizleme", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["delete"])

    @discord.ui.button(label="AI Moderasyon", style=discord.ButtonStyle.gray)
    async def ai(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["ai"])

    @discord.ui.button(label="Template", style=discord.ButtonStyle.blurple)
    async def template(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["template"])

    @discord.ui.button(label="İstatistik", style=discord.ButtonStyle.green)
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["stats"])

    @discord.ui.button(label="Ana Menü", style=discord.ButtonStyle.secondary)
    async def main(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=self.pages["main"])


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Botun tüm komutlarını ve kategorilerini gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):

        pages = {}

        # 🔹 ANA SAYFA
        main_embed = discord.Embed(
            title="📘 SROEdgeBot — Yardım Menüsü",
            description="Aşağıdaki butonlardan bir kategori seçiniz:",
            color=0x3498db
        )
        main_embed.add_field(name="🕒 Otomatik Mesaj Sistemi", value="Planlı mesaj gönderme sistemi.", inline=False)
        main_embed.add_field(name="🎁 Giveaway Sistemi", value="Ödüllü çekiliş başlatma / bitirme.", inline=False)
        main_embed.add_field(name="🧹 Temizleme Komutları", value="Belirli mesajları toplu silme.", inline=False)
        main_embed.add_field(name="🧠 AI Moderasyon", value="Uygunsuz mesaj tespiti & timeout sistemi.", inline=False)
        main_embed.add_field(name="📦 Template Sistemi", value="Sunucu şablonu kaydetme / uygulama.", inline=False)
        main_embed.add_field(name="📊 Kullanıcı İstatistikleri", value="AI puanlarını görüntüleme.", inline=False)

        pages["main"] = main_embed

        # 🔹 OTOMATİK MESAJ
        pages["automsg"] = discord.Embed(
            title="🕒 Otomatik Mesaj Komutları",
            description="Planlı mesaj oluşturma ve yönetme komutları:",
            color=0x2980b9
        )
        pages["automsg"].add_field(name="/automsg_create", value="Belirli saat/tarihte gönderilecek mesaj oluşturur.", inline=False)
        pages["automsg"].add_field(name="/automsg_list", value="Planlanan tüm mesajları listeler.", inline=False)
        pages["automsg"].add_field(name="/automsg_delete", value="ID girerek seçili planlı mesajı siler.", inline=False)

        # 🔹 GIVEAWAY
        pages["giveaway"] = discord.Embed(
            title="🎁 Giveaway Komutları",
            description="Sunucuda çekiliş oluşturma ve bitirme:",
            color=0x27ae60
        )
        pages["giveaway"].add_field(name="/giveaway_start", value="Çekiliş başlatır (ödül, süre, butonlu katılım).", inline=False)
        pages["giveaway"].add_field(name="/giveaway_end", value="Aktif çekilişi manuel sonlandırır.", inline=False)
        pages["giveaway"].add_field(name="/giveaway_list", value="Devam eden çekilişleri gösterir.", inline=False)

        # 🔹 DELETE
        pages["delete"] = discord.Embed(
            title="🧹 Temizleme Komutları",
            description="Mesaj silme işlemleri:",
            color=0xe74c3c
        )
        pages["delete"].add_field(name="/delete_last", value="Son X mesajı siler.", inline=False)
        pages["delete"].add_field(name="/delete_user", value="Belirli kullanıcının mesajlarını siler.", inline=False)

        # 🔹 AI MODERASYON
        pages["ai"] = discord.Embed(
            title="🧠 AI Moderasyon Sistemi",
            description="Toxic mesaj tespiti ve ceza sistemi:",
            color=0x8e44ad
        )
        pages["ai"].add_field(name="• Uygunsuz mesaj algılama", value="AI puanlama sistemi ile toxicity tespiti.", inline=False)
        pages["ai"].add_field(name="• Otomatik uyarı sistemi", value="Warn seviyelerine göre işlem uygular.", inline=False)
        pages["ai"].add_field(name="• Timeout Ceza", value="Uyarı seviyesine göre 60s / 5m / 10m timeout.", inline=False)

        # 🔹 TEMPLATE
        pages["template"] = discord.Embed(
            title="📦 Sunucu Şablon Sistemi",
            description="Sunucu yapısını kaydetme ve uygulama:",
            color=0xf1c40f
        )
        pages["template"].add_field(name="/template_save", value="Sunucu kanal/rol yapısını kaydeder.", inline=False)
        pages["template"].add_field(name="/template_apply", value="Kaydedilmiş şablonu uygular.", inline=False)

        # 🔹 STATS
        pages["stats"] = discord.Embed(
            title="📊 Kullanıcı İstatistikleri",
            description="AI tarafından verilen pozitif/negatif puanları gösterir:",
            color=0x2ecc71
        )
        pages["stats"].add_field(name="/stats", value="Kullanıcının AI analiz puanlarını gösterir.", inline=False)

        view = HelpView(pages)

        await interaction.response.send_message(embed=pages["main"], view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))
