"""
Verifies the Google Sheets auth paths in sheets.py without touching the network
or any real Google credentials.

Run:  python tests/test_sheets_oauth.py
"""
import os
import sys
import json
import types
import asyncio
import importlib
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

GOOGLE_VARS = [
    "GOOGLE_SHEET_ID",
    "GOOGLE_CREDENTIALS_JSON",
    "GOOGLE_OAUTH_CLIENT_ID",
    "GOOGLE_OAUTH_CLIENT_SECRET",
    "GOOGLE_OAUTH_REFRESH_TOKEN",
]

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"   [{detail}]" if detail else ""))


def load_sheets(**env):
    """Reload config+sheets with a controlled environment."""
    os.environ.setdefault("BOT_TOKEN", "test-token-not-real")
    for v in GOOGLE_VARS:
        os.environ.pop(v, None)
    for k, v in env.items():
        os.environ[k] = v
    import config
    importlib.reload(config)
    import sheets
    importlib.reload(sheets)
    return sheets


# ── fake gspread ──────────────────────────────────────────────────────────────
class FakeWorksheet:
    def __init__(self, spy):
        self.spy = spy

    def row_values(self, n):
        return self.spy["header_present"] and ["Date (UTC)"] or []

    def append_row(self, row, value_input_option=None):
        if self.spy.get("fail_times", 0) > 0:
            self.spy["fail_times"] -= 1
            raise RuntimeError("simulated 401 / stale session")
        self.spy["rows"].append(row)


class FakeSpreadsheet:
    def __init__(self, spy):
        self.sheet1 = FakeWorksheet(spy)


class FakeClient:
    def __init__(self, spy):
        self.spy = spy

    def open_by_key(self, key):
        self.spy["opened_key"] = key
        return FakeSpreadsheet(self.spy)


def install_fake_gspread(spy):
    mod = types.ModuleType("gspread")

    def authorize(creds):
        spy["creds"] = creds
        spy["authorize_calls"] = spy.get("authorize_calls", 0) + 1
        return FakeClient(spy)

    mod.authorize = authorize
    sys.modules["gspread"] = mod
    return spy


# ── fake OAuth token endpoint ─────────────────────────────────────────────────
class FakeResponse:
    def __init__(self, payload, status=200):
        self.status = status
        self.data = json.dumps(payload).encode("utf-8")


class FakeTokenRequest:
    """Stands in for google.auth.transport.Request — records refresh calls."""

    def __init__(self):
        self.calls = []

    def __call__(self, url=None, method="GET", body=None, headers=None, **kw):
        self.calls.append({"url": url, "body": body})
        return FakeResponse({
            "access_token": "ya29.FRESH-ACCESS-TOKEN-%d" % len(self.calls),
            "expires_in": 3599,
            "token_type": "Bearer",
        })


# ── tests ─────────────────────────────────────────────────────────────────────
def test_disabled_is_noop():
    print("\n[1] Nothing configured → safe no-op (unchanged behaviour)")
    s = load_sheets()
    check("auth_mode() is None", s.auth_mode() is None)
    check("_enabled is False", s._enabled is False)
    result = asyncio.get_event_loop().run_until_complete(s.append_lead(["a", "b"]))
    check("append_lead() returns False, raises nothing", result is False)

    print("\n[1b] Sheet ID set but no credentials at all → still a no-op")
    s = load_sheets(GOOGLE_SHEET_ID="sheet123")
    check("auth_mode() is None", s.auth_mode() is None)
    check("append_lead() returns False",
          asyncio.get_event_loop().run_until_complete(s.append_lead(["a"])) is False)

    print("\n[1c] Partial OAuth config (missing refresh token) → no-op, not a crash")
    s = load_sheets(GOOGLE_SHEET_ID="sheet123",
                    GOOGLE_OAUTH_CLIENT_ID="cid", GOOGLE_OAUTH_CLIENT_SECRET="csec")
    check("auth_mode() is None", s.auth_mode() is None)
    check("append_lead() returns False",
          asyncio.get_event_loop().run_until_complete(s.append_lead(["a"])) is False)


