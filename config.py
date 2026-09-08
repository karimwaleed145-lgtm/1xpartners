import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x.strip().isdigit()]
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///partners.db")

# Optional Google Sheets logging (leave empty to disable)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "").strip()
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "").strip()

# Optional alternative to GOOGLE_CREDENTIALS_JSON: OAuth 2.0 user credentials.
# Use these when your Google Cloud org blocks service-account key creation
# (policy iam.disableServiceAccountKeyCreation). Generate the refresh token once
# with: python get_google_refresh_token.py   (see README section C2).
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "").strip()
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "").strip()
GOOGLE_OAUTH_REFRESH_TOKEN = os.getenv("GOOGLE_OAUTH_REFRESH_TOKEN", "").strip()

# Optional: a Telegram file_id for the referral how-to video (speeds up resends).
# Leave empty and the bot will upload media/referral_howto.mp4 the first time.
REFERRAL_VIDEO_FILE_ID = os.getenv("REFERRAL_VIDEO_FILE_ID", "").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Add it to your .env file (local) or to Railway "
        "Variables (production). Get the token from @BotFather on Telegram."
    )
