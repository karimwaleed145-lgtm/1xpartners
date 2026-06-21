import re
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import os
from datetime import datetime
from aiogram.types import FSInputFile
from aiogram.types import FSInputFile as _FS
from texts import TEXTS, DEFAULT_LANG, CHOOSE_LANG, FAQ, FAQ_INTRO, REFER_TEXT, DEMO
from config import REFERRAL_VIDEO_FILE_ID
from keyboards import lang_kb, menu_kb, back_kb, confirm_kb, faq_list_kb, faq_answer_kb, demo_choice_kb
from sheets import append_lead
from database import save_partner
from config import ADMIN_IDS

router = Router()
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


async def _show(c: CallbackQuery, text: str, markup):
    """Edit the message if it's text; if it's media (video/photo) or edit fails, send fresh."""
    try:
        if c.message.text is not None:
            await c.message.edit_text(text, reply_markup=markup)
            return
    except Exception:
        pass
    await c.message.answer(text, reply_markup=markup)

INFO_KEYS = {"commission": "commission", "withdraw": "withdraw", "banners": "banners", "about": "about"}


class Reg(StatesGroup):
    name = State()
    email = State()
    promocode = State()
    phone = State()


class Demo(StatesGroup):
    aff_id = State()
    player_id = State()
    currency = State()
    screenshot = State()


_MEDIA = os.path.join(os.path.dirname(__file__), "media")


def L(lang: str) -> str:
    return lang if lang in TEXTS else DEFAULT_LANG


# ---------- start & language ----------
@router.message(CommandStart())
async def start(m: Message, state: FSMContext):
    await state.clear()
    await m.answer(CHOOSE_LANG, reply_markup=lang_kb())


@router.callback_query(F.data.startswith("lang:"))
async def set_lang(c: CallbackQuery, state: FSMContext):
    lang = L(c.data.split(":")[1])
    await state.clear()
    await state.update_data(lang=lang)
    await c.message.edit_text(TEXTS[lang]["welcome"], reply_markup=menu_kb(lang))
    await c.answer()


@router.callback_query(F.data == "m:lang:_")
async def change_lang(c: CallbackQuery):
    await c.message.edit_text(CHOOSE_LANG, reply_markup=lang_kb())
    await c.answer()


@router.callback_query(F.data.startswith("m:menu:"))
async def to_menu(c: CallbackQuery, state: FSMContext):
    lang = L(c.data.split(":")[2])
    await state.clear()
    await state.update_data(lang=lang)
    await _show(c, TEXTS[lang]["welcome"], menu_kb(lang))
    await c.answer()


# ---------- info pages ----------
@router.callback_query(F.data.regexp(r"^m:(commission|withdraw|banners|about):"))
async def info_page(c: CallbackQuery):
    _, key, lang = c.data.split(":")
    lang = L(lang)
    await _show(c, TEXTS[lang][INFO_KEYS[key]], back_kb(lang))
    await c.answer()


@router.callback_query(F.data.startswith("m:faq:"))
async def faq_open(c: CallbackQuery):
    lang = L(c.data.split(":")[2])
    await _show(c, FAQ_INTRO[lang], faq_list_kb(lang))
    await c.answer()


@router.callback_query(F.data.startswith("faq:"))
async def faq_item(c: CallbackQuery):
    parts = c.data.split(":")
    key, lang = parts[1], L(parts[2])
    if key == "list":
        await _show(c, FAQ_INTRO[lang], faq_list_kb(lang))
    else:
        i = int(key)
        await _show(c, FAQ[lang][i][1], faq_answer_kb(lang))
    await c.answer()


# ---------- referral / sub-manager ----------
_VIDEO_PATH = os.path.join(os.path.dirname(__file__), "media", "referral_howto.mp4")


@router.callback_query(F.data.startswith("m:refer:"))
async def refer(c: CallbackQuery, bot: Bot):
    lang = L(c.data.split(":")[2])
    await c.answer()
    caption = REFER_TEXT[lang]
    try:
        if REFERRAL_VIDEO_FILE_ID:
            video = REFERRAL_VIDEO_FILE_ID
        elif os.path.exists(_VIDEO_PATH):
            video = FSInputFile(_VIDEO_PATH)
        else:
            video = None
        if video is not None:
            sent = await bot.send_video(c.from_user.id, video, caption=caption, reply_markup=back_kb(lang))
            # log the file_id once so you can set REFERRAL_VIDEO_FILE_ID for faster resends
            try:
                if sent.video and not REFERRAL_VIDEO_FILE_ID:
                    print("REFERRAL_VIDEO_FILE_ID =", sent.video.file_id)
            except Exception:
                pass
        else:
            await bot.send_message(c.from_user.id, caption, reply_markup=back_kb(lang))
    except Exception as e:
        print("Referral video error:", e)
        await bot.send_message(c.from_user.id, caption, reply_markup=back_kb(lang))


