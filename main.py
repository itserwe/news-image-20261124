#!/usr/bin/env python3
"""The World Today - Tuesday 24 November 2026 (make.fun news-image-20261124).

Draws the newspaper front page (1024x1024 PNG) and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).

Grader runtime: Python 3.13, standard library ONLY, repo read-only at /bot,
only $MAKEFUN_OUTPUT_DIR writable, no network, nothing installed. Pillow is
NOT available on the grader, so the import below is guarded: when Pillow is
present (build machine) the page is drawn fresh with PIL; when it is absent
(the grader) the repo's own pre-drawn entry.png is copied to the output
directory with shutil. Nothing is ever written to the script's directory.
"""
import os
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
    HAVE_PIL = True
except ImportError:  # grader: no Pillow installed
    HAVE_PIL = False

W, H = 1024, 1024
BG = (250, 248, 245)      # #FAF8F5 ivory
INK = (26, 26, 26)        # #1A1A1A
RED = (166, 30, 30)
GREY = (110, 105, 98)
RULE = (26, 26, 26)
LIGHT = (232, 224, 208)
GREEN = (30, 122, 52)
AMBER = (150, 100, 10)
BLUE = (30, 90, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; returns list of lines (max 3 enforced by caller)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=None, max_lines=3):
    lines = wrap(draw, text, fnt, width)[:max_lines]
    lh = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def chip(draw, x, y, label, color):
    fnt = font(SANS_B, 10)
    w = int(draw.textlength(label, font=fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=color)
    draw.text((x + 6, y + 2), label, font=fnt, fill=(255, 255, 255))
    return x + w


# ---------------------------------------------------------------- map data
# Simplified continent outlines as (lon, lat) polygons.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-75, 62), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-70, 10), (-60, 5), (-50, 0), (-40, -5),
     (-35, -10), (-40, -20), (-50, -30), (-60, -35), (-70, -40), (-70, -50),
     (-75, -55), (-70, -40), (-75, -20), (-80, -5), (-80, 10)],
    # Europe
    [(-10, 36), (-5, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 65),
     (40, 55), (35, 50), (30, 46), (28, 41), (23, 40), (19, 42), (12, 44),
     (8, 44), (3, 42), (0, 39), (-9, 37)],
    # Africa
    [(-17, 15), (-15, 25), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (43, 11), (48, 11), (51, 10), (45, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (13, -10),
     (9, 4), (0, 5), (-8, 5), (-13, 8), (-17, 15)],
    # Asia
    [(30, 36), (35, 36), (40, 38), (45, 40), (50, 42), (55, 45), (60, 50),
     (65, 55), (70, 60), (75, 65), (80, 70), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 66), (170, 66),
     (178, 65), (170, 60), (162, 56), (158, 52), (150, 60), (142, 55),
     (140, 45), (135, 42), (130, 38), (127, 35), (122, 32), (120, 28),
     (115, 22), (110, 20), (108, 12), (105, 8), (100, 7), (97, 10),
     (95, 15), (92, 20), (90, 22), (86, 20), (82, 17), (80, 10), (77, 8),
     (73, 15), (70, 22), (66, 25), (62, 25), (58, 26), (55, 26), (52, 26),
     (48, 28), (50, 30), (48, 30), (44, 29), (42, 28), (40, 30), (38, 32),
     (36, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12),
     (135, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
     (113, -22)],
]

