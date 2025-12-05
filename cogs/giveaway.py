import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
import asyncio
from utils.storage import load, save
from utils.permissions import is_allowed
from utils.logger import log

GIVEAWAY_PATH = "data/giveaways.json"


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_loop.start()

    # ==============================================
    #   ARKA PLAN KONTROLÜ (Her 20 saniyede bir)
    # ==============================================
    @tasks.loop(seconds=20)
    async def check_loop(self):
        data = load(GIVEAWAY_PATH, {})

        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        for gid, info in list(data.items()):
            if info["time"] == now:
                channel = self.bot.get_channel(info["channel"])
                if not channel:
                    continue

                try:
                    msg = await channel.fetch_message(info["message_id"])
                except:
                    continue

                # Katılımcı listesi
                participants = info.get("participants", [])
                if not participants:
                    winner_text = "Kimse katılmadığı için kazanan yok."
                else:
                    winner_id = random.choice(participants)
                    winner_text = f"<@{winner_id}> 🎉 kazandı!"

                await msg.reply(f"🎉 **Giveaway Bitti!**\nÖdül: **{info['prize']}**\nKazanan: {winner_text}")

                await log(self.bot, channel.guild.id, "GIVEAWAY", f"{info['prize']} çekilişi tamamlandı.")

                del data[gid]
                save(GIVEAWAY_PATH, data)

    # ==============================================
    #   GIVEAWAY BAŞLATMA (Tarihli)
    # ==============================================
    @app_commands.command(name="giveaway_start", description="Belirli bir tarihte giveaway başlatır.")
    async def giveaway_start(self, interaction: discord.Interaction,
                             channel: discord.TextChannel,
                             prize: str,
                             datetime_str: str):

        if not is_allowed(interaction.user.id):
            return await interaction.response.send_message("❌ Yetkin yok.", ephemeral=True)

        # Tarih kontrolü
        try:
            datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except:
            return await interaction.response.send_message(
                "❌ Format hatalı. Doğru format: **2025-02-10 18:45**",
                ephemeral=True
            )

        embed = discord.Embed(
            title="🎉 Giveaway Başladı!",
            description=f"Ödül: **{prize}**\nBaşlangıç: `{datetime_str}`\n\nKatılmak için 🎉 emojisine tıklayın!",
            color=discord.Color.random()
        )

        msg = await channel.send(embed=embed)
        await msg.add_reaction("🎉")

        # JSON'a kaydet
        data = load(GIVEAWAY_PATH, {})
        data[str(len(data) + 1)] = {
            "channel": channel.id,
            "message_id": msg.id,
            "prize": prize,
            "time": datetime_str,
            "participants": []
        }

        save(GIVEAWAY_PATH, data)

        await interaction.response.send_message("🎉 Giveaway ayarlandı!")

    # ==============================================
    #   REACTION TRACKER — Katılımcıları kaydet
    # ==============================================
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) != "🎉":
            return

        data = load(GIVEAWAY_PATH, {})
        for gid, info in data.items():
            if info["message_id"] == payload.message_id:
                if payload.user_id not in info["participants"]:
                    info["participants"].append(payload.user_id)
                    save(GIVEAWAY_PATH, data)
                break

    # ==============================================
    #   KATILIMCI LİSTESİ (Yeni Komut)
    # ==============================================
    @app_commands.command(name="giveaway_list", description="Aktif giveaway katılımcılarını gösterir.")
    async def giveaway_list(self, interaction: discord.Interaction, giveaway_id: str):

        data = load(GIVEAWAY_PATH, {})

        if giveaway_id not in data:
            return await interaction.response.send_message("❌ Böyle bir giveaway ID’si yok.")

        info = data[giveaway_id]
        participants = info.get("participants", [])

        embed = discord.Embed(
            title="🎉 Giveaway Katılımcıları",
            description=f"Ödül: **{info['prize']}**\nToplam Katılımcı: **{len(participants)}**",
            color=discord.Color.green()
        )

        if participants:
            embed.add_field(
                name="Katılımcılar:",
                value="\n".join([f"<@{uid}>" for uid in participants]),
                inline=False
            )
        else:
            embed.add_field(
                name="Katılımcılar:",
                value="Katılımcı yok 😢",
                inline=False
            )

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Giveaway(bot))
