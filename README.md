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
