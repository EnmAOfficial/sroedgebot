import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
from datetime import datetime, timedelta
import asyncio
from utils.permissions import is_allowed
from utils.storage import load, save
from utils.logger import log

SCHEDULE_PATH = "data/schedules.json"

class AutoMSG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_messages.start()

    # ======================================================
    #   ARKAPLAN LOOP — HER 30 SANİYEDE BİR ÇALIŞIR
    # ======================================================
    @tasks.loop(seconds=30)
    async def check_messages(self):
        data = load(SCHEDULE_PATH, {})
        now = datetime.now()

        for mid, info in list(data.items()):
            # =============================
            #   TEK SEFERLIK MESAJ
            # =============================
            if info["type"] == "once":
                if info["time"] == now.strftime("%Y-%m-%d %H:%M"):
                    channel = self.bot.get_channel(info["channel"])
                    if channel:
                        await channel.send(info["message"])
                        await log(self.bot, channel.guild.id, "AUTOMSG", f"Zamanlanmış mesaj gönderildi.")

                    del data[mid]
                    save(SCHEDULE_PATH, data)

            # =============================
            #   TEKRAR EDEN MESAJ
            # =============================
            elif info["type"] == "repeat":
                next_run = datetime.strptime(info["next_run"], "%Y-%m-%d %H:%M:%S")

                if now >= next_run:
                    channel = self.bot.get_channel(info["channel"])
                    if channel:
                        await channel.send(info["message"])
                        await log(self.bot, channel.guild.id, "AUTOMSG", f"Tekrarlayan mesaj gönderildi.")

                    # Bir sonraki çalışmayı hesapla
                    interval_sec = info["interval"]
                    new_run = now + timedelta(seconds=interval_sec)

                    info["next_run"] = new_run.strftime("%Y-%m-%d %H:%M:%S")
                    save(SCHEDULE_PATH, data)

    # ======================================================
    #   TEK SEFERLIK MESAJ OLUŞTURMA
    # ======================================================
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
            "type": "once",
            "channel": channel.id,
            "time": datetime_str,
            "message": message
        }

        save(SCHEDULE_PATH, data)
        await interaction.response.send_message("✅ Tek seferlik zamanlanmış mesaj oluşturuldu.")

    # ======================================================
    #   TEKRARLAYAN MESAJ OLUŞTURMA
    # ======================================================
    @app_commands.command(name="automsg_repeat", description="Belirli aralıklarla mesaj gönder.")
    async def automsg_repeat(self, interaction: discord.Interaction,
                             channel: discord.TextChannel,
                             interval: str,
                             *, message: str):

        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

        # Örn: 10m, 2h, 1d
        unit = interval[-1]
        value = int(interval[:-1])

        if unit == "m":
            seconds = value * 60
        elif unit == "h":
            seconds = value * 3600
        elif unit == "d":
            seconds = value * 86400
        else:
            return await interaction.response.send_message("❌ Geçersiz format. Örnek: 10m, 2h, 1d")

        now = datetime.now()
        next_run = now + timedelta(seconds=seconds)

        data = load(SCHEDULE_PATH, {})
        data[str(len(data) + 1)] = {
            "type": "repeat",
            "channel": channel.id,
            "interval": seconds,
            "next_run": next_run.strftime("%Y-%m-%d %H:%M:%S"),
            "message": message
        }

        save(SCHEDULE_PATH, data)
        await interaction.response.send_message(f"🔁 Tekrarlayan mesaj oluşturuldu. Her **{interval}**'de bir gönderilecek.")

    # ======================================================
    #   LISTELEME
    # ======================================================
    @app_commands.command(name="automsg_list", description="Zamanlanmış mesajları göster.")
    async def automsg_list(self, interaction: discord.Interaction):
        data = load(SCHEDULE_PATH, {})

        if not data:
            return await interaction.response.send_message("Kayıtlı mesaj yok.")

        embed = discord.Embed(title="⏰ Zamanlanmış Mesajlar")

        for mid, info in data.items():
            if info["type"] == "once":
                embed.add_field(
                    name=f"🟢 Tek Seferlik | ID: {mid}",
                    value=f"Kanal: <#{info['channel']}>\nZaman: {info['time']}\nMesaj: {info['message']}",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"🔁 Tekrarlayan | ID: {mid}",
                    value=f"Kanal: <#{info['channel']}>\nAralık: {info['interval']} sn\nSonraki Çalışma: {info['next_run']}\nMesaj: {info['message']}",
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

    # ======================================================
    #   SİLME
    # ======================================================
    @app_commands.command(name="automsg_delete", description="Zamanlanmış mesajı sil.")
    async def automsg_delete(self, interaction: discord.Interaction, msg_id: str):
        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.")

        data = load(SCHEDULE_PATH, {})

        if msg_id not in data:
            return await interaction.response.send_message("❌ Böyle bir ID yok.")

        del data[msg_id]
        save(SCHEDULE_PATH, data)

        await interaction.response.send_message("🗑️ Mesaj silindi.")


async def setup(bot):
    await bot.add_cog(AutoMSG(bot))
