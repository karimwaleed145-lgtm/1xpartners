import json
import asyncio
import logging
from config import (
    GOOGLE_SHEET_ID,
    GOOGLE_CREDENTIALS_JSON,
    GOOGLE_OAUTH_CLIENT_ID,
    GOOGLE_OAUTH_CLIENT_SECRET,
    GOOGLE_OAUTH_REFRESH_TOKEN,
)

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
TOKEN_URI = "https://oauth2.googleapis.com/token"

# OAuth is the fallback when a service-account JSON key can't be created
# (org policy iam.disableServiceAccountKeyCreation). All three parts are needed.
_oauth_ready = bool(
    GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET and GOOGLE_OAUTH_REFRESH_TOKEN
)

_enabled = bool(GOOGLE_SHEET_ID and (GOOGLE_CREDENTIALS_JSON or _oauth_ready))
_ws = None
HEADER = ["Date (UTC)", "Full name", "Email", "Promo code", "Phone", "Username", "Telegram ID", "Language"]


def auth_mode():
    """Which auth path is active: 'service_account', 'oauth', or None (disabled)."""
    if not GOOGLE_SHEET_ID:
        return None
    if GOOGLE_CREDENTIALS_JSON:
        return "service_account"
    if _oauth_ready:
        return "oauth"
    return None


def _build_credentials():
    """Build google-auth credentials for whichever path is configured."""
    mode = auth_mode()
    if mode == "service_account":
        from google.oauth2.service_account import Credentials

        info = json.loads(GOOGLE_CREDENTIALS_JSON)
        return Credentials.from_service_account_info(info, scopes=SCOPES)

    if mode == "oauth":
        from google.oauth2.credentials import Credentials as UserCredentials

        # No access token is stored: passing token=None makes the credentials
        # "not valid", so google-auth mints a fresh access token from the
        # refresh token before the very first request, and again whenever the
        # ~1h token expires. A 24/7 process never needs manual intervention.
        return UserCredentials(
            None,
            refresh_token=GOOGLE_OAUTH_REFRESH_TOKEN,
            token_uri=TOKEN_URI,
            client_id=GOOGLE_OAUTH_CLIENT_ID,
            client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
            scopes=SCOPES,
        )

    return None


def _get_ws():
    """Lazily authorize and cache the worksheet. Runs in a thread (gspread is sync)."""
    global _ws
    if _ws is not None:
        return _ws
    import gspread

    creds = _build_credentials()
    if creds is None:
        raise RuntimeError("Google Sheets is not configured")
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
    try:
        if not ws.row_values(1):
            ws.append_row(HEADER)
    except Exception:
        pass
    _ws = ws
    return _ws


def _reset():
    """Drop the cached worksheet so the next call re-authorizes from scratch."""
    global _ws
    _ws = None


async def append_lead(row: list) -> bool:
    """Append a lead row to the Google Sheet. No-op (returns False) if not configured."""
    if not _enabled:
        return False

    def _do():
        _get_ws().append_row(row, value_input_option="USER_ENTERED")
        return True

    try:
        return await asyncio.to_thread(_do)
    except Exception as e:
        # A cached session can go stale (revoked token, rotated secret, network
        # blip). Rebuild credentials once and retry; never let this reach the
        # caller in a way that could stop the lead going out over Telegram.
        log.warning("Sheets append failed (%s: %s) — retrying with fresh auth", type(e).__name__, e)
        _reset()
        return await asyncio.to_thread(_do)
