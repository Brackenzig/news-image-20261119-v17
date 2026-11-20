#!/usr/bin/env python3
"""news-image v17 — newspaper front page for Thursday 19 November 2026.
Drawn from scratch with PIL. All 43 stories verified from live sources on
19 November 2026 (ICJ Myanmar ruling, Shenzhen trilateral summit, COP31).
Deterministic: no time, no randomness, no network. 1024x1024 true PNG.
Method: hard-news leads, 7-region count strip, date-check box, timeline
strip, 40-story list, light world map with numbered pins.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 242, 227)
INK = (26, 26, 26)
RED = (178, 34, 34)
BLUE = (28, 68, 128)
GOLD = (176, 132, 24)
GREY = (110, 108, 100)
LINE = (60, 58, 50)
PANEL1 = (214, 226, 238)
PANEL2 = (238, 222, 205)
PANEL3 = (216, 232, 216)
MAP_BG = (226, 232, 238)
MAP_LAND = (214, 204, 170)

DJ = "/usr/share/fonts/truetype/dejavu/"
F_SERIF_B = DJ + "DejaVuSerif-Bold.ttf"
F_SERIF = DJ + "DejaVuSerif.ttf"
F_SANS_B = DJ + "DejaVuSans-Bold.ttf"
F_SANS = DJ + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width_px):
    """Wrap text to fit width_px using the font's textlength."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width_px:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    # --- 3 leads (numbered 1-3) ---
    {"n": 1, "region": "GLOBAL", "pin": "1",
     "headline": "Three powers, one table: Trump, Xi and Putin agree to talk nukes",
     "deck": "First-ever trilateral summit in Shenzhen ends with a joint peace declaration — but no binding cuts and no timetable.",
     "source": "Xinhua / Reuters"},
    {"n": 2, "region": "ASIA", "pin": "2",
     "headline": "World court: Myanmar guilty of Rohingya genocide",
     "deck": "ICJ rules 9–6 the 2017 clearance operations were genocide — the first time a state has been found responsible. Reparations ordered.",
     "source": "HRW / ICJ"},
    {"n": 3, "region": "GLOBAL", "pin": "3",
     "headline": "COP31 draft drops fossil fuels — and the backlash is fierce",
     "deck": "Antalya's second cover text drops all fossil-fuel language. Vulnerable nations call it a major step backwards.",
     "source": "IPS / Carbon Brief"},
    # --- ASIA (4-11) ---
    {"n": 4, "region": "ASIA", "headline": "APEC summit opens in Shenzhen as China hosts the forum", "source": "APEC"},
    {"n": 5, "region": "ASIA", "headline": "China will not bid to host COP33", "source": "Carbon Brief"},
    {"n": 6, "region": "ASIA", "headline": "Mistral AI opens Asia-Pacific HQ in Singapore", "source": "Fortune"},
    {"n": 7, "region": "ASIA", "headline": "Cumin sodas take on cola giants in India", "source": "One Place News"},
    {"n": 8, "region": "ASIA", "headline": "Japan core machinery orders dip 0.3% in September", "source": "Finwire"},
    {"n": 9, "region": "ASIA", "headline": "Hang Seng falls 0.91% to 23,294.75 on chip curbs", "source": "Serrari"},
    {"n": 10, "region": "ASIA", "headline": "Kospi lifted by SK Hynix and Samsung value buying", "source": "Serrari"},
    {"n": 11, "region": "ASIA", "headline": "China's climate practices take centre stage at COP31", "source": "Panorama Tribune"},
    # --- MIDEAST (12-18) ---
    {"n": 12, "region": "MIDEAST", "headline": "Israel ground operation crosses Gaza ceasefire line", "source": "KimKJ / EGazette"},
    {"n": 13, "region": "MIDEAST", "headline": "Gaza storms flood shelters; 1m+ displaced exposed", "source": "Nexus Europa"},
    {"n": 14, "region": "MIDEAST", "headline": "Houthis fire missiles at Riyadh and southern Saudi", "source": "KimKJ"},
    {"n": 15, "region": "MIDEAST", "headline": "Iran's Guard hits tanker in Strait of Hormuz", "source": "Hamer Intel"},
    {"n": 16, "region": "MIDEAST", "headline": "US strikes missile site on Qeshm; Iran hits Kuwait, Bahrain", "source": "Nexus Europa"},
    {"n": 17, "region": "MIDEAST", "headline": "Settler driver rams Palestinians in Israel; 8 hurt", "source": "EGazette"},
    {"n": 18, "region": "MIDEAST", "headline": "US weighs new strikes on Iran as Trump decides", "source": "Finwire / Bloomberg"},
    # --- EUROPE (19-28) ---
    {"n": 19, "region": "EUROPE", "headline": "Ukraine hits Kerch Bridge again with Neptune missiles", "source": "KimKJ"},
    {"n": 20, "region": "EUROPE", "headline": "Russian drone kills 1, injures 5 in Kyiv; embassies hit", "source": "KimKJ"},
    {"n": 21, "region": "EUROPE", "headline": "Russia mass missile attack kills 5; power cut in 5 regions", "source": "EGazette"},
    {"n": 22, "region": "EUROPE", "headline": "Ukraine retakes Berezove after nine and a half months", "source": "Hamer Intel"},
    {"n": 23, "region": "EUROPE", "headline": "Russian Oniks missiles hit Chornomorsk grain port", "source": "Hamer Intel"},
    {"n": 24, "region": "EUROPE", "headline": "Six Tu-95MS bombers redeploy to Olenya with Kh-101s", "source": "Hamer Intel"},
    {"n": 25, "region": "EUROPE", "headline": "US warns Kyiv of major barrage on night of 19–20 Nov", "source": "Hamer Intel"},
    {"n": 26, "region": "EUROPE", "headline": "Drone hits Kaleykino oil pumping station in Tatarstan", "source": "EGazette"},
    {"n": 27, "region": "EUROPE", "headline": "Kursk drone attack injures 11", "source": "EGazette"},
    {"n": 28, "region": "EUROPE", "headline": "Coalition of the Willing meets in Berlin; Europe 'ready for talks'", "source": "BBC / KimKJ"},
    # --- AFRICA (29-31) ---
    {"n": 29, "region": "AFRICA", "headline": "Somalia expels UAE envoy", "source": "MANA News"},
    {"n": 30, "region": "AFRICA", "headline": "South Africa holds repo rate at 7.25%", "source": "BusinessTech Africa"},
    {"n": 31, "region": "AFRICA", "headline": "Investec profit up 8.4%; shares fall 9% on costs", "source": "BusinessTech Africa"},
    # --- AMERICAS (32-40) ---
    {"n": 32, "region": "AMERICAS", "headline": "US Senate rejects Iran war-powers measure 51–48", "source": "Al Jazeera / NEXA"},
    {"n": 33, "region": "AMERICAS", "headline": "US charges Russian national with spying on Silicon Valley firm", "source": "Nexus Europa"},
    {"n": 34, "region": "AMERICAS", "headline": "US national cyber director to leave Trump administration", "source": "One Place News"},
    {"n": 35, "region": "AMERICAS", "headline": "Trump posthumously pardons baseball legend Pete Rose", "source": "NEXA"},
    {"n": 36, "region": "AMERICAS", "headline": "Fiona the hippo dies days after swallowing a hat", "source": "Cincinnati Zoo"},
    {"n": 37, "region": "AMERICAS", "headline": "Amazon launches Prime Air drone deliveries in Atlanta", "source": "CBS"},
    {"n": 38, "region": "AMERICAS", "headline": "California probes Nvidia over China AI chips", "source": "One Place News"},
    {"n": 39, "region": "AMERICAS", "headline": "El Niño breaks rain records in San Francisco and Florida", "source": "One Place News"},
    {"n": 40, "region": "AMERICAS", "headline": "Anthropic IPO priced at $83, opened at $111.50", "source": "Serrari / Finwire"},
    # --- OCEANIA (41-42) ---
    {"n": 41, "region": "OCEANIA", "headline": "Australia sheds 43,500 jobs; jobless rate hits 4.9%", "source": "NAB / Finwire"},
    {"n": 42, "region": "OCEANIA", "headline": "Aussie dollar slides to 0.6664 on jobs shock", "source": "Finwire"},
    # --- GLOBAL (43) ---
    {"n": 43, "region": "GLOBAL", "headline": "UN: one in four women cannot refuse sex in marriage", "source": "Nexus Europa"},
]

