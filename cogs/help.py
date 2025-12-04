import discord
from discord import app_commands
from discord.ext import commands
from utils.config_help_theme import HELP_THEME
from utils.help_embed_fx import fancy_embed


# ======================================================
#     PREMIUM HELP VIEW – Butonlu Çoklu Menü Sistemi
# ======================================================
class HelpView(discord.ui.View):
    def __init__(self, pages, active="main"):
        super().__init__(timeout=180)
        self.pages = pages
        self.active = active
        self.update_buttons()

    def update_buttons(self):
        # Aktif kategori yeşil gözükecek
        for child in self.children:
            if hasattr(child, "custom_id"):
                child.style = (
                    discord.ButtonStyle.success
                    if child.custom_id == self.active else discord.ButtonStyle.secondary
                )

    async def switch(self, interaction, category):
        self.active = category
        self.update_buttons()
        await interaction.response.edit_message(
            embed=self.pages[category],
            view=self
        )

    @discord.ui.button(label="Ana Menü", custom_id="main", row=0)
    async def main(self, interaction, button):
        await self.switch(interaction, "main")

    @discord.ui.button(label="Otomatik Mesaj", custom_id="automsg", row=0)
    async def automsg(self, interaction, button):
        await self.switch(interaction, "automsg")

    @discord.ui.button(label="Giveaway", custom_id="giveaway", row=0)
    async def giveaway(self, interaction, button):
        await self.switch(interaction, "giveaway")

    @discord.ui.button(label="Temizleme", custom_id="delete", row=1)
    async def delete(self, interaction, button):
        await self.switch(interaction, "delete")

    @discord.ui.button(label="AI Moderasyon", custom_id="ai", row=1)
    async def ai(self, interaction, button):
        await self.switch(interaction, "ai")

    @discord.ui.button(label="Template", custom_id="template", row=1)
    async def template(self, interaction, button):
        await self.switch(interaction, "template")

    @discord.ui.button(label="İstatistik", custom_id="stats", row=2)
    async def stats(self, interaction, button):
        await self.switch(interaction, "stats")


# ======================================================
#                 HELP COG – Slash Komutu
# ======================================================
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Bot yardım menüsünü açar.")
    async def help_cmd(self, interaction: discord.Interaction):

        user_avatar = interaction.user.avatar or interaction.user.default_avatar
        bot_avatar = self.bot.user.avatar or self.bot.user.default_avatar

        # ====== Embed sayfaları ======
        pages = {}

        pages["main"] = fancy_embed(
            f"{HELP_THEME['main']} Genel Yardım Menüsü",
            "**Kategori seçmek için aşağıdaki butonları kullanın.**\n\n"
            f"👤 **Kullanıcı:** {interaction.user.mention}\n"
            f"🤖 **Bot:** {self.bot.user.name}\n"
        )
        pages["main"].set_thumbnail(url=str(bot_avatar))

        pages["automsg"] = fancy_embed(
            f"{HELP_THEME['automsg']} Otomatik Mesaj Sistemi",
            "• `/automsg create`\n• `/automsg list`\n• `/automsg delete`"
        )

        pages["giveaway"] = fancy_embed(
            f"{HELP_THEME['giveaway']} Giveaway Sistemi",
            "• `/giveaway start`\n• `/giveaway reroll`"
        )

        pages["delete"] = fancy_embed(
            f"{HELP_THEME['delete']} Temizleme Komutları",
            "• `/delete_last` → Son mesajları siler\n"
            "• `/delete_user` → Belirli kullanıcının mesajlarını siler"
        )

        pages["ai"] = fancy_embed(
            f"{HELP_THEME['ai']} AI Moderasyon",
            "• Toxicity algılama\n"
            "• Otomatik uyarı sistemi\n"
            "• 60s / 5m / 10m timeout"
        )

        pages["template"] = fancy_embed(
            f"{HELP_THEME['template']} Sunucu Template Sistemi",
            "• `/template install`"
        )

        pages["stats"] = fancy_embed(
            f"{HELP_THEME['stats']} Kullanıcı İstatistikleri",
            "• `/stats` → Pozitif / negatif puanları gösterir"
        )

        view = HelpView(pages)

        await interaction.response.send_message(
            embed=pages["main"],
            view=view
        )


async def setup(bot):
    await bot.add_cog(Help(bot))
