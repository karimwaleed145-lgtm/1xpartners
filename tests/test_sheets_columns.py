"""
Verifies the header row, the date format, and the Country / Affiliate ID
columns in sheets.py. No network, no real credentials.

Run:  python tests/test_sheets_columns.py
"""
import os
import sys
import types
import asyncio
import importlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(("  PASS  " if cond else "  FAIL  ") + name + (f"   [{detail}]" if detail else ""))


def load_sheets(**env):
    os.environ.setdefault("BOT_TOKEN", "test-token-not-real")
    # Set to "" rather than popping: load_dotenv() would otherwise refill them
    # from the developer's real .env and break test isolation.
    for v in ("GOOGLE_SHEET_ID", "GOOGLE_CREDENTIALS_JSON", "GOOGLE_OAUTH_CLIENT_ID",
              "GOOGLE_OAUTH_CLIENT_SECRET", "GOOGLE_OAUTH_REFRESH_TOKEN"):
        os.environ[v] = ""
    os.environ.update(env)
    import config
    importlib.reload(config)
    import sheets
    importlib.reload(sheets)
    return sheets


OAUTH = dict(GOOGLE_SHEET_ID="SHEET", GOOGLE_OAUTH_CLIENT_ID="cid",
             GOOGLE_OAUTH_CLIENT_SECRET="csec", GOOGLE_OAUTH_REFRESH_TOKEN="1//r")


class FakeWorksheet:
    def __init__(self, spy):
        self.spy = spy

    def row_values(self, n):
        return list(self.spy["existing_header"])

    def append_row(self, row, value_input_option=None, table_range=None):
        self.spy["rows"].append(row)
        self.spy.setdefault("opts", []).append(value_input_option)
        self.spy.setdefault("ranges", []).append(table_range)


def install_fake_gspread(existing_header):
    spy = {"rows": [], "existing_header": existing_header}
    mod = types.ModuleType("gspread")
    mod.authorize = lambda creds: type(
        "C", (), {"open_by_key": lambda self, k: type(
            "S", (), {"sheet1": FakeWorksheet(spy)})()})()
    sys.modules["gspread"] = mod
    return spy


def run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


# ── 1. header ─────────────────────────────────────────────────────────────────
def test_header():
    print("\n[1] Header row")
    s = load_sheets(**OAUTH)
    expected = ["Date", "Full Name", "Email", "Promo Code", "Phone",
                "Telegram Username", "Telegram ID", "Language", "Country", "Affiliate ID"]
    check("HEADER matches the requested 10 columns", s.HEADER == expected, str(s.HEADER))
    check("first 8 columns unchanged in order/meaning",
          s.HEADER[:8] == expected[:8] and s.HEADER[8:] == ["Country", "Affiliate ID"])

    print("\n[1a] Empty sheet → header written first, then the lead")
    spy = install_fake_gspread(existing_header=[])
    run(s.append_lead(["2026-09-09 01:47", "A", "a@x.com", "P", "+213770772883", "@a", "1", "en"]))
    check("exactly 2 rows written (header + lead)", len(spy["rows"]) == 2, str(len(spy["rows"])))
    check("row 1 is the header", spy["rows"][0] == expected)
    check("row 2 is the lead", spy["rows"][1][1] == "A")

    print("\n[1b] Sheet that already has a header → not touched, not duplicated")
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=["Date", "Full Name", "Email"])
    run(s.append_lead(["2026-09-09 01:47", "B", "b@x.com", "P", "+213770772883", "@b", "2", "en"]))
    check("only 1 row written (the lead, no second header)", len(spy["rows"]) == 1,
          str(len(spy["rows"])))
    check("no header among the written rows", expected not in spy["rows"])

    print("\n[1bb] Row 1 with a stray cell → left alone, lead still lands in column A")
    # Never overwrite anything already in row 1 -- that is the caller's data.
    # The important guarantee is that the lead is still anchored to column A
    # and does not drift to wherever the stray cell happens to sit.
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=["", "", "", "", "", "", "", "", "", "Affiliate ID"])
    run(s.append_lead(["2026-09-09 01:47", "S", "s@x.com", "P", "+213770772883", "@s", "9", "en"]))
    check("row 1 not overwritten (only the lead was written)", len(spy["rows"]) == 1,
          str(len(spy["rows"])))
    check("lead is the row written", spy["rows"][0][1] == "S", str(spy["rows"][0][:3]))
    check("anchored to A1, does not drift to the stray column",
          set(spy["ranges"]) == {"A1"}, str(spy["ranges"]))

    print("\n[1bc] Truly blank row 1 → header written")
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=["", "", ""])
    run(s.append_lead(["2026-09-09 01:47", "T", "t@x.com", "P", "+201000000", "@t", "9", "en"]))
    check("header written", spy["rows"][0] == expected, str(spy["rows"][0][:3]))

    print("\n[1c] Sheet with an OLD 8-column header → still not duplicated")
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=["Date (UTC)", "Full name", "Email"])
    run(s.append_lead(["2026-09-09 01:47", "C", "c@x.com", "P", "+20100000000", "@c", "3", "en"]))
    check("only the lead row written", len(spy["rows"]) == 1, str(len(spy["rows"])))
    check("lead still has 10 columns", len(spy["rows"][0]) == 10)