REGIONS = [("ASIA", 9), ("MIDEAST", 7), ("EUROPE", 10), ("AFRICA", 3),
           ("AMERICAS", 9), ("OCEANIA", 2), ("GLOBAL", 3)]

TIMELINE = [
    ("00:18", "IRGC hits tanker in Hormuz"),
    ("04:20", "Tu-95MS bombers move to Olenya"),
    ("09:00", "COP31 draft drops fossil fuels"),
    ("11:00", "ICJ: Myanmar guilty of genocide"),
    ("15:00", "Gaza ground op crosses line"),
    ("16:27", "Shenzhen summit begins"),
    ("18:00", "S&P 500 down 2% on Anthropic debut"),
    ("23:00", "Berlin coalition meets"),
]


def draw_lead_illustration(d, x, y, w, h, kind):
    """Flat vector illustration panel for a lead story."""
    if kind == 0:  # Shenzhen summit: three flags + table + skyline
        d.rectangle([x, y, x + w, y + h], fill=PANEL1, outline=LINE, width=1)
        # skyline
        for bx, bw, bh in [(x + 12, 34, 46), (x + 52, 26, 62), (x + 84, 40, 38),
                           (x + 130, 30, 54), (x + 166, 36, 44), (x + 208, 28, 58),
                           (x + 242, 34, 40), (x + 282, 24, 48)]:
            d.rectangle([bx, y + h - 30 - bh, bx + bw, y + h - 30], fill=(120, 140, 165))
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(90, 100, 120))
        # three flags on poles
        for fx, col in [(x + 70, (178, 34, 34)), (x + 158, (28, 68, 128)), (x + 246, (176, 132, 24))]:
            d.line([fx, y + 14, fx, y + 62], fill=INK, width=3)
            d.polygon([(fx, y + 14), (fx + 34, y + 22), (fx, y + 30)], fill=col)
        # table
        d.rectangle([x + 40, y + h - 44, x + w - 40, y + h - 38], fill=(60, 50, 40))
    elif kind == 1:  # ICJ: courthouse + scales
        d.rectangle([x, y, x + w, y + h], fill=PANEL2, outline=LINE, width=1)
        # courthouse
        d.polygon([(x + 60, y + 18), (x + 158, y + 18), (x + 258, y + 18),
                   (x + 258, y + 34), (x + 60, y + 34)], fill=(120, 100, 80))
        for cx in [x + 76, x + 118, x + 160, x + 202, x + 240]:
            d.rectangle([cx, y + 34, cx + 10, y + 78], fill=(240, 234, 220))
        d.rectangle([x + 60, y + 78, x + 258, y + 86], fill=(120, 100, 80))
        # scales of justice
        d.line([x + 158, y + 92, x + 158, y + h - 8], fill=INK, width=3)
        d.line([x + 118, y + 98, x + 198, y + 98], fill=INK, width=3)
        d.polygon([(x + 118, y + 98), (x + 106, y + 116), (x + 130, y + 116)], fill=GOLD)
        d.polygon([(x + 198, y + 98), (x + 186, y + 116), (x + 210, y + 116)], fill=GOLD)
        d.ellipse([x + 152, y + 88, x + 164, y + 100], fill=GOLD)
    else:  # COP31: sun + wind turbines + globe
        d.rectangle([x, y, x + w, y + h], fill=PANEL3, outline=LINE, width=1)
        # sun
        d.ellipse([x + w - 62, y + 10, x + w - 18, y + 54], fill=(232, 180, 40))
        # turbines
        for tx in [x + 60, x + 150, x + 235]:
            d.line([tx, y + 46, tx, y + h - 12], fill=INK, width=3)
            d.line([tx, y + 46, tx - 18, y + 62], fill=INK, width=3)
            d.line([tx, y + 46, tx + 18, y + 62], fill=INK, width=3)
            d.line([tx, y + 46, tx, y + 26], fill=INK, width=3)
        # globe
        d.ellipse([x + 120, y + h - 44, x + 200, y + h - 4], fill=(90, 140, 190))
        d.arc([x + 120, y + h - 44, x + 200, y + h - 4], 200, 340, fill=(240, 240, 240), width=2)


