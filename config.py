import os
import json

# Yetkili kullanıcılar
ALLOWED_USERS = json.loads(os.getenv("ALLOWED_USER_IDS", "[]"))

# Log kanalı
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))

# AI Moderasyon Uyarı Seviyeleri
AI_WARN_LEVELS = {
    "warn_1": 3,  # 1. Uyarı
    "timeout_60s": 5,  # 60 saniye timeout
    "timeout_5m": 7,   # 5 dakika timeout
    "timeout_10m": 10  # 10 dakika timeout
}
