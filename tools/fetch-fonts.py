#!/usr/bin/env python3
"""
Download the self-hosted webfonts into assets/fonts/ and print the @font-face CSS.

    python3 tools/fetch-fonts.py            # download + print CSS
    python3 tools/fetch-fonts.py --dry-run  # just report what it would fetch

design.md 4.4 requires the fonts to be self-hosted as subsetted WOFF2. Serving
them from Google cost the Arabic page 548 KB across 19 files behind two extra
DNS+TLS handshakes and a render-blocking third-party stylesheet, which is why
that page — and only that page — visibly reflowed for seconds on first load.

The manifest below is the exact set of (family, weight, subset) triples the two
pages actually use. It is deliberately narrow: Cairo was being pulled at four
weights when the Arabic page only ever sets 700, which alone was 224 KB of
waste. Before adding a weight here, check that a rule really asks for it —
a weight that is downloaded but unused costs every visitor, and a weight that
is used but missing gets synthesised, which 4.6 forbids outright.

Google's own subsets are used as-is rather than re-cut: they already split
arabic / latin on sensible unicode-ranges, and the arabic subset carries the
full joining set plus Arabic-Indic numerals, which 4.4 requires be retained
even where unused so user-generated content cannot tofu.
"""

import argparse
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "fonts")
API = "https://fonts.googleapis.com/css2?family="

# A modern UA is required or the API serves TTF instead of WOFF2.
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"}

# (family, weights, subsets kept) — see the module docstring before editing.
MANIFEST = [
    # English page
    ("Archivo",              ["600", "700", "800"],        {"latin"}),
    ("Plus Jakarta Sans",    ["400", "600"],               {"latin"}),
    # Both pages. 700 is for .tb-val.ltr on the Arabic page, which inherits
    # weight 700 from .tb-val and family from .ltr; without it that one string
    # ("A / C / T") renders as synthetic bold.
    ("IBM Plex Mono",        ["400", "500", "600", "700"], {"latin"}),
    # Arabic page. Cairo is display-only and every display rule is 700.
    ("Cairo",                ["700"],                      {"arabic", "latin"}),
    # Body face, and the Arabic fallback inside --font-mono: 400 is body copy,
    # 500 is .mono/.eyebrow, 600 is .btn / .spec-row dt / .dv-code.
    ("IBM Plex Sans Arabic", ["400", "500", "600"],        {"arabic", "latin"}),
]

SLUG = {"IBM Plex Sans Arabic": "plex-sans-arabic", "IBM Plex Mono": "plex-mono",
        "Plus Jakarta Sans": "jakarta", "Archivo": "archivo", "Cairo": "cairo"}


def get(url, binary=False):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA)) as r:
        return r.read() if binary else r.read().decode()


def faces(family, weights, subsets):
    """Ask the API for one family and keep only the wanted subsets."""
    url = "%s%s:wght@%s&display=swap" % (API, family.replace(" ", "+"), ";".join(weights))
    css = get(url)
    out = []
    for m in re.finditer(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S):
        subset, block = m.group(1), m.group(2)
        if subset not in subsets:
            continue
        out.append({
            "family": re.search(r"font-family: '([^']+)'", block).group(1),
            "weight": re.search(r"font-weight: (\d+)", block).group(1),
            "range":  re.search(r"unicode-range: (.*?);", block, re.S).group(1).strip(),
            "url":    re.search(r"url\((https[^)]+)\)", block).group(1),
            "subset": subset,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.dry_run:
        os.makedirs(OUT, exist_ok=True)

    css_lines, total = [], 0
    for family, weights, subsets in MANIFEST:
        for f in faces(family, weights, subsets):
            name = "%s-%s-%s.woff2" % (SLUG[family], f["weight"], f["subset"])
            path = os.path.join(OUT, name)
            if args.dry_run:
                size = len(get(f["url"], binary=True))
            else:
                data = get(f["url"], binary=True)
                with open(path, "wb") as fh:
                    fh.write(data)
                size = len(data)
            total += size
            print("  %-40s %6.1f KB" % (name, size / 1024))
            css_lines.append(
                "        @font-face {\n"
                "            font-family: '%s';\n"
                "            font-style: normal;\n"
                "            font-weight: %s;\n"
                "            font-display: swap;\n"
                "            src: url('%s/%s') format('woff2');\n"
                "            unicode-range: %s;\n"
                "        }" % (f["family"], f["weight"], "%FONTDIR%", name, f["range"]))

    print("  %-40s %6.1f KB total" % ("", total / 1024))
    print("\n/* ---- paste into each page's <style>, %FONTDIR% -> ./assets/fonts "
          "(EN) or ../assets/fonts (AR) ---- */")
    print("\n".join(css_lines))


if __name__ == "__main__":
    main()
