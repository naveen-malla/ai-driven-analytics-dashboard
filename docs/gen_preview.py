"""Generate SVG dashboard preview images for the README."""
import math, textwrap

W, H = 1280, 800
HDR = 60        # header height
SB  = 210       # sidebar width
CHAT = 350      # chat panel width
MAIN = W - SB - CHAT  # 720

CARD_W = (MAIN - 20*3) // 2  # ~340
CARD_H = 222
GAP    = 16
PAD    = 20

# ── colours ────────────────────────────────────────────────────────────────
BG      = "#060D1B"
SURFACE = "#0E1729"
BORDER  = "#172236"
BLUE    = "#3B82F6"
AMBER   = "#F59E0B"
EMERALD = "#10B981"
VIOLET  = "#A78BFA"
ROSE    = "#F43F5E"
LIME    = "#22C55E"
ORANGE  = "#F97316"
RED     = "#EF4444"
TEXT    = "#F1F5F9"
MUTED   = "#94A3B8"
SUBTLE  = "#475569"

NORMAL_COLORS = [BLUE, AMBER, EMERALD, VIOLET, ROSE]
LOWER_COLORS  = [EMERALD, LIME, AMBER, ORANGE, RED]

LOWER_IS_BETTER = {"maternal_mortality", "under5_mortality", "hiv_prevalence"}

# ── chart data ──────────────────────────────────────────────────────────────
charts = [
  {"id": "contraceptive_prevalence", "title": "Contraceptive Prevalence", "unit": "%",
   "data": [("RWA",64.2),("KEN",61.4),("ETH",40.3),("TZA",38.2),("UGA",35.8)], "max": 70},
  {"id": "maternal_mortality",        "title": "Maternal Mortality",        "unit": "/100k",
   "data": [("RWA",259),("UGA",284),("ETH",401),("TZA",468),("KEN",530)],  "max": 560},
  {"id": "antenatal_care",            "title": "Antenatal Care Coverage",   "unit": "%",
   "data": [("RWA",44.2),("KEN",55.3),("ETH",43.1),("TZA",25.7),("UGA",43.2)], "max": 60},
  {"id": "skilled_birth",             "title": "Skilled Birth Attendance",  "unit": "%",
   "data": [("RWA",90.7),("KEN",89.2),("ETH",50.5),("TZA",83.8),("UGA",74.3)], "max": 95},
  {"id": "under5_mortality",          "title": "Under-5 Mortality Rate",    "unit": "/1k",
   "data": [("RWA",35.3),("KEN",40.9),("UGA",44.8),("TZA",47.5),("ETH",48.7)], "max": 55},
  {"id": "hiv_prevalence",            "title": "HIV Prevalence",            "unit": "%",
   "data": [("ETH",0.9),("RWA",2.5),("KEN",4.3),("TZA",4.8),("UGA",5.1)],  "max": 6},
]

