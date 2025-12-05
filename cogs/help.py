import discord
from discord import app_commands
from discord.ext import commands
from utils.config_help_theme import HELP_THEME
from utils.help_embed_fx import fancy_embed


class HelpView(discord.ui.View):
    def __init__(self, pages, author_id, active="main"):
        super().__init__(timeout=180)
        self.pages = pages
        self.author_id = author_id  # Güvenlik
        self.active = active
        self.update_styles()

    # =============================
    # BUTON RENKLERİNİ GÜNCELLE
    # =============================
    def update_styles(self):
        for child in self.children:
            if not hasattr(child, "custom_id"):
                continue

            if child.custom_id == self.active:
                child.style = discord.ButtonStyle.success
            else:
                # Her kategoriye özel renk
                color_map = {
                    "main": discord.ButtonStyle.primary,
                    "automsg": discord.ButtonStyle.secondary,
                    "giveaway": discord.ButtonStyle.blurple,
                    "delete": discord.ButtonStyle.danger,
                    "ai": discord.ButtonStyle.secondary,
                    "template": discord.ButtonStyle.primary,
                    "stats": discord.ButtonStyle.blurple,
                }
                child.style = color_map.get(child.custom_id, discord.ButtonStyle.secondary)

    # =============================
    # BUTON KONTROL & CATEGORY SWITCH
    # =============================
    async def switch(self, interaction, category):
        if interaction.user.id != self.author_id:
            return await interaction.response.send_message(
                "❌ Bu menüyü sadece açan kişi kontrol edebilir.",
                ephemeral=True
            )

        self.active = category
        self.update_styles()

        await interaction.response.edit_message(
            embed=self.pages[category],
            view=self
        )

    # ============================
    #   TIMEOUT → Disable Buttons
    # ============================
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

    # ============================
    #   BUTONLAR
    # ============================
    @discord.ui.button(label="Ana Menü", emoji="🏠", custom_id="main", row=0)
    async def main(self, interaction, button):
        await self.switch(interaction, "main")

    @discord.ui.button(label="Otomatik Mesaj", emoji="💬", custom_id="automsg", row=0)
    async def automsg(self, interaction, button):
        await self.switch(interaction, "automsg")

    @discord.ui.button(label="Giveaway", emoji="🎉", custom_id="giveaway", row=0)
    async def giveaway(self, interaction, button):
        await self.switch(interaction, "giveaway")

    @discord.ui.button(label="Temizleme", emoji="🧹", custom_id="delete", row=1)
    async def delete(self, interaction, button):
        await self.switch(interaction, "delete")

    @discord.ui.button(label="AI Moderasyon", emoji="🤖", custom_id="ai", row=1)
    async def ai(self, interaction, button):
        await self.switch(interaction, "ai")

    @discord.ui.button(label="Template", emoji="📦", custom_id="template", row=1)
    async def template(self, interaction, button):
        await self.switch(interaction, "template")

    @discord.ui.button(label="İstatistik", emoji="📊", custom_id="stats", row=2)
    async def stats(self, interaction, button):
        await self.switch(interaction, "stats")


# ==============================================
# COG – SLASH HELP KOMUTU
# ==============================================
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Bot yardım menüsünü açar.")
    async def help_cmd(self, interaction: discord.Interaction):

        bot_avatar = self.bot.user.avatar or self.bot.user.default_avatar

        pages = {}

        pages["main"] = fancy_embed(
            f"{HELP_THEME['main']} Genel Yardım Menüsü",
            "Kategoriler arasında gezinmek için aşağıdaki butonları kullanın.\n\n"
            f"👤 **Kullanıcı:** {interaction.user.mention}\n"
            f"🤖 **Bot:** {self.bot.user.name}"
        )
        pages["main"].set_thumbnail(url=str(bot_avatar))

        pages["automsg"] = fancy_embed(
            f"{HELP_THEME['automsg']} Otomatik Mesaj",
            "`/automsg create`\n`/automsg list`\n`/automsg delete`"
        )

        pages["giveaway"] = fancy_embed(
            f"{HELP_THEME['giveaway']} Giveaway",
            "`/giveaway start`\n`/giveaway reroll`"
        )

        pages["delete"] = fancy_embed(
            f"{HELP_THEME['delete']} Temizleme",
            "`/delete_last`\n`/delete_user`"
        )

        pages["ai"] = fancy_embed(
            f"{HELP_THEME['ai']} AI Moderasyon",
            "Toxicity analiz + otomatik uyarı sistemi"
        )

        pages["template"] = fancy_embed(
            f"{HELP_THEME['template']} Template",
            "`/template install`"
        )

        pages["stats"] = fancy_embed(
            f"{HELP_THEME['stats']} İstatistik",
            "`/stats` kullanıcı puanlarını gösterir"
        )

        view = HelpView(pages, interaction.user.id)

        await interaction.response.send_message(
            embed=pages["main"],
            view=view
        )


async def setup(bot):
    await bot.add_cog(Help(bot))
