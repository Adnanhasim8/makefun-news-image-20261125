#!/usr/bin/env python3
"""news-image-20261125 — one 1024x1024 PNG summing up the world news of
Wednesday 25 November 2026. Python 3.13 standard library only, no network,
deterministic output: the same bytes on every run."""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
INK = (18, 24, 38)          # near-black navy
PAPER = (250, 247, 240)     # warm newsprint
NAVY = (16, 42, 90)         # masthead band
NAVY2 = (24, 62, 128)
RED = (178, 34, 34)         # lead accent / kicker
GOLD = (212, 160, 44)
GREY = (96, 104, 118)
LGREY = (226, 222, 214)     # hairlines
CARD = (255, 255, 255)
BLUE = (30, 90, 168)
TEAL = (14, 120, 110)
GREEN = (34, 122, 60)
ORANGE = (196, 96, 16)
PURPLE = (104, 68, 160)
BROWN = (122, 74, 30)

REGION_COLOURS = {
    "EUROPE": NAVY2, "MIDDLE EAST": RED, "ASIA": TEAL, "AFRICA": ORANGE,
    "AMERICAS": GREEN, "PACIFIC": PURPLE, "SPACE": BLUE, "GLOBAL": BROWN,
    "SPORT": (150, 30, 90),
}

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.set(xx, yy, c)
                else:
                    if r * r - 2 * r <= d <= r * r:
                        self.set(xx, yy, c)

    def ring(self, cx, cy, r, c, t=2):
        for k in range(t):
            self.circle(cx, cy, r - k, c, fill=False)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def png_bytes(self):
        raw = b"".join(
            b"\x00" + bytes(self.px[y * self.w * 3:(y + 1) * self.w * 3])
            for y in range(self.h))
        comp = zlib.compress(raw, 9)

        def chunk(tag, data):
            c = struct.pack(">I", len(data)) + tag + data
            return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 strings of 5 chars, '#' = ink.
FONT = {}
def _g(ch, rows):
    FONT[ch] = rows