# ── helpers ─────────────────────────────────────────────────────────────────
def rect(x,y,w,h,fill=SURFACE,rx=12,stroke=BORDER,sw=1,opacity=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" ' \
           f'stroke="{stroke}" stroke-width="{sw}" fill-opacity="{opacity}"/>'

def text_(x,y,txt,fill=TEXT,size=12,weight=400,anchor="start",family="sans-serif"):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" ' \
           f'text-anchor="{anchor}" font-family="{family}">{txt}</text>'

def badge(x,y,label,color,bgopacity=0.12):
    bw = len(label)*6.5+12
    return (f'<rect x="{x}" y="{y-11}" width="{bw}" height="15" rx="7" fill="{color}" fill-opacity="{bgopacity}"/>'
            f'<text x="{x+bw/2}" y="{y}" fill="{color}" font-size="9" font-weight="600" '
            f'text-anchor="middle" font-family="sans-serif">{label}</text>')

def bar_chart(cx, cy, chart, chart_w=310, chart_h=122):
    lower = chart["id"] in LOWER_IS_BETTER
    colors = LOWER_COLORS if lower else NORMAL_COLORS
    data = chart["data"]
    n = len(data)
    max_v = chart["max"]
    bar_w = 38
    spacing = 12
    total_bars_w = n * bar_w + (n-1) * spacing
    start_x = cx + (chart_w - total_bars_w) // 2

    out = []
    # subtle grid lines
    for pct in [0.33, 0.67, 1.0]:
        gy = cy + chart_h - int(pct * chart_h)
        out.append(f'<line x1="{cx}" y1="{gy}" x2="{cx+chart_w}" y2="{gy}" '
                   f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="3,3"/>')

    for i,(country, val) in enumerate(data):
        bh = max(4, int((val / max_v) * chart_h))
        bx = start_x + i * (bar_w + spacing)
        by = cy + chart_h - bh
        col = colors[i % len(colors)]
        # bar with rounded top corners (use path)
        r = 4
        out.append(
            f'<path d="M{bx+r},{by} h{bar_w-2*r} q{r},0 {r},{r} v{bh-r} h-{bar_w} v-{bh-r} q0,-{r} {r},-{r}z" '
            f'fill="{col}" fill-opacity="0.85"/>'
        )
        # label
        out.append(f'<text x="{bx+bar_w//2}" y="{cy+chart_h+14}" fill="{SUBTLE}" '
                   f'font-size="9" text-anchor="middle" font-family="sans-serif">{country}</text>')
    return "\n".join(out)

def chart_card(x, y, chart, selected=False):
    lower = chart["id"] in LOWER_IS_BETTER
    accent = EMERALD if lower else BLUE
    badge_label = "↓ lower is better" if lower else "↑ higher is better"
    border_col = f"rgba(59,130,246,0.5)" if selected else BORDER

    out = [rect(x, y, CARD_W, CARD_H, rx=14, stroke="#2A3F5F" if selected else BORDER, sw=1.5 if selected else 1)]
    if selected:
        out.append(f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="14" '
                   f'fill="{BLUE}" fill-opacity="0.05"/>')
    # title
    out.append(text_(x+14, y+22, chart["title"], fill=TEXT, size=11, weight=600))
    # badge
    out.append(badge(x+14, y+38, badge_label, accent))
    # chart
    out.append(bar_chart(x+14, y+54, chart, CARD_W-28, 118))
    # definition toggle hint
    out.append(rect(x+14, y+CARD_H-28, CARD_W-28, 20, fill="#0A1220", rx=6, stroke=BORDER, sw=1))
    out.append(text_(x+22, y+CARD_H-14, "Metric definition", fill=SUBTLE, size=9))
    out.append(text_(x+CARD_W-26, y+CARD_H-14, "∨", fill=SUBTLE, size=10))
    # ask AI button
    btn_w, btn_h = 68, 20
    bx = x + CARD_W - 14 - btn_w
    by_ = y + 14
    out.append(rect(bx, by_, btn_w, btn_h, fill=BLUE, rx=6, stroke="none", sw=0))
    out.append(f'<rect x="{bx}" y="{by_}" width="{btn_w}" height="{btn_h}" rx="6" fill="{BLUE}" fill-opacity="0.9"/>')
    out.append(text_(bx+btn_w//2, by_+13, "Ask AI", fill=TEXT, size=9, weight=600, anchor="middle"))
    return "\n".join(out)

# ── build full SVG ───────────────────────────────────────────────────────────
def build_svg():
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
                 f'width="{W}" height="{H}">')

    # ── background
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    parts.append(f'<defs>'
                 f'<radialGradient id="g1" cx="15%" cy="65%" r="55%">'
                 f'<stop offset="0%" stop-color="#3B82F6" stop-opacity="0.12"/>'
                 f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/>'
                 f'</radialGradient>'
                 f'<radialGradient id="g2" cx="85%" cy="15%" r="50%">'
                 f'<stop offset="0%" stop-color="#A78BFA" stop-opacity="0.08"/>'
                 f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/>'
                 f'</radialGradient>'
                 f'</defs>')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#g1)"/>')
    parts.append(f'<rect width="{W}" height="{H}" fill="url(#g2)"/>')

    # ── header
    parts.append(f'<rect width="{W}" height="{HDR}" fill="{SURFACE}" fill-opacity="0.8" '
                 f'stroke="{BORDER}" stroke-width="1"/>')
    # logo icon bg
    parts.append(f'<rect x="16" y="16" width="28" height="28" rx="8" fill="{BLUE}" fill-opacity="0.2" '
                 f'stroke="{BLUE}" stroke-opacity="0.3" stroke-width="1"/>')
    # activity icon (simple lines)
    parts.append(f'<polyline points="22,30 26,24 30,32 34,28 38,30" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append(text_(54, 26, "HealthAnalytics", fill=TEXT, size=13, weight=600))
    parts.append(text_(54, 41, "AI COPILOT", fill=SUBTLE, size=8, weight=600))
    # separator
    parts.append(f'<line x1="180" y1="16" x2="180" y2="44" stroke="{BORDER}" stroke-width="1"/>')
    # status dots
    for i,(label,ok) in enumerate([("Backend",True),("Data",True),("AI",True)]):
        dx = 196 + i*80
        col = EMERALD if ok else RED
        parts.append(f'<circle cx="{dx}" cy="30" r="4" fill="{col}"/>')
        parts.append(f'<circle cx="{dx}" cy="30" r="4" fill="{col}" opacity="0.4">'
                     f'<animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0.4;0;0.4" dur="2s" repeatCount="indefinite"/>'
                     f'</circle>')
        parts.append(text_(dx+10, 34, label, fill=SUBTLE, size=10))
    # date
    parts.append(text_(W-200, 34, "Sat, Apr 18 2026", fill=SUBTLE, size=10, anchor="start"))
    # toggle icons (bars + chat)
    for ix, icon_x in enumerate([W-50, W-24]):
        bg_fill = f'{BLUE}" fill-opacity="0.15' if ix == 0 else SURFACE
        parts.append(f'<rect x="{icon_x-10}" y="18" width="24" height="24" rx="6" fill="{bg_fill}"/>')
    parts.append(text_(W-42, 34, "⊞", fill=BLUE, size=14, anchor="middle"))
    parts.append(text_(W-16, 34, "💬", fill=SUBTLE, size=12, anchor="middle"))

    # ── sidebar
    parts.append(f'<rect x="0" y="{HDR}" width="{SB}" height="{H-HDR}" fill="{SURFACE}" fill-opacity="0.6" '
                 f'stroke="{BORDER}" stroke-width="1"/>')
    parts.append(text_(16, HDR+22, "INDICATORS", fill=SUBTLE, size=8, weight=600))

    sidebar_items = [
        ("♀", "Contraceptive Prev.", False, False),
        ("♥", "Maternal Mortality", True, True),
        ("✚", "Antenatal Care", False, False),
        ("★", "Skilled Birth Att.", False, False),
        ("◆", "Under-5 Mortality", True, False),
        ("⬡", "HIV Prevalence", True, False),
    ]
    for i,(icon,label,lower,active) in enumerate(sidebar_items):
        iy = HDR + 36 + i*58
        if active:
            parts.append(f'<rect x="8" y="{iy}" width="{SB-16}" height="50" rx="8" '
                         f'fill="{BLUE}" fill-opacity="0.12" stroke="{BLUE}" stroke-opacity="0.25" stroke-width="1"/>')
        tcol = TEXT if active else MUTED
        parts.append(text_(22, iy+18, icon, fill=BLUE if active else SUBTLE, size=12))
        parts.append(text_(40, iy+18, label, fill=tcol, size=10, weight=600 if active else 400))
        bcol = EMERALD if lower else BLUE
        bl = "↓ lower" if lower else "↑ higher"
        parts.append(badge(40, iy+34, bl, bcol))

    # WHO badge at bottom of sidebar
    parts.append(f'<line x1="0" y1="{H-30}" x2="{SB}" y2="{H-30}" stroke="{BORDER}" stroke-width="1"/>')
    parts.append(text_(SB//2, H-12, "WHO GHO · 5 countries", fill=SUBTLE, size=8, anchor="middle"))

    # ── chart grid
    for i, chart in enumerate(charts):
        col = i % 2
        row = i // 2
        cx = SB + PAD + col*(CARD_W + GAP)
        cy = HDR + PAD + row*(CARD_H + GAP)
        parts.append(chart_card(cx, cy, chart, selected=(i==1)))

    # ── chat panel
    cx_ = W - CHAT
    parts.append(f'<rect x="{cx_}" y="{HDR}" width="{CHAT}" height="{H-HDR}" fill="{SURFACE}" fill-opacity="0.6" '
                 f'stroke="{BORDER}" stroke-width="1"/>')
    # chat header
    parts.append(f'<rect x="{cx_}" y="{HDR}" width="{CHAT}" height="46" fill="{BG}" fill-opacity="0.4" '
                 f'stroke="{BORDER}" stroke-width="1"/>')
    parts.append(f'<rect x="{cx_+12}" y="{HDR+10}" width="26" height="26" rx="8" fill="{VIOLET}" fill-opacity="0.15" '
                 f'stroke="{VIOLET}" stroke-opacity="0.25" stroke-width="1"/>')
    parts.append(text_(cx_+23, HDR+21, "✨", fill=VIOLET, size=11, anchor="middle"))
    parts.append(text_(cx_+46, HDR+24, "Health Copilot", fill=TEXT, size=11, weight=600))
    parts.append(text_(cx_+46, HDR+37, "Context: Maternal Mortality", fill=SUBTLE, size=9))

    # empty-state hint
    esy = HDR + 70
    parts.append(f'<rect x="{cx_+CHAT//2-30}" y="{esy}" width="60" height="60" rx="16" '
                 f'fill="{VIOLET}" fill-opacity="0.1" stroke="{VIOLET}" stroke-opacity="0.2" stroke-width="1"/>')
    parts.append(text_(cx_+CHAT//2, esy+36, "✨", fill=VIOLET, size=24, anchor="middle"))
    parts.append(text_(cx_+CHAT//2, esy+72, "Ask anything about health data", fill=TEXT, size=11, anchor="middle", weight=500))
    parts.append(text_(cx_+CHAT//2, esy+88, "WHO data across 5 East African countries", fill=SUBTLE, size=9, anchor="middle"))

    # suggestion pills
    suggestions = ["Compare maternal mortality across countries", "Which country has highest HIV?", "Show contraceptive trends"]
    for j,sg in enumerate(suggestions):
        sy_ = esy + 102 + j*32
        parts.append(f'<rect x="{cx_+12}" y="{sy_}" width="{CHAT-24}" height="24" rx="8" '
                     f'fill="{BG}" fill-opacity="0.8" stroke="{BORDER}" stroke-width="1"/>')
        parts.append(text_(cx_+20, sy_+15, sg, fill=SUBTLE, size=9))

    # chat messages (sample conversation)
    messages = [
        ("user",  "Compare maternal mortality rates"),
        ("ai",    "Rwanda has the lowest MMR at 259/100k, followed by Uganda (284). Kenya has the highest at 530/100k."),
    ]
    msg_y = esy + 200
    for role, content in messages:
        is_user = role == "user"
        bubble_x = cx_+12 if not is_user else cx_+60
        bubble_w = CHAT - 24 - 48 if not is_user else CHAT - 24 - 48
        bubble_fill = f"{BLUE}" if is_user else SURFACE
        fill_opacity = "0.2" if is_user else "1"
        avatar_x = cx_+CHAT-20 if is_user else cx_+18
        # avatar
        av_col = BLUE if is_user else VIOLET
        parts.append(f'<circle cx="{avatar_x}" cy="{msg_y+12}" r="11" fill="{av_col}" fill-opacity="0.15" '
                     f'stroke="{av_col}" stroke-opacity="0.3" stroke-width="1"/>')
        icon_t = "👤" if is_user else "🤖"
        parts.append(text_(avatar_x, msg_y+16, icon_t, fill=av_col, size=10, anchor="middle"))

        bx2 = cx_+40 if not is_user else cx_+12
        # wrap content
        lines = textwrap.wrap(content, 34)
        bh2 = 16 + len(lines)*14
        parts.append(f'<rect x="{bx2}" y="{msg_y}" width="{CHAT-60}" height="{bh2}" rx="10" '
                     f'fill="{bubble_fill}" fill-opacity="{fill_opacity}" stroke="{BORDER}" stroke-width="1"/>')
        for li,line in enumerate(lines):
            parts.append(text_(bx2+10, msg_y+13+li*14, line, fill=TEXT if is_user else MUTED, size=9))
        msg_y += bh2 + 12

    # chat input area
    input_y = H - 60
    parts.append(f'<line x1="{cx_}" y1="{input_y}" x2="{W}" y2="{input_y}" stroke="{BORDER}" stroke-width="1"/>')
    parts.append(f'<rect x="{cx_+12}" y="{input_y+8}" width="{CHAT-52}" height="34" rx="10" '
                 f'fill="{BG}" fill-opacity="0.8" stroke="{BORDER}" stroke-width="1"/>')
    parts.append(text_(cx_+22, input_y+28, "Ask about Maternal Mortality…", fill=SUBTLE, size=9))
    # send button
    parts.append(f'<rect x="{W-40}" y="{input_y+8}" width="34" height="34" rx="10" fill="{BLUE}"/>')
    parts.append(text_(W-23, input_y+29, "▶", fill=TEXT, size=11, anchor="middle"))

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    import os
    os.makedirs("docs", exist_ok=True)
    svg = build_svg()
    with open("docs/dashboard-preview.svg", "w") as f:
        f.write(svg)
    print(f"Written docs/dashboard-preview.svg ({len(svg):,} bytes)")