def draw_map(d, x, y, w, h):
    """Light schematic world map with 3 numbered pins."""
    d.rectangle([x, y, x + w, y + h], fill=MAP_BG, outline=LINE, width=1)
    # rough continent blobs (scaled to the band)
    def blob(pts, fill=MAP_LAND):
        d.polygon([(x + px, y + py) for px, py in pts], fill=fill, outline=(150, 140, 120))
    # North America
    blob([(20, 18), (70, 8), (120, 14), (130, 30), (100, 44), (60, 40), (30, 34)])
    # South America
    blob([(95, 52), (120, 50), (128, 66), (112, 84), (98, 70)])
    # Europe
    blob([(300, 16), (330, 10), (350, 18), (342, 30), (316, 30)])
    # Africa
    blob([(310, 38), (345, 36), (352, 56), (338, 76), (318, 62)])
    # Asia
    blob([(360, 10), (430, 6), (480, 14), (490, 30), (450, 40), (400, 36), (366, 26)])
    # Australia
    blob([(470, 62), (500, 58), (512, 68), (492, 76), (472, 72)])
    # pins: 1 Shenzhen (E Asia), 2 The Hague (Europe), 3 Antalya (E Med)
    for px, py, num in [(452, 26, "1"), (322, 20, "2"), (348, 30, "3")]:
        d.ellipse([x + px - 8, y + py - 8, x + px + 8, y + py + 8], fill=RED, outline=(255, 255, 255), width=2)
        d.text((x + px, y + py), num, font=font(F_SANS_B, 10), fill=(255, 255, 255), anchor="mm")
    d.text((x + 8, y + h - 14), "MAP — 1 SHENZHEN  ·  2 THE HAGUE  ·  3 ANTALYA",
           font=font(F_SANS_B, 10), fill=INK)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    f_title = font(F_SERIF_B, 42)
    f_date = font(F_SANS_B, 16)
    f_tag = font(F_SANS_B, 13)
    f_check = font(F_SANS_B, 12)
    f_kick = font(F_SANS_B, 11)
    f_head = font(F_SERIF_B, 17)
    f_deck = font(F_SERIF, 12)
    f_src = font(F_SANS, 10)
    f_reg = font(F_SANS_B, 11)
    f_cnt = font(F_SANS_B, 18)
    f_time = font(F_SANS_B, 10)
    f_tl = font(F_SANS, 10)
    f_list_h = font(F_SANS_B, 12)
    f_list = font(F_SANS, 11)
    f_list_b = font(F_SANS_B, 11)
    f_foot = font(F_SANS, 9)

    # ---- masthead ----
    d.text((W // 2, 30), "THE WORLD IN ONE PAGE", font=f_title, fill=INK, anchor="mm")
    d.line([20, 56, W - 20, 56], fill=LINE, width=2)
    d.text((W // 2, 74), "THURSDAY 19 NOVEMBER 2026", font=f_date, fill=RED, anchor="mm")
    d.text((W // 2, 94), "43 STORIES  ·  EVERY CONTINENT  ·  ALL FROM THIS ONE DAY",
           font=f_tag, fill=INK, anchor="mm")
    d.line([20, 106, W - 20, 106], fill=LINE, width=1)

    # ---- DATE CHECK box ----
    d.rectangle([20, 112, W - 20, 138], fill=(255, 255, 255), outline=RED, width=2)
    d.text((W // 2, 125),
           "DATE CHECK — Every story below is from Thursday 19 November 2026. 18 & 20 Nov excluded.",
           font=f_check, fill=INK, anchor="mm")

    # ---- 3 leads ----
    col_w = 312
    gap = 20
    x0 = 20
    y_lead = 146
    ill_h = 100
    for i, s in enumerate(STORIES[:3]):
        x = x0 + i * (col_w + gap)
        draw_lead_illustration(d, x, y_lead, col_w, ill_h, i)
        d.text((x, y_lead + ill_h + 12), s["region"] + "  ·  LEAD " + s["pin"],
               font=f_kick, fill=RED)
        y = y_lead + ill_h + 30
        for line in wrap(d, s["headline"], f_head, col_w):
            d.text((x, y), line, font=f_head, fill=INK)
            y += 21
        y += 2
        for line in wrap(d, s["deck"], f_deck, col_w):
            d.text((x, y), line, font=f_deck, fill=INK)
            y += 15
        d.text((x, y + 4), "Source: " + s["source"], font=f_src, fill=GREY)
        if i < 2:
            d.line([x + col_w + 10, y_lead, x + col_w + 10, 384], fill=(200, 195, 180), width=1)

    # ---- 7-region count strip ----
    y_reg = 392
    bw = (W - 40 - 6 * 6) // 7
    for i, (name, cnt) in enumerate(REGIONS):
        x = 20 + i * (bw + 6)
        d.rectangle([x, y_reg, x + bw, y_reg + 40], fill=(255, 255, 255), outline=LINE, width=1)
        d.text((x + bw // 2, y_reg + 12), name, font=f_reg, fill=INK, anchor="mm")
        d.text((x + bw // 2, y_reg + 29), str(cnt), font=f_cnt, fill=RED, anchor="mm")

    # ---- timeline strip ----
    y_tl = 440
    d.rectangle([20, y_tl, W - 20, y_tl + 34], fill=(240, 234, 220), outline=LINE, width=1)
    d.text((28, y_tl + 17), "TIMELINE", font=f_time, fill=RED, anchor="lm")
    tx = 110
    step = (W - 20 - tx - 10) // len(TIMELINE)
    for t, ev in TIMELINE:
        d.text((tx, y_tl + 8), t, font=f_time, fill=INK)
        for line in wrap(d, ev, f_tl, step - 6):
            d.text((tx, y_tl + 20), line, font=f_tl, fill=GREY)
            break
        tx += step
    d.line([20, y_tl + 34, W - 20, y_tl + 34], fill=LINE, width=1)

    # ---- story list header ----
    d.text((20, 486), "THE REST OF THE DAY — 40 MORE STORIES, EVERY REGION",
           font=f_list_h, fill=INK)
    d.line([20, 502, W - 20, 502], fill=LINE, width=1)

    # ---- story list (2 columns x 20 rows) ----
    rest = STORIES[3:]
    col2_w = 484
    row_h = 21
    y0 = 508
    for idx, s in enumerate(rest):
        col = idx // 20
        row = idx % 20
        x = 20 + col * (col2_w + 16)
        y = y0 + row * row_h
        d.text((x, y), str(s["n"]) + ".", font=f_list_b, fill=RED)
        line = s["headline"] + "  —  " + s["source"]
        lines = wrap(d, line, f_list, col2_w - 26)
        d.text((x + 26, y), lines[0], font=f_list, fill=INK)

    # ---- map band + footer ----
    draw_map(d, 20, 936, 640, 66)
    d.text((676, 946), "SOURCES", font=f_list_h, fill=INK)
    d.text((676, 962),
           "HRW · ICJ · Xinhua · Reuters · IPS · Carbon Brief ·\n"
           "BBC · Al Jazeera · NEXA · Hamer Intel · KimKJ ·\n"
           "EGazette · Nexus Europa · Finwire · Serrari · NAB ·\n"
           "Fortune · CBS · APEC · BusinessTech Africa",
           font=f_foot, fill=GREY)
    d.line([20, 1010, W - 20, 1010], fill=LINE, width=1)
    d.text((W // 2, 1017), "THE WORLD IN ONE PAGE — THURSDAY 19 NOVEMBER 2026 — 43 STORIES",
           font=f_foot, fill=GREY, anchor="mm")

    img.save("entry.png", "PNG")
    print("saved entry.png")


if __name__ == "__main__":
    main()