# ── 2. date ───────────────────────────────────────────────────────────────────
def test_date():
    print("\n[2] Date format: 'YYYY-MM-DD HH:MM (Dayname)'")
    s = load_sheets(**OAUTH)
    cases = [
        ("2026-09-09 01:47", "2026-09-09 01:47 (Wednesday)"),
        ("2026-09-08 23:00", "2026-09-08 23:00 (Tuesday)"),
        ("2026-09-13 12:30", "2026-09-13 12:30 (Sunday)"),
        ("2026-01-01 00:00", "2026-01-01 00:00 (Thursday)"),
        ("2026-09-09 01:47:33", "2026-09-09 01:47 (Wednesday)"),
    ]
    for raw, want in cases:
        got = s._format_date(raw)
        check(f"{raw!r} -> {want!r}", got == want, got)

    check("already-formatted value is not double-suffixed",
          s._format_date("2026-09-09 01:47 (Wednesday)") == "2026-09-09 01:47 (Wednesday)",
          s._format_date("2026-09-09 01:47 (Wednesday)"))
    check("unrecognised text passed through, not discarded",
          s._format_date("whatever") == "whatever", s._format_date("whatever"))
    blank = s._format_date("")
    check("blank falls back to now, never an empty Date cell",
          blank.endswith(")") and len(blank) > 18, blank)
    check("day name is English regardless of locale",
          all(d in s.DAY_NAMES for d in ["Monday", "Sunday"]))


# ── 3. country ────────────────────────────────────────────────────────────────
def test_country():
    print("\n[3] Country derived from the phone's dialling code")
    s = load_sheets(**OAUTH)
    cases = [
        ("+213770772883",   "Algeria",  "Algeria, well-formed"),
        ("+2130772883453",  "Algeria",  "Algeria, MALFORMED (extra 0, 1 digit too long)"),
        ("+201234567890",   "Egypt",    "Egypt, well-formed"),
        ("+20 10 1234 5678", "Egypt",   "Egypt, with spaces"),
        ("+9647701234567",  "Iraq",     "Iraq, well-formed"),
        ("+964 770 123 4567", "Iraq",   "Iraq, with spaces"),
    ]
    for phone, want, label in cases:
        got = s._country_from_phone(phone)
        check(f"{phone:20} -> {want!r}  ({label})", got == want, got)

    print("\n[3a] Unparseable / hostile input -> empty string, never a crash")
    for bad, label in [("+999999999999", "no such country code"),
                       ("not-a-number", "free text"),
                       ("", "empty"),
                       (None, "None"),
                       ("12345", "no + prefix"),
                       ("+", "just a plus"),
                       ("++++", "garbage"),
                       ("0772883453", "local format, no country code"),
                       (12345, "an int, not a str")]:
        try:
            got = s._country_from_phone(bad)
            ok = got == ""
        except Exception as e:
            got, ok = f"RAISED {type(e).__name__}", False
        check(f"{str(bad):20} -> ''  ({label})", ok, repr(got))


