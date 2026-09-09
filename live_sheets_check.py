#!/usr/bin/env python3
"""
Live end-to-end check: really connects to Google Sheets with your configured
credentials, writes one clearly-marked test row, reads it back, then deletes it
so your sheet is left clean.

Run:  ./venv/bin/python live_sheets_check.py
      ./venv/bin/python live_sheets_check.py --keep    (leave the test row in)

Prints no secrets.
"""
import sys
import asyncio
from datetime import datetime

KEEP = "--keep" in sys.argv


def fail(msg, hint=""):
    print(f"\n  ✗ {msg}")
    if hint:
        print("\n" + hint)
    sys.exit(1)


def explain(e):
    """Turn the usual Google errors into something actionable."""
    t = f"{type(e).__name__}: {e}"
    low = t.lower()
    if "invalid_grant" in low:
        return ("Your refresh token was rejected. Usual causes:\n"
                "  • The OAuth consent screen is still in 'Testing' — tokens expire after 7 days.\n"
                "    Publish the app (In production), then re-run get_google_refresh_token.py.\n"
                "  • Access was revoked at myaccount.google.com/permissions.\n"
                "  • The client secret was rotated after the token was minted.")
    if "invalid_client" in low:
        return ("Client ID / secret mismatch. Make sure GOOGLE_OAUTH_CLIENT_ID and\n"
                "GOOGLE_OAUTH_CLIENT_SECRET in .env came from the SAME OAuth client\n"
                "as the refresh token.")
    if "403" in t or "permission" in low or "forbidden" in low:
        return ("Permission denied. Either:\n"
                "  • The Google account you approved doesn't have Editor access to the sheet, or\n"
                "  • The Google Sheets API isn't enabled for that Cloud project.")
    if "404" in t or "notfound" in low or "not found" in low:
        return ("Sheet not found — check GOOGLE_SHEET_ID in .env. It's the long id in the URL:\n"
                "  docs.google.com/spreadsheets/d/<THIS PART>/edit")
    if "apinotactivated" in low.replace(" ", "") or "has not been used" in low:
        return ("The Google Sheets API isn't enabled for this project.\n"
                "  console.cloud.google.com → APIs & Services → Library → Google Sheets API → Enable")
    return ""


def main():
    print("=" * 66)
    print(" Live Google Sheets check")
    print("=" * 66)

    try:
        import config
        import sheets
    except Exception as e:
        fail(f"Could not load config/sheets — {type(e).__name__}: {e}")

    # 1. configuration
    mode = sheets.auth_mode()
    print(f"\n1. Configuration")
    print(f"   auth mode        : {mode}")
    print(f"   sheet id set     : {'yes' if config.GOOGLE_SHEET_ID else 'NO'}")
    print(f"   client id set    : {'yes' if config.GOOGLE_OAUTH_CLIENT_ID else 'no'}")
    print(f"   client secret set: {'yes' if config.GOOGLE_OAUTH_CLIENT_SECRET else 'no'}")
    print(f"   refresh token set: {'yes' if config.GOOGLE_OAUTH_REFRESH_TOKEN else 'no'}")

    if mode is None:
        fail("Sheets is not configured — the bot would silently skip logging.",
             "Check .env has GOOGLE_SHEET_ID plus the three GOOGLE_OAUTH_* values.")
    if mode == "service_account":
        print("\n   Note: GOOGLE_CREDENTIALS_JSON is set, so the service-account path")
        print("   is being used. Clear it if you meant to test OAuth.")

    # 2. token
    print(f"\n2. Minting an access token from the refresh token")
    try:
        from google.auth.transport.requests import Request
        creds = sheets._build_credentials()
        print(f"   before refresh   : valid={creds.valid} (expected False — no token stored)")
        creds.refresh(Request())
        print(f"   after refresh    : valid={creds.valid}, expires {creds.expiry} UTC")
        print(f"   access token     : {str(creds.token)[:12]}… (hidden)")
    except Exception as e:
        fail(f"Token refresh failed — {type(e).__name__}: {e}", explain(e))

    # 3. open the sheet
    print(f"\n3. Opening the spreadsheet")
    try:
        import gspread
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(config.GOOGLE_SHEET_ID)
        ws = sh.sheet1
        print(f"   title            : {sh.title}")
        print(f"   worksheet        : {ws.title}")
        before = ws.get_all_values()
        print(f"   rows before      : {len(before)}")
        if before:
            print(f"   current header   : {before[0]}")
    except Exception as e:
        fail(f"Could not open the sheet — {type(e).__name__}: {e}", explain(e))

    # 4. write through the real bot code path
    print(f"\n4. Writing a test row through sheets.append_lead()")
    stamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    marker = f"LIVE-TEST-{datetime.utcnow().strftime('%H%M%S')}"
    row = [stamp, marker, "test@example.com", "TESTPROMO",
           "+213770772883", "@livetest", "000000", "en"]
    try:
        ok = asyncio.get_event_loop().run_until_complete(sheets.append_lead(row))
        print(f"   append_lead()    : {ok}")
    except Exception as e:
        fail(f"append_lead() failed — {type(e).__name__}: {e}", explain(e))

    # 5. read back
    print(f"\n5. Reading it back")
    after = ws.get_all_values()
    print(f"   rows after       : {len(after)}")
    hit = [(i, r) for i, r in enumerate(after, start=1) if marker in r]
    if not hit:
        fail("The row was not found in the sheet after writing.")
    idx, got = hit[0]
    # get_all_values() trims trailing empty cells, so a row whose last column is
    # blank comes back short. Pad before indexing.
    got = list(got) + [""] * (10 - len(got))
    print(f"   found at row     : {idx}")
    print(f"   header           : {after[0]}")
    print(f"   written row      : {got}")

    checks = [
        ("10 columns", len(got) == 10),
        ("date has day name", got[0].endswith(")") and stamp in got[0]),
        ("phone kept its leading + (not eaten as a formula)", got[4] == row[4]),
        ("telegram id kept leading zeros (not turned into 0)", got[6] == row[6]),
        ("country derived from +213", got[8] == "Algeria"),
        ("affiliate id blank", got[9] == ""),
        ("header present", after[0][:2] == ["Date", "Full Name"] or len(after[0]) >= 8),
    ]
    print()
    allok = True
    for label, cond in checks:
        print(("   ✓ " if cond else "   ✗ ") + label)
        allok = allok and cond

    # 6. clean up
    if KEEP:
        print(f"\n6. Leaving the test row in place (--keep). Delete row {idx} by hand.")
    else:
        print(f"\n6. Deleting the test row")
        try:
            ws.delete_rows(idx)
            print(f"   rows now         : {len(ws.get_all_values())} (sheet left clean)")
        except Exception as e:
            print(f"   could not delete row {idx}: {type(e).__name__}: {e}")
            print(f"   delete it by hand — it's the one marked {marker}")

    print("\n" + "=" * 66)
    if allok:
        print(" ALL GOOD — the bot can write leads to your sheet. Safe to deploy.")
        print(" Remember to set the same 4 variables in Railway → Variables.")
    else:
        print(" Connected and wrote successfully, but some column checks failed above.")
    print("=" * 66)
    return 0 if allok else 1


if __name__ == "__main__":
    if sys.version_info >= (3, 10):
        asyncio.set_event_loop(asyncio.new_event_loop())
    sys.exit(main())
