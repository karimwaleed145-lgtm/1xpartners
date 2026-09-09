# 1xBet Partners — Recruitment Bot (Aiogram 3)

A clean Telegram bot that:
1. Lets a user pick a language (Arabic / French / English / Dari)
2. Shows a welcome + menu
3. Collects partner info (full name, email, promo code, phone) one step at a time
4. **Forwards every completed lead to you (admin) instantly**, and saves a copy to a local database
5. Shows info pages: Commission (FTD ladder), Withdrawal conditions, Free designs, How it works

## Files
- `bot.py` — entry point (starts polling)
- `config.py` — reads BOT_TOKEN, ADMIN_IDS, DB_URL from environment
- `texts.py` — all text in 4 languages
- `keyboards.py` — inline buttons
- `handlers.py` — all logic (start, language, registration flow, menu)
- `database.py` — saves leads (SQLite via SQLAlchemy async)

---

## A. Run locally (test on your computer)

1. Talk to **@BotFather** on Telegram → `/newbot` → copy the token.
2. Find your numeric Telegram ID via **@userinfobot** (it replies with your ID).
3. In this folder, create a file named `.env` (copy `.env.example`) and fill in:
   ```
   BOT_TOKEN=123456:ABC...your token...
   ADMIN_IDS=your_numeric_id
   ```
4. Then:
   ```bash
   python -m venv venv
   source venv/bin/activate          # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python bot.py
   ```
5. Open your bot in Telegram, press **Start**. To receive leads, make sure you
   (the admin) have pressed Start on the bot at least once.

---

## B. Deploy to Railway (stays online 24/7)

1. Push this folder to a **GitHub** repo (the `.env` is git-ignored — never commit it).
2. On **railway.app**: New Project → Deploy from GitHub repo → pick this repo.
3. Railway detects Python and installs `requirements.txt` automatically.
4. In the service **Variables** tab, add:
   - `BOT_TOKEN` = your BotFather token
   - `ADMIN_IDS` = your numeric Telegram ID (comma-separated for several)
5. Start command: Railway uses the `Procfile` (`worker: python bot.py`).
   If it doesn't, set the start command manually to: `python bot.py`
6. Deploy. Check the **Logs** — you should see “Bot started. Polling…”.

That's it — your bot is live and will keep running.

---

## Notes
- **Leads are never lost:** even though SQLite on Railway resets on redeploy,
  every lead is also sent to you (admin) in Telegram the moment it's submitted.
- **FSM storage is in-memory.** If the bot restarts while someone is mid-registration,
  they just press Start again. For production-grade persistence you can switch to
  Redis storage later (optional).
- Edit all wording in `texts.py`. Edit the commission/withdrawal numbers there too.

---

## C. (Optional) Log every lead to Google Sheets

The bot works without this. When you're ready, leads will also append as rows in a
Google Sheet you can sort, filter, and share. One-time setup (~10 min):

1. Create a Google Sheet. From its URL copy the ID:
   `docs.google.com/spreadsheets/d/`**`THIS_LONG_ID`**`/edit` → that's `GOOGLE_SHEET_ID`.
2. Go to **console.cloud.google.com** → create a project (free).
3. In **APIs & Services → Library**, enable **Google Sheets API**.
4. In **APIs & Services → Credentials → Create credentials → Service account**.
   Create it, then open it → **Keys → Add key → JSON** → download the JSON file.
5. Open the JSON, find the `"client_email"` (looks like `name@project.iam.gserviceaccount.com`).
   In your Google Sheet, click **Share** and share it with that email (Editor).
6. Put the values in your environment:
   - `GOOGLE_SHEET_ID` = the ID from step 1
   - `GOOGLE_CREDENTIALS_JSON` = the **entire** contents of the JSON file, as one value
     (locally: paste it on one line in `.env`. On Railway: paste it into the variable —
     multi-line is fine there.)
7. Restart the bot. New confirmed leads now also append to the sheet. Header row is
   created automatically: Date, Full Name, Email, Promo Code, Phone, Telegram Username,
   Telegram ID, Language, Country, Affiliate ID. Country is derived from the phone's
   dialling code; Affiliate ID is left blank for you to fill in by hand.

**Security:** the JSON key is a password — never commit it to GitHub or paste it in chat.
It lives only in your local `.env` (git-ignored) and in Railway Variables.

---

## C2. (Alternative) Google Sheets via OAuth — when service-account keys are blocked

Use this **instead of** section C if your Google Cloud organization enforces
`iam.disableServiceAccountKeyCreation`, so the **Keys → Add key → JSON** button
in step 4 of section C is greyed out or errors. Same result: leads append to your
sheet. The difference is the bot authenticates *as you* with an OAuth refresh
token instead of as a service account with a JSON key.

**If `GOOGLE_CREDENTIALS_JSON` is set it still wins** — leave it empty to use OAuth.
If neither is set, Sheets logging stays off and the bot behaves exactly as before.

### 1. In Google Cloud Console (console.cloud.google.com)

