"""Generate close-up SVG of a single chart card + chat bubble."""
W, H = 860, 340
BG = "#060D1B"; SURFACE = "#0E1729"; BORDER = "#172236"
BLUE = "#3B82F6"; AMBER = "#F59E0B"; EMERALD = "#10B981"
VIOLET = "#A78BFA"; ROSE = "#F43F5E"; LIME = "#22C55E"
ORANGE = "#F97316"; RED = "#EF4444"
TEXT = "#F1F5F9"; MUTED = "#94A3B8"; SUBTLE = "#475569"

def build():
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(f'<defs>'
             f'<radialGradient id="g1" cx="20%" cy="70%" r="60%">'
             f'<stop offset="0%" stop-color="{BLUE}" stop-opacity="0.12"/>'
             f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/>'
             f'</radialGradient></defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#g1)"/>')

    # ── Card 1: Contraceptive Prevalence ─────────────────────────────────────
    cx, cy, cw, ch = 20, 20, 400, 300
    # card bg
    p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" '
             f'fill="{SURFACE}" stroke="{BORDER}" stroke-width="1.5"/>')
    # header strip
    p.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="50" rx="14" '
             f'fill="{BLUE}" fill-opacity="0.06"/>')
    p.append(f'<rect x="{cx}" y="{cy+36}" width="{cw}" height="14" fill="{BLUE}" fill-opacity="0.06"/>')
    # title
    p.append(f'<text x="{cx+14}" y="{cy+22}" fill="{TEXT}" font-size="13" font-weight="600" '
             f'font-family="sans-serif">Contraceptive Prevalence</text>')
    # badge
    badge_w = 106
    p.append(f'<rect x="{cx+14}" y="{cy+30}" width="{badge_w}" height="16" rx="8" '
             f'fill="{BLUE}" fill-opacity="0.12"/>')
    p.append(f'<text x="{cx+14+badge_w//2}" y="{cy+41}" fill="{BLUE}" font-size="9" font-weight="600" '
             f'text-anchor="middle" font-family="sans-serif">↑ Higher is better</text>')
    # Ask AI button
    p.append(f'<rect x="{cx+cw-84}" y="{cy+12}" width="70" height="24" rx="7" fill="{BLUE}"/>')
    p.append(f'<text x="{cx+cw-49}" y="{cy+28}" fill="{TEXT}" font-size="10" font-weight="600" '
             f'text-anchor="middle" font-family="sans-serif">Ask AI</text>')

    # Chart area
    chart_x, chart_y, chart_w, chart_h = cx+14, cy+58, cw-28, 170
    # grid
    for pct in [0.33, 0.67, 1.0]:
        gy = chart_y + chart_h - int(pct*chart_h)
        p.append(f'<line x1="{chart_x}" y1="{gy}" x2="{chart_x+chart_w}" y2="{gy}" '
                 f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="4,4"/>')
    # bars: RWA:64.2, KEN:61.4, ETH:40.3, TZA:38.2, UGA:35.8 (max=70)
    data = [("RWA",64.2,BLUE),("KEN",61.4,AMBER),("ETH",40.3,EMERALD),("TZA",38.2,VIOLET),("UGA",35.8,ROSE)]
    bar_w = 46; gap = 16
    total_bars = 5*bar_w + 4*gap  # 278
    bx_start = chart_x + (chart_w - total_bars)//2
    for i,(country,val,col) in enumerate(data):
        bh = int((val/70)*chart_h)
        bx = bx_start + i*(bar_w+gap)
        by = chart_y + chart_h - bh
        r = 5
        p.append(f'<path d="M{bx+r},{by} h{bar_w-2*r} q{r},0 {r},{r} v{bh-r} h-{bar_w} v-{bh-r} q0,-{r} {r},-{r}z" '
                 f'fill="{col}" fill-opacity="0.85"/>')
        # value label on top of bar
        p.append(f'<text x="{bx+bar_w//2}" y="{by-5}" fill="{col}" font-size="9" font-weight="600" '
                 f'text-anchor="middle" font-family="\'Fira Code\',monospace">{val}</text>')
        # country label
        p.append(f'<text x="{bx+bar_w//2}" y="{chart_y+chart_h+14}" fill="{SUBTLE}" font-size="10" '
                 f'text-anchor="middle" font-family="sans-serif">{country}</text>')
    # Y axis label
    p.append(f'<text x="{chart_x-4}" y="{chart_y+chart_h//2}" fill="{SUBTLE}" font-size="9" '
             f'text-anchor="middle" font-family="sans-serif" transform="rotate(-90 {chart_x-4} {chart_y+chart_h//2})">Prevalence (%)</text>')
    # toggle bar at bottom
    p.append(f'<rect x="{cx+14}" y="{cy+ch-32}" width="{cw-28}" height="22" rx="6" '
             f'fill="{BG}" fill-opacity="0.7" stroke="{BORDER}" stroke-width="1"/>')
    p.append(f'<text x="{cx+22}" y="{cy+ch-17}" fill="{SUBTLE}" font-size="9" font-family="sans-serif">Metric definition</text>')
    p.append(f'<text x="{cx+cw-22}" y="{cy+ch-17}" fill="{SUBTLE}" font-size="11" text-anchor="middle">∨</text>')

    # ── Card 2: Maternal Mortality (lower is better, selected) ────────────────
    cx2, cy2, cw2, ch2 = 440, 20, 400, 300
    LOWER_COLS = [EMERALD, LIME, AMBER, ORANGE, RED]
    p.append(f'<rect x="{cx2}" y="{cy2}" width="{cw2}" height="{ch2}" rx="14" '
             f'fill="{SURFACE}" stroke="{BLUE}" stroke-width="1.5" stroke-opacity="0.5"/>')
    p.append(f'<rect x="{cx2}" y="{cy2}" width="{cw2}" height="{ch2}" rx="14" '
             f'fill="{BLUE}" fill-opacity="0.04"/>')
    p.append(f'<text x="{cx2+14}" y="{cy2+22}" fill="{TEXT}" font-size="13" font-weight="600" '
             f'font-family="sans-serif">Maternal Mortality</text>')
    badge_w2 = 100
    p.append(f'<rect x="{cx2+14}" y="{cy2+30}" width="{badge_w2}" height="16" rx="8" '
             f'fill="{EMERALD}" fill-opacity="0.12"/>')
    p.append(f'<text x="{cx2+14+badge_w2//2}" y="{cy2+41}" fill="{EMERALD}" font-size="9" font-weight="600" '
             f'text-anchor="middle" font-family="sans-serif">↓ Lower is better</text>')
    p.append(f'<rect x="{cx2+cw2-84}" y="{cy2+12}" width="70" height="24" rx="7" fill="{BLUE}"/>')
    p.append(f'<text x="{cx2+cw2-49}" y="{cy2+28}" fill="{TEXT}" font-size="10" font-weight="600" '
             f'text-anchor="middle" font-family="sans-serif">Ask AI</text>')

    chart2_x, chart2_y = cx2+14, cy2+58
    for pct in [0.33, 0.67, 1.0]:
        gy = chart2_y + 170 - int(pct*170)
        p.append(f'<line x1="{chart2_x}" y1="{gy}" x2="{chart2_x+cw2-28}" y2="{gy}" '
                 f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="4,4"/>')
    # sorted ascending (best first): RWA:259,UGA:284,ETH:401,TZA:468,KEN:530  max=560
    data2 = [("RWA",259),("UGA",284),("ETH",401),("TZA",468),("KEN",530)]
    total_bars2 = 5*bar_w + 4*gap
    bx2_start = chart2_x + (cw2-28 - total_bars2)//2
    for i,((country,val),col) in enumerate(zip(data2, LOWER_COLS)):
        bh = int((val/560)*170)
        bx = bx2_start + i*(bar_w+gap)
        by = chart2_y + 170 - bh
        r = 5
        p.append(f'<path d="M{bx+r},{by} h{bar_w-2*r} q{r},0 {r},{r} v{bh-r} h-{bar_w} v-{bh-r} q0,-{r} {r},-{r}z" '
                 f'fill="{col}" fill-opacity="0.85"/>')
        p.append(f'<text x="{bx+bar_w//2}" y="{by-5}" fill="{col}" font-size="9" font-weight="600" '
                 f'text-anchor="middle" font-family="\'Fira Code\',monospace">{val}</text>')
        p.append(f'<text x="{bx+bar_w//2}" y="{chart2_y+184}" fill="{SUBTLE}" font-size="10" '
                 f'text-anchor="middle" font-family="sans-serif">{country}</text>')

    p.append(f'<rect x="{cx2+14}" y="{cy2+ch2-32}" width="{cw2-28}" height="22" rx="6" '
             f'fill="{BG}" fill-opacity="0.7" stroke="{BORDER}" stroke-width="1"/>')
    p.append(f'<text x="{cx2+22}" y="{cy2+ch2-17}" fill="{SUBTLE}" font-size="9" font-family="sans-serif">Metric definition</text>')
    p.append(f'<text x="{cx2+cw2-22}" y="{cy2+ch2-17}" fill="{SUBTLE}" font-size="11" text-anchor="middle">∨</text>')

    # selected glow
    p.append(f'<rect x="{cx2}" y="{cy2}" width="{cw2}" height="{ch2}" rx="14" '
             f'fill="none" stroke="{BLUE}" stroke-width="2" stroke-opacity="0.3"/>')

    p.append("</svg>")
    return "\n".join(p)

if __name__ == "__main__":
    import os; os.makedirs("docs", exist_ok=True)
    svg = build()
    with open("docs/card-closeup.svg", "w") as f:
        f.write(svg)
    print(f"Written docs/card-closeup.svg ({len(svg):,} bytes)")
