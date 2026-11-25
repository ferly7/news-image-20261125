#!/usr/bin/env python3
"""THE WORLD TODAY - front page renderer, Wednesday 25 November 2026.
Pure stdlib, no network. Deterministic output.
Original 5x7 bitmap typeface + hand-rolled PNG writer.
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (243, 238, 226)
INK = (24, 24, 28)
RED = (178, 30, 30)
DARKRED = (120, 18, 18)
GREY = (96, 96, 100)
LGREY = (206, 200, 186)
BLUE = (28, 62, 110)
GOLD = (176, 132, 40)
SKY = (196, 214, 228)
BLDG = (70, 78, 92)
WIN = (240, 224, 150)

FONT = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 15),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 21, 19, 17, 17, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "R": (30, 17, 17, 30, 20, 18, 17),
    "S": (15, 16, 16, 14, 1, 1, 30),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 21, 10),
    "X": (17, 10, 4, 4, 4, 10, 17),
    "Y": (17, 10, 4, 4, 4, 4, 4),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 6, 8, 16, 31),
    "3": (30, 1, 1, 14, 1, 1, 30),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (14, 16, 16, 30, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 1, 14),
    "-": (0, 0, 0, 31, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 12, 12),
    ",": (0, 0, 0, 0, 12, 4, 8),
    ":": (0, 12, 12, 0, 12, 12, 0),
    ";": (0, 12, 12, 0, 12, 4, 8),
    "'": (4, 4, 8, 0, 0, 0, 0),
    "/": (1, 1, 2, 4, 8, 16, 16),
    "(": (2, 4, 8, 8, 8, 4, 2),
    ")": (8, 4, 2, 2, 2, 4, 8),
    "$": (4, 15, 20, 14, 5, 30, 4),
    "%": (24, 25, 2, 4, 8, 19, 3),
    "+": (0, 4, 4, 31, 4, 4, 0),
    "&": (12, 18, 20, 8, 21, 18, 13),
    "!": (4, 4, 4, 4, 4, 0, 4),
    "?": (14, 17, 1, 6, 4, 0, 4),
    '"': (10, 10, 10, 0, 0, 0, 0),
}


def png_bytes(pixels, width, height):
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(pixels[y * stride:(y + 1) * stride])

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw), 9)
    return sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set_px(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = col[0]
            self.px[i + 1] = col[1]
            self.px[i + 2] = col[2]

    def fill_rect(self, x, y, w, h, col):
        for yy in range(y, y + h):
            if 0 <= yy < self.h:
                base = yy * self.w
                for xx in range(x, x + w):
                    if 0 <= xx < self.w:
                        i = (base + xx) * 3
                        self.px[i] = col[0]
                        self.px[i + 1] = col[1]
                        self.px[i + 2] = col[2]

    def hline(self, x, y, w, col, thick=1):
        self.fill_rect(x, y, w, thick, col)

    def vline(self, x, y, h, col, thick=1):
        self.fill_rect(x, y, thick, h, col)


def text_width(s, scale):
    """Each glyph cell: 5 px wide + 1 px gap, scaled."""
    if not s:
        return 0
    return len(s) * 6 * scale - scale


def draw_text(cv, x, y, s, scale, col):
    s = s.upper()
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT["?"])
        for row in range(7):
            bits = glyph[row]
            for col_i in range(5):
                if bits & (1 << (4 - col_i)):
                    cv.fill_rect(cx + col_i * scale, y + row * scale,
                                 scale, scale, col)
        cx += 6 * scale
    return cx


def draw_centered(cv, cx, y, s, scale, col):
    w = text_width(s, scale)
    return draw_text(cv, cx - w // 2, y, s, scale, col)


def draw_right(cv, xr, y, s, scale, col):
    w = text_width(s, scale)
    return draw_text(cv, xr - w, y, s, scale, col)


def wrap(s, max_chars):
    words = s.split()
    lines = []
    cur = ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_para(cv, x, y, s, scale, col, max_chars, line_gap):
    lines = wrap(s, max_chars)
    for i, ln in enumerate(lines):
        draw_text(cv, x, y + i * line_gap, ln, scale, col)
    return y + len(lines) * line_gap, lines


def draw_line(cv, x0, y0, x1, y1, col, thick=1):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy), 1)
    for i in range(steps + 1):
        px = x0 + dx * i // steps
        py = y0 + dy * i // steps
        cv.fill_rect(px, py, thick, thick, col)


def draw_disc(cv, cx, cy, r, col):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                cv.set_px(xx, yy, col)


def draw_burst(cv, cx, cy, r_out, r_in, col):
    """Jagged explosion star: alternating radii at 16 angles."""
    import math
    pts = []
    for k in range(32):
        ang = math.pi * k / 16.0
        r = r_out if k % 2 == 0 else r_in
        pts.append((cx + int(r * math.cos(ang)), cy + int(r * math.sin(ang))))
    for k in range(32):
        x0, y0 = pts[k]
        x1, y1 = pts[(k + 1) % 32]
        draw_line(cv, x0, y0, x1, y1, col, 2)
        draw_line(cv, cx, cy, x0, y0, col, 1)
    draw_disc(cv, cx, cy, r_in, col)


def draw_tower(cv, x, y, w, h):
    """Simple skyscraper: body, window grid, spire, red burst at top."""
    cv.fill_rect(x, y, w, h, SKY)
    cv.fill_rect(x, y, w, h, SKY)
    tw = w * 2 // 5
    tx = x + (w - tw) // 2
    cv.fill_rect(tx, y + 26, tw, h - 26, BLDG)
    # stepped crown
    cv.fill_rect(tx + 8, y + 16, tw - 16, 12, BLDG)
    cv.fill_rect(tx + tw // 2 - 2, y + 2, 4, 16, BLDG)
    # windows
    for wy in range(y + 36, y + h - 10, 14):
        for wx in range(tx + 8, tx + tw - 8, 12):
            cv.fill_rect(wx, wy, 6, 8, WIN)
    # ground neighbours
    cv.fill_rect(x + 6, y + h - 44, 34, 44, GREY)
    cv.fill_rect(x + w - 40, y + h - 58, 34, 58, GREY)
    cv.fill_rect(x, y + h - 3, w, 3, INK)
    # explosion near crown
    draw_burst(cv, tx + tw - 6, y + 30, 30, 13, RED)
    draw_burst(cv, tx + tw - 6, y + 30, 17, 8, GOLD)


MX = 36
CW = W - 2 * MX


def section(cv, x, y, w, label, label_col, headline, body):
    draw_text(cv, x, y, label, 2, label_col)
    y += 19
    y, _ = draw_para(cv, x, y, headline, 3, INK, w // 18, 25)
    y += 2
    y, _ = draw_para(cv, x, y, body, 2, INK, w // 12, 16)
    return y


def render():
    cv = Canvas(W, H, PAPER)
    # outer frame
    cv.fill_rect(18, 18, W - 36, 2, INK)
    cv.fill_rect(18, H - 20, W - 36, 2, INK)
    cv.fill_rect(18, 18, 2, H - 36, INK)
    cv.fill_rect(W - 20, 18, 2, H - 36, INK)

    # masthead
    cv.hline(MX, 30, CW, INK, 3)
    draw_centered(cv, W // 2, 40, "THE WORLD TODAY", 7, INK)
    draw_centered(cv, W // 2, 96, "WEDNESDAY - 25 NOVEMBER 2026", 2, GREY)
    cv.hline(MX, 118, CW, INK, 2)
    cv.hline(MX, 123, CW, INK, 1)

    # ---- lead story ----
    ly = 136
    draw_text(cv, MX, ly, "SAUDI ARABIA - RIYADH", 2, RED)
    draw_text(cv, 620, ly, "LEAD STORY", 2, GREY)
    hy, _ = draw_para(cv, MX, ly + 20, "HOUTHI DRONE HITS RIYADH TOWER",
                      5, INK, 18, 41)
    lead_body = (
        "A HOUTHI DRONE STRUCK THE 80-STOREY PIF TOWER IN THE KING "
        "ABDULLAH FINANCIAL DISTRICT ON TUESDAY, THE SECOND SUCH HIT "
        "IN UNDER A WEEK. AT LEAST 11 PEOPLE WERE WOUNDED - 4 FROM "
        "EGYPT, 3 FROM NEPAL, 2 FROM INDIA AND 2 SAUDIS - THE SAUDI "
        "CIVIL DEFENSE SAID. THE FIRST ATTACK, ON 19 NOVEMBER, "
        "INJURED NO ONE."
    )
    draw_para(cv, MX, hy + 8, lead_body, 2, INK, 46, 16)
    draw_tower(cv, 620, ly + 20, 368, 208)

    # stat strip
    sy = 386
    stats = [("11", "WOUNDED"), ("80", "STOREYS"),
             ("2ND", "HIT IN A WEEK"), ("19 NOV", "FIRST HIT")]
    bw = (CW - 24) // 4
    for i, (num, lab) in enumerate(stats):
        bx = MX + i * (bw + 8)
        cv.fill_rect(bx, sy, bw, 54, LGREY)
        cv.hline(bx, sy, bw, RED, 3)
        draw_centered(cv, bx + bw // 2, sy + 8, num, 3, DARKRED)
        draw_centered(cv, bx + bw // 2, sy + 36, lab, 1, INK)
    cv.hline(MX, sy + 66, CW, INK, 2)

    # ---- two-column grid ----
    gy = sy + 74
    colw = 464
    rx = MX + colw + 24
    cv.vline(MX + colw + 11, gy, 300, LGREY, 2)
    y1 = section(
        cv, MX, gy, colw, "FRANCE", BLUE,
        "SARKOZY AND BRUNI ORDERED TO STAND TRIAL",
        "JUDGES SENT THE FORMER PRESIDENT AND CARLA BRUNI TO TRIAL "
        "OVER AN ALLEGED PLOT TO RETRACT TESTIMONY IN THE LIBYAN "
        "FUNDING CASE. ELEVEN PEOPLE FACE TRIAL IN ALL, WITH A "
        "PRE-TRIAL HEARING SET FOR 1 APRIL 2027.")
    y2 = section(
        cv, rx, gy, colw, "TECH - UNITED STATES", BLUE,
        "HUAWEI GUILTY ON 10 OF 12 COUNTS IN US TRIAL",
        "A BROOKLYN JURY CONVICTED HUAWEI OF BANK FRAUD, SANCTIONS "
        "VIOLATIONS AND TRADE-SECRET THEFT, AND ACQUITTED IT OF "
        "RACKETEERING. SENTENCING IS SET FOR SEPTEMBER 2027.")
    row2 = max(y1, y2) + 10
    y3 = section(
        cv, MX, row2, colw, "UKRAINE WAR", RED,
        "KYIV CONFIRMS HIT ON RUSSIAN SHIP",
        "PRESIDENT ZELENSKIY CONFIRMED SATURDAY'S DRONE STRIKE ON "
        "THE CARGO SHIP SPARTA II IN THE GULF OF FINLAND, CALLING "
        "IT A LEGITIMATE TARGET. NORWAY URGED CAUTION.")
    y4 = section(
        cv, rx, row2, colw, "YEMEN", RED,
        "HOUTHIS 60 KM FROM ADEN, ARMY SAYS CITY HOLDS",
        "HOUTHI FORCES ARE 60 KM FROM ADEN, THE INTERIM CAPITAL, "
        "BUT WILL NOT TAKE IT, YEMEN'S MILITARY SAID, AS ITS TROOPS "
        "DUG TRENCHES AROUND THE CITY.")
    by = max(y3, y4) + 12

    # ---- Laos band ----
    cv.hline(MX, by, CW, INK, 2)
    by += 10
    draw_text(cv, MX, by, "DEVELOPMENT - LAOS", 2, GOLD)
    by += 19
    draw_text(cv, MX, by, "LAOS GRADUATES FROM UN LEAST-DEVELOPED LIST",
              3, INK)
    by += 24
    by, _ = draw_para(
        cv, MX, by,
        "LAO PDR LEFT THE UN LIST OF LEAST-DEVELOPED COUNTRIES ON "
        "24 NOVEMBER, ENDING 55 YEARS ON IT SINCE 1971, AFTER MEETING "
        "ALL THREE UN CRITERIA, INCLUDING GNI PER PERSON OF $2,375.",
        2, INK, 79, 16)
    by += 4

    # ---- also in the news ----
    cv.hline(MX, by, CW, INK, 2)
    by += 9
    draw_text(cv, MX, by, "ALSO IN THE NEWS", 2, RED)
    by += 18
    briefs_l = [
        "- TURKEY PARDON: FREEDOM AND FEATHERS",
        "- TRUMP: MEDAL OF FREEDOM TO GIULIANI",
        "- EU PROPOSES 22ND RUSSIA SANCTIONS",
    ]
    briefs_r = [
        "- RADAR DELAYS O'HARE FLIGHTS - FAA",
        "- ENGLAND BEAT AUSTRALIA, 2ND T20I",
    ]
    for i, b in enumerate(briefs_l):
        draw_text(cv, MX, by + i * 16, b, 2, INK)
    for i, b in enumerate(briefs_r):
        draw_text(cv, rx, by + i * 16, b, 2, INK)
    by += 3 * 16 + 5

    cv.hline(MX, by, CW, INK, 1)
    draw_centered(cv, W // 2, by + 7,
                  "SOURCES: REUTERS - WSJ - AFP - US DOJ - EC - UN",
                  1, GREY)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = render()
    data = png_bytes(cv.px, W, H)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote", path, len(data), "bytes")


if __name__ == "__main__":
    main()