# ---------- demo account (create / recharge) ----------
@router.callback_query(F.data.startswith("m:demo:"))
async def demo_open(c: CallbackQuery, state: FSMContext):
    lang = L(c.data.split(":")[2])
    await state.clear()
    await _show(c, DEMO[lang]["intro"], demo_choice_kb(lang))
    await c.answer()


@router.callback_query(F.data.regexp(r"^demo:(create|recharge):"))
async def demo_start(c: CallbackQuery, state: FSMContext, bot: Bot):
    _, kind, lang = c.data.split(":")
    lang = L(lang)
    await state.set_state(Demo.aff_id)
    await state.update_data(lang=lang, kind=kind)
    cond = DEMO[lang]["cond_create"] if kind == "create" else DEMO[lang]["cond_recharge"]
    await c.answer()
    await bot.send_message(c.from_user.id, cond)
    # show the Aff ID helper image, then ask for the Aff ID
    img = os.path.join(_MEDIA, "affid_help.jpg")
    try:
        if os.path.exists(img):
            await bot.send_photo(c.from_user.id, _FS(img), caption=DEMO[lang]["ask_aff"])
        else:
            await bot.send_message(c.from_user.id, DEMO[lang]["ask_aff"])
    except Exception as e:
        print("affid image error:", e)
        await bot.send_message(c.from_user.id, DEMO[lang]["ask_aff"])


@router.message(Demo.aff_id)
async def demo_aff(m: Message, state: FSMContext):
    data = await state.get_data(); lang = L(data.get("lang", DEFAULT_LANG))
    await state.update_data(aff_id=(m.text or "").strip())
    await state.set_state(Demo.player_id)
    await m.answer(DEMO[lang]["ask_player"])


@router.message(Demo.player_id)
async def demo_player(m: Message, state: FSMContext):
    data = await state.get_data(); lang = L(data.get("lang", DEFAULT_LANG))
    await state.update_data(player_id=(m.text or "").strip())
    await state.set_state(Demo.currency)
    await m.answer(DEMO[lang]["ask_currency"])


@router.message(Demo.currency)
async def demo_currency(m: Message, state: FSMContext, bot: Bot):
    data = await state.get_data(); lang = L(data.get("lang", DEFAULT_LANG))
    await state.update_data(currency=(m.text or "").strip())
    await state.set_state(Demo.screenshot)
    # show how-to-find-deposits videos, then ask for the screenshot
    for fn in ("deposits_apk.mp4", "deposits_site.mp4"):
        p = os.path.join(_MEDIA, fn)
        try:
            if os.path.exists(p):
                await bot.send_video(m.chat.id, _FS(p))
        except Exception as e:
            print("deposit video error:", e)
    await m.answer(DEMO[lang]["ask_shot"])


@router.message(Demo.screenshot, F.photo)
async def demo_shot(m: Message, state: FSMContext, bot: Bot):
    data = await state.get_data(); lang = L(data.get("lang", DEFAULT_LANG))
    kind = data.get("kind", "create")
    photo_id = m.photo[-1].file_id
    uname = f"@{m.from_user.username}" if m.from_user.username else "—"
    header = DEMO[lang]["admin_create"] if kind == "create" else DEMO[lang]["admin_recharge"]
    caption = (
        f"{header}\n"
        f"🆔 Aff ID: {data.get('aff_id','')}\n"
        f"🎮 Player ID: {data.get('player_id','')}\n"
        f"💱 Currency: {data.get('currency','')}\n"
        f"💬 {uname} (<code>{m.from_user.id}</code>)\n"
        f"🌍 {lang}"
    )
    for aid in ADMIN_IDS:
        try:
            await bot.send_photo(aid, photo_id, caption=caption)
        except Exception as e:
            print(f"Could not send demo request to admin {aid}:", e)
    await state.clear()
    await m.answer(DEMO[lang]["received"], reply_markup=menu_kb(lang))


