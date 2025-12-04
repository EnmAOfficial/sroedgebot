import discord
from discord import app_commands
from discord.ext import commands
from utils.config_help_theme import HELP_THEME
from utils.help_embed_fx import fancy_embed

class HelpView(discord.ui.View):
    def __init__(self, pages, active="main"):
        super().__init__(timeout=180)
        self.pages = pages
        self.active = active
        self.update_buttons()

    def update_buttons(self):
        for child in self.children:
            if hasattr(child, "custom_id"):
                child.style = (
                    discord.ButtonStyle.success 
                    if child.custom_id == self.active else discord.ButtonStyle.secondary
                )

    async def switch(self, interaction, category):
        self.active = category
        self.update_buttons()
        await interaction.response.edit_message(embed=self.pages[category], view=self)

    @discord.ui.button(label="Ana Menü", custom_id="main")
    async def main(self, interaction, button):
        await self.switch(interaction, "main")

    @discord.ui.button(label="Otomatik Mesaj", custom_id="automsg")
    async def automsg(self, interaction, button):
        await self.switch(interaction, "automsg")

    @discord.ui.button(label="Giveaway", custom_id="giveaway")
    async def giveaway(self, interaction, button):
        await self.switch(interaction, "giveaway")

    @discord.ui.button(label="Temizleme", custom_id="delete")
    async def delete(self, interaction, button):
        await self.switch(interaction, "delete")

    @discord.ui.button(label="AI Moderasyon", custom_id="ai")
    async def ai(self, interaction, button):
        await self.switch(interaction, "ai")

    @discord.ui.button(label="Template", custom_id="template")
    async def template(self, interaction, button):
        await self.switch(interaction, "template")

    @discord.ui.button(label="İstatistik", custom_id="stats")
    async def stats(self, interaction, button):
        await self.switch(interaction, "stats")


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Tüm komutlar için kategorili yardım menüsünü gösterir.")
    async def help_cmd(self, interaction: discord.Interaction):

        pages = {}

        # ANA SAYFA
        pages["main"] = fancy_embed(
            f"{HELP_THEME['main']} SROEdgeBot Yardım Menüsü",
            "Bir kategori seçerek detaylara ulaşabilirsiniz."
        )

        # OTOMATIK MESAJ
        pages["automsg"] = fancy_embed(
            f"{HELP_THEME['automsg']} Otomatik Mesaj Komutları",
            "/automsg_create\n/automsg_list\n/automsg_delete"
        )

        # GIVEAWAY
        pages["giveaway"] = fancy_embed(
            f"{HELP_THEME['giveaway']} Giveaway Komutları",
            "/giveaway_start\n/giveaway_end\n/giveaway_list"
        )

        # DELETE
        pages["delete"] = fancy_embed(
            f"{HELP_THEME['delete']} Temizleme Komutları",
            "/delete_last\n/delete_user"
        )

        # AI
        pages["ai"] = fancy_embed(
            f"{HELP_THEME['ai']} AI Moderasyon Sistemi",
            "Toxicity analiz + otomatik ceza sistemi."
        )

        # TEMPLATE
        pages["template"] = fancy_embed(
            f"{HELP_THEME['template']} Template Sistemi",
            "/template_save\n/template_apply"
        )

        # STATS
        pages["stats"] = fancy_embed(
            f"{HELP_THEME['stats']} Kullanıcı İstatistikleri",
            "/stats → Pozitif / negatif puanlar."
        )

        view = HelpView(pages)

        await interaction.response.send_message(embed=pages["main"], view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))
