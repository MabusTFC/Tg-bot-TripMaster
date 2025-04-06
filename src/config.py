import os
from dotenv import load_dotenv

load_dotenv()

# Bot envs
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_HOOK_URL = os.getenv("WEB_HOOK_URL")
WEB_HOOK_PATH = os.getenv("WEB_HOOK_PATH")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
OWNER_ID = os.getenv("OWNER_ID")
SERVER_URL = os.getenv("SERVER_URL")
MAP_URL = os.getenv("MAP_URL")