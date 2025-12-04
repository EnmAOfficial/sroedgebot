import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
from datetime import datetime
import asyncio
from utils.permissions import is_allowed
from utils.storage import load, save
from utils.logger import log

SCHEDULE_PATH = "data/schedules.json"

class AutoMSG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_messages.start()

    @tasks.loop(seconds=30)
    async def check_messages(self):
        data = load(SCHEDULE_PATH, {})

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        for mid, info in list(data.items()):
            if info["time"] == now:
                channel = self.bot.get_channel(info["channel"])

                if channel:
                    await channel.send(info["message"])
                    await log(self.bot, channel.guild.id, "AUTOMSG", f"Zamanlanmış mesaj gönderildi: {info['message']}")

                del data[mid]
                save(SCHEDULE_PATH, data)

    @app_commands.command(name="automsg_create", description="Zamanlanmış mesaj oluştur.")
    async def automsg_create(self, interaction: discord.Interaction,
                             channel: discord.TextChannel,
                             datetime_str: str,
                             *, message: str):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except:
            return await interaction.response.send_message("❌ Format yanlış. Örnek: 2025-01-15 18:30")

        data = load(SCHEDULE_PATH, {})
        data[str(len(data) + 1)] = {
            "channel": channel.id,
            "time": datetime_str,
            "message": message
        }

        save(SCHEDULE_PATH, data)

        await log(self.bot, interaction.guild_id, "AUTOMSG", f"Yeni otomatik mesaj zamanlandı ({datetime_str})")

        await interaction.response.send_message("✅ Zamanlanmış mesaj oluşturuldu.")

    @app_commands.command(name="automsg_list", description="Zamanlanmış mesajları göster.")
    async def automsg_list(self, interaction: discord.Interaction):
        data = load(SCHEDULE_PATH, {})

        if not data:
            return await interaction.response.send_message("Kayıtlı mesaj yok.")

        embed = discord.Embed(title="⏰ Zamanlanmış Mesajlar")

        for mid, info in data.items():
            embed.add_field(
                name=f"ID: {mid}",
                value=f"Kanal: <#{info['channel']}>\nZaman: {info['time']}\nMesaj: {info['message']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="automsg_delete", description="Zamanlanmış mesajı sil.")
    async def automsg_delete(self, interaction: discord.Interaction, msg_id: str):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.")

        data = load(SCHEDULE_PATH, {})

        if msg_id not in data:
            return await interaction.response.send_message("❌ Böyle bir ID yok.")

        del data[msg_id]
        save(SCHEDULE_PATH, data)

        await interaction.response.send_message("🗑️ Silindi.")

async def setup(bot):
    await bot.add_cog(AutoMSG(bot))