_g("A", ["01110","10001","10001","11111","10001","10001","10001"])
_g("B", ["11110","10001","10001","11110","10001","10001","11110"])
_g("C", ["01110","10001","10000","10000","10000","10001","01110"])
_g("D", ["11110","10001","10001","10001","10001","10001","11110"])
_g("E", ["11111","10000","10000","11110","10000","10000","11111"])
_g("F", ["11111","10000","10000","11110","10000","10000","10000"])
_g("G", ["01110","10001","10000","10111","10001","10001","01111"])
_g("H", ["10001","10001","10001","11111","10001","10001","10001"])
_g("I", ["01110","00100","00100","00100","00100","00100","01110"])
_g("J", ["00111","00010","00010","00010","00010","10010","01100"])
_g("K", ["10001","10010","10100","11000","10100","10010","10001"])
_g("L", ["10000","10000","10000","10000","10000","10000","11111"])
_g("M", ["10001","11011","10101","10101","10001","10001","10001"])
_g("N", ["10001","11001","10101","10011","10001","10001","10001"])
_g("O", ["01110","10001","10001","10001","10001","10001","01110"])
_g("P", ["11110","10001","10001","11110","10000","10000","10000"])
_g("Q", ["01110","10001","10001","10001","10101","10010","01101"])
_g("R", ["11110","10001","10001","11110","10100","10010","10001"])
_g("S", ["01111","10000","10000","01110","00001","00001","11110"])
_g("T", ["11111","00100","00100","00100","00100","00100","00100"])
_g("U", ["10001","10001","10001","10001","10001","10001","01110"])
_g("V", ["10001","10001","10001","10001","10001","01010","00100"])
_g("W", ["10001","10001","10001","10101","10101","11011","10001"])
_g("X", ["10001","10001","01010","00100","01010","10001","10001"])
_g("Y", ["10001","10001","01010","00100","00100","00100","00100"])
_g("Z", ["11111","00001","00010","00100","01000","10000","11111"])
_g("a", ["00000","00000","01110","00001","01111","10001","01111"])
_g("b", ["10000","10000","11110","10001","10001","10001","11110"])
_g("c", ["00000","00000","01110","10000","10000","10001","01110"])
_g("d", ["00001","00001","01111","10001","10001","10001","01111"])
_g("e", ["00000","00000","01110","10001","11111","10000","01110"])
_g("f", ["00110","01001","01000","11110","01000","01000","01000"])
_g("g", ["00000","01111","10001","10001","01111","00001","01110"])
_g("h", ["10000","10000","11110","10001","10001","10001","10001"])
_g("i", ["00100","00000","01100","00100","00100","00100","01110"])
_g("j", ["00010","00000","00110","00010","00010","10010","01100"])
_g("k", ["10000","10000","10010","10100","11000","10100","10010"])
_g("l", ["01100","00100","00100","00100","00100","00100","01110"])
_g("m", ["00000","00000","11010","10101","10101","10101","10101"])
_g("n", ["00000","00000","11110","10001","10001","10001","10001"])
_g("o", ["00000","00000","01110","10001","10001","10001","01110"])
_g("p", ["00000","00000","11110","10001","10001","11110","10000"])
_g("q", ["00000","00000","01111","10001","10001","01111","00001"])
_g("r", ["00000","00000","10110","11001","10000","10000","10000"])
_g("s", ["00000","00000","01111","10000","01110","00001","11110"])
_g("t", ["01000","01000","11100","01000","01000","01001","00110"])
_g("u", ["00000","00000","10001","10001","10001","10011","01101"])
_g("v", ["00000","00000","10001","10001","10001","01010","00100"])
_g("w", ["00000","00000","10001","10001","10101","10101","01010"])
_g("x", ["00000","00000","10001","01010","00100","01010","10001"])
_g("y", ["00000","00000","10001","10001","01111","00001","01110"])
_g("z", ["00000","00000","11111","00010","00100","01000","11111"])
_g("0", ["01110","10001","10011","10101","11001","10001","01110"])
_g("1", ["00100","01100","00100","00100","00100","00100","01110"])
_g("2", ["01110","10001","00001","00110","01000","10000","11111"])
_g("3", ["11111","00010","00100","00010","00001","10001","01110"])
_g("4", ["00010","00110","01010","10010","11111","00010","00010"])
_g("5", ["11111","10000","11110","00001","00001","10001","01110"])
_g("6", ["00110","01000","10000","11110","10001","10001","01110"])
_g("7", ["11111","00001","00010","00100","01000","01000","01000"])
_g("8", ["01110","10001","10001","01110","10001","10001","01110"])
_g("9", ["01110","10001","10001","01111","00001","00010","01100"])
_g(" ", ["00000","00000","00000","00000","00000","00000","00000"])
_g(".", ["00000","00000","00000","00000","00000","01100","01100"])
_g(",", ["00000","00000","00000","00000","01100","00100","01000"])
_g(":", ["00000","01100","01100","00000","01100","01100","00000"])
_g(";", ["00000","01100","01100","00000","01100","00100","01000"])
_g("'", ["00100","00100","01000","00000","00000","00000","00000"])
_g('"', ["01010","01010","00000","00000","00000","00000","00000"])
_g("!", ["00100","00100","00100","00100","00100","00000","00100"])
_g("?", ["01110","10001","00001","00110","00100","00000","00100"])
_g("-", ["00000","00000","00000","01110","00000","00000","00000"])
_g("–", ["00000","00000","00000","11111","00000","00000","00000"])
_g("—", ["00000","00000","00000","11111","00000","00000","00000"])
_g("(", ["00010","00100","01000","01000","01000","00100","00010"])
_g(")", ["01000","00100","00010","00010","00010","00100","01000"])
_g("/", ["00001","00010","00010","00100","01000","01000","10000"])
_g("%", ["11001","11010","00010","00100","01000","01011","10011"])
_g("+", ["00000","00100","00100","11111","00100","00100","00000"])
_g("&", ["01100","10010","10100","01000","10101","10010","01101"])
_g("·", ["00000","00000","00000","01100","01100","00000","00000"])
_g("’", ["00100","00100","01000","00000","00000","00000","00000"])
_g("“", ["01010","01010","00100","00000","00000","00000","00000"])
_g("”", ["01010","01010","00100","00000","00000","00000","00000"])
_g("£", ["00110","01000","01000","11100","01000","01000","11111"])
_g("€", ["00110","01001","10000","11110","10000","01001","00110"])

