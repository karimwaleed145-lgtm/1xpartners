#!/usr/bin/env python3
"""
One-time helper: turn an OAuth client ID + secret into a refresh token.

Run this ONCE on your own computer (not on the server). It opens your browser,
you approve access to your own Google account, and it prints the three values
you paste into .env / Railway Variables.

Use this instead of a service-account JSON key when your Google Cloud
organization enforces `iam.disableServiceAccountKeyCreation`.

────────────────────────────────────────────────────────────────────────
DO THIS IN GOOGLE CLOUD CONSOLE FIRST (console.cloud.google.com)
────────────────────────────────────────────────────────────────────────
1. Pick or create a project (top-left project picker).

2. APIs & Services → Library → search "Google Sheets API" → Enable.

3. APIs & Services → OAuth consent screen:
     • User type:      External
       (Internal only appears if you have a Workspace org; either works —
        Internal skips the test-user step below.)
     • App name:       anything, e.g. "1xPartners Bot Sheets"
     • User support email + Developer contact email: your own address.
     • Scopes:         you can leave this empty here; the scope is requested
                       by this script at run time.
     • Test users:     ADD YOUR OWN GOOGLE ACCOUNT (the one that owns the
                       sheet). Required while the app is in "Testing".
     • Publishing status: leave it on "Testing".
       ⚠️  A refresh token from a "Testing" app expires after 7 days.
           For a 24/7 bot, click "PUBLISH APP" once the consent screen is
           saved. It stays unverified (you'll see an "unverified app"
           warning during this script — click Advanced → Go to ... ), but
           the refresh token then does NOT expire. Verification is only
           needed to remove the warning for other users; for your own
           account it is not required.

4. APIs & Services → Credentials → Create credentials → OAuth client ID:
     • Application type: **Desktop app**   ← important, not "Web application"
     • Name:             anything.
     • Click Create, then copy the Client ID and Client secret.
     Desktop-app clients implicitly allow the loopback redirect URI
     (http://localhost:<random-port>/) that this script uses — you do not
     need to type a redirect URI anywhere.
     If you must use a "Web application" client instead, add this exact
     authorized redirect URI:  http://localhost:8080/

5. Share the Google Sheet with the SAME Google account you'll approve below
   (it's your own account, so it usually already has access).

────────────────────────────────────────────────────────────────────────
THEN RUN:
    pip install google-auth-oauthlib
    python get_google_refresh_token.py
────────────────────────────────────────────────────────────────────────
"""
import sys

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
REDIRECT_PORT = 8080


def main():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install google-auth-oauthlib")

    print("Paste the values from Google Cloud Console → Credentials → your OAuth client.\n")
    client_id = input("Client ID:     ").strip()
    client_secret = input("Client secret: ").strip()
    if not client_id or not client_secret:
        sys.exit("Both Client ID and Client secret are required.")

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    print("\nA browser window will open. Sign in with the Google account that owns the sheet.")
    print('If you see "Google hasn\'t verified this app", click Advanced → Go to ... (unsafe).\n')

    # access_type=offline + prompt=consent guarantees a refresh_token is returned
    # (Google omits it on re-consent otherwise).
    creds = flow.run_local_server(
        port=REDIRECT_PORT,
        access_type="offline",
        prompt="consent",
        open_browser=True,
    )

    if not creds.refresh_token:
        sys.exit(
            "No refresh token was returned. Revoke this app's access at\n"
            "  https://myaccount.google.com/permissions\n"
            "and run the script again."
        )

    print("\n" + "=" * 64)
    print("Success. Add these to your .env (local) or Railway Variables:")
    print("=" * 64)
    print(f"GOOGLE_OAUTH_CLIENT_ID={client_id}")
    print(f"GOOGLE_OAUTH_CLIENT_SECRET={client_secret}")
    print(f"GOOGLE_OAUTH_REFRESH_TOKEN={creds.refresh_token}")
    print("=" * 64)
    print("Also set GOOGLE_SHEET_ID (the long ID in your sheet's URL).")
    print("Leave GOOGLE_CREDENTIALS_JSON empty/unset — it takes priority if set.")
    print("\nTreat the refresh token like a password. Never commit it.")


if __name__ == "__main__":
    main()
