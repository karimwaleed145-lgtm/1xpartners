import json
import asyncio
from config import GOOGLE_SHEET_ID, GOOGLE_CREDENTIALS_JSON

_enabled = bool(GOOGLE_SHEET_ID and GOOGLE_CREDENTIALS_JSON)
_ws = None
HEADER = ["Date (UTC)", "Full name", "Email", "Promo code", "Phone", "Username", "Telegram ID", "Language"]


def _get_ws():
    """Lazily authorize and cache the worksheet. Runs in a thread (gspread is sync)."""
    global _ws
    if _ws is not None:
        return _ws
    import gspread
    from google.oauth2.service_account import Credentials

    info = json.loads(GOOGLE_CREDENTIALS_JSON)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    gc = gspread.authorize(creds)
    ws = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
    try:
        if not ws.row_values(1):
            ws.append_row(HEADER)
    except Exception:
        pass
    _ws = ws
    return _ws


async def append_lead(row: list) -> bool:
    """Append a lead row to the Google Sheet. No-op (returns False) if not configured."""
    if not _enabled:
        return False

    def _do():
        _get_ws().append_row(row, value_input_option="USER_ENTERED")
        return True

    return await asyncio.to_thread(_do)
