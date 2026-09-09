import json
import asyncio
import logging
from datetime import datetime
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
HEADER = [
    "Date", "Full Name", "Email", "Promo Code", "Phone",
    "Telegram Username", "Telegram ID", "Language",
    "Country", "Affiliate ID",
]

# strftime("%A") is locale-dependent; the sheet must always read in English.
DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


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


def _format_date(value):
    """'2026-09-09 01:47' -> '2026-09-09 01:47 (Tuesday)'.

    `value` is the confirmation timestamp handlers.py already stamps when the
    lead presses confirm, so the sheet shows when they registered, not when the
    API call happened. Anything unrecognised is passed through untouched rather
    than discarded.
    """
    raw = str(value or "").strip()
    if not raw:
        # Never leave the Date cell blank; append runs seconds after confirm.
        dt = datetime.utcnow()
        return f"{dt.strftime('%Y-%m-%d %H:%M')} ({DAY_NAMES[dt.weekday()]})"
    if raw.endswith(")"):
        return raw  # already carries a day name
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(raw, fmt)
        except ValueError:
            continue
        return f"{dt.strftime('%Y-%m-%d %H:%M')} ({DAY_NAMES[dt.weekday()]})"
    return raw


def _country_from_phone(phone):
    """Country name from the phone's dialling code, or "" if undeterminable.

    Deliberately does not require is_valid_number(): a lead who typed one digit
    too many is still reachable info about which country they are in. Only a
    number phonenumbers cannot parse at all yields "". Never raises.
    """
    try:
        import phonenumbers
        from phonenumbers import geocoder

        parsed = phonenumbers.parse(str(phone or "").strip(), None)
        name = geocoder.country_name_for_number(parsed, "en")
        if name:
            return name
        # Fall back to the ISO code when the geocoder has no display name.
        region = (
            phonenumbers.region_code_for_number(parsed)
            or phonenumbers.region_code_for_country_code(parsed.country_code)
        )
        return "" if not region or region == "ZZ" else region
    except Exception:
        return ""


def _build_row(row):
    """Normalise a caller row into the 10 columns of HEADER.

    The first 8 columns keep their existing order and meaning; only the Date
    cell is reformatted. Country is derived, Affiliate ID is always blank (it
    is filled in by hand after a partner is activated).
    """
    values = [("" if v is None else v) for v in list(row or [])][:8]
    values += [""] * (8 - len(values))
    values[0] = _format_date(values[0])
    return values + [_country_from_phone(values[4]), ""]


def _row_is_blank(values):
    """True if a row has no real content. row_values() can return ['', '', ...]."""
    return not any(str(v).strip() for v in (values or []))


def _ensure_header(ws):
    """Write HEADER only when row 1 is blank. Never duplicates an existing header."""
    try:
        if _row_is_blank(ws.row_values(1)):
            # table_range pins the write to column A; without it Sheets picks its
            # own anchor from whatever cells happen to be filled.
            ws.append_row(HEADER, value_input_option="RAW", table_range="A1")
    except Exception as e:
        log.warning("Could not verify/write the header row: %s: %s", type(e).__name__, e)


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
    _ensure_header(ws)
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

    values = _build_row(row)

    def _do():
        # RAW, not USER_ENTERED: Sheets would otherwise treat "+2137..." as a
        # formula and strip the leading +, and turn a Telegram ID like "000000"
        # into the number 0. Leads must survive verbatim.
        # table_range="A1" anchors the append to column A. Without it gspread
        # lets Sheets auto-detect the table, which drifts to whichever column
        # happens to hold data — silently writing leads into the wrong columns.
        _get_ws().append_row(values, value_input_option="RAW", table_range="A1")
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