@router.message(Demo.screenshot)
async def demo_need_photo(m: Message, state: FSMContext):
    data = await state.get_data(); lang = L(data.get("lang", DEFAULT_LANG))
    await m.answer(DEMO[lang]["need_photo"])


# ---------- registration flow ----------
@router.callback_query(F.data.startswith("m:register:"))
async def reg_start(c: CallbackQuery, state: FSMContext):
    lang = L(c.data.split(":")[2])
    await state.set_state(Reg.name)
    await state.update_data(lang=lang)
    await c.message.edit_text(TEXTS[lang]["ask_name"])
    await c.answer()


@router.message(Reg.name)
async def reg_name(m: Message, state: FSMContext):
    data = await state.get_data()
    lang = L(data.get("lang", DEFAULT_LANG))
    name = (m.text or "").strip()
    if len(name) < 3:
        await m.answer(TEXTS[lang]["invalid_name"])
        return
    await state.update_data(full_name=name)
    await state.set_state(Reg.email)
    await m.answer(TEXTS[lang]["ask_email"])


@router.message(Reg.email)
async def reg_email(m: Message, state: FSMContext):
    data = await state.get_data()
    lang = L(data.get("lang", DEFAULT_LANG))
    email = (m.text or "").strip()
    if not EMAIL_RE.match(email):
        await m.answer(TEXTS[lang]["invalid_email"])
        return
    await state.update_data(email=email)
    await state.set_state(Reg.promocode)
    await m.answer(TEXTS[lang]["ask_promocode"])


@router.message(Reg.promocode)
async def reg_promo(m: Message, state: FSMContext):
    data = await state.get_data()
    lang = L(data.get("lang", DEFAULT_LANG))
    await state.update_data(promocode=(m.text or "").strip())
    await state.set_state(Reg.phone)
    await m.answer(TEXTS[lang]["ask_phone"])


@router.message(Reg.phone)
async def reg_phone(m: Message, state: FSMContext):
    data = await state.get_data()
    lang = L(data.get("lang", DEFAULT_LANG))
    phone = (m.text or "").strip()
    if len(re.sub(r"\D", "", phone)) < 6:
        await m.answer(TEXTS[lang]["invalid_phone"])
        return
    await state.update_data(phone=phone)
    data = await state.get_data()
    summary = TEXTS[lang]["confirm"].format(
        name=data["full_name"], email=data["email"],
        promocode=data["promocode"], phone=data["phone"],
    )
    await m.answer(summary, reply_markup=confirm_kb(lang))


@router.callback_query(F.data.startswith("reg:restart:"))
async def reg_restart(c: CallbackQuery, state: FSMContext):
    lang = L(c.data.split(":")[2])
    await state.set_state(Reg.name)
    await state.update_data(lang=lang)
    await c.message.edit_text(TEXTS[lang]["ask_name"])
    await c.answer()


@router.callback_query(F.data.startswith("reg:confirm:"))
async def reg_confirm(c: CallbackQuery, state: FSMContext, bot: Bot):
    lang = L(c.data.split(":")[2])
    data = await state.get_data()

    try:
        await save_partner(
            telegram_id=c.from_user.id,
            username=c.from_user.username,
            language=lang,
            full_name=data.get("full_name", ""),
            email=data.get("email", ""),
            promocode=data.get("promocode", ""),
            phone=data.get("phone", ""),
        )
    except Exception as e:
        print("DB save error:", e)

    uname = f"@{c.from_user.username}" if c.from_user.username else "—"

    # append to Google Sheet (no-op if not configured)
    try:
        await append_lead([
            datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
            data.get("full_name", ""), data.get("email", ""),
            data.get("promocode", ""), data.get("phone", ""),
            uname, str(c.from_user.id), lang,
        ])
    except Exception as e:
        print("Sheets error:", e)

    admin_txt = (
        "🆕 <b>New partner lead</b>\n"
        f"👤 {data.get('full_name','')}\n"
        f"📧 {data.get('email','')}\n"
        f"🎟 {data.get('promocode','')}\n"
        f"📞 {data.get('phone','')}\n"
        f"💬 {uname} (<code>{c.from_user.id}</code>)\n"
        f"🌍 {lang}"
    )
    for aid in ADMIN_IDS:
        try:
            await bot.send_message(aid, admin_txt)
        except Exception as e:
            print(f"Could not message admin {aid}:", e)

    await state.clear()
    await c.message.edit_text(TEXTS[lang]["saved"], reply_markup=menu_kb(lang))
    await c.answer()
