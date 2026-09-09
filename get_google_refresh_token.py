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
THEN RUN either of:

    python get_google_refresh_token.py                      # type/paste the two values
    python get_google_refresh_token.py client_secret.json   # read them from the JSON

The second form is easier: type the command, a space, then DRAG the JSON file
you downloaded from Google Cloud onto the Terminal window (that inserts its
path for you) and press Enter.
────────────────────────────────────────────────────────────────────────
"""
import os
import sys
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
REDIRECT_PORT = 8080


def _write_env(values, env_path=".env"):
    """Write/replace the GOOGLE_OAUTH_* keys in .env. Backs up first. No copy-paste."""
    import shutil
    from datetime import datetime

    env_path = os.path.abspath(env_path)
    lines = []
    if os.path.isfile(env_path):
        backup = f"{env_path}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        shutil.copy2(env_path, backup)
        print(f"   backed up existing .env -> {os.path.basename(backup)}")
        with open(env_path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()

    replaced = set()
    out = []
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line else ""
        if key in values:
            out.append(f"{key}={values[key]}")
            replaced.add(key)
        else:
            out.append(line)

    missing = [k for k in values if k not in replaced]
    if missing:
        if out and out[-1].strip():
            out.append("")
        out.append("# Google Sheets logging via OAuth — see README section C2")
        out += [f"{k}={values[k]}" for k in missing]

    with open(env_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")

    for k in values:
        print(f"   {'updated' if k in replaced else 'added  '} {k}")
    return env_path


def _autodiscover():
    """Find a downloaded OAuth client JSON so the script can run with no arguments."""
    import glob

    seen, found = set(), []
    for d in (os.getcwd(), os.path.expanduser("~/Downloads"), os.path.expanduser("~/Desktop")):
        for f in sorted(glob.glob(os.path.join(d, "client_secret*.json")),
                        key=os.path.getmtime, reverse=True):
            real = os.path.realpath(f)
            if real not in seen:
                seen.add(real)
                found.append(f)
    return found


def _from_json_file(path):
    """Pull client_id/client_secret out of a downloaded OAuth client JSON."""
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        sys.exit(f"No such file: {path}\nDrag the JSON file onto the Terminal window to insert its path.")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception as e:
        sys.exit(f"Could not read {path} as JSON ({e}).")

    if "type" in data and data.get("type") == "service_account":
        sys.exit(
            "That's a service-account key, not an OAuth client.\n"
            "You need Credentials → Create credentials → OAuth client ID → Desktop app."
        )
    block = data.get("installed") or data.get("web") or data
    cid, secret = block.get("client_id", ""), block.get("client_secret", "")
    if not cid or not secret:
        sys.exit(f"{path} has no client_id/client_secret. Is it the OAuth client JSON?")
    if "web" in data:
        print("Note: this is a *Web application* client. Make sure "
              "http://localhost:8080/ is listed under Authorized redirect URIs.\n")
    return cid, secret


def main():
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit("Missing dependency. Run:  pip install google-auth-oauthlib")

    path = " ".join(sys.argv[1:]).strip().strip("'\"")

    if not path:
        candidates = _autodiscover()
        if len(candidates) == 1:
            path = candidates[0]
            print(f"Found your OAuth client JSON: {path}")
            print("(Pass a path as an argument if you meant a different one.)\n")
        elif len(candidates) > 1:
            print("Found several OAuth client JSON files:\n")
            for f in candidates:
                print(f"  {f}")
            print("\nRe-run with the one you want, e.g.:")
            print(f'  python get_google_refresh_token.py "{candidates[0]}"\n')
            sys.exit("Not guessing between them.")

    if path:
        client_id, client_secret = _from_json_file(path)
        print(f"Read the OAuth client from {os.path.basename(path)}")
        print(f"  Client ID: {client_id}\n")
    else:
        print("Paste the values from Google Cloud Console → Credentials → your OAuth client.")
        print("(Tip: re-run this with your downloaded JSON file instead —")
        print(" type the command, a space, then drag the file onto this window.)\n")
        try:
            client_id = input("Client ID:     ").strip()
            client_secret = input("Client secret: ").strip()
        except (EOFError, KeyboardInterrupt):
            sys.exit("\nCancelled — no token was created. Nothing was changed.")
        if not client_id or not client_secret:
            sys.exit(
                "Nothing was entered, so no token was created — the prompt exits on an "
                "empty line.\nRun the script again, or pass your JSON file:\n"
                "    python get_google_refresh_token.py client_secret.json"
            )

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

    values = {
        "GOOGLE_OAUTH_CLIENT_ID": client_id,
        "GOOGLE_OAUTH_CLIENT_SECRET": client_secret,
        "GOOGLE_OAUTH_REFRESH_TOKEN": creds.refresh_token,
    }

    print("\n" + "=" * 64)
    print("Success — got a refresh token.")
    print("=" * 64)

    if "--print" in sys.argv:
        for k, v in values.items():
            print(f"{k}={v}")
        print("=" * 64)
        print("Copy those into .env or Railway Variables yourself.")
    else:
        print("\nWriting them into .env for you (no copy-paste needed):")
        try:
            path = _write_env(values)
            print(f"\n   .env updated: {path}")
        except Exception as e:
            sys.exit(
                f"\nCould not write .env ({type(e).__name__}: {e}).\n"
                "Re-run with --print to show the values and add them by hand."
            )
        print("\nStill to do:")
        print("  • GOOGLE_SHEET_ID must also be in .env (the long id from your sheet URL).")
        print("  • Leave GOOGLE_CREDENTIALS_JSON empty/unset — it takes priority if set.")
        print("  • Copy the same variables into Railway → Variables for production.")
        print("\nVerify now with:  ./venv/bin/python live_sheets_check.py")

    print("\nTreat the refresh token like a password. Never commit or screenshot it.")


if __name__ == "__main__":
    main()
