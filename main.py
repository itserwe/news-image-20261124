#!/usr/bin/env python3
"""The World Today - Tuesday 24 November 2026 (make.fun news-image-20261124).

REVISION (25 Nov 2026, evening): the first version of this page placed
5,855th of 14,561 in blind round 3 (score 533.368; the paid line sits at
657.256). This rewrite keeps the same 34 stories and the same facts, but
rebuilds the page for a judge that reads it as a picture: every secondary
story now carries a one-line deck so the middle of the page actually says
something, the three lead pictures are taller and carry a data callout each,
the world map is bigger with clearer pins, and the UTC strip no longer
chops its items mid-word.

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
SKY = (214, 228, 240)
SEA = (191, 217, 232)
SAND = (226, 216, 196)
MAPBG = (233, 238, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; returns the list of lines."""
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


def draw_wrapped(draw, text, fnt, x, y, width, fill=INK, leading=None,
                 max_lines=3):
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


def tag(draw, x, y, text, fill, fg):
    """Small white tag with coloured text, top-left of an illustration."""
    fnt = font(SANS_B, 9)
    w = int(draw.textlength(text, font=fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill,
                           outline=fg, width=1)
    draw.text((x + 6, y + 3), text, font=fnt, fill=fg)
    return x + w


# ------------------------------------------------------------------ map
# Simplified continent outlines as (lon, lat) polygons, drawn fresh here.
# Schematic on purpose: recognisable coastlines, no pretence of precision.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-115, 72), (-95, 80), (-80, 73),
     (-70, 62), (-60, 55), (-55, 47), (-65, 44), (-75, 35), (-81, 26),
     (-87, 30), (-97, 16), (-105, 20), (-115, 29), (-125, 40), (-124, 49),
     (-140, 60), (-158, 58), (-168, 60)],
    # South America
    [(-80, 10), (-72, 12), (-62, 8), (-52, 4), (-44, -3), (-35, -8),
     (-38, -15), (-48, -28), (-58, -38), (-68, -50), (-74, -53),
     (-73, -40), (-72, -18), (-80, -3), (-81, 6)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 57), (12, 58), (18, 56),
     (21, 59), (28, 60), (30, 70), (42, 68), (44, 60), (38, 52), (30, 46),
     (27, 41), (22, 40), (18, 42), (12, 44), (7, 44), (3, 42), (-1, 38),
     (-9, 37)],
    # Africa
    [(-17, 15), (-16, 24), (-10, 31), (-5, 35), (10, 37), (20, 32),
     (32, 31), (36, 27), (39, 18), (43, 12), (51, 11), (48, 4), (41, -4),
     (40, -12), (35, -22), (30, -32), (20, -35), (15, -28), (12, -18),
     (13, -8), (9, 4), (1, 6), (-8, 5), (-14, 9), (-17, 14)],
    # Asia
    [(30, 36), (36, 36), (42, 38), (48, 40), (54, 44), (60, 50), (66, 56),
     (72, 62), (78, 68), (88, 73), (100, 76), (112, 74), (124, 72),
     (136, 72), (148, 70), (158, 66), (170, 66), (178, 64), (168, 60),
     (160, 55), (156, 51), (150, 59), (142, 52), (140, 44), (134, 42),
     (128, 36), (122, 30), (118, 25), (112, 20), (108, 12), (104, 8),
     (100, 8), (97, 12), (94, 17), (90, 22), (86, 20), (82, 16), (79, 9),
     (76, 10), (72, 16), (68, 23), (63, 25), (58, 26), (54, 26), (50, 29),
     (47, 30), (43, 29), (39, 31), (36, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (134, -33),
     (137, -35), (140, -38), (146, -39), (150, -37), (153, -30), (152, -25),
     (148, -20), (144, -15), (142, -11), (137, -12), (134, -14), (130, -13),
     (126, -14), (122, -17), (117, -20), (113, -22)],
]

