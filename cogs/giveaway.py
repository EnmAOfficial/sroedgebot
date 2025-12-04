import discord
from discord.ext import commands
from discord import app_commands
from utils.permissions import is_allowed
from utils.logger import log
import random

class GiveawayButton(discord.ui.View):
    def __init__(self, entrants):
        super().__init__(timeout=None)
        self.entrants = entrants

    @discord.ui.button(label="🎉 Katıl", style=discord.ButtonStyle.green)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user.id in self.entrants:
            return await interaction.response.send_message("Zaten katıldın!", ephemeral=True)

        self.entrants.append(user.id)
        await interaction.response.send_message("🎉 Katıldın!", ephemeral=True)

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="giveaway_start", description="Çekiliş başlat.")
    async def giveaway_start(self, interaction: discord.Interaction,
                             duration_minutes: int,
                             *, prize: str):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("Yetkin yok.", ephemeral=True)

        entrants = []
        view = GiveawayButton(entrants)

        embed = discord.Embed(title="🎉 ÇEKİLİŞ BAŞLADI!", description=f"Ödül: **{prize}**")
        embed.set_footer(text=f"Bitiş: {duration_minutes} dakika")

        msg = await interaction.response.send_message(embed=embed, view=view)
        result_msg = await interaction.original_response()

        await log(self.bot, interaction.guild_id, "GIVEAWAY", f"{prize} ödüllü çekiliş başladı.")

        await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(minutes=duration_minutes))

        if entrants:
            winner = random.choice(entrants)
            await result_msg.edit(content=f"🎉 **Kazanan:** <@{winner}>", embed=None, view=None)
            await log(self.bot, interaction.guild_id, "GIVEAWAY", f"Kazanan: <@{winner}>")
        else:
            await result_msg.edit(content="Kimse katılmadı.", embed=None, view=None)

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