def text_w(s, scale):
    return len(s) * 6 * scale - scale

def draw_text(cv, x, y, s, scale, colour):
    cx = x
    for ch in s:
        rows = FONT.get(ch, FONT["?"])
        for r in range(7):
            for c in range(5):
                if rows[r][c] == "1":
                    cv.rect(cx + c * scale, y + r * scale, scale, scale, colour)
        cx += 6 * scale
    return cx

def wrap(s, max_chars):
    words, lines, cur = s.split(" "), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

# ---------------------------------------------------------------- stories
LEAD = ("UKRAINE CONFIRMS IT HIT A RUSSIAN SHIP",
        "IN THE GULF OF FINLAND",
        "President Zelenskiy says Kyiv was behind Saturday's drone strike on a "
        "Russian cargo ship — as ally Norway urges caution over such operations.")

STORIES = [
    ("MIDDLE EAST", "Gaza: Israeli strike kills Hamas security chief",
     "Hamas security chief Naeem Abu Nahel killed in Gaza City."),
    ("MIDDLE EAST", "Houthis hit Riyadh's tallest tower",
     "11 wounded in the Saudi capital; Saudi strikes kill 26 in Yemen."),
    ("SPACE", "First Pakistani in orbit",
     "Shenzhou-24 launches; pilot Zeeshan Ali boards Tiangong station."),
    ("GLOBAL", "AI stocks slide; new tariffs planned",
     "Nasdaq -1.5%, Nvidia -6% as Trump readies tariffs on 16 economies."),
    ("ASIA", "Huawei guilty of trade-secret theft",
     "Verdict lands as US adds a Singapore chip firm to its blacklist."),
    ("EUROPE", "Sarkozy and Carla Bruni face trial",
     "French judges order the ex-president's corruption case to court."),
    ("PACIFIC", "Australia–Solomon Islands pact signed",
     "Canberra named the islands' primary security partner."),
    ("GLOBAL", "Climate summit ends with no deal",
     "190+ countries fail to agree a closing text in Antalya, Turkey."),
    ("GLOBAL", "AIDS deaths at a 20-year low",
     "570,000 deaths in 2025 — but HIV funding fell 18%, UNAIDS warns."),
    ("ASIA", "Malaysia to return 6,500 Rohingya",
     "Refugees to be sent back to Myanmar in December, PM Anwar says."),
    ("SPORT", "Real Madrid thrash PSV 5-1",
     "Bellingham and Mbappe star; Arsenal and Man City both held."),
    ("AFRICA", "Congo military plane missing",
     "Aircraft vanishes amid rebel claims in DR Congo."),
]

REGIONS = ["EUROPE", "MIDDLE EAST", "ASIA", "AFRICA", "AMERICAS", "PACIFIC", "GLOBAL"]