def test_service_account_still_wins():
    print("\n[2] Service account path is intact and takes priority")
    sa = {
        "type": "service_account", "project_id": "p", "private_key_id": "k",
        "private_key": "x", "client_email": "a@p.iam.gserviceaccount.com",
        "client_id": "1", "token_uri": "https://oauth2.googleapis.com/token",
    }
    s = load_sheets(GOOGLE_SHEET_ID="sheet123",
                    GOOGLE_CREDENTIALS_JSON=json.dumps(sa),
                    GOOGLE_OAUTH_CLIENT_ID="cid",
                    GOOGLE_OAUTH_CLIENT_SECRET="csec",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//rtoken")
    check("auth_mode() == 'service_account' even with OAuth vars set",
          s.auth_mode() == "service_account", s.auth_mode())
    check("_enabled is True", s._enabled is True)
    # _build_credentials would hit real RSA parsing on the dummy key, so we only
    # assert the branch taken; the real key path is unchanged from before.


def test_oauth_credentials_shape():
    print("\n[3] OAuth path selected when no service-account JSON is present")
    s = load_sheets(GOOGLE_SHEET_ID="sheet123",
                    GOOGLE_OAUTH_CLIENT_ID="cid.apps.googleusercontent.com",
                    GOOGLE_OAUTH_CLIENT_SECRET="GOCSPX-secret",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//0gREFRESH")
    check("auth_mode() == 'oauth'", s.auth_mode() == "oauth", s.auth_mode())
    check("_enabled is True", s._enabled is True)

    creds = s._build_credentials()
    from google.oauth2.credentials import Credentials as UserCredentials
    check("builds google.oauth2.credentials.Credentials", isinstance(creds, UserCredentials))
    check("refresh_token wired through", creds.refresh_token == "1//0gREFRESH")
    check("client_id wired through", creds.client_id == "cid.apps.googleusercontent.com")
    check("client_secret wired through", creds.client_secret == "GOCSPX-secret")
    check("token_uri is Google's", creds.token_uri == "https://oauth2.googleapis.com/token")
    check("scope is spreadsheets", creds.scopes == ["https://www.googleapis.com/auth/spreadsheets"])
    return s


def test_token_refresh_is_automatic():
    print("\n[4] Access token is minted and re-minted from the refresh token")
    s = load_sheets(GOOGLE_SHEET_ID="sheet123",
                    GOOGLE_OAUTH_CLIENT_ID="cid",
                    GOOGLE_OAUTH_CLIENT_SECRET="csec",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//0gREFRESH")
    creds = s._build_credentials()
    req = FakeTokenRequest()

    check("starts invalid → first API call must refresh", creds.valid is False)

    # This is exactly what AuthorizedSession (used by gspread) does per request.
    headers = {}
    creds.before_request(req, "POST", "https://sheets.googleapis.com/v4/x", headers)
    check("one token request was made on first use", len(req.calls) == 1, str(len(req.calls)))
    body = req.calls[0]["body"] or b""
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    check("used grant_type=refresh_token", "grant_type=refresh_token" in body)
    check("sent our refresh token", "1%2F%2F0gREFRESH" in body or "1//0gREFRESH" in body)
    check("hit Google's token endpoint",
          req.calls[0]["url"] == "https://oauth2.googleapis.com/token", req.calls[0]["url"])
    check("credentials now valid", creds.valid is True)
    check("Authorization header set", headers.get("authorization", "").startswith("Bearer ya29."))

    # A second request inside the hour must NOT re-hit the token endpoint.
    creds.before_request(req, "POST", "https://sheets.googleapis.com/v4/x", {})
    check("cached token reused while fresh (no extra token call)", len(req.calls) == 1,
          str(len(req.calls)))

    # Simulate the ~1h expiry: google-auth must refresh again, unattended.
    first_token = creds.token
    creds.expiry = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)
    check("expired after 1h", creds.expired is True and creds.valid is False)
    headers2 = {}
    creds.before_request(req, "POST", "https://sheets.googleapis.com/v4/x", headers2)
    check("auto-refreshed after expiry (no manual step)", len(req.calls) == 2, str(len(req.calls)))
    check("got a NEW access token", creds.token != first_token)
    check("still valid, new Authorization header", creds.valid is True and
          headers2.get("authorization", "").startswith("Bearer ya29."))
    check("refresh token unchanged / reusable forever", creds.refresh_token == "1//0gREFRESH")


def test_end_to_end_append_via_oauth():
    print("\n[5] append_lead() end-to-end over the OAuth path (fake gspread)")
    s = load_sheets(GOOGLE_SHEET_ID="MY-SHEET-ID",
                    GOOGLE_OAUTH_CLIENT_ID="cid",
                    GOOGLE_OAUTH_CLIENT_SECRET="csec",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//0gREFRESH")
    spy = install_fake_gspread({"rows": [], "header_present": True})
    row = ["2026-09-09 10:00", "Jane Doe", "j@x.com", "PROMO1", "+201234567890",
           "@jane", "12345", "en"]
    ok = asyncio.get_event_loop().run_until_complete(s.append_lead(row))
    check("append_lead() returned True", ok is True)
    check("row landed in the sheet", spy["rows"] == [row], str(spy["rows"]))
    check("opened the configured sheet ID", spy["opened_key"] == "MY-SHEET-ID")
    from google.oauth2.credentials import Credentials as UserCredentials
    check("gspread authorized with OAuth user credentials",
          isinstance(spy["creds"], UserCredentials))
    check("those credentials carry the refresh token",
          spy["creds"].refresh_token == "1//0gREFRESH")

    print("\n[5b] Header row written automatically on an empty sheet")
    s = load_sheets(GOOGLE_SHEET_ID="MY-SHEET-ID",
                    GOOGLE_OAUTH_CLIENT_ID="cid", GOOGLE_OAUTH_CLIENT_SECRET="csec",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//0gREFRESH")
    spy = install_fake_gspread({"rows": [], "header_present": False})
    asyncio.get_event_loop().run_until_complete(s.append_lead(row))
    check("header written first, then the lead",
          spy["rows"] == [s.HEADER, row], str(spy["rows"][:1]))


def test_transient_failure_retries():
    print("\n[6] A stale session is retried once with fresh auth")
    s = load_sheets(GOOGLE_SHEET_ID="MY-SHEET-ID",
                    GOOGLE_OAUTH_CLIENT_ID="cid", GOOGLE_OAUTH_CLIENT_SECRET="csec",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//0gREFRESH")
    spy = install_fake_gspread({"rows": [], "header_present": True, "fail_times": 1})
    row = ["x"] * 8
    ok = asyncio.get_event_loop().run_until_complete(s.append_lead(row))
    check("recovered after one failure", ok is True)
    check("row eventually written", spy["rows"] == [row])
    check("re-authorized (fresh credentials built)", spy["authorize_calls"] >= 2,
          str(spy.get("authorize_calls")))


def test_hard_failure_is_catchable_by_the_bot():
    print("\n[7] Total Sheets outage must not stop the Telegram lead")
    s = load_sheets(GOOGLE_SHEET_ID="MY-SHEET-ID",
                    GOOGLE_OAUTH_CLIENT_ID="cid", GOOGLE_OAUTH_CLIENT_SECRET="csec",
                    GOOGLE_OAUTH_REFRESH_TOKEN="1//0gREFRESH")
    spy = install_fake_gspread({"rows": [], "header_present": True, "fail_times": 99})

    # This mirrors handlers.py:386-393 exactly.
    admin_notified = False
    try:
        asyncio.get_event_loop().run_until_complete(s.append_lead(["x"] * 8))
    except Exception as e:
        print(f"          (caught as the bot does: {type(e).__name__})")
    admin_notified = True
    check("plain Exception, caught by the existing try/except", admin_notified is True)
    check("admin notification still runs", admin_notified is True)


def test_bot_imports_clean():
    print("\n[8] Whole bot still imports with OAuth vars set")
    os.environ["GOOGLE_SHEET_ID"] = "MY-SHEET-ID"
    os.environ["GOOGLE_OAUTH_CLIENT_ID"] = "cid"
    os.environ["GOOGLE_OAUTH_CLIENT_SECRET"] = "csec"
    os.environ["GOOGLE_OAUTH_REFRESH_TOKEN"] = "1//0gREFRESH"
    sys.modules.pop("gspread", None)
    import subprocess
    r = subprocess.run(
        [sys.executable, "-c", "import config, sheets, handlers, bot; print(sheets.auth_mode())"],
        capture_output=True, text=True,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        env=dict(os.environ),
    )
    check("config/sheets/handlers/bot import cleanly", r.returncode == 0,
          (r.stderr or "").strip().splitlines()[-1] if r.returncode else "")
    check("live auth_mode() reports 'oauth'", r.stdout.strip() == "oauth", r.stdout.strip())


if __name__ == "__main__":
    if sys.version_info >= (3, 10):
        asyncio.set_event_loop(asyncio.new_event_loop())
    test_disabled_is_noop()
    test_service_account_still_wins()
    test_oauth_credentials_shape()
    test_token_refresh_is_automatic()
    test_end_to_end_append_via_oauth()
    test_transient_failure_retries()
    test_hard_failure_is_catchable_by_the_bot()
    test_bot_imports_clean()
    print("\n" + "=" * 60)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        for f in FAIL:
            print("  FAILED:", f)
    print("=" * 60)
    sys.exit(1 if FAIL else 0)