# ── 4. full row ───────────────────────────────────────────────────────────────
def test_row_shape():
    print("\n[4] Full row: 8 existing columns untouched + Country + Affiliate ID")
    s = load_sheets(**OAUTH)
    incoming = ["2026-09-09 01:47", "Yacine B.", "yacine@mail.com", "PROMO7",
                "+2130772883453", "@yacine", "556677", "fr"]
    spy = install_fake_gspread(existing_header=["Date"])
    run(s.append_lead(incoming))
    got = spy["rows"][0]

    check("row has exactly 10 columns", len(got) == 10, str(len(got)))
    check("col 0 Date reformatted", got[0] == "2026-09-09 01:47 (Wednesday)", got[0])
    for i, name in [(1, "Full Name"), (2, "Email"), (3, "Promo Code"), (4, "Phone"),
                    (5, "Telegram Username"), (6, "Telegram ID"), (7, "Language")]:
        check(f"col {i} {name} passed through unchanged", got[i] == incoming[i], repr(got[i]))
    check("col 8 Country derived", got[8] == "Algeria", repr(got[8]))
    check("col 9 Affiliate ID always blank", got[9] == "", repr(got[9]))
    check("written as RAW so Sheets cannot reinterpret the values",
          set(spy["opts"]) == {"RAW"}, str(spy["opts"]))
    check("anchored to A1 so columns cannot drift",
          set(spy["ranges"]) == {"A1"}, str(spy["ranges"]))

    print("\n[4c] Values Sheets would otherwise mangle survive verbatim")
    s2 = load_sheets(**OAUTH)
    spy2 = install_fake_gspread(existing_header=["Date"])
    run(s2.append_lead(["2026-09-09 01:47", "Z", "z@x.com", "P",
                        "+213770772883", "@z", "000000", "en"]))
    g2 = spy2["rows"][0]
    check("phone keeps its leading +", g2[4] == "+213770772883", repr(g2[4]))
    check("telegram id keeps leading zeros", g2[6] == "000000", repr(g2[6]))
    check("append option is RAW", spy2["opts"] == ["RAW"], str(spy2["opts"]))

    print("\n[4a] Affiliate ID stays blank even if a caller supplies extra values")
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=["Date"])
    run(s.append_lead(incoming + ["JUNK", "MORE"]))
    check("extra caller values ignored, still 10 cols", len(spy["rows"][0]) == 10)
    check("Affiliate ID still blank", spy["rows"][0][9] == "", repr(spy["rows"][0][9]))

    print("\n[4b] Short row from a caller is padded, not crashed")
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=["Date"])
    run(s.append_lead(["2026-09-09 01:47", "Solo"]))
    check("padded to 10 columns", len(spy["rows"][0]) == 10, str(len(spy["rows"][0])))
    check("missing phone -> empty Country", spy["rows"][0][8] == "", repr(spy["rows"][0][8]))


# ── 5. still a no-op when unconfigured ────────────────────────────────────────
def test_still_noop():
    print("\n[5] Unconfigured is still a safe no-op")
    s = load_sheets()
    check("append_lead() returns False, no exception",
          run(s.append_lead(["2026-09-09 01:47", "X", "", "", "+213770772883"])) is False)
    check("helpers work standalone even when disabled",
          s._country_from_phone("+201234567890") == "Egypt")


# ── 6. realistic sample, printed for eyeballing ───────────────────────────────
def show_sample():
    print("\n[6] What actually lands in the sheet")
    s = load_sheets(**OAUTH)
    spy = install_fake_gspread(existing_header=[])
    leads = [
        ["2026-09-09 01:47", "Yacine Benali", "yacine@mail.com", "1XPRO", "+213770772883", "@yacine", "556677", "fr"],
        ["2026-09-09 09:15", "Karim Waleed", "karim@mail.com", "1XKW", "+201234567890", "@karim", "112233", "ar"],
        ["2026-09-12 18:02", "Ali Hassan", "ali@mail.com", "1XAH", "+9647701234567", "@ali", "445566", "ar"],
        ["2026-09-13 22:40", "Broken Number", "b@mail.com", "1XBN", "+2130772883453", "@broken", "778899", "fr"],
        ["2026-09-13 23:05", "No Phone", "n@mail.com", "1XNP", "not-a-number", "@nophone", "990011", "en"],
    ]
    for l in leads:
        run(s.append_lead(l))

    widths = [28, 15, 17, 9, 17, 10, 12, 5, 9, 13]
    for i, r in enumerate(spy["rows"]):
        cells = " | ".join(str(c).ljust(w)[:w] for c, w in zip(r, widths))
        print(("  HDR  " if i == 0 else f"  r{i}   ") + cells)
    check("header + 5 leads written", len(spy["rows"]) == 6, str(len(spy["rows"])))
    check("every row has 10 columns", all(len(r) == 10 for r in spy["rows"]))
    check("countries: Algeria, Egypt, Iraq, Algeria, ''",
          [r[8] for r in spy["rows"][1:]] == ["Algeria", "Egypt", "Iraq", "Algeria", ""],
          str([r[8] for r in spy["rows"][1:]]))


if __name__ == "__main__":
    if sys.version_info >= (3, 10):
        asyncio.set_event_loop(asyncio.new_event_loop())
    test_header()
    test_date()
    test_country()
    test_row_shape()
    test_still_noop()
    show_sample()
    print("\n" + "=" * 60)
    print(f"{len(PASS)} passed, {len(FAIL)} failed")
    for f in FAIL:
        print("  FAILED:", f)
    print("=" * 60)
    sys.exit(1 if FAIL else 0)