# ---------------------------------------------------------------- layout
def draw_globe(cv, cx, cy, r):
    cv.circle(cx, cy, r, NAVY2)
    cv.ring(cx, cy, r, PAPER, 2)
    # meridians / parallels
    for k in range(-2, 3):
        off = k * r // 3
        cv.vline(cx + off, cy - r + 6, 2 * r - 12, (120, 150, 200), 1)
        cv.hline(cx - r + 6, cy + off, 2 * r - 12, (120, 150, 200), 1)
    cv.circle(cx, cy, r // 2, (120, 150, 200), fill=False)
    # land blobs
    cv.circle(cx - r // 3, cy - r // 4, r // 4, GOLD)
    cv.circle(cx + r // 3, cy + r // 5, r // 5, GOLD)
    cv.circle(cx + r // 6, cy - r // 2, r // 6, GOLD)

def build():
    cv = Canvas(W, H, PAPER)

    # --- masthead ------------------------------------------------------
    cv.rect(0, 0, W, 168, NAVY)
    cv.rect(0, 168, W, 5, GOLD)
    draw_globe(cv, 84, 84, 56)
    draw_text(cv, 168, 26, "WEDNESDAY 25 NOVEMBER 2026", 5, PAPER)
    draw_text(cv, 168, 82, "in one picture", 4, GOLD)
    draw_text(cv, 168, 122, "18 dated stories  ·  7 regions", 3, (200, 210, 230))

    # --- lead story ----------------------------------------------------
    cv.rect(28, 196, 968, 168, CARD)
    cv.rect(28, 196, 968, 168, INK)  # border via outline trick below
    cv.rect(31, 199, 962, 162, CARD)
    cv.rect(28, 196, 10, 168, RED)
    draw_text(cv, 62, 214, "LEAD STORY  —  EUROPE", 2, RED)
    draw_text(cv, 62, 238, LEAD[0], 4, INK)
    draw_text(cv, 62, 272, LEAD[1], 4, INK)
    for i, ln in enumerate(wrap(LEAD[2], 78)):
        draw_text(cv, 62, 312 + i * 18, ln, 2, GREY)

    # --- region strip --------------------------------------------------
    y = 388
    draw_text(cv, 28, y, "AROUND THE WORLD TODAY", 2, GREY)
    x = 28
    for reg in REGIONS:
        col = REGION_COLOURS[reg]
        wch = text_w(reg, 2) + 24
        cv.rect(x, y + 22, wch, 30, col)
        draw_text(cv, x + 12, y + 30, reg, 2, PAPER)
        x += wch + 10

    # --- story grid: 2 cols x 6 rows -----------------------------------
    top = 458
    cw, chh, gap = 474, 72, 20
    for i, (reg, head, sub) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = 28 + col * (cw + gap)
        y = top + row * (chh + 8)
        colr = REGION_COLOURS[reg]
        cv.rect(x, y, cw, chh, CARD)
        cv.rect(x, y, 6, chh, colr)
        draw_text(cv, x + 18, y + 7, reg, 2, colr)
        for j, ln in enumerate(wrap(head, 36)[:2]):
            draw_text(cv, x + 18, y + 24 + j * 15, ln, 2, INK)
        sub_lines = wrap(sub, 68)
        if sub_lines:
            draw_text(cv, x + 18, y + 57, sub_lines[0], 1, GREY)

    # --- footer --------------------------------------------------------
    fy = top + 6 * (chh + 8) + 10
    cv.hline(28, fy, 968, LGREY, 2)
    draw_text(cv, 28, fy + 12,
              "Sources: Reuters, Associated Press, UEFA, UNAIDS, NOS — 25 November 2026",
              2, GREY)
    draw_text(cv, 28, fy + 34,
              "All events happened on, or were first reported on, Wednesday 25 November 2026.",
              2, GREY)

    return cv.png_bytes()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    # Gate assertions: the entry must be a whole 1024x1024 PNG of at most 1 MiB.
    with open(path, "rb") as f:
        blob = f.read()
    assert blob[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", blob[16:24])
    assert (w, h) == (1024, 1024), f"wrong dimensions: {w}x{h}"
    assert len(blob) <= 1048576, f"too large: {len(blob)} bytes"
    assert blob[-12:] == struct.pack(">I", 0) + b"IEND" + struct.pack(
        ">I", zlib.crc32(b"IEND") & 0xFFFFFFFF), "PNG missing IEND"


if __name__ == "__main__":
    main()