# Numbered pins: (story no, lon, lat, dx, dy) — dx/dy nudge the drawn pin
# away from its true spot (leader line) where pins would collide.
PINS = [
    (1, 46.7, 24.7, -11, -9),   # Riyadh
    (2, 56.5, 26.5, 11, 7),     # Strait of Hormuz
    (3, -74.0, 40.7, 0, 0),     # New York markets
    (4, 34.5, 31.5, -13, 11),   # Gaza
    (5, 35.2, 47.8, 1, -13),    # Zaporizhzhia
    (6, 37.6, 55.7, 13, -11),   # Moscow (Russian war dead)
    (7, 13.4, 52.5, 0, 0),      # Berlin (Delta system)
    (8, 4.4, 50.9, -13, 9),     # Brussels (NATO space defence)
    (9, -17.4, 14.7, 0, 0),     # Dakar, Senegal
    (10, -0.1, 51.5, -3, -13),  # London
    (11, 96.0, 20.0, 0, 0),     # Myanmar
    (12, 6.1, 46.2, 11, 11),    # Geneva (chess)
    (13, 29.5, 1.5, 0, 0),      # Ituri, DRC
    (14, 44.4, 33.3, 13, 9),    # Baghdad, Iraq
]


def draw_map(draw, x0, y0, w, h):
    """Schematic world map with numbered pins matching stories 1-14."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(233, 238, 240),
                   outline=INK, width=1)
    # graticule
    for gx in range(-150, 181, 30):
        px = x0 + (gx + 180) / 360.0 * w
        draw.line([(px, y0), (px, y0 + h)], fill=(210, 218, 222), width=1)
    for gy in range(-60, 86, 30):
        py = y0 + (85 - gy) / 145.0 * h
        draw.line([(x0, py), (x0 + w, py)], fill=(210, 218, 222), width=1)

    def proj(lon, lat):
        return (x0 + (lon + 180) / 360.0 * w,
                y0 + (85 - lat) / 145.0 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=(226, 216, 196), outline=(90, 80, 66))
    # pins (nudged where they would collide; leader line to true spot)
    fnt = font(SANS_B, 8)
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        qx, qy = px + dx, py + dy
        if dx or dy:
            draw.line([(px, py), (qx, qy)], fill=RED, width=1)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        draw.ellipse([qx - 7, qy - 7, qx + 7, qy + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        tw = draw.textlength(str(num), font=fnt)
        draw.text((qx - tw / 2, qy - 5), str(num), font=fnt,
                  fill=(255, 255, 255))


# ------------------------------------------------------- flat illustrations
def illo_riyadh(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # sun + skyline
    draw.ellipse([x + w - 52, y + 10, x + w - 22, y + 40], fill=(240, 200, 90))
    base = y + h
    for bx, bw, bh in [(0, 42, 52), (46, 34, 70), (84, 30, 44),
                       (118, 40, 62), (162, 36, 48), (202, 44, 66),
                       (250, 38, 54), (288, 24, 40)]:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(70, 84, 100))
    # PIF Tower: tallest, centre
    tx = x + w // 2 - 16
    draw.rectangle([tx, y + 18, tx + 32, base], fill=(38, 52, 68))
    draw.polygon([(tx + 16, y + 2), (tx + 22, y + 18), (tx + 10, y + 18)],
                 fill=(38, 52, 68))
    for wy in range(y + 30, base - 6, 10):
        draw.rectangle([tx + 5, wy, tx + 27, wy + 4], fill=(150, 190, 220))
    # drone + smoke
    draw.ellipse([tx + 34, y + 26, tx + 44, y + 34], fill=(26, 26, 26))
    draw.line([(tx + 30, y + 30), (tx + 48, y + 30)], fill=(26, 26, 26), width=2)
    draw.ellipse([tx - 6, y + 12, tx + 6, y + 24], fill=(200, 200, 200))
    draw.ellipse([tx + 2, y + 6, tx + 14, y + 18], fill=(220, 220, 220))
    draw.rectangle([x, base - 16, x + w, base], fill=(26, 26, 26))
    draw.text((x + 8, base - 14), "PIF TOWER  ·  RIYADH",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def illo_hormuz(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(191, 217, 232))
    # sky + sun
    draw.ellipse([x + 18, y + 10, x + 44, y + 36], fill=(240, 200, 90))
    # tanker
    hx, hy = x + 40, y + h - 58
    draw.rectangle([hx, hy, hx + 190, hy + 26], fill=(40, 52, 66))
    draw.rectangle([hx + 8, hy - 22, hx + 60, hy], fill=(180, 60, 50))
    draw.rectangle([hx + 68, hy - 22, hx + 120, hy], fill=(60, 120, 90))
    draw.rectangle([hx + 128, hy - 22, hx + 180, hy], fill=(200, 150, 60))
    draw.rectangle([hx + 168, hy - 40, hx + 190, hy - 22], fill=(240, 240, 240))
    # mine in the water
    mx, my = x + w - 62, y + h - 34
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(26, 26, 26))
    for dx, dy in [(-12, 0), (12, 0), (0, -12), (0, 12), (-9, -9), (9, -9),
                   (-9, 9), (9, 9)]:
        draw.line([(mx, my), (mx + dx, my + dy)], fill=(26, 26, 26), width=2)
    # waves
    for wy in (y + h - 24, y + h - 12):
        for wx in range(x + 6, x + w - 6, 26):
            draw.arc([wx, wy, wx + 22, wy + 10], 180, 360,
                     fill=(255, 255, 255), width=2)
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(26, 26, 26))
    draw.text((x + 8, y + h - 14), "STRAIT OF HORMUZ",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def illo_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 230))
    # grid
    for gx in range(x + 20, x + w, 40):
        draw.line([(gx, y + 8), (gx, y + h - 22)], fill=(220, 216, 208), width=1)
    for gy in range(y + 16, y + h - 16, 22):
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(220, 216, 208), width=1)
    # falling line
    pts = [(x + 14, y + 22), (x + 70, y + 34), (x + 120, y + 30),
           (x + 175, y + 52), (x + 225, y + 66), (x + 275, y + 62),
           (x + 300, y + 88)]
    draw.line(pts, fill=(166, 30, 30), width=4, joint="curve")
    draw.polygon([(x + 300, y + 88), (x + 288, y + 78), (x + 290, y + 92)],
                 fill=(166, 30, 30))
    # bitcoin coin
    cx, cy = x + 52, y + 66
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(240, 180, 60),
                 outline=(180, 120, 20), width=2)
    draw.text((cx - 9, cy - 13), "B", font=font(SANS_B, 24), fill=(120, 75, 10))
    draw.text((x + w - 92, y + 14), "-2.4%", font=font(SANS_B, 20),
              fill=(166, 30, 30))
    draw.rectangle([x, y + h - 16, x + w, y + h], fill=(26, 26, 26))
    draw.text((x + 8, y + h - 14), "MARKETS  ·  NEW YORK",
              font=font(SANS_B, 10), fill=(255, 255, 255))

LEADS = [
    dict(num=1, headline="RIYADH TOWER HIT AGAIN",
         deck=("Houthi drone hits PIF Tower, Riyadh's tallest, a second "
               "time in five days. 11 hurt, all stable."),
         chip=("CONFIRMED", GREEN), source="Reuters, SPA, AFP",
         illo=illo_riyadh),
    dict(num=2, headline="HORMUZ: 4TH TANKER HIT",
         deck=("IRGC says a fourth tanker hit a mine; oil traffic down "
               "40%. Iran refuses talks until 7 conditions met."),
         chip=("REPORTED", AMBER), source="Reuters, AP, WSJ",
         illo=illo_hormuz),
    dict(num=3, headline="BITCOIN BELOW $60,000",
         deck=("A day after Nvidia's +31% surge, markets slide: S&P 500 "
               "-0.7%, Nasdaq -1.6%. Bitcoin falls below $60,000."),
         chip=("REPORTED", AMBER), source="CoinDesk, Babypips",
         illo=illo_markets),
]

SECONDARIES = [
    (4, "GAZA — Airstrikes kill Hamas security chief + 6", "Reuters / AP"),
    (5, "UKRAINE — Strike on Zaporizhzhia kills 2, wounds ~40", "AP"),
    (6, "UKRAINE — 700,000+ Russian soldiers killed in war", "Kyiv Independent"),
    (7, "UKRAINE — Germany first to access Delta system", "Kyiv Independent"),
    (8, "SPACE — NATO vows defence as Russia readies armed satellite", "BBC"),
    (9, "SENEGAL — CAS restores AFCON crown, 1–0 over Morocco", "CAS / AP"),
    (10, "UK — Sanctions on Myanmar generals after ICJ ruling", "10things"),
    (11, "ROHINGYA — Malaysia to return 6,500+ refugees", "JAWS / Medium"),
    (12, "CHESS — World title match begins in Geneva", "CareerIndia"),
    (13, "DRC — Fighting traps Ebola responders near hospital", "WHO / UN News"),
    (14, "IRAQ — PM orders takeover of Kurdish oilfields", "Reuters / Al Arabiya"),
]

BRIEFS = [
    (15, "US — Pentagon: Canada short on defence", "Just Security"),
    (16, "US — Trump to speed death sentences", "Just Security"),
    (17, "US — Rep. Gomez resigns, ethics probe", "CWEB"),
    (18, "US — Watchdog: ICE cut training too far", "JAWS"),
    (19, "US — Commerce Dept blacklists cloud firm", "Just Security"),
    (20, "CLIMATE — EU seeks change after COP31", "One Turn"),
    (21, "LIBYA — UN wants probe of port attacks", "UN News"),
    (22, "CRICKET — India–NZ Test ends in draw", "CareerIndia"),
    (23, "UAE — Bus crash kills 13, injures 14", "CWEB"),
    (24, "SOLOMON IS. — To end China pact", "10things"),
    (25, "S. KOREA — $375k rewards vs AI cheats", "Just Security"),
    (26, "FOOD — Wars threaten aid for 7.3m", "10things"),
    (27, "US WEATHER — King tides; Florida floods", "CWEB"),
    (28, "US ECONOMY — Thanksgiving dinner +6.3%", "CWEB"),
    (29, "BELGIUM — PM sets budget deadline", "Facebook"),
    (30, "POPE — Francis diary: crisis, visions", "CWEB"),
    (31, "SPORT — Super Bowl LXI shown in IMAX", "ESPN / NFL"),
    (32, "MARKETS — Anthropic -4% to ~$84", "CoinDesk"),
    (33, "CRYPTO — Bitcoin down ~21% in Nov", "AiEon"),
    (34, "EARNINGS — Best Buy, Dick's report", "CWEB"),
]

UTC_STRIP = [
    ("~06:00", "Drone hits PIF Tower"),
    ("10:08", "Bitcoin below $60,000"),
    ("12:37", "PIF Tower hit, 2nd in 5 days"),
    ("12:46", "S&P futures -1.08%"),
    ("16:00", "Houthis yet to claim strike"),
    ("17:46", "CAS restores Senegal"),
    ("18:39", "CAF accepts Senegal ruling"),
]

NUMBERS = ["11 INJURED RIYADH", "4 TANKERS HIT", "700,000+ RUSSIAN DEAD",
           "BITCOIN BELOW $60,000", "103.3 CONFIDENCE", "6,500 ROHINGYA",
           "13 DEAD UAE BUS", "1–0 SENEGAL"]


def draw_page():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 24
    CW = W - 2 * M  # 976

    # ---- masthead ------------------------------------------------------
    y = 12
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 54)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 62
    date = "TUESDAY,  24  NOVEMBER  2026"
    df = font(SANS_B, 19)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, y), date, font=df, fill=RED)
    y += 27
    d.line([(M, y), (W - M, y)], fill=RULE, width=3)
    y += 4
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 9

    # ---- UTC strip -----------------------------------------------------
    d.text((M, y), "THE DAY IN UTC", font=font(SANS_B, 12), fill=INK)
    y += 17
    # two rows: 4 + 3; each item truncated to its column width
    rows = [UTC_STRIP[:4], UTC_STRIP[4:]]
    for row in rows:
        x = M
        col_w = CW / 4
        for t, txt in row:
            tfnt, xfnt = font(SANS_B, 11), font(SANS, 11)
            twd = d.textlength(t, font=tfnt)
            d.text((x, y), t, font=tfnt, fill=RED)
            avail = col_w - twd - 8
            while d.textlength(txt, font=xfnt) > avail and len(txt) > 4:
                txt = txt[:-1]
            d.text((x + twd + 5, y), txt, font=xfnt, fill=INK)
            x += col_w
        y += 14
    y += 3
    d.line([(M, y), (W - M, y)], fill=LIGHT, width=1)
    y += 6

    # ---- numbers strip (black band, auto-fit font) ---------------------
    band_h = 25
    d.rectangle([M, y, W - M, y + band_h], fill=INK)
    nsize = 12
    while nsize > 9:
        nf = font(SANS_B, nsize)
        parts = "   ·   ".join(NUMBERS)
        if d.textlength(parts, font=nf) <= CW - 16:
            break
        nsize -= 1
    nf = font(SANS_B, nsize)
    parts = "   ·   ".join(NUMBERS)
    pw = d.textlength(parts, font=nf)
    d.text(((W - pw) / 2, y + 5), parts, font=nf, fill=(255, 255, 255))
    y += band_h + 6

    # ---- coverage line -------------------------------------------------
    cov = ("34 STORIES  ·  MIDDLE EAST 5  ·  EUROPE 8  ·  ASIA 5  ·  "
           "AFRICA 3  ·  N. AMERICA 10  ·  GLOBAL 3")
    cf = font(SANS_B, 12)
    cw = d.textlength(cov, font=cf)
    d.text(((W - cw) / 2, y), cov, font=cf, fill=INK)
    y += 20
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 8

    # ---- 3 leads -------------------------------------------------------
    lead_w = (CW - 2 * 16) // 3  # 314
    lead_bottom = y
    for i, lead in enumerate(LEADS):
        x = M + i * (lead_w + 16)
        d.text((x, y), f"{lead['num']}", font=font(SERIF_B, 15), fill=RED)
        d.text((x + 16, y + 1), "LEAD", font=font(SANS_B, 10), fill=GREY)
        ly = y + 20
        lead["illo"](d, x, ly, lead_w, 110)
        ty = ly + 110 + 7
        ty = draw_wrapped(d, lead["headline"], font(SERIF_B, 19),
                          x, ty, lead_w, leading=22, max_lines=2)
        ty += 3
        ty = draw_wrapped(d, lead["deck"], font(SANS, 12),
                          x, ty, lead_w, leading=15, max_lines=2)
        ty += 5
        cx = chip(d, x, ty, *lead["chip"])
        d.text((cx + 6, ty + 2), "Source: " + lead["source"],
               font=font(SANS, 10), fill=GREY)
        lead_bottom = max(lead_bottom, ty + 15)
    y = lead_bottom + 8

    # ---- secondaries ---------------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6
    d.text((M, y), "MORE FROM THE DAY", font=font(SANS_B, 12), fill=INK)
    y += 18
    col_w = (CW - 24) // 2
    for ci, group in enumerate([SECONDARIES[:6], SECONDARIES[6:]]):
        x = M + ci * (col_w + 24)
        yy = y
        for num, head, src in group:
            bf = font(SERIF_B, 13)
            d.text((x, yy), f"{num}.", font=bf, fill=RED)
            yy = draw_wrapped(d, head, font(SANS_B, 12), x + 24, yy,
                              col_w - 24, leading=15, max_lines=2)
            d.text((x + 24, yy), "Source: " + src,
                   font=font(SANS, 10), fill=GREY)
            yy += 14
        if ci == 0:
            left_end = yy
    y = max(left_end, yy) + 2

    # ---- map + date check ----------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6
    map_w, map_h = 500, 132
    dc_x = M + map_w + 16
    dc_w = CW - map_w - 16
    d.text((M, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    d.text((dc_x, y), "DATE CHECK — NOT 24 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    y += 17
    draw_map(d, M, y, map_w, map_h)
    # date check box
    d.rectangle([dc_x, y, dc_x + dc_w, y + map_h], outline=RED, width=1)
    d.text((dc_x + 10, y + 6),
           "Left out on purpose — these happened on other days:",
           font=font(SANS_B, 11), fill=INK)
    dc_items = [
        "COP31 collapse itself — 22 Nov (EU seeks rule change 24 Nov)",
        "Merkury sinking off Libya — 22 Nov, confirmed 23 Nov",
        "Alcaraz wins ATP Finals — 22 Nov",
        "ICJ Myanmar genocide ruling — 20 Nov (UK sanctions 24 Nov)",
        "Nvidia CEO Huang reinstated — Mon 23 Nov",
        "Zelensky calls for NATO admission — 23 Nov",
        "Nepal PM Shah India visit — 23 Nov",
    ]
    yy = y + 23
    for it in dc_items:
        d.text((dc_x + 10, yy), "•  " + it, font=font(SANS, 10), fill=INK)
        yy += 12
    d.text((dc_x + 10, y + map_h - 13),
           "This page carries only their 24 Nov follow-ups.",
           font=font(SANS, 10), fill=GREY)
    y += map_h + 4
    d.text((M, y), "Pins 1–14 match the numbered stories above.",
           font=font(SANS, 10), fill=GREY)
    y += 15

    # ---- briefs --------------------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 6
    d.text((M, y), "ALSO ON 24 NOVEMBER", font=font(SANS_B, 12), fill=INK)
    y += 18
    bcol_w = (CW - 2 * 16) // 3
    groups = [BRIEFS[:7], BRIEFS[7:14], BRIEFS[14:]]
    for ci, group in enumerate(groups):
        x = M + ci * (bcol_w + 16)
        yy = y
        for num, head, src in group:
            d.text((x, yy), f"{num}.", font=font(SANS_B, 10), fill=RED)
            # one line: headline + source; trim the headline, never the source
            bf = font(SANS, 10)
            suffix = "  (" + src + ")"
            htxt = head
            while d.textlength(htxt + suffix, font=bf) > bcol_w - 22 \
                    and len(htxt) > 12:
                htxt = htxt[:-1].rstrip()
            d.text((x + 22, yy), htxt + suffix, font=bf, fill=INK)
            yy += 14
    y += 7 * 14 + 6

    # ---- footer --------------------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 6
    d.text((M, y), "● CONFIRMED — officially confirmed    ● REPORTED — "
           "reported by named sources",
           font=font(SANS, 10), fill=GREY)
    y += 14
    foot = ("Sources: Reuters, AP, AFP, WSJ, BBC, CoinDesk, SPA, CAS, "
            "UN News, Kyiv Independent — named per story.  ·  THE WORLD TODAY")
    d.text((M, y), foot, font=font(SANS, 10), fill=GREY)
    y += 14
    return img, y


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png(path):
    """Validate the written file: PNG signature + 1024x1024 IHDR dimensions."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_SIGNATURE:
        raise ValueError("not a PNG file: bad signature in " + path)
    if head[12:16] != b"IHDR":
        raise ValueError("not a PNG file: missing IHDR chunk in " + path)
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    if (width, height) != (W, H):
        raise ValueError("wrong size %dx%d, expected %dx%d"
                         % (width, height, W, H))
    return width, height


def main():
    """Write entry.png to $MAKEFUN_OUTPUT_DIR (default /output)."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    if HAVE_PIL:
        page, _end_y = draw_page()
        page.save(out_path, "PNG", optimize=True)
    else:
        # No Pillow on the grader: copy the pre-drawn page from the repo.
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile(os.path.join(here, "entry.png"), out_path)
    check_png(out_path)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
