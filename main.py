#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""THE WORLD TODAY - Wednesday, 25 November 2026, in one image.

Entry for the make.fun competition "news-image-20261125"
("Sum up 25 November's world news in one image", $100 pool).

The program draws a complete newspaper front page - masthead, lead
story, four side stories, a bottom story, an "also in the news" box
and a sources line - onto a 1024x1024 canvas and writes it as a PNG
to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Everything is drawn in code: a hand-built 5x7 bitmap typeface, a
small software rasteriser (rectangles, lines, circles, polylines)
and a minimal PNG encoder.  Python 3 standard library only, no
network access, no randomness, no clock: two runs always produce
byte-identical output.

Stories carried on the page (all reported 24-25 November 2026 and
checked against the sources named):

  LEAD - RIYADH: a drone launched by Yemen's Houthi fighters struck
    the tallest tower in Riyadh, the 80-storey PIF Tower in the King
    Abdullah Financial District, on Tuesday for the second time in
    less than a week, wounding at least 11 people (four Egyptians,
    three Nepalis, two Indians, two Saudis, per Saudi Civil
    Defense). The first hit, on 19 November, caused damage but no
    injuries. The Saudi-led coalition said the attack was carried
    out with a drone and vowed a decisive response.
    Sources: Reuters; Wall Street Journal; TBS News.
  FRANCE: French judges ordered former President Nicolas Sarkozy
    and his wife Carla Bruni to stand trial over the retraction of
    witness Ziad Takieddine's testimony in the Libya campaign
    funding case; 11 defendants face charges including receiving
    stolen goods, witness tampering and criminal conspiracy; an
    initial pre-trial hearing is set for 1 April 2027; a verdict on
    Sarkozy's appeal in the main Libya case is due 30 November.
    Sources: Reuters; AFP via The Voice; QNC News.
  TECH / US: a federal jury in Brooklyn convicted China's Huawei
    on 10 of 12 criminal counts, including bank fraud, wire fraud,
    sanctions violations and conspiring to steal trade secrets; it
    was acquitted of racketeering conspiracy and conspiracy to
    obstruct justice. The case began in 2018; sentencing was set
    for September 2027.
    Sources: Reuters; CNN; US Department of Justice.
  UKRAINE: President Zelenskiy confirmed Ukraine's Saturday drone
    strike on the Russian cargo ship Sparta II in the Gulf of
    Finland, calling it a legitimate military target; the ship,
    owned by defence-logistics firm Oboronlogistika and bound for
    Kaliningrad, caught fire, drifted into Finnish waters and was
    towed back to St Petersburg. Norway's Defence Minister Tore
    Sandvik urged caution and stability in the Baltic.
    Sources: Reuters; Bloomberg via gCaptain; MarineLink.
  YEMEN: Yemen's military said Houthi forces have pushed to within
    60 km (37 miles) of Aden, the internationally recognised
    government's temporary capital, but will not capture it;
    spokesman Col. Majed Abdullah Al-Nuzaily said government forces
    have set up checkpoints, reinforcements and trenches.
    Source: Reuters.
  LAOS: Lao PDR officially graduated from the United Nations'
    least developed country (LDC) category on 24 November 2026,
    ending 55 years in the group, which it joined when the category
    was established in 1971; it met all three UN criteria, with
    GNI per capita of $2,375.
    Sources: UN in Lao PDR; UN OHRLLS; KPL.
  ALSO IN THE NEWS: Trump pardons the Thanksgiving turkeys Freedom
    and Feathers (Reuters); Trump awards Rudy Giuliani the Medal
    of Freedom (Reuters); the EU proposes its 22nd Russia
    sanctions package, with a visa ban for combatants, a sports
    ban and 60 more banks off SWIFT (European Commission);
    a radar issue delays flights at Chicago O'Hare, FAA says
    (Reuters); England beat Australia by eight wickets in the
    second T20I, chasing 185 to level the series (Jagran Josh).