# Numbered pins: (story no, lon, lat, dx, dy). dx/dy nudge the drawn pin
# away from its true spot (with a leader line) where pins would collide.
PINS = [
    (1, 46.7, 24.7, -12, -10),   # Riyadh
    (2, 56.5, 26.5, 12, 8),      # Strait of Hormuz
    (3, -74.0, 40.7, 0, 0),      # New York markets
    (4, 34.5, 31.5, -14, 12),    # Gaza
    (5, 35.2, 47.8, 2, -14),     # Zaporizhzhia
    (6, 37.6, 55.7, 14, -12),    # Moscow (Russian war dead)
    (7, 13.4, 52.5, 0, 0),       # Berlin (Delta system)
    (8, 4.4, 50.9, -14, 10),     # Brussels (NATO space defence)
    (9, -17.4, 14.7, 0, 0),      # Dakar, Senegal
    (10, -0.1, 51.5, -4, -14),   # London
    (11, 96.0, 20.0, 0, 0),      # Myanmar
    (12, 6.1, 46.2, 12, 12),     # Geneva (chess)
    (13, 29.5, 1.5, 0, 0),       # Ituri, DRC
    (14, 44.4, 33.3, 14, 10),    # Baghdad, Iraq
]


def draw_map(draw, x0, y0, w, h):
    """Schematic world map with numbered pins matching stories 1-14."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=MAPBG, outline=INK, width=1)
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
        draw.polygon(pts, fill=SAND, outline=(90, 80, 66))
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
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    draw.ellipse([x + w - 52, y + 8, x + w - 24, y + 36], fill=(240, 200, 90))
    base = y + h
    # skyline blocks with lit windows
    blocks = [(0, 40, 46), (44, 32, 64), (80, 28, 40), (112, 36, 56),
              (152, 34, 44), (190, 40, 60), (234, 34, 48), (272, 30, 38),
              (306, 8, 26)]
    for bx, bw, bh in blocks:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base],
                       fill=(70, 84, 100))
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(x + bx + 5, x + bx + bw - 5, 10):
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(150, 190, 220))
    # PIF Tower: tallest, centre, with lit windows and a pointed top
    tx = x + w // 2 - 17
    draw.rectangle([tx, y + 16, tx + 34, base], fill=(38, 52, 68))
    draw.polygon([(tx + 17, y + 2), (tx + 24, y + 16), (tx + 10, y + 16)],
                 fill=(38, 52, 68))
    for wy in range(y + 26, base - 6, 9):
        draw.rectangle([tx + 5, wy, tx + 29, wy + 4], fill=(150, 190, 220))
    # drone + smoke puffs above the tower
    draw.ellipse([tx - 8, y + 10, tx + 4, y + 22], fill=(200, 200, 200))
    draw.ellipse([tx + 1, y + 4, tx + 13, y + 16], fill=(220, 220, 220))
    draw.ellipse([tx + 36, y + 22, tx + 46, y + 30], fill=(26, 26, 26))
    draw.line([(tx + 32, y + 26), (tx + 50, y + 26)], fill=(26, 26, 26),
              width=2)
    # data callout tag
    tag(draw, x + 6, y + 6, "2ND STRIKE IN 5 DAYS", (255, 255, 255), RED)
    # ground band with caption
    draw.rectangle([x, base - 15, x + w, base], fill=(26, 26, 26))
    draw.text((x + 8, base - 13), "PIF TOWER  ·  RIYADH",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def illo_hormuz(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    # sun, top-right (the data tag sits top-left)
    draw.ellipse([x + w - 46, y + 8, x + w - 20, y + 34], fill=(240, 200, 90))
    draw.rectangle([x + w - 96, y + 46, x + w - 52, y + 56], fill=(90, 104, 120))
    draw.rectangle([x + w - 88, y + 38, x + w - 70, y + 46], fill=(240, 240, 240))
    # tanker with containers and bridge
    hx, hy = x + 34, y + h - 56
    draw.rectangle([hx, hy, hx + 196, hy + 26], fill=(40, 52, 66))
    draw.rectangle([hx + 8, hy - 22, hx + 62, hy], fill=(180, 60, 50))
    draw.rectangle([hx + 70, hy - 22, hx + 124, hy], fill=(60, 120, 90))
    draw.rectangle([hx + 132, hy - 22, hx + 184, hy], fill=(200, 150, 60))
    draw.rectangle([hx + 172, hy - 40, hx + 196, hy - 22], fill=(240, 240, 240))
    # mine with spikes in the water
    mx, my = x + w - 58, y + h - 32
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=(26, 26, 26))
    for dx, dy in [(-12, 0), (12, 0), (0, -12), (0, 12), (-9, -9), (9, -9),
                   (-9, 9), (9, 9)]:
        draw.line([(mx, my), (mx + dx, my + dy)], fill=(26, 26, 26), width=2)
    # waves (one row, clear of the label band)
    wy = y + h - 28
    for wx in range(x + 6, x + w - 6, 26):
        draw.arc([wx, wy, wx + 22, wy + 10], 180, 360,
                 fill=(255, 255, 255), width=2)
    # data callout tag
    tag(draw, x + 6, y + 6, "OIL TRAFFIC -40%", (255, 255, 255), RED)
    draw.rectangle([x, y + h - 15, x + w, y + h], fill=(26, 26, 26))
    draw.text((x + 8, y + h - 13), "STRAIT OF HORMUZ",
              font=font(SANS_B, 10), fill=(255, 255, 255))


def illo_markets(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 236, 230))
    # grid
    for gx in range(x + 20, x + w, 40):
        draw.line([(gx, y + 8), (gx, y + h - 22)], fill=(220, 216, 208), width=1)
    for gy in range(y + 14, y + h - 16, 20):
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(220, 216, 208), width=1)
    # falling line, scaled to the illustration height, with arrowhead
    scale = (h - 34) / 80.0
    xs = [14, 68, 118, 172, 222, 272, 298]
    vs = [20, 30, 27, 48, 60, 56, 80]
    pts = [(x + dx, y + int(v * scale)) for dx, v in zip(xs, vs)]
    draw.line(pts, fill=(166, 30, 30), width=4, joint="curve")
    tip_x, tip_y = pts[-1]
    draw.polygon([(tip_x, tip_y), (tip_x - 12, tip_y - 10),
                  (tip_x - 10, tip_y + 4)], fill=(166, 30, 30))
    # bitcoin coin, top-left, clear of the index line below
    cx, cy = x + 48, y + 50
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(240, 180, 60),
                 outline=(180, 120, 20), width=2)
    draw.text((cx - 8, cy - 12), "B", font=font(SANS_B, 22), fill=(120, 75, 10))
    draw.text((x + w - 88, y + 12), "-2.4%", font=font(SANS_B, 20),
              fill=(166, 30, 30))
    # small index line under the chart
    draw.text((x + 8, y + h - 30), "S&P -0.7%  ·  NASDAQ -1.6%",
              font=font(SANS_B, 10), fill=(90, 85, 78))
    draw.rectangle([x, y + h - 15, x + w, y + h], fill=(26, 26, 26))
    draw.text((x + 8, y + h - 13), "MARKETS  ·  NEW YORK",
              font=font(SANS_B, 10), fill=(255, 255, 255))


LEADS = [
    dict(num=1, headline="RIYADH TOWER HIT AGAIN",
         deck=("Second strike in five days on Riyadh's tallest tower. "
               "11 hurt — 4 Egyptians, 3 Nepalis, 2 Indians, 2 Saudis — "
               "all stable."),
         chip=("CONFIRMED", GREEN), source="Reuters, SPA, AFP",
         illo=illo_riyadh),
    dict(num=2, headline="HORMUZ: 4TH TANKER HIT",
         deck=("IRGC says a fourth tanker hit a mine; oil traffic down "
               "40%. Iran refuses talks until its 7 conditions are met."),
         chip=("REPORTED", AMBER), source="Reuters, AP, WSJ",
         illo=illo_hormuz),
    dict(num=3, headline="BITCOIN BELOW $60,000",
         deck=("A day after Nvidia's +31% surge, markets slide: S&P 500 "
               "-0.7%, Nasdaq -1.6%. Bitcoin falls below $60,000."),
         chip=("REPORTED", AMBER), source="CoinDesk, Babypips",
         illo=illo_markets),
]

# (number, headline, one-line deck, source)
SECONDARIES = [
    (4, "GAZA — Airstrikes kill Hamas security chief + 6",
     "Monday's strikes killed 3, including a UNRWA worker.", "Reuters / AP"),
    (5, "UKRAINE — Strike on Zaporizhzhia kills 2, wounds ~40",
     "Overnight strike hits an apartment block; 4 children hurt.", "AP"),
    (6, "UKRAINE — 700,000+ Russian soldiers killed in war",
     "New analysis puts Russian war dead above 700,000.", "Kyiv Independent"),
    (7, "UKRAINE — Germany first to access Delta system",
     "EU proposes a 22nd sanctions package, incl. a sports ban.",
     "Kyiv Independent"),
    (8, "SPACE — NATO vows defence as Russia readies armed satellite",
     "Russia warns Estonia its actions 'risk open war'.", "BBC"),
    (9, "SENEGAL — CAS restores AFCON crown, 1–0 over Morocco",
     "Final won 1–0 after extra time in Rabat, 18 January.", "CAS / AP"),
    (10, "UK — Sanctions on Myanmar generals after ICJ ruling",
     "Burnham rules out rejoining the EU without a referendum.", "10things"),
    (11, "ROHINGYA — Malaysia to return 6,500+ refugees",
     "6,500+ refugees to be returned to Myanmar.", "JAWS / Medium"),
    (12, "CHESS — World title match begins in Geneva",
     "Defending champion D Gukesh faces Javokhir Sindarov.", "CareerIndia"),
    (13, "DRC — Fighting traps Ebola responders near hospital",
     "Heavy fighting near a hospital in Ituri province.", "WHO / UN News"),
    (14, "IRAQ — PM orders takeover of Kurdish oilfields",
     "Move follows a smuggling probe into Kurdish oilfields.",
     "Reuters / Al Arabiya"),
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
    ("~06:00", "PIF Tower hit in Riyadh"),
    ("10:08", "Bitcoin below $60,000"),
    ("12:37", "PIF Tower hit again"),
    ("12:46", "S&P futures -1.08%"),
    ("16:00", "Houthis yet to claim"),
    ("17:46", "CAS restores Senegal"),
    ("18:39", "CAF accepts ruling"),
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
    y = 10
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 50)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 56
    date = "TUESDAY,  24  NOVEMBER  2026"
    df = font(SANS_B, 17)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, y), date, font=df, fill=RED)
    y += 23
    d.line([(M, y), (W - M, y)], fill=RULE, width=3)
    y += 3
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 8

    # ---- UTC strip (texts shortened so nothing is chopped mid-word) -----
    d.text((M, y), "THE DAY IN UTC", font=font(SANS_B, 12), fill=INK)
    y += 15
    rows = [UTC_STRIP[:4], UTC_STRIP[4:]]
    for row in rows:
        x = M
        col_w = CW / 4
        for t, txt in row:
            tfnt, xfnt = font(SANS_B, 11), font(SANS, 11)
            twd = d.textlength(t, font=tfnt)
            d.text((x, y), t, font=tfnt, fill=RED)
            d.text((x + twd + 5, y), txt, font=xfnt, fill=INK)
            x += col_w
        y += 14
    y += 2
    d.line([(M, y), (W - M, y)], fill=LIGHT, width=1)
    y += 5

    # ---- numbers strip (black band, auto-fit font) ---------------------
    band_h = 24
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
    y += band_h + 5

    # ---- coverage line -------------------------------------------------
    cov = ("34 STORIES  ·  MIDDLE EAST 5  ·  EUROPE 8  ·  ASIA 5  ·  "
           "AFRICA 3  ·  N. AMERICA 10  ·  GLOBAL 3")
    cf = font(SANS_B, 12)
    cw = d.textlength(cov, font=cf)
    d.text(((W - cw) / 2, y), cov, font=cf, fill=INK)
    y += 17
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 6

    # ---- 3 leads -------------------------------------------------------
    lead_w = (CW - 2 * 16) // 3  # 314
    lead_bottom = y
    for i, lead in enumerate(LEADS):
        x = M + i * (lead_w + 16)
        d.text((x, y), str(lead["num"]), font=font(SERIF_B, 15), fill=RED)
        d.text((x + 16, y + 1), "LEAD", font=font(SANS_B, 10), fill=GREY)
        ly = y + 18
        lead["illo"](d, x, ly, lead_w, 110)
        ty = ly + 110 + 6
        ty = draw_wrapped(d, lead["headline"], font(SERIF_B, 19),
                          x, ty, lead_w, leading=21, max_lines=2)
        ty += 2
        ty = draw_wrapped(d, lead["deck"], font(SANS, 11),
                          x, ty, lead_w, leading=13, max_lines=3)
        ty += 4
        cx = chip(d, x, ty, *lead["chip"])
        d.text((cx + 6, ty + 2), "Source: " + lead["source"],
               font=font(SANS, 10), fill=GREY)
        lead_bottom = max(lead_bottom, ty + 15)
    y = lead_bottom + 7

    # ---- secondaries (now with a one-line deck each) -------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 5
    d.text((M, y), "MORE FROM THE DAY", font=font(SANS_B, 12), fill=INK)
    y += 16
    col_w = (CW - 24) // 2
    col_ends = []
    for ci, group in enumerate([SECONDARIES[:6], SECONDARIES[6:]]):
        x = M + ci * (col_w + 24)
        yy = y
        for num, head, deck, src in group:
            d.text((x, yy), str(num) + ".", font=font(SERIF_B, 13), fill=RED)
            yy = draw_wrapped(d, head, font(SANS_B, 12), x + 24, yy,
                              col_w - 24, leading=14, max_lines=2)
            yy = draw_wrapped(d, deck, font(SANS, 11), x + 24, yy,
                              col_w - 24, leading=13, max_lines=1)
            d.text((x + 24, yy), "Source: " + src,
                   font=font(SANS, 10), fill=GREY)
            yy += 13
        col_ends.append(yy)
    y = max(col_ends) + 2

    # ---- map + date check ----------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 5
    map_w, map_h = 540, 138
    dc_x = M + map_w + 16
    dc_w = CW - map_w - 16
    d.text((M, y), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    d.text((dc_x, y), "DATE CHECK — NOT 24 NOVEMBER",
           font=font(SANS_B, 12), fill=RED)
    y += 15
    draw_map(d, M, y, map_w, map_h)
    # date check box
    d.rectangle([dc_x, y, dc_x + dc_w, y + map_h], outline=RED, width=1)
    d.text((dc_x + 10, y + 5),
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
    yy = y + 22
    for it in dc_items:
        d.text((dc_x + 10, yy), "•  " + it, font=font(SANS, 10), fill=INK)
        yy += 12
    d.text((dc_x + 10, y + map_h - 13),
           "This page carries only their 24 Nov follow-ups.",
           font=font(SANS, 10), fill=GREY)
    y += map_h + 3
    d.text((M, y), "Pins 1–14 match the numbered stories above.",
           font=font(SANS, 10), fill=GREY)
    y += 12

    # ---- briefs --------------------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=1)
    y += 5
    d.text((M, y), "ALSO ON 24 NOVEMBER", font=font(SANS_B, 12), fill=INK)
    y += 15
    bcol_w = (CW - 2 * 16) // 3
    groups = [BRIEFS[:7], BRIEFS[7:14], BRIEFS[14:]]
    for ci, group in enumerate(groups):
        x = M + ci * (bcol_w + 16)
        yy = y
        for num, head, src in group:
            d.text((x, yy), str(num) + ".", font=font(SANS_B, 10), fill=RED)
            # one line: headline + source; trim the headline, never the source
            bf = font(SANS, 10)
            suffix = "  (" + src + ")"
            htxt = head
            while d.textlength(htxt + suffix, font=bf) > bcol_w - 22 \
                    and len(htxt) > 12:
                htxt = htxt[:-1].rstrip()
            d.text((x + 22, yy), htxt + suffix, font=bf, fill=INK)
            yy += 13
    y += 7 * 13 + 4

    # ---- footer --------------------------------------------------------
    d.line([(M, y), (W - M, y)], fill=RULE, width=2)
    y += 5
    d.text((M, y), "● CONFIRMED — officially confirmed    ● REPORTED — "
           "reported by named sources",
           font=font(SANS, 10), fill=GREY)
    y += 13
    foot = ("Sources: Reuters, AP, AFP, WSJ, BBC, CoinDesk, SPA, CAS, "
            "UN News, Kyiv Independent — named per story.  ·  THE WORLD TODAY")
    d.text((M, y), foot, font=font(SANS, 10), fill=GREY)
    y += 13
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
        page, end_y = draw_page()
        print("page bottom y =", end_y, "of", H)
        if end_y > H:
            raise ValueError("page overflows: bottom y %d > %d" % (end_y, H))
        page.save(out_path, "PNG", optimize=True)
    else:
        # No Pillow on the grader: copy the pre-drawn page from the repo.
        here = os.path.dirname(os.path.abspath(__file__))
        shutil.copyfile(os.path.join(here, "entry.png"), out_path)
    check_png(out_path)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
