"""Stamps a partner's promo code onto a pre-rendered generic banner template."""
import os
from PIL import Image, ImageDraw, ImageFont

_HERE = os.path.dirname(__file__)
_TEMPLATES = os.path.join(_HERE, "media", "templates")
_FONT = os.path.join(_HERE, "media", "ArchivoBlack.ttf")

# pixel box (x0,y0,x1,y1) where the code text is centered, per style
_CODE_BOX = {
    "cinematic": (200, 712, 880, 770),
    "bright": (200, 690, 880, 748),
}
_CODE_COLOR = {
    "cinematic": (20, 28, 52),
    "bright": (20, 28, 52),
}

STYLES = ("cinematic", "bright")
LANGS = ("ar", "fa", "fr", "en", "es", "ru")


def _fit_font(draw, text, max_w, max_size=52, min_size=22):
    size = max_size
    while size > min_size:
        f = ImageFont.truetype(_FONT, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(_FONT, min_size)


def generate(style: str, lang: str, code: str, out_path: str) -> str:
    if style not in STYLES:
        raise ValueError(f"unknown style {style}")
    if lang not in LANGS:
        raise ValueError(f"unknown lang {lang}")
    template_path = os.path.join(_TEMPLATES, f"{style}_{lang}.png")
    img = Image.open(template_path).convert("RGB")
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = _CODE_BOX[style]
    code = code.strip()[:24]  # sane length cap
    f = _fit_font(d, code, x1 - x0 - 40)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.text((cx, cy), code, font=f, fill=_CODE_COLOR[style], anchor="mm")
    img.save(out_path, quality=95)
    return out_path
