import os
import json

ALLOWED_USERS = json.loads(os.getenv("ALLOWED_USER_IDS", "[]"))
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