1. Pick or create a project, then **APIs & Services → Library** → enable **Google Sheets API**.
2. **APIs & Services → OAuth consent screen**:
   - **User type: External** (choose Internal instead if you have a Workspace org — it skips the test-user step).
   - App name: anything. User support email + developer contact: your own address.
   - **Scopes:** leave empty here — the helper script requests the scope at run time.
   - **Test users:** add your own Google account (the one that owns the sheet).
   - ⚠️ **Then click "PUBLISH APP".** A refresh token issued while the app is in
     *Testing* **expires after 7 days**, which would silently break a 24/7 bot.
     Published-but-unverified is fine and the token then never expires — you just
     click **Advanced → Go to … (unsafe)** once during step 3. Google verification
     is only needed to remove that warning for *other* people, not for your own account.
3. **APIs & Services → Credentials → Create credentials → OAuth client ID**:
   - **Application type: Desktop app** (not "Web application").
   - Copy the **Client ID** and **Client secret**.
   - No redirect URI to type: desktop clients allow the loopback URI
     `http://localhost:<port>/` automatically. (If you're forced to use a
     *Web application* client, add exactly `http://localhost:8080/` as an
     authorized redirect URI.)
4. Make sure the Google account you'll approve has **Editor** access to the sheet
   (if it's your own sheet, it already does).

### 2. On your own computer, generate the refresh token (once)

```bash
pip install google-auth-oauthlib
python get_google_refresh_token.py
```

It asks for the Client ID and secret, opens your browser to approve access, then
prints the three values to copy. Run it locally, **not** on Railway — it needs a browser.

Requested scope: `https://www.googleapis.com/auth/spreadsheets` (sheets only, no Drive access).

### 3. Set the environment variables

In `.env` locally, or Railway → Variables:

- `GOOGLE_SHEET_ID` — the long ID from your sheet's URL (same as section C step 1)
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GOOGLE_OAUTH_REFRESH_TOKEN`
- `GOOGLE_CREDENTIALS_JSON` — leave **unset/empty**

Restart the bot. The header row is created automatically, same as section C.

### Notes

- **Token refresh is automatic.** The bot stores no access token; on each request
  `google-auth` mints a fresh one from the refresh token and reuses it until it
  expires (~1 hour), then renews it. Nothing to do manually, ever.
- **Failures never block a lead.** Sheets writes run inside the existing
  try/except in `handlers.py` — if Google is down or the token is revoked, the
  error is logged and the lead still reaches you on Telegram.
- **A refresh token is a password.** Never commit it. It lives only in `.env`
  (git-ignored) and in Railway Variables. Revoke at
  [myaccount.google.com/permissions](https://myaccount.google.com/permissions).
- **Verify the wiring** without deploying:
  ```bash
  python tests/test_sheets_oauth.py
  ```

---

## D. Referral / Sub-manager button ("Refer & earn 3%")

The menu has a **Refer & earn 3%** button. When tapped, the bot explains the
sub-manager role (RS 25% from players + Ref 3% from sub-affiliates) and sends the
how-to video (`media/referral_howto.mp4`) showing affiliates how to get their own
referral link from their 1x.partners dashboard.

- The video ships inside the project (`media/` folder) — nothing else to configure.
- The first time the bot sends it, it prints a line in the logs like
  `REFERRAL_VIDEO_FILE_ID = BAAC...`. This is optional: copy that value into a
  `REFERRAL_VIDEO_FILE_ID` variable (Railway or `.env`) and resends become instant
  (Telegram reuses the uploaded file instead of re-uploading). Totally optional.
- To replace the video later, just drop a new `media/referral_howto.mp4` and clear
  `REFERRAL_VIDEO_FILE_ID` if you had set it.

---

## E. Demo account button (create / recharge)

The menu has a **🎮 Demo account** button. The partner chooses **Unlock** or **Recharge**:
- **Unlock**: condition shown = 20 new registrations with deposits (new clean 1xBet account).
- **Recharge**: conditions shown = more than 1 week since last demo + 20 new registrations with deposits.

The bot then collects: **Aff ID** (shows `media/affid_help.jpg` as a guide), **new Player/Account ID**,
**currency**, and a **screenshot** of the deposits report (shows `media/deposits_apk.mp4` and
`media/deposits_site.mp4` as how-to guides). It forwards the full request + screenshot to the
admin(s). **You approve manually** after checking the 1x.partners dashboard — the bot never
grants a demo automatically (screenshots are intake/claims, the dashboard is the source of truth).

All media lives in `media/` and ships with the project; nothing else to configure.

---

## F. Banner generator test

Before deploying any change to `banner_gen.py` or the templates in `media/templates/`,
run:

```bash
python tests/test_banners.py
```

and confirm all 12 pass. It generates a banner for every style x language combination,
checks for exceptions, verifies output dimensions, and checks that the stamped promo
code is actually visible against the code-box background (this is what catches a
white-on-white or navy-on-navy text bug before it ships). It's a standalone script —
it doesn't run as part of the bot and doesn't touch any live code.
