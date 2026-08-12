#!/usr/bin/env python3
"""
Regenerate every derived NEXO brand asset from the masters in brand-source/.

    python3 tools/build-brand-assets.py

The previous identity's generator was never kept, so the icons had to be rebuilt by
hand when the mark changed. This script exists so that does not happen again: it is
the single source of truth for everything below, and re-running it is the only
supported way to reissue them.

Reads (brand-source/):
    symbol-master.png   the approved X, flat single colour on white
    lockup-en.jpg       LTR master: symbol left, NEXO + ENGINEERING & CONTRACTING
    lockup-ar.jpg       supplied AR artwork, symbol left (see build_lockups)

Writes:
    assets/brand/nexo-symbol.svg      vector master, fill="currentColor"
    assets/brand/nexo-lockup-en.png   dark-surface lockup, 3x
    assets/brand/nexo-lockup-ar.png   dark-surface lockup, 3x, symbol RIGHT per 2.2
    assets/icons/{favicon-32,apple-touch-icon,icon-192,icon-512}.png
    favicon.ico
    assets/images/og-cover.png

Requires Pillow only. No network access; the mono face used on the OG card is
committed at tools/fonts/.

Section references are to design.md (Digital Identity Guidelines v2.0).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "brand-source")
BRAND = os.path.join(ROOT, "assets", "brand")
ICONS = os.path.join(ROOT, "assets", "icons")
IMAGES = os.path.join(ROOT, "assets", "images")
MONO = os.path.join(ROOT, "tools", "fonts", "IBMPlexMono-Medium.ttf")

# 3.1 / 3.2 / 3.4 — the palette is the authority. #D4AF37 and #2E2E2E are superseded.
GOLD = (201, 162, 78)        # C9A24E  NEXO Gold
GOLD_DEEP = (138, 111, 46)   # 8A6F2E
INK = (10, 12, 16)           # 0A0C10  Deep Ink
INK_PANEL = (23, 27, 36)     # 171B24
SILVER = (227, 231, 238)     # E3E7EE  Structural Silver
MUTE = (138, 147, 163)       # 8A93A3

# 2.3 — clear space on all four sides equals one arm's stroke width. The traced
# member is ~148 units wide in a 1000 box, so the mark occupies ~70% of an icon.
CLEAR_SPACE = 0.148

SS = 4  # supersampling factor for polygon rasterisation


def luma(rgb):
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b


# ---------------------------------------------------------------- symbol vector


def trace_symbol(path):
    """Trace the flat master into a closed polygon in a 0..1000 box.

    The mark is built from straight cuts only (2.1), so a Moore-neighbour boundary
    walk followed by Douglas-Peucker collapses cleanly to ~26 vertices with no
    curve fitting. The angled end-cuts and the central joint void survive exactly;
    the void is the mark's defining feature and must never be closed or softened.
    """
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()

    def filled(x, y):
        if x < 0 or y < 0 or x >= w or y >= h:
            return False
        r, g, b = px[x, y]
        return r > 120 and r < 235 and b < 170 and (r - b) > 45

    start = None
    for y in range(h):
        for x in range(w):
            if filled(x, y):
                start = (x, y)
                break
        if start:
            break
    if start is None:
        raise SystemExit("no mark found in %s" % path)

    nbr = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    cur, d, pts = start, 0, [start]
    for _ in range(400000):
        for k in range(8):
            di = (d + 6 + k) % 8
            nx, ny = cur[0] + nbr[di][0], cur[1] + nbr[di][1]
            if filled(nx, ny):
                cur, d = (nx, ny), di
                pts.append(cur)
                break
        else:
            break
        if cur == start and len(pts) > 10:
            break

    def rdp(p, eps):
        if len(p) < 3:
            return p
        a, b = p[0], p[-1]
        far, idx = -1.0, 0
        for i in range(1, len(p) - 1):
            x, y = p[i]
            den = math.hypot(b[0] - a[0], b[1] - a[1])
            dist = (abs((b[0] - a[0]) * (a[1] - y) - (a[0] - x) * (b[1] - a[1])) / den
                    if den else math.hypot(x - a[0], y - a[1]))
            if dist > far:
                far, idx = dist, i
        if far > eps:
            return rdp(p[:idx + 1], eps)[:-1] + rdp(p[idx:], eps)
        return [a, b]

    # Split the closed loop before simplifying: with start == end the perpendicular
    # distance is measured against a zero-length segment and everything collapses.
    a = pts[0]
    split = max(range(len(pts)), key=lambda i: (pts[i][0] - a[0]) ** 2 + (pts[i][1] - a[1]) ** 2)
    poly = rdp(pts[:split + 1], 2.5)[:-1] + rdp(pts[split:], 2.5)[:-1]

    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    ox, oy = min(xs), min(ys)
    scale = 1000.0 / max(max(xs) - ox, max(ys) - oy)
    return [((x - ox) * scale, (y - oy) * scale) for x, y in poly]


def write_symbol_svg(poly):
    d = "M " + " L ".join("%.2f %.2f" % p for p in poly) + " Z"
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" '
        'role="img" aria-label="NEXO">\n'
        "  <title>NEXO</title>\n"
        "  <!-- Generated by tools/build-brand-assets.py from brand-source/symbol-master.png.\n"
        "       Straight cuts only. The diagonal void at the crossing is THE JOINT (2.1):\n"
        "       never close, fill, soften or round it. Uniform scaling only (2.4). -->\n"
        '  <path fill="currentColor" d="%s"/>\n'
        "</svg>\n" % d
    )
    os.makedirs(BRAND, exist_ok=True)
    with open(os.path.join(BRAND, "nexo-symbol.svg"), "w") as fh:
        fh.write(svg)
    return d


def render_symbol(poly, size, fg, bg=None, clear=CLEAR_SPACE):
    """Rasterise the mark, supersampled then downsampled so the cuts stay clean."""
    big = size * SS
    inner = big * (1 - 2 * clear)
    off = big * clear
    pts = [(off + x / 1000.0 * inner, off + y / 1000.0 * inner) for x, y in poly]

    im = Image.new("RGBA", (big, big), (bg + (255,)) if bg else (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon(pts, fill=fg + (255,))
    return im.resize((size, size), Image.LANCZOS)


# ------------------------------------------------------------------- lockups


def _art_bbox(px, w, h):
    cols = [x for x in range(w) if any(luma(px[x, y]) < 225 for y in range(h))]
    rows = [y for y in range(h) if any(luma(px[x, y]) < 225 for x in range(w))]
    return cols[0], rows[0], cols[-1], rows[-1]


def extract_lockup(path):
    """Lift the supplied artwork off its white JPEG background, recoloured for dark.

    The supplied lockups are black-on-white JPEGs, unusable on Deep Ink. 2.4 forbids
    rebuilding the wordmark in a substitute typeface, so the letterforms are kept as
    raster and only their colour is changed: the near-black wordmark becomes
    Structural Silver, the gold run is renormalised to NEXO Gold.

    Each pixel is treated as its foreground composited over white, so alpha recovers
    from luminance against that foreground's own solid tone. Keying on luminance
    alone would leave the gold half-transparent -- it is far lighter than the
    wordmark, and a flat key reads that lightness as "nearly white".

    Returns (image, split_x) where split_x is the gap between symbol and wordmark.
    """
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    x0, y0, x1, y1 = _art_bbox(px, w, h)

    def is_gold(rgb):
        r, g, b = rgb
        return (r - b) > 25 and r > 90

    # Measure the solid tones actually present rather than trusting nominal values;
    # JPEG shifts them a little and the alpha solve is sensitive to the endpoint.
    golds = [luma(px[x, y]) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
             if is_gold(px[x, y])]
    darks = [luma(px[x, y]) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)
             if not is_gold(px[x, y]) and luma(px[x, y]) < 120]
    golds.sort()
    darks.sort()
    y_gold = golds[len(golds) // 2] if golds else 164.0
    y_dark = darks[len(darks) // 2] if darks else 48.0

    out = Image.new("RGBA", (x1 - x0 + 1, y1 - y0 + 1), (0, 0, 0, 0))
    op = out.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            rgb = px[x, y]
            lum = luma(rgb)
            if lum >= 250:
                continue
            if is_gold(rgb):
                fg, solid = GOLD, y_gold
            else:
                fg, solid = SILVER, y_dark
            a = (255.0 - lum) / (255.0 - solid)
            a = 0.0 if a < 0 else (1.0 if a > 1 else a)
            op[x - x0, y - y0] = fg + (int(round(a * 255)),)

    # Widest fully empty column band inside the artwork = the symbol/wordmark gap.
    colcount = [sum(1 for y in range(y0, y1 + 1) if luma(px[x, y]) < 225)
                for x in range(x0, x1 + 1)]
    best, run = (0, 0), None
    for i, c in enumerate(colcount + [1]):
        if c == 0 and run is None:
            run = i
        elif c != 0 and run is not None:
            if i - run > best[1] - best[0]:
                best = (run, i)
            run = None
    return out, best


def build_lockups(target_h=138):
    """Export both lockups at 3x the 46px display height.

    2.3 sets the full-lockup floor at 140px wide. The artwork is ~3.7:1, so the
    46px display height used in the header and the title block yields ~171px --
    clear of the floor, which the previous 40px footer logo was not.
    """
    os.makedirs(BRAND, exist_ok=True)
    sizes = {}

    for lang in ("en", "ar"):
        art, (gap_a, gap_b) = extract_lockup(os.path.join(SRC, "lockup-%s.jpg" % lang))

        if lang == "ar":
            # 2.2 -- the RTL master places the symbol on the RIGHT, wordmark left of
            # it. The supplied Arabic file has it on the left, so the two blocks are
            # swapped here. This mirrors the LAYOUT only: the symbol is moved, never
            # flipped, and each block keeps its own internal composition and its own
            # vertical position.
            symbol = art.crop((0, 0, gap_a, art.height))
            word = art.crop((gap_b, 0, art.width, art.height))
            gap = gap_b - gap_a
            art2 = Image.new("RGBA", art.size, (0, 0, 0, 0))
            art2.paste(word, (0, 0), word)
            art2.paste(symbol, (word.width + gap, 0), symbol)
            art = art2

        w = max(1, int(round(art.width * target_h / art.height)))
        out = art.resize((w, target_h), Image.LANCZOS)
        path = os.path.join(BRAND, "nexo-lockup-%s.png" % lang)
        out.save(path, optimize=True)
        sizes[lang] = out.size
        print("  assets/brand/nexo-lockup-%s.png  %dx%d" % (lang, out.width, out.height))
    return sizes


# --------------------------------------------------------------------- icons


def build_icons(poly):
    os.makedirs(ICONS, exist_ok=True)
    for name, size in (("favicon-32", 32), ("apple-touch-icon", 180),
                       ("icon-192", 192), ("icon-512", 512)):
        im = render_symbol(poly, size, GOLD, INK)
        im.convert("RGB").save(os.path.join(ICONS, "%s.png" % name), optimize=True)
        print("  assets/icons/%s.png  %dx%d" % (name, size, size))

    ico = render_symbol(poly, 256, GOLD, INK).convert("RGB")
    ico.save(os.path.join(ROOT, "favicon.ico"),
             sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico  16/32/48")


# ------------------------------------------------------------------ og cover


def build_og(poly):
    """1200x630 social card: real lockup letterforms, real mark, drafting grid."""
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), INK)
    dr = ImageDraw.Draw(im)

    # 6 -- drafting grid. Ink Panel rather than Rule at 6%: the guideline value is
    # tuned for a screen you look at directly, and vanishes entirely once a social
    # card is JPEG-recompressed and shown at thumbnail size.
    for x in range(0, W, 80):
        dr.line([(x, 0), (x, H)], fill=INK_PANEL, width=1)
    for y in range(0, H, 80):
        dr.line([(0, y), (W, y)], fill=INK_PANEL, width=1)

    mark = render_symbol(poly, 300, GOLD, clear=0.0)
    im.paste(mark, (W - 300 - 110, (H - 300) // 2), mark)

    # 2.4 -- the wordmark is the supplied artwork, never re-set in a substitute face.
    art, (gap_a, gap_b) = extract_lockup(os.path.join(SRC, "lockup-en.jpg"))
    word = art.crop((gap_b, 0, art.width, art.height))
    ww = 470
    word = word.resize((ww, max(1, int(round(word.height * ww / word.width)))), Image.LANCZOS)
    im.paste(word, (86, (H - word.height) // 2 - 6), word)

    font = ImageFont.truetype(MONO, 21)
    small = ImageFont.truetype(MONO, 18)

    top = (H - word.height) // 2 - 6
    dr.line([(88, top - 44), (128, top - 44)], fill=GOLD, width=3)
    dr.text((142, top - 55), "BAGHDAD · IRAQ", font=font, fill=GOLD)

    # The three codes are parallel disciplines, not a sequence, so they sit on one
    # rule as equals -- stacking one of them below the others implies an order.
    base = top + word.height + 52
    dr.line([(88, base), (742, base)], fill=GOLD_DEEP, width=1)
    for x, code, name in ((88, "A—01", "DESIGN"),
                          (310, "C—02", "CONTRACTING"),
                          (562, "T—03", "TRAINING")):
        dr.text((x, base + 20), code, font=small, fill=GOLD)
        dr.text((x + 62, base + 20), name, font=small, fill=MUTE)

    os.makedirs(IMAGES, exist_ok=True)
    im.save(os.path.join(IMAGES, "og-cover.png"), optimize=True)
    print("  assets/images/og-cover.png  %dx%d" % (W, H))


def main():
    print("Tracing brand-source/symbol-master.png ...")
    poly = trace_symbol(os.path.join(SRC, "symbol-master.png"))
    print("  %d vertices, all straight cuts" % len(poly))
    write_symbol_svg(poly)
    print("  assets/brand/nexo-symbol.svg")

    print("Lockups ...")
    build_lockups()
    print("Icons ...")
    build_icons(poly)
    print("Social card ...")
    build_og(poly)
    print("Done.")


if __name__ == "__main__":
    main()
