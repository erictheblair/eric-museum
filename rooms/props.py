# Generates the room prop SVGs (rooms/prop-*.svg). Run: python3 props.py <outdir>
import sys, os, math, random
W = "xmlns='http://www.w3.org/2000/svg'"
ART = {}
def f(v): return f"{v:.1f}"
R = random.Random(7)
# Eric's Mummula wordmark, cream with a dark outline, embedded so it works inside a CSS background image.
def _wordmark():
    import base64, io
    from PIL import Image, ImageFilter
    src = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "mummula-wordmark.png")).convert("RGBA")
    m = src.resize((560, round(src.height * 560 / src.width)), Image.LANCZOS); pad = 10
    A = Image.new("L", (m.width + 2 * pad, m.height + 2 * pad), 0); A.paste(m.getchannel("A"), (pad, pad))
    out = Image.new("RGBA", A.size, (42, 11, 56, 0)); out.putalpha(A.filter(ImageFilter.MaxFilter(13)))
    fill = Image.new("RGBA", A.size, (255, 247, 194, 255)); fill.putalpha(A); out.alpha_composite(fill)
    buf = io.BytesIO(); out.save(buf, "WEBP", quality=90, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
WORDMARK = _wordmark()

# ======================= 50s DINER =======================
# Jukebox: wood cabinet, chrome trim, glowing colour-cycling arch tubes with rising bubbles, spinning record, notes floating up.
def bubbles(x, y0, y1, n, dur, seed):
    r = random.Random(seed); out = []
    for k in range(n):
        d = dur * r.uniform(.8, 1.3); b = -r.uniform(0, d)
        out.append(f"<circle cx='{f(x + r.uniform(-1.2, 1.2))}' r='{f(r.uniform(1.1, 2))}' fill='#fff' opacity='.85'>"
                   f"<animate attributeName='cy' values='{y0};{y1}' dur='{f(d)}s' begin='{f(b)}s' repeatCount='indefinite'/></circle>")
    return "".join(out)
cyc = lambda vals, dur, b=0: f"<animate attributeName='stop-color' values='{vals}' dur='{dur}s' begin='{b}s' repeatCount='indefinite'/>"
notes = "".join(
    f"<g opacity='0'><text x='{x}' y='0' font-size='{s}' fill='{c}' font-family='Arial,sans-serif'>{ch}</text>"
    f"<animateTransform attributeName='transform' type='translate' values='0 70;{dx} 4' dur='{d}s' begin='{b}s' repeatCount='indefinite'/>"
    f"<animate attributeName='opacity' values='0;1;1;0' keyTimes='0;.2;.7;1' dur='{d}s' begin='{b}s' repeatCount='indefinite'/></g>"
    for x, s, c, ch, dx, d, b in [(70, 22, '#ff4f7b', '♪', -14, 4.2, 0), (118, 18, '#3fd6d0', '♫', 16, 5.0, -1.6), (95, 16, '#ffd23f', '♪', 6, 4.6, -3.1)])
ART["jukebox"] = (f"<svg {W} viewBox='0 0 200 400'><defs>"
 "<linearGradient id='wd' x1='0' x2='1'><stop offset='0' stop-color='#4a1a08'/><stop offset='.25' stop-color='#a4481c'/><stop offset='.5' stop-color='#c8662a'/><stop offset='.75' stop-color='#a4481c'/><stop offset='1' stop-color='#3e1606'/></linearGradient>"
 "<linearGradient id='cr' x1='0' x2='1'><stop offset='0' stop-color='#6d7479'/><stop offset='.3' stop-color='#f6f8f9'/><stop offset='.55' stop-color='#9aa3a8'/><stop offset='.8' stop-color='#ffffff'/><stop offset='1' stop-color='#5f666b'/></linearGradient>"
 f"<linearGradient id='t1' x1='0' y1='1' x2='0' y2='0'><stop offset='0' stop-color='#ff2d55'>{cyc('#ff2d55;#ffb02e;#36e0c8;#b44dff;#ff2d55', 6)}</stop><stop offset='1' stop-color='#ffb02e'>{cyc('#ffb02e;#36e0c8;#b44dff;#ff2d55;#ffb02e', 6)}</stop></linearGradient>"
 f"<linearGradient id='t2' x1='0' y1='1' x2='0' y2='0'><stop offset='0' stop-color='#36e0c8'>{cyc('#36e0c8;#b44dff;#ff2d55;#ffb02e;#36e0c8', 6)}</stop><stop offset='1' stop-color='#b44dff'>{cyc('#b44dff;#ff2d55;#ffb02e;#36e0c8;#b44dff', 6)}</stop></linearGradient>"
 "<radialGradient id='gl' cx='.5' cy='.4' r='.6'><stop offset='0' stop-color='#ffe9b0'/><stop offset='1' stop-color='#ff9b3d'/></radialGradient>"
 "<radialGradient id='halo' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='#ffb46b' stop-opacity='.55'/><stop offset='1' stop-color='#ff7b3d' stop-opacity='0'/></radialGradient>"
 "<filter id='bl' x='-30%' y='-30%' width='160%' height='160%'><feGaussianBlur stdDeviation='3'/></filter>"
 "</defs>"
 "<ellipse cx='100' cy='160' rx='120' ry='130' fill='url(#halo)'/>"
 f"{notes}"
 # cabinet body with arched top
 "<path d='M22 396 V170 C22 108 56 76 100 76 C144 76 178 108 178 170 V396 Z' fill='url(#wd)'/>"
 "<path d='M22 396 V170 C22 108 56 76 100 76 C144 76 178 108 178 170 V396' fill='none' stroke='#2a0e04' stroke-width='2'/>"
 # glowing tubes (outer pair), blurred glow under them
 "<g filter='url(#bl)' opacity='.9'><path d='M30 380 V172 C30 116 62 86 100 86 C138 86 170 116 170 172 V380' fill='none' stroke='url(#t1)' stroke-width='12'/></g>"
 "<path d='M30 380 V172 C30 116 62 86 100 86 C138 86 170 116 170 172 V380' fill='none' stroke='url(#t1)' stroke-width='8'/>"
 "<path d='M30 380 V172 C30 116 62 86 100 86 C138 86 170 116 170 172 V380' fill='none' stroke='#fff' stroke-opacity='.45' stroke-width='2'/>"
 + bubbles(30, 378, 180, 7, 3.4, 1) + bubbles(170, 378, 180, 7, 3.4, 2) +
 # inner chrome arch + record window
 "<path d='M44 250 V172 C44 128 70 102 100 102 C130 102 156 128 156 172 V250 Z' fill='url(#cr)'/>"
 "<path d='M50 246 V174 C50 134 73 110 100 110 C127 110 150 134 150 174 V246 Z' fill='#22120a'/>"
 "<path d='M50 246 V174 C50 134 73 110 100 110 C127 110 150 134 150 174 V246 Z' fill='url(#gl)' opacity='.22'/>"
 # stacked records + spinning record
 "<g fill='#0d0d0d' stroke='#3a3a3a' stroke-width='.6'>" + "".join(f"<ellipse cx='100' cy='{186 + k*5}' rx='38' ry='6'/>" for k in range(6)) + "</g>"
 "<g transform='translate(100 160)'><circle r='30' fill='#111'/><circle r='26' fill='none' stroke='#2b2b2b' stroke-width='1'/><circle r='21' fill='none' stroke='#2b2b2b' stroke-width='1'/><circle r='16' fill='none' stroke='#2b2b2b'/>"
 "<circle r='10' fill='#e23b3b'/><circle r='1.6' fill='#ddd'/>"
 "<path d='M0 0 L28 -10 A30 30 0 0 1 30 2 Z' fill='#fff' opacity='.12'><animateTransform attributeName='transform' type='rotate' from='0' to='360' dur='1.8s' repeatCount='indefinite'/></path>"
 "<path d='M-6 -6 h4' stroke='#fff' stroke-width='2' opacity='.6'><animateTransform attributeName='transform' type='rotate' from='0' to='360' dur='1.8s' repeatCount='indefinite'/></path></g>"
 # tone arm
 "<path d='M144 128 L120 150' stroke='url(#cr)' stroke-width='3' stroke-linecap='round'/><circle cx='144' cy='128' r='4' fill='url(#cr)'/>"
 # glass glare
 "<path d='M58 176 C58 140 76 120 96 116 C80 128 70 146 68 176 Z' fill='#fff' opacity='.14'/>"
 # selector strip with title cards
 "<rect x='40' y='252' width='120' height='34' rx='4' fill='url(#cr)'/><rect x='45' y='256' width='110' height='26' rx='2' fill='#fff8e6'/>"
 + "".join(f"<rect x='{48 + (k%5)*21.4}' y='{258 + (k//5)*12}' width='18' height='9' fill='#fffdf4' stroke='#d33' stroke-width='.6'/><path d='M{50 + (k%5)*21.4} {262 + (k//5)*12} h13 M{50 + (k%5)*21.4} {265 + (k//5)*12} h9' stroke='#555' stroke-width='.7'/>" for k in range(10)) +
 # buttons
 "".join(f"<rect x='{46 + k*14}' y='290' width='10' height='7' rx='2' fill='{c}'/>" for k, c in enumerate(['#e33', '#f5f5f5', '#e33', '#f5f5f5', '#e33', '#f5f5f5', '#e33', '#f5f5f5'])) +
 # speaker grille with sunburst
 "<rect x='40' y='304' width='120' height='70' rx='8' fill='url(#cr)'/><rect x='46' y='309' width='108' height='60' rx='6' fill='#3b1d0e'/>"
 "<clipPath id='gc'><rect x='46' y='309' width='108' height='60' rx='6'/></clipPath><g stroke='url(#cr)' stroke-width='2.4' clip-path='url(#gc)'>" + "".join(f"<path d='M100 372 L{f(100 + 70*math.cos(math.radians(a)))} {f(372 - 70*math.sin(math.radians(a)))}'/>" for a in range(15, 170, 15)) + "</g>"
 "<rect x='46' y='309' width='108' height='60' rx='6' fill='none' stroke='#2a0e04' stroke-width='2'/>"
 "<circle cx='100' cy='372' r='14' fill='url(#cr)'/><circle cx='100' cy='372' r='8' fill='#c83232'/>"
 # base
 "<rect x='16' y='378' width='168' height='18' rx='3' fill='url(#cr)'/><rect x='16' y='392' width='168' height='6' fill='#222'/>"
 "</svg>")

# Neon "MALTS" sign: pink script, teal underline, letters flicker now and then.
def neon_text(txt, x, y, size, col, flick_at=None):
    fl = ""
    if flick_at is not None:
        fl = f"<animate attributeName='opacity' values='1;1;.15;1;.3;1;1' keyTimes='0;{flick_at};{flick_at+.01};{flick_at+.02};{flick_at+.035};{flick_at+.045};1' dur='7s' repeatCount='indefinite'/>"
    t = f"x='{x}' y='{y}' font-size='{size}' font-family=\"'Brush Script MT','Segoe Script','Snell Roundhand',cursive\" font-style='italic' font-weight='700' text-anchor='middle'"
    return (f"<g>{fl}<text {t} fill='none' stroke='{col}' stroke-width='9' opacity='.35' filter='url(#nb)'>{txt}</text>"
            f"<text {t} fill='none' stroke='{col}' stroke-width='3.4'>{txt}</text><text {t} fill='none' stroke='#fff' stroke-width='1.1' opacity='.85'>{txt}</text></g>")
ART["malts"] = (f"<svg {W} viewBox='0 0 260 150'><defs><filter id='nb' x='-20%' y='-40%' width='140%' height='180%'><feGaussianBlur stdDeviation='5'/></filter></defs>"
 "<rect x='14' y='14' width='232' height='122' rx='18' fill='#121a1c' opacity='.75'/><rect x='14' y='14' width='232' height='122' rx='18' fill='none' stroke='#3a4a4e' stroke-width='3'/>"
 + neon_text("Malts", 130, 78, 62, '#ff4f9a', .62) +
 "<g><animate attributeName='opacity' values='1;1;.2;1' keyTimes='0;.3;.31;.33' dur='9s' repeatCount='indefinite'/>"
 "<path d='M48 96 H212' stroke='#3fe0e6' stroke-width='9' opacity='.3' filter='url(#nb)'/><path d='M48 96 H212' stroke='#3fe0e6' stroke-width='3.4' stroke-linecap='round'/><path d='M48 96 H212' stroke='#fff' stroke-width='1' opacity='.8'/>"
 "<text x='130' y='122' font-size='17' font-family='Arial Black,Arial,sans-serif' font-weight='900' text-anchor='middle' letter-spacing='4' fill='none' stroke='#3fe0e6' stroke-width='1.6'>&amp; SHAKES</text></g>"
 "<circle cx='26' cy='26' r='3' fill='#556'/><circle cx='234' cy='26' r='3' fill='#556'/><circle cx='26' cy='124' r='3' fill='#556'/><circle cx='234' cy='124' r='3' fill='#556'/>"
 "</svg>")

# ======================= NEON ARCADE =======================
def mummy(x, y, s=1, col='#efe6cf'):
    # tiny pixel mummy (8x10 grid)
    px = ["..XXXX..", ".XXXXXX.", ".XR..RX.", ".XXXXXX.", "..XXXX..", "XXXXXXXX", "X.XXXX.X", "..XXXX..", "..X..X..", ".XX..XX."]
    out = []
    for r, row in enumerate(px):
        for c, ch in enumerate(row):
            if ch == 'X': out.append(f"<rect x='{x + c*s}' y='{y + r*s}' width='{s}' height='{s}' fill='{col}'/>")
            if ch == 'R': out.append(f"<rect x='{x + c*s}' y='{y + r*s}' width='{s}' height='{s}' fill='#ff3b3b'/>")
    stripes = "".join(f"<rect x='{x + s}' y='{y + r*s + s*.45}' width='{6*s}' height='{s*.18}' fill='#b9ae94'/>" for r in (1, 3, 5, 7))
    return "".join(out) + stripes
def ufo(cx, cy, col):
    return (f"<g transform='translate({cx} {cy})'><ellipse rx='9' ry='3' fill='{col}'/><ellipse cy='-2.5' rx='4.5' ry='3.2' fill='#9ff'/>"
            "<rect x='-6' y='1' width='2' height='2' fill='#ff0'/><rect x='-1' y='1' width='2' height='2' fill='#ff0'/><rect x='4' y='1' width='2' height='2' fill='#ff0'/></g>")
def cabinet(key, title1, title2, c1, c2, screen):
    return (f"<svg {W} viewBox='0 0 180 380'><defs>"
     f"<linearGradient id='sd' x1='0' x2='1'><stop offset='0' stop-color='#120624'/><stop offset='.5' stop-color='#24104a'/><stop offset='1' stop-color='#0c0418'/></linearGradient>"
     f"<linearGradient id='mq' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='{c1}'/><stop offset='1' stop-color='{c2}'/></linearGradient>"
     "<filter id='g' x='-30%' y='-30%' width='160%' height='160%'><feGaussianBlur stdDeviation='4'/></filter>"
     "<radialGradient id='scr' cx='.5' cy='.5' r='.7'><stop offset='.6' stop-color='#000' stop-opacity='0'/><stop offset='1' stop-color='#000' stop-opacity='.55'/></radialGradient>"
     "<pattern id='sl' width='4' height='3' patternUnits='userSpaceOnUse'><rect width='4' height='1' fill='#000' opacity='.28'/></pattern>"
     "<clipPath id='sc'><rect x='30' y='86' width='120' height='100' rx='8'/></clipPath></defs>"
     # glow on the floor/wall
     f"<ellipse cx='90' cy='150' rx='92' ry='120' fill='{c1}' opacity='.22' filter='url(#g)'/>"
     # cabinet silhouette (front view with angled sides)
     "<path d='M14 30 L166 30 L166 200 L178 262 L178 376 L2 376 L2 262 L14 200 Z' fill='url(#sd)'/>"
     f"<path d='M14 30 L166 30 L166 200 L178 262 L178 376 L2 376 L2 262 L14 200 Z' fill='none' stroke='{c1}' stroke-width='2.5'/>"
     f"<path d='M14 30 L166 30 L166 200 L178 262 L178 376 L2 376 L2 262 L14 200 Z' fill='none' stroke='{c1}' stroke-width='7' opacity='.35' filter='url(#g)'/>"
     # marquee
     "<rect x='10' y='8' width='160' height='58' rx='6' fill='#0b0414'/>"
     "<rect x='14' y='12' width='152' height='50' rx='4' fill='url(#mq)'/>"
     "<rect x='14' y='12' width='152' height='50' rx='4' fill='#fff' opacity='.08'><animate attributeName='opacity' values='.04;.16;.04' dur='2.4s' repeatCount='indefinite'/></rect>"
     f"<image x='25' y='12' width='130' height='32' href='{WORDMARK}'/>"  # Eric's wordmark, outlined (rooms/src/mummula-wordmark.png)
     f"<text x='90' y='54' text-anchor='middle' font-family=\"'Arial Black',Arial,sans-serif\" font-weight='900' font-size='{11 if len(title2) < 16 else 9.4}' fill='#fff' stroke='#2a0b38' stroke-width='2.4' paint-order='stroke'>{title1} {title2}</text>"
     # bezel + screen
     "<rect x='22' y='78' width='136' height='116' rx='10' fill='#05020a'/>"
     f"<g clip-path='url(#sc)'>{screen}<rect x='30' y='86' width='120' height='100' fill='url(#sl)'/><rect x='30' y='86' width='120' height='100' fill='url(#scr)'/>"
     "<rect x='30' y='86' width='120' height='100' fill='#fff' opacity='0'><animate attributeName='opacity' values='0;.05;0' dur='.12s' repeatCount='indefinite'/></rect></g>"
     "<path d='M34 92 C60 88 90 88 112 90 L40 140 Z' fill='#fff' opacity='.07'/>"
     # control panel
     "<path d='M14 200 L166 200 L178 262 L2 262 Z' fill='#1a0b30'/>"
     f"<path d='M14 200 L166 200 L178 262 L2 262 Z' fill='none' stroke='{c2}' stroke-width='1.5'/>"
     "<ellipse cx='52' cy='236' rx='13' ry='5' fill='#000' opacity='.5'/><path d='M52 236 L49 214' stroke='#ccc' stroke-width='3.4' stroke-linecap='round'>"
     "<animateTransform attributeName='transform' type='rotate' values='0 52 236;-12 52 236;8 52 236;0 52 236;14 52 236;0 52 236' dur='3.2s' repeatCount='indefinite'/></path>"
     "<circle cx='49' cy='212' r='7' fill='#ff2f3d'><animateTransform attributeName='transform' type='rotate' values='0 52 236;-12 52 236;8 52 236;0 52 236;14 52 236;0 52 236' dur='3.2s' repeatCount='indefinite'/></circle>"
     + "".join(f"<ellipse cx='{x}' cy='{y}' rx='7.5' ry='5.5' fill='{c}'/><ellipse cx='{x}' cy='{y-1.5}' rx='5' ry='3' fill='#fff' opacity='.35'/>" for x, y, c in [(104, 228, '#ffe04a'), (124, 224, '#3cf0ff'), (144, 228, '#ff4fd8'), (114, 244, '#7dff5a'), (134, 244, '#ff8a2e')]) +
     # coin door
     "<rect x='58' y='290' width='64' height='70' rx='4' fill='#0e0618' stroke='#3c2a55' stroke-width='2'/>"
     + "".join(f"<rect x='{x}' y='302' width='14' height='22' rx='2' fill='#1c0d0d'/><rect x='{x+5.5}' y='306' width='3' height='12' fill='#ff3030'><animate attributeName='opacity' values='1;.35;1' dur='1.6s' begin='{b}s' repeatCount='indefinite'/></rect>" for x, b in [(68, 0), (98, -.8)]) +
     "<text x='90' y='344' text-anchor='middle' font-family='Arial,sans-serif' font-weight='700' font-size='10' fill='#ffcf3a'>25¢</text>"
     # neon side stripes
     f"<path d='M8 274 V370' stroke='{c2}' stroke-width='3'/><path d='M172 274 V370' stroke='{c2}' stroke-width='3'/>"
     f"<path d='M8 274 V370 M172 274 V370' stroke='{c2}' stroke-width='9' opacity='.35' filter='url(#g)'/>"
     "</svg>")
# Screen 1: Moon Men — saucers drift, the mummy slides along the ground firing up.
stars = "".join(f"<rect x='{R.randint(31, 148)}' y='{R.randint(87, 160)}' width='1.2' height='1.2' fill='#fff' opacity='{R.choice([.4, .7, 1])}'/>" for _ in range(40))
scr1 = ("<rect x='30' y='86' width='120' height='100' fill='#06031a'/>" + stars +
 "<circle cx='128' cy='104' r='11' fill='#e8e4c8'/><circle cx='124' cy='101' r='2.5' fill='#c8c2a0'/><circle cx='131' cy='108' r='1.8' fill='#c8c2a0'/>"
 "<rect x='30' y='176' width='120' height='10' fill='#3a3a52'/><rect x='30' y='176' width='120' height='2' fill='#7b7ba3'/>"
 "<g><animateTransform attributeName='transform' type='translate' values='0 0;30 6;60 0;30 -4;0 0' dur='5s' repeatCount='indefinite'/>"
 + ufo(48, 112, '#7dff5a') + ufo(72, 120, '#ff4fd8') + ufo(96, 112, '#3cf0ff') + "</g>"
 "<g><animateTransform attributeName='transform' type='translate' values='0 0;70 0;20 0;0 0' dur='6s' repeatCount='indefinite'/>"
 + mummy(40, 160, 1.6) +
 "<rect x='46' y='150' width='1.6' height='6' fill='#ffef5a'><animate attributeName='y' values='156;92' dur='.9s' repeatCount='indefinite'/></rect></g>"
 ""
 "<text x='112' y='95' font-family='Courier New,monospace' font-weight='700' font-size='7' fill='#7dff5a'>♥♥♥</text>")
# Screen 2: Monster Island — volcano puffs, a giant lizard rises from the sea and roars, mummy on the beach, INSERT COIN blinks.
scr2 = ("<rect x='30' y='86' width='120' height='100' fill='#ff7a3a'/><rect x='30' y='86' width='120' height='50' fill='#4a1458'/><rect x='30' y='120' width='120' height='30' fill='#c8366a' opacity='.6'/>"
 "<circle cx='60' cy='128' r='14' fill='#ffd04a'/>"
 "<rect x='30' y='150' width='120' height='36' fill='#1b4f8a'/>" + "".join(f"<rect x='{x}' y='{y}' width='8' height='1.4' fill='#7cc4ff'/>" for x, y in [(40, 158), (70, 166), (110, 156), (126, 170), (52, 176)]) +
 "<path d='M30 150 L58 112 L66 118 L74 108 L104 150 Z' fill='#2a1a2e'/><path d='M66 118 L70 112 L74 116 Z' fill='#ff4a1a'/>"
 "<g fill='#666' opacity='.85'><circle cx='70' cy='104' r='4'><animate attributeName='cy' values='108;88' dur='2.2s' repeatCount='indefinite'/><animate attributeName='r' values='2;6' dur='2.2s' repeatCount='indefinite'/><animate attributeName='opacity' values='1;0' dur='2.2s' repeatCount='indefinite'/></circle></g>"
 # kaiju rises and sinks
 "<g><animateTransform attributeName='transform' type='translate' values='0 34;0 0;0 0;0 34' keyTimes='0;.3;.8;1' dur='7s' repeatCount='indefinite'/>"
 "<path d='M112 152 C110 130 114 116 124 110 C132 106 142 110 144 120 L146 128 L138 128 L136 134 L140 152 Z' fill='#2f8f4a'/>"
 "<path d='M114 132 l-4 -4 l5 0 l-3 -6 l6 2 l-1 -6 l6 4' fill='#7dff5a'/>"
 "<rect x='133' y='116' width='4' height='3' fill='#ffef3a'><animate attributeName='height' values='3;3;.5;3' keyTimes='0;.9;.95;1' dur='2s' repeatCount='indefinite'/></rect>"
 "<path d='M138 128 L146 128 L146 131 L140 131 Z' fill='#fff'/></g>"
 "<rect x='30' y='150' width='120' height='3' fill='#7cc4ff' opacity='.6'/>"
 "<path d='M30 178 C60 172 90 176 110 186 L30 186 Z' fill='#e8c878'/>"
 + mummy(48, 162, 1.5) +
 "<text x='90' y='112' text-anchor='middle' font-family='Courier New,monospace' font-weight='700' font-size='8' fill='#fff'>INSERT COIN<animate attributeName='opacity' values='1;1;0;0' keyTimes='0;.5;.5;1' dur='1.2s' repeatCount='indefinite'/></text>")
ART["arcade1"] = cabinet("1", "vs.", "THE MOON MEN", "#ff3cc8", "#2ee6ff", scr1)
ART["arcade2"] = cabinet("2", "vs.", "MONSTER ISLAND", "#3cff7a", "#ffcf3a", scr2)

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for k, v in ART.items():
        open(f"{out}/prop-{k}.svg", "w").write(v); print(k, len(v))
