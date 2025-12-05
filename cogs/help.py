class HelpView(discord.ui.View):
    def __init__(self, pages, active="main"):
        super().__init__(timeout=180)
        self.pages = pages
        self.active = active
        self.apply_colors()

    # ===============================================
    # BUTON RENK ve STİLLERİ
    # ===============================================
    def apply_colors(self):
        for child in self.children:
            if not hasattr(child, "custom_id"):
                continue

            cid = child.custom_id

            # Renk atamaları
            if cid == "main":
                child.style = discord.ButtonStyle.success      # Yeşil
            elif cid == "automsg":
                child.style = discord.ButtonStyle.primary      # Mavi
            elif cid == "giveaway":
                child.style = discord.ButtonStyle.blurple      # Mor
            elif cid == "delete":
                child.style = discord.ButtonStyle.danger       # Kırmızı
            elif cid == "ai":
                child.style = discord.ButtonStyle.secondary    # Gri
            elif cid == "template":
                child.style = discord.ButtonStyle.secondary    # Gri
            elif cid == "stats":
                child.style = discord.ButtonStyle.success      # Yeşil

    # ===============================================
    # SAYFA DEĞİŞTİRME FONKSİYONU
    # ===============================================
    async def switch(self, interaction, category):
        self.active = category
        await interaction.response.edit_message(
            embed=self.pages[category],
            view=self
        )

    # ===============================================
    #              BUTONLAR (İKONLU)
    # ===============================================

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
