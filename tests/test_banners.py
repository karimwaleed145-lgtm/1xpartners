"""Standalone check for banner_gen.py — not part of the live bot, run manually or in CI.

Usage:
    python tests/test_banners.py

Loops every style x language combination, calls the real banner_gen.generate(),
and verifies: no exception, correct output dimensions, and that the stamped promo
code text is actually visible (contrasts against the code-box background) rather
than blending into it (e.g. the white-on-white regression this test was written for).
"""
import os
import sys
import traceback

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from PIL import Image
import banner_gen

OUT_DIR = os.path.join(PROJECT_ROOT, "tests", "_banner_output")
SAMPLE_CODE = "CODE123"
MIN_COLOR_DISTANCE = 40  # sum of abs per-channel diff; anti-aliased edges give small deltas, real text gives large ones


def color_distance(c1, c2):
    return sum(abs(a - b) for a, b in zip(c1, c2))


def check_combo(style, lang):
    out_path = os.path.join(OUT_DIR, f"{style}_{lang}.png")

    try:
        banner_gen.generate(style, lang, SAMPLE_CODE, out_path)
    except Exception:
        return "FAIL", f"exception during generate(): {traceback.format_exc(limit=1).strip().splitlines()[-1]}"

    template_path = os.path.join(banner_gen._TEMPLATES, f"{style}_{lang}.png")
    try:
        img = Image.open(out_path).convert("RGB")
        tmpl = Image.open(template_path).convert("RGB")
    except Exception as e:
        return "FAIL", f"could not open image(s): {e}"

    if img.size != tmpl.size:
        return "FAIL", f"dimension mismatch: output {img.size} vs template {tmpl.size}"

    x0, y0, x1, y1 = banner_gen._CODE_BOX[style]
    box = img.crop((x0, y0, x1, y1))
    w, h = box.size
    px = box.load()

    margin = 2
    bg_samples = [
        px[margin, margin], px[w - 1 - margin, margin],
        px[margin, h - 1 - margin], px[w - 1 - margin, h - 1 - margin],
    ]
    bg = tuple(sum(c[i] for c in bg_samples) // len(bg_samples) for i in range(3))

    max_dist = 0
    for yy in range(0, h, 2):
        for xx in range(0, w, 2):
            d = color_distance(px[xx, yy], bg)
            if d > max_dist:
                max_dist = d

    if max_dist < MIN_COLOR_DISTANCE:
        return "FAIL", f"text not visible — max pixel/bg color distance {max_dist} < threshold {MIN_COLOR_DISTANCE} (bg={bg})"

    return "PASS", f"size={img.size}, box bg={bg}, max text/bg color distance={max_dist}"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for style in banner_gen.STYLES:
        for lang in banner_gen.LANGS:
            status, detail = check_combo(style, lang)
            results.append((f"{style}/{lang}", status, detail))

    print(f"{'combo':16s} {'result':5s} detail")
    print("-" * 90)
    for combo, status, detail in results:
        print(f"{combo:16s} {status:5s} {detail}")

    fails = [r for r in results if r[1] == "FAIL"]
    print("-" * 90)
    print(f"Total: {len(results)}  Pass: {len(results) - len(fails)}  Fail: {len(fails)}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