"""

import os
import struct
import zlib

WIDTH = 1024
HEIGHT = 1024

PAPER = (246, 243, 234)
INK = (22, 20, 18)
RED = (168, 32, 24)
ORANGE = (214, 116, 36)
GREY = (96, 92, 84)
FAINT = (203, 197, 182)
BOX = (236, 231, 218)

# ------------------------------------------------------------------
# 5x7 bitmap typeface.  Each glyph is seven rows of five pixels,
# written as strings where '#' is ink and '.' is empty.
# ------------------------------------------------------------------

FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#...#", ".###."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": (".##..", ".##..", ".#...", ".....", ".....", ".....", "....."),
    '"': ("#...#", "#...#", "#...#", ".....", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "/": ("....#", "....#", "...#.", "..#..", "..#..", ".#...", "#...."),
    "(": ("...##", "..#..", ".#...", ".#...", ".#...", "..#..", "...##"),
    ")": ("##...", "..#..", "...#.", "...#.", "...#.", "..#..", "##..."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#...", "#.##."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "*": (".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
}

# ------------------------------------------------------------------
# Canvas and rasteriser
# ------------------------------------------------------------------

PIX = bytearray(WIDTH * HEIGHT * 3)


def fill_background():
    row = bytes(PAPER) * WIDTH
    for y in range(HEIGHT):
        PIX[y * WIDTH * 3:(y + 1) * WIDTH * 3] = row


def plot(x, y, colour):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        i = (y * WIDTH + x) * 3
        PIX[i:i + 3] = bytes(colour)


def rect(x, y, w, h, colour):
    for yy in range(y, y + h):
        if 0 <= yy < HEIGHT:
            x0 = max(0, x)
            x1 = min(WIDTH, x + w)
            if x0 < x1:
                i = (yy * WIDTH + x0) * 3
                PIX[i:i + (x1 - x0) * 3] = bytes(colour) * (x1 - x0)


def line(x0, y0, x1, y1, colour, thick=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        for ox in range(thick):
            for oy in range(thick):
                plot(x0 + ox, y0 + oy, colour)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def circle(cx, cy, r, colour, thick=2):
    steps = max(24, r * 6)
    for i in range(steps + 1):
        import math
        a = 2.0 * math.pi * i / steps
        x = int(round(cx + r * math.cos(a)))
        y = int(round(cy + r * math.sin(a)))
        for ox in range(thick):
            for oy in range(thick):
                plot(x + ox, y + oy, colour)


def ellipse(cx, cy, rx, ry, colour, thick=2):
    import math
    steps = max(24, rx * 6)
    for i in range(steps + 1):
        a = 2.0 * math.pi * i / steps
        x = int(round(cx + rx * math.cos(a)))
        y = int(round(cy + ry * math.sin(a)))
        for ox in range(thick):
            for oy in range(thick):
                plot(x + ox, y + oy, colour)


# ------------------------------------------------------------------
# Text
# ------------------------------------------------------------------

def clean(text):
    out = []
    for ch in text.upper():
        if ch in FONT:
            out.append(ch)
        elif ch in "-\u2013\u2014":
            out.append("-")
        else:
            out.append(" ")
    return "".join(out)


def text_width(text, scale, spacing=1):
    text = clean(text)
    if not text:
        return 0
    return len(text) * (5 + spacing) * scale - spacing * scale


def draw_text(x, y, text, scale, colour, spacing=1):
    text = clean(text)
    cx = x
    for ch in text:
        glyph = FONT[ch]
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "#":
                    rect(cx + col * scale, y + row * scale, scale, scale, colour)
        cx += (5 + spacing) * scale
    return cx - spacing * scale


def draw_centered(y, text, scale, colour, spacing=1):
    w = text_width(text, scale, spacing)
    return draw_text((WIDTH - w) // 2, y, text, scale, colour, spacing)


def draw_right(x_right, y, text, scale, colour, spacing=1):
    w = text_width(text, scale, spacing)
    return draw_text(x_right - w, y, text, scale, colour, spacing)


def wrap(text, scale, max_width, spacing=1):
    words = clean(text).split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_width(trial, scale, spacing) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(x, y, text, scale, colour, max_width, leading):
    lines = wrap(text, scale, max_width)
    for i, ln in enumerate(lines):
        draw_text(x, y + i * leading, ln, scale, colour)
    return y + len(lines) * leading


def draw_two_columns(x, y, col_w, gap, text, scale, colour, leading):
    lines = wrap(text, scale, col_w)
    half = (len(lines) + 1) // 2
    for i, ln in enumerate(lines[:half]):
        draw_text(x, y + i * leading, ln, scale, colour)
    for i, ln in enumerate(lines[half:]):
        draw_text(x + col_w + gap, y + i * leading, ln, scale, colour)
    return y + half * leading


# ------------------------------------------------------------------
# Illustrations
# ------------------------------------------------------------------

def draw_tower(cx, top, base):
    """Riyadh's tallest tower with a red burst halfway up."""
    w = 54
    x0 = cx - w // 2
    line(x0 + 8, top, x0 + w - 8, top, INK, 3)
    line(x0 + 8, top, x0, base, INK, 3)
    line(x0 + w - 8, top, x0 + w, base, INK, 3)
    line(x0 - 4, base, x0 + w + 4, base, INK, 3)
    for i in range(6):
        yy = top + 16 + i * ((base - top - 24) // 6)
        line(x0 + 10, yy, x0 + w - 10, yy, FAINT, 2)
        rect(x0 + 14, yy - 6, 6, 5, GREY)
        rect(x0 + w - 20, yy - 6, 6, 5, GREY)
    # burst on the facade, halfway up
    import math
    bx, by = x0 + w + 2, (top + base) // 2
    for k in range(8):
        a = 2.0 * math.pi * k / 8.0
        x2 = int(round(bx + 16 * math.cos(a)))
        y2 = int(round(by + 16 * math.sin(a)))
        line(bx, by, x2, y2, RED, 3)
    rect(bx - 3, by - 3, 7, 7, RED)


def draw_courthouse(x, y, w):
    """Pediment and columns for the Sarkozy trial story."""
    cx = x + w // 2
    line(cx - 34, y + 12, cx, y, INK, 3)
    line(cx, y, cx + 34, y + 12, INK, 3)
    line(cx - 38, y + 14, cx + 38, y + 14, INK, 3)
    for dx in (-28, -10, 10, 28):
        line(cx + dx, y + 18, cx + dx, y + 38, INK, 3)
    line(cx - 38, y + 42, cx + 38, y + 42, INK, 3)


def draw_chip(x, y, w):
    """A microchip for the Huawei verdict story."""
    cx = x + w // 2
    rect(cx - 17, y + 6, 34, 34, PAPER)
    for yy in range(y + 6, y + 40):
        line(cx - 17, yy, cx - 17, yy, INK, 1)
    rect(cx - 17, y + 6, 34, 3, INK)
    rect(cx - 17, y + 37, 34, 3, INK)
    rect(cx + 14, y + 6, 3, 34, INK)
    rect(cx - 17, y + 6, 3, 34, INK)
    rect(cx - 6, y + 17, 12, 12, RED)
    for dx in (-12, 0, 12):
        line(cx + dx, y, cx + dx, y + 6, INK, 3)
        line(cx + dx, y + 40, cx + dx, y + 46, INK, 3)
    for dy in (12, 23, 34):
        line(cx - 23, y + dy, cx - 17, y + dy, INK, 3)
        line(cx + 17, y + dy, cx + 23, y + dy, INK, 3)


def draw_rising_arrow(x, y):
    """A rising arrow for the Laos graduation story."""
    pts = [(x, y + 34), (x + 22, y + 22), (x + 40, y + 26), (x + 62, y + 6)]
    for a, b in zip(pts, pts[1:]):
        line(a[0], a[1], b[0], b[1], ORANGE, 4)
    ex, ey = pts[-1]
    line(ex, ey, ex - 13, ey + 1, ORANGE, 4)
    line(ex, ey, ex - 3, ey + 12, ORANGE, 4)


# ------------------------------------------------------------------
# Page composition
# ------------------------------------------------------------------

MARGIN = 40
RIGHT = WIDTH - MARGIN
CONTENT_W = RIGHT - MARGIN


def rule(y, h, colour=INK):
    rect(MARGIN, y, CONTENT_W, h, colour)


def kicker(x, y, text):
    draw_text(x, y, text, 2, RED)


def column_story(x, y, w, kick, headline, body, illus=None,
                 illus_h=62, body_leading=17):
    kicker(x, y, kick)
    y += 22
    y = draw_paragraph(x, y, headline, 3, INK, w, 27)
    y += 6
    if illus is not None:
        illus(x, y, w)
        y += illus_h
    y = draw_paragraph(x, y, body, 2, INK, w, body_leading)
    return y


def draw_ship_icon(x, y):
    """Tiny warship silhouette beside the Ukraine kicker."""
    rect(x + 14, y + 6, 12, 5, INK)
    line(x + 20, y, x + 20, y + 6, INK, 2)
    rect(x + 2, y + 11, 36, 4, INK)
    line(x + 2, y + 15, x + 8, y + 18, INK, 2)
    line(x + 38, y + 15, x + 32, y + 18, INK, 2)
    rect(x + 8, y + 18, 24, 2, INK)


def also_item(x, y, w, text):
    """One bulleted brief in the ALSO IN THE NEWS box."""
    rect(x, y + 3, 7, 7, RED)
    lines = wrap(text, 2, w - 16)
    for i, ln in enumerate(lines):
        draw_text(x + 16, y + i * 14, ln, 2, INK)
    return y + len(lines) * 14 + 2


def build_page():
    fill_background()

    # ---- masthead -------------------------------------------------
    rule(22, 4)
    rule(31, 1)
    draw_centered(42, "THE WORLD TODAY", 9, INK)
    draw_text(MARGIN, 119, "VOL. I - NO. 25", 2, GREY)
    draw_right(RIGHT, 119, "PRICE: ONE IMAGE", 2, GREY)
    draw_centered(114, "WEDNESDAY - 25 NOVEMBER 2026", 3, INK)
    rule(144, 5)
    rule(153, 2)

    # ---- lead: Riyadh tower ---------------------------------------
    kicker(MARGIN, 168, "SAUDI ARABIA - RIYADH")
    draw_right(RIGHT, 168, "SECOND HIT IN A WEEK", 2, GREY)
    draw_text(MARGIN, 188, "HOUTHI DRONE HITS RIYADH TOWER", 5, INK)
    rule(232, 2, GREY)
    lead = ("A DRONE LAUNCHED BY YEMEN'S HOUTHI FIGHTERS STRUCK THE "
            "TALLEST TOWER IN RIYADH ON TUESDAY, WOUNDING AT LEAST "
            "11 PEOPLE. IT WAS THE SECOND HIT IN LESS THAN A WEEK "
            "ON THE 80-STOREY PIF TOWER; THE FIRST, ON 19 NOVEMBER, "
            "DAMAGED THE FACADE BUT HURT NO ONE. SAUDI CIVIL DEFENSE "
            "SAID THE WOUNDED WERE FOUR EGYPTIANS, THREE NEPALIS, "
            "TWO INDIANS AND TWO SAUDIS.")
    draw_two_columns(MARGIN, 246, 318, 18, lead, 2, INK, 17)
    draw_tower(872, 252, 368)
    draw_centered(382, "RIYADH, BY THE NUMBERS", 2, GREY)
    draw_centered(402,
                  "11 WOUNDED * 80 STOREYS * 2ND HIT IN A WEEK * "
                  "FIRST HIT 19 NOV", 2, INK)
    rule(426, 4)

    # ---- row A: france | huawei ------------------------------------
    col_w = 456
    col2 = 528
    column_story(MARGIN, 444, col_w, "FRANCE - PARIS",
                 "SARKOZY AND BRUNI ORDERED TO STAND TRIAL",
                 "FRENCH JUDGES SENT THE FORMER PRESIDENT AND HIS "
                 "WIFE TO TRIAL OVER AN ALLEGED WITNESS-RETRACTION "
                 "PLOT; 11 PEOPLE FACE TRIAL IN ALL.",
                 illus=lambda x, y, w: draw_courthouse(x, y, w),
                 illus_h=50, body_leading=16)
    column_story(col2, 444, col_w, "TECH - NEW YORK",
                 "HUAWEI GUILTY ON 10 OF 12 COUNTS IN US TRIAL",
                 "A BROOKLYN JURY CONVICTED CHINA'S TELECOM GIANT "
                 "OF BANK FRAUD, SANCTIONS BREACHES AND "
                 "TRADE-SECRET THEFT.",
                 illus=lambda x, y, w: draw_chip(x, y, w),
                 illus_h=50, body_leading=16)
    line(512, 444, 512, 632, FAINT, 2)
    rule(642, 2, GREY)

    # ---- row B: ukraine | yemen -------------------------------------
    column_story(MARGIN, 656, col_w, "UKRAINE - GULF OF FINLAND",
                 "KYIV CONFIRMS HIT ON RUSSIAN SHIP",
                 "ZELENSKIY CONFIRMED SATURDAY'S DRONE STRIKE ON "
                 "THE SPARTA II IN THE GULF OF FINLAND, CALLING IT "
                 "A LEGITIMATE TARGET. NORWAY URGED CAUTION.",
                 body_leading=16)
    draw_ship_icon(456, 652)
    column_story(col2, 656, col_w, "YEMEN - ADEN",
                 "HOUTHIS 60 KM FROM ADEN, ARMY SAYS CITY HOLDS",
                 "YEMEN'S MILITARY SAID HOUTHI FORCES ARE 60 KM "
                 "FROM ADEN, ITS TEMPORARY CAPITAL, BUT WILL NOT "
                 "TAKE IT. TROOPS DUG TRENCHES.",
                 body_leading=16)
    line(512, 656, 512, 802, FAINT, 2)
    rule(812, 4)

    # ---- laos --------------------------------------------------------
    kicker(MARGIN, 824, "DEVELOPMENT - LAOS")
    draw_text(MARGIN, 844, "LAOS GRADUATES FROM UN LEAST-DEVELOPED LIST",
              3, INK)
    draw_rising_arrow(884, 826)
    draw_paragraph(MARGIN, 874,
                   "LAO PDR LEFT THE UN'S LEAST DEVELOPED COUNTRY "
                   "LIST ON 24 NOVEMBER, ENDING 55 YEARS IN THE GROUP "
                   "SINCE 1971; IT MET ALL THREE UN CRITERIA.", 2, INK,
                   CONTENT_W, 16)

    # ---- also in the news: all five briefs, two columns --------------
    rect(MARGIN, 914, CONTENT_W, 104, BOX)
    draw_text(MARGIN + 12, 923, "ALSO IN THE NEWS", 2, RED)
    draw_right(RIGHT - 12, 926,
               "SOURCES: REUTERS - WSJ - AFP - US DOJ - EC - UN",
               1, GREY)
    ay = 942
    y1 = also_item(52, ay, 436,
                   "TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS")
    y1 = also_item(52, y1, 436,
                   "TRUMP AWARDS GIULIANI MEDAL OF FREEDOM")
    also_item(52, y1, 436, "ENGLAND BEAT AUSTRALIA IN 2ND T20I")
    y2 = also_item(536, ay, 436,
                   "EU PROPOSES 22ND RUSSIA SANCTIONS PACKAGE")
    also_item(536, y2, 436,
              "RADAR ISSUE DELAYS CHICAGO O'HARE FLIGHTS - FAA")


# ------------------------------------------------------------------
# PNG encoder (deterministic: filter 0 rows, zlib level 9)
# ------------------------------------------------------------------

def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))


def encode_png():
    raw = bytearray()
    stride = WIDTH * 3
    for y in range(HEIGHT):
        raw.append(0)
        raw += PIX[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    build_page()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(encode_png())
    print("wrote", path)


if __name__ == "__main__":
    main()
