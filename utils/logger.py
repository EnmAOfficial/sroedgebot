import os
import json
from datetime import datetime
import discord

async def log(bot, guild_id: int, category: str, message: str):
    log_channel_id = int(os.getenv("LOG_CHANNEL_ID"))
    channel = bot.get_channel(log_channel_id)

    entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "category": category,
        "message": message
    }

    path = f"data/logs/{guild_id}.json"
    os.makedirs("data/logs", exist_ok=True)

    try:
        logs = json.load(open(path, "r", encoding="utf-8"))
    except:
        logs = []

    logs.append(entry)
    json.dump(logs, open(path, "w", encoding="utf-8"), indent=4)

    if channel:
        await channel.send(f"**[{category}]** {message}")
