from aiogram.utils.keyboard import InlineKeyboardBuilder
from texts import (TEXTS, LANGS, BTN_FAQ, BTN_FAQ_BACK, FAQ, FAQ_INTRO, BTN_REFER,
                   BTN_DEMO, DEMO_CREATE_BTN, DEMO_RECHARGE_BTN)


def lang_kb():
    b = InlineKeyboardBuilder()
    for code, label in LANGS:
        b.button(text=label, callback_data=f"lang:{code}")
    b.adjust(2)
    return b.as_markup()


def menu_kb(lang: str):
    t = TEXTS[lang]
    b = InlineKeyboardBuilder()
    b.button(text=t["btn_register"], callback_data=f"m:register:{lang}")
    b.button(text=t["btn_commission"], callback_data=f"m:commission:{lang}")
    b.button(text=t["btn_withdraw"], callback_data=f"m:withdraw:{lang}")
    b.button(text=t["btn_banners"], callback_data=f"m:banners:{lang}")
    b.button(text=t["btn_about"], callback_data=f"m:about:{lang}")
    b.button(text=BTN_DEMO[lang], callback_data=f"m:demo:{lang}")
    b.button(text=BTN_REFER[lang], callback_data=f"m:refer:{lang}")
    b.button(text=BTN_FAQ[lang], callback_data=f"m:faq:{lang}")
    b.button(text=t["btn_lang"], callback_data="m:lang:_")
    b.adjust(1, 2, 2, 2, 2)
    return b.as_markup()


def demo_choice_kb(lang: str):
    b = InlineKeyboardBuilder()
    b.button(text=DEMO_CREATE_BTN[lang], callback_data=f"demo:create:{lang}")
    b.button(text=DEMO_RECHARGE_BTN[lang], callback_data=f"demo:recharge:{lang}")
    b.button(text=TEXTS[lang]["btn_back"], callback_data=f"m:menu:{lang}")
    b.adjust(1)
    return b.as_markup()


def faq_list_kb(lang: str):
    b = InlineKeyboardBuilder()
    for i, (label, _ans) in enumerate(FAQ[lang]):
        b.button(text=label, callback_data=f"faq:{i}:{lang}")
    b.button(text=TEXTS[lang]["btn_back"], callback_data=f"m:menu:{lang}")
    b.adjust(1)
    return b.as_markup()


def faq_answer_kb(lang: str):
    b = InlineKeyboardBuilder()
    b.button(text=BTN_FAQ_BACK[lang], callback_data=f"faq:list:{lang}")
    b.button(text=TEXTS[lang]["btn_back"], callback_data=f"m:menu:{lang}")
    b.adjust(1)
    return b.as_markup()


def back_kb(lang: str):
    b = InlineKeyboardBuilder()
    b.button(text=TEXTS[lang]["btn_back"], callback_data=f"m:menu:{lang}")
    return b.as_markup()


def confirm_kb(lang: str):
    b = InlineKeyboardBuilder()
    b.button(text=TEXTS[lang]["btn_confirm"], callback_data=f"reg:confirm:{lang}")
    b.button(text=TEXTS[lang]["btn_restart"], callback_data=f"reg:restart:{lang}")
    b.adjust(1)
    return b.as_markup()
