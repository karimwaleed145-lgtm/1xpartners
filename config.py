import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x.strip().isdigit()]
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///partners.db")

# Optional Google Sheets logging (leave empty to disable)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "").strip()
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "").strip()

# Optional: a Telegram file_id for the referral how-to video (speeds up resends).
# Leave empty and the bot will upload media/referral_howto.mp4 the first time.
REFERRAL_VIDEO_FILE_ID = os.getenv("REFERRAL_VIDEO_FILE_ID", "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Add it to your .env file (local) or to Railway "
        "Variables (production). Get the token from @BotFather on Telegram."
    )
