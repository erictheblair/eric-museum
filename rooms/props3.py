# Props for the haunted mansion, aquarium, starship and Christmas rooms.
# Run: python3 props3.py <outdir>   (writes only the props defined here)
import sys, os, math, random
W = "xmlns='http://www.w3.org/2000/svg'"
def f(v): return f"{v:.1f}"
ART = {}
SPL = "calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1'"

def candle_flame(x, y, dur=1.2, sk=6):
    # Flame drawn with its base at the wick (0,0); every transform pivots there, so it never leaves the wick.
    return (f"<g transform='translate({f(x)} {f(y)})'><ellipse cy='-7' rx='9' ry='12' fill='#ffcf5a' opacity='.22'><animate attributeName='opacity' values='.22;.32;.18;.22' dur='{dur*1.4:.2f}s' repeatCount='indefinite'/></ellipse>"
            f"<path d='M0 0 C-3.6 -3 -2.6 -9 0 -15 C2.6 -9 3.6 -3 0 0Z' fill='#ffcf5a'><animateTransform attributeName='transform' type='skewX' values='0;{sk};{-sk*.7:.1f};0' dur='{dur}s' repeatCount='indefinite'/>"
            f"<animateTransform attributeName='transform' type='scale' additive='sum' values='1 1;.92 1.12;1.05 .9;1 1' dur='{dur*.7:.2f}s' repeatCount='indefinite'/></path>"
            "<path d='M0 -1 C-1.4 -3 -1 -6 0 -8 C1 -6 1.4 -3 0 -1Z' fill='#fff6d0'/></g>")

def candle(x, base, h, w=10, col='#e9e1cc', dur=1.2, sk=6):
    top = base - h
    return (f"<rect x='{f(x-w/2)}' y='{f(top)}' width='{w}' height='{h}' fill='{col}'/><rect x='{f(x-w/2)}' y='{f(top)}' width='{f(w*.3)}' height='{h}' fill='#fff' opacity='.25'/>"
            f"<path d='M{f(x-w/2)} {f(top+1)} c2 4 3 9 1 14' stroke='{col}' stroke-width='2.4' fill='none'/>"
            f"<path d='M{f(x)} {f(top)} V{f(top-3)}' stroke='#2a1a10' stroke-width='1.2'/>" + candle_flame(x, top - 2, dur, sk))

def rise(x, y0, y1, n, dur, seed, r0=1.4, r1=3.2, col='#e8fbff', sway=6):
    r = random.Random(seed); out = []
    for k in range(n):
        d = dur * r.uniform(.8, 1.3); b = -r.uniform(0, d); xx = x + r.uniform(-3, 3); rr = r.uniform(r0, r1)
        out.append(f"<circle r='{f(rr)}' fill='none' stroke='{col}' stroke-width='1' opacity='.9'>"
                   f"<animate attributeName='cy' values='{y0};{y1}' dur='{f(d)}s' begin='{f(b)}s' repeatCount='indefinite'/>"
                   f"<animate attributeName='cx' values='{f(xx)};{f(xx+sway)};{f(xx-sway*.6)};{f(xx+sway*.3)}' dur='{f(d)}s' begin='{f(b)}s' repeatCount='indefinite'/>"
                   f"<animate attributeName='opacity' values='0;.9;.9;0' keyTimes='0;.1;.85;1' dur='{f(d)}s' begin='{f(b)}s' repeatCount='indefinite'/></circle>")
    return "".join(out)

# ======================= HAUNTED MANSION =======================
mahog = ("<linearGradient id='wd' x1='0' x2='1'><stop offset='0' stop-color='#1a0b06'/><stop offset='.35' stop-color='#4a2414'/><stop offset='.55' stop-color='#5e301b'/><stop offset='1' stop-color='#160905'/></linearGradient>"
         "<linearGradient id='wd2' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3e1e10'/><stop offset='1' stop-color='#1c0d07'/></linearGradient>"
         "<radialGradient id='br' cx='.35' cy='.3' r='.75'><stop offset='0' stop-color='#fff2b8'/><stop offset='.35' stop-color='#d6a640'/><stop offset='1' stop-color='#5c3e10'/></radialGradient>"
         "<linearGradient id='brl' x1='0' x2='1'><stop offset='0' stop-color='#6a4812'/><stop offset='.5' stop-color='#e8c766'/><stop offset='1' stop-color='#5a3c0e'/></linearGradient>")
def web(x, y, s, fx=1, fy=1):
    # a corner cobweb, anchored at (x,y); fx/fy flip which corner it fills
    A = (0, 22, 45, 68, 90)
    g = f"<g transform='translate({x} {y}) scale({fx * s} {fy * s})' stroke='#d8d8e0' stroke-opacity='.5' stroke-width='.8' fill='none'>"
    for a in A: g += f"<path d='M0 0 L{f(40*math.cos(math.radians(a)))} {f(40*math.sin(math.radians(a)))}'/>"
    for r in (10, 19, 28, 37):
        p = [(r*math.cos(math.radians(a)), r*math.sin(math.radians(a))) for a in A]
        d = f"M{f(p[0][0])} {f(p[0][1])}"
        for i in range(1, len(p)):
            mx, my = (p[i][0] + p[i-1][0]) / 2 * .86, (p[i][1] + p[i-1][1]) / 2 * .86
            d += f" Q{f(mx)} {f(my)} {f(p[i][0])} {f(p[i][1])}"
        g += f"<path d='{d}'/>"
    return g + "</g>"

numerals = "".join(f"<path d='M{f(100 + 33*math.sin(math.radians(a)))} {f(112 - 33*math.cos(math.radians(a)))} L{f(100 + 28*math.sin(math.radians(a)))} {f(112 - 28*math.cos(math.radians(a)))}' stroke='#2a1a10' stroke-width='{2.6 if a % 90 == 0 else 1.4}'/>" for a in range(0, 360, 30))
ART["clock"] = (f"<svg {W} viewBox='0 0 200 440'><defs>{mahog}"
 "<radialGradient id='dl' cx='.45' cy='.4' r='.7'><stop offset='0' stop-color='#efe3c2'/><stop offset='.8' stop-color='#cdb98a'/><stop offset='1' stop-color='#8a7448'/></radialGradient>"
 "<linearGradient id='gl' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#0b0708'/><stop offset='1' stop-color='#1d1418'/></linearGradient>"
 "<clipPath id='door'><path d='M74 352 V214 C74 200 86 192 100 192 C114 192 126 200 126 214 V352 Z'/></clipPath>"
 "<clipPath id='face'><circle cx='100' cy='112' r='37'/></clipPath></defs>"
 "<ellipse cx='100' cy='436' rx='74' ry='5' fill='#000' opacity='.5'/>"
 # base, feet
 "<path d='M50 434 L54 424 H146 L150 434 Z' fill='#120704'/><rect x='46' y='378' width='108' height='48' rx='2' fill='url(#wd)'/>"
 "<rect x='58' y='388' width='84' height='28' rx='2' fill='none' stroke='#120704' stroke-width='2'/><rect x='42' y='372' width='116' height='8' rx='2' fill='url(#wd2)'/>"
 # trunk with glass door
 "<rect x='58' y='176' width='84' height='198' fill='url(#wd)'/><rect x='54' y='170' width='92' height='8' fill='url(#wd2)'/>"
 "<path d='M70 356 V214 C70 196 84 188 100 188 C116 188 130 196 130 214 V356 Z' fill='#2a140b' stroke='#140805' stroke-width='2'/>"
 "<path d='M74 352 V214 C74 200 86 192 100 192 C114 192 126 200 126 214 V352 Z' fill='url(#gl)'/>"
 "<g clip-path='url(#door)'>"
 # weights on chains
 "<path d='M84 192 V262 M116 192 V292' stroke='#8a7040' stroke-width='1.2' stroke-dasharray='2 1.5'/>"
 "<rect x='79' y='262' width='10' height='34' rx='2' fill='url(#brl)'/><rect x='111' y='292' width='10' height='34' rx='2' fill='url(#brl)'/>"
 # pendulum, pivoting at the top of the case
 f"<g><animateTransform attributeName='transform' type='rotate' values='-11 100 190;11 100 190;-11 100 190' dur='2.4s' repeatCount='indefinite' {SPL}/>"
 "<path d='M100 190 V312' stroke='url(#brl)' stroke-width='3'/><circle cx='100' cy='322' r='15' fill='url(#br)' stroke='#4a3008' stroke-width='1.5'/>"
 "<circle cx='100' cy='322' r='6' fill='none' stroke='#5a3c0e' stroke-width='1' opacity='.6'/></g>"
 # glass reflection, kept inside the door
 "<path d='M76 340 L112 196 L122 196 L86 340 Z' fill='#fff' opacity='.06'/><path d='M92 350 L124 230 L126 236 L96 350 Z' fill='#fff' opacity='.04'/>"
 "</g>"
 # hood
 "<rect x='44' y='56' width='112' height='114' fill='url(#wd)'/><rect x='40' y='150' width='120' height='14' fill='url(#wd2)'/>"
 "<rect x='48' y='60' width='8' height='92' fill='#1a0b06'/><rect x='144' y='60' width='8' height='92' fill='#1a0b06'/>"
 "<path d='M36 58 H164 L158 46 H42 Z' fill='url(#wd2)'/>"
 # swan-neck crown + finial
 "<path d='M44 48 C44 20 80 26 92 30 L92 46 Z M156 48 C156 20 120 26 108 30 L108 46 Z' fill='#2e160b' stroke='#140805' stroke-width='1.5'/>"
 "<circle cx='52' cy='30' r='5' fill='url(#brl)'/><circle cx='148' cy='30' r='5' fill='url(#brl)'/>"
 "<path d='M96 46 V24 H104 V46 Z' fill='#2e160b'/><path d='M100 4 C106 12 106 18 100 24 C94 18 94 12 100 4 Z' fill='url(#brl)'/>"
 # dial with a moon window that slowly turns
 "<circle cx='100' cy='112' r='42' fill='url(#brl)'/><circle cx='100' cy='112' r='38' fill='url(#dl)'/>"
 "<g clip-path='url(#face)'><g opacity='.9'><path d='M66 92 A36 36 0 0 1 134 92 Z' fill='#1b2450'/>"
 "<g><animateTransform attributeName='transform' type='rotate' values='-40 100 112;40 100 112;-40 100 112' dur='40s' repeatCount='indefinite'/>"
 "<circle cx='100' cy='78' r='8' fill='#f4ecd0'/><circle cx='97' cy='76' r='1.6' fill='#c9bd98'/><circle cx='103' cy='81' r='1.2' fill='#c9bd98'/></g>"
 "<circle cx='76' cy='86' r='1' fill='#fff'/><circle cx='124' cy='84' r='1' fill='#fff'/><circle cx='112' cy='90' r='.8' fill='#fff'/></g>"
 "<path d='M66 92 H134' stroke='#8a7448' stroke-width='1'/></g>"
 + numerals +
 # hands: the hour hand creeps forward, the minute hand runs backwards
 "<g><animateTransform attributeName='transform' type='rotate' values='0 100 112;360 100 112' dur='240s' repeatCount='indefinite'/><path d='M100 114 L97 112 L100 92 L103 112 Z' fill='#1a1010'/></g>"
 "<g><animateTransform attributeName='transform' type='rotate' values='360 100 112;0 100 112' dur='24s' repeatCount='indefinite'/><path d='M100 116 L98.4 112 L100 80 L101.6 112 Z' fill='#1a1010'/></g>"
 "<circle cx='100' cy='112' r='2.6' fill='url(#brl)'/>"
 # cobwebs and dust
 + web(44, 56, .9) + web(142, 374, .6, -1, -1) +
 "<path d='M58 176 H142' stroke='#bbb' stroke-opacity='.12' stroke-width='3'/>"
 "</svg>")

ART["seance"] = (f"<svg {W} viewBox='0 0 220 300'><defs>{mahog}"
 "<radialGradient id='orb' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='#d8f6ff'/><stop offset='.45' stop-color='#7fb6e0'/><stop offset='.8' stop-color='#3a3f8e'/><stop offset='1' stop-color='#1a1640'/></radialGradient>"
 "<radialGradient id='halo' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='#9fe8ff' stop-opacity='.55'/><stop offset='1' stop-color='#6a7aff' stop-opacity='0'/></radialGradient>"
 "<linearGradient id='cl' x1='0' x2='1'><stop offset='0' stop-color='#1c0d22'/><stop offset='.4' stop-color='#4a2052'/><stop offset='.6' stop-color='#55265e'/><stop offset='1' stop-color='#170a1c'/></linearGradient>"
 "<filter id='mist' x='-50%' y='-50%' width='200%' height='200%'><feGaussianBlur stdDeviation='4'/></filter>"
 "<clipPath id='ball'><circle cx='110' cy='124' r='34'/></clipPath></defs>"
 "<ellipse cx='110' cy='296' rx='84' ry='5' fill='#000' opacity='.5'/>"
 # claw-foot pedestal
 "<path d='M104 236 H116 L118 268 C130 276 150 284 160 292 L150 294 C138 288 124 282 114 280 H106 C96 282 82 288 70 294 L60 292 C70 284 90 276 102 268 Z' fill='url(#wd)'/>"
 # table top under a tattered cloth
 "<ellipse cx='110' cy='166' rx='86' ry='14' fill='#2a1030'/>"
 "<path d='M24 166 C24 176 30 206 34 238 L44 230 L52 246 L62 234 L72 250 L84 238 L96 254 L110 240 L124 254 L136 238 L148 250 L158 234 L168 246 L176 230 L186 238 C190 206 196 176 196 166 Z' fill='url(#cl)'/>"
 "<path d='M40 180 C44 204 46 222 48 240 M70 182 C72 210 74 228 76 246 M110 184 V244 M150 182 C148 210 146 228 144 246 M180 180 C176 204 174 222 172 240' stroke='#000' stroke-opacity='.25' stroke-width='4' fill='none'/>"
 "<path d='M24 166 C24 176 30 206 34 238 L44 230 L52 246 L62 234 L72 250 L84 238 L96 254 L110 240 L124 254 L136 238 L148 250 L158 234 L168 246 L176 230 L186 238 C190 206 196 176 196 166' stroke='#c9a24a' stroke-opacity='.5' stroke-width='1.2' fill='none'/>"
 "<ellipse cx='110' cy='164' rx='86' ry='13' fill='#5a2a64'/><ellipse cx='110' cy='164' rx='86' ry='13' fill='none' stroke='#c9a24a' stroke-opacity='.45'/>"
 # tarot cards
 "<g transform='rotate(-14 62 166)'><rect x='52' y='158' width='16' height='9' rx='1' fill='#e8dcbc'/><rect x='54' y='159.5' width='12' height='6' fill='#6a1a20'/></g>"
 "<g transform='rotate(10 152 168)'><rect x='144' y='160' width='16' height='9' rx='1' fill='#e8dcbc'/><rect x='146' y='161.5' width='12' height='6' fill='#1a2a5a'/></g>"
 # candles stand on the cloth; flames sit on their wicks
 + candle(40, 166, 40, 10, '#e2d9c0', 1.25, 6) + candle(182, 168, 28, 10, '#e2d9c0', 1.05, -5) +
 "<path d='M34 166 H46 M176 168 H188' stroke='#8a6a30' stroke-width='3' stroke-linecap='round'/>"
 # glow halo that breathes
 "<circle cx='110' cy='124' r='70' fill='url(#halo)'><animate attributeName='opacity' values='.55;1;.55' dur='4s' repeatCount='indefinite'/></circle>"
 # brass claw stand
 "<path d='M88 162 C92 152 98 150 110 150 C122 150 128 152 132 162 Z' fill='url(#brl)'/><ellipse cx='110' cy='162' rx='24' ry='4' fill='#5a3c0e'/>"
 # the ball, mist swirling inside it
 "<circle cx='110' cy='124' r='34' fill='url(#orb)'/>"
 "<g clip-path='url(#ball)'><g filter='url(#mist)' opacity='.85'>"
 "<g><animateTransform attributeName='transform' type='rotate' values='0 110 124;360 110 124' dur='9s' repeatCount='indefinite'/><ellipse cx='98' cy='118' rx='18' ry='8' fill='#fff' opacity='.8'/><ellipse cx='124' cy='134' rx='14' ry='6' fill='#c6b0ff' opacity='.9'/></g>"
 "<g><animateTransform attributeName='transform' type='rotate' values='360 110 124;0 110 124' dur='13s' repeatCount='indefinite'/><ellipse cx='112' cy='106' rx='16' ry='6' fill='#a8f0ff'/><ellipse cx='104' cy='142' rx='12' ry='5' fill='#fff' opacity='.7'/></g></g>"
 # a face that drifts up out of the mist now and then
 "<g opacity='0'><animate attributeName='opacity' values='0;0;.55;.55;0;0' keyTimes='0;.55;.65;.78;.88;1' dur='14s' repeatCount='indefinite'/>"
 "<ellipse cx='103' cy='120' rx='3' ry='4' fill='#1a1640'/><ellipse cx='117' cy='120' rx='3' ry='4' fill='#1a1640'/><ellipse cx='110' cy='133' rx='4' ry='5' fill='#1a1640'/></g>"
 "<ellipse cx='98' cy='108' rx='14' ry='8' fill='#fff' opacity='.35' transform='rotate(-30 98 108)'/><circle cx='94' cy='104' r='3' fill='#fff' opacity='.8'/></g>"
 "<circle cx='110' cy='124' r='34' fill='none' stroke='#cfeeff' stroke-opacity='.5'/>"
 "</svg>")

ART["trunk"] = (f"<svg {W} viewBox='0 0 260 190'><defs>{mahog}"
 "<linearGradient id='tk' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3b2a1c'/><stop offset='1' stop-color='#1e140c'/></linearGradient>"
 "<linearGradient id='lid' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#4a3524'/><stop offset='1' stop-color='#2a1d12'/></linearGradient>"
 "<radialGradient id='eye' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='#fffbd0'/><stop offset='.5' stop-color='#ffd23a'/><stop offset='1' stop-color='#ff9a1a' stop-opacity='0'/></radialGradient></defs>"
 "<ellipse cx='130' cy='186' rx='116' ry='5' fill='#000' opacity='.55'/>"
 # dark gap and the eyes in it
 "<rect x='26' y='72' width='208' height='20' fill='#050304'/>"
 "<g opacity='0'><animate attributeName='opacity' values='0;0;1;1;0;0' keyTimes='0;.6;.66;.8;.84;1' dur='11s' repeatCount='indefinite'/>"
 "<ellipse cx='112' cy='82' rx='7' ry='4' fill='url(#eye)'><animate attributeName='ry' values='4;4;.5;4;4' keyTimes='0;.7;.73;.76;1' dur='11s' repeatCount='indefinite'/></ellipse>"
 "<ellipse cx='146' cy='82' rx='7' ry='4' fill='url(#eye)'><animate attributeName='ry' values='4;4;.5;4;4' keyTimes='0;.7;.73;.76;1' dur='11s' repeatCount='indefinite'/></ellipse>"
 "<circle cx='112' cy='82' r='1.5' fill='#2a0a00'/><circle cx='146' cy='82' r='1.5' fill='#2a0a00'/></g>"
 # body
 "<rect x='20' y='90' width='220' height='92' rx='4' fill='url(#tk)'/>"
 + "".join(f"<path d='M24 {y} H236' stroke='#000' stroke-opacity='.3' stroke-width='1.2'/>" for y in (112, 136, 160)) +
 "<rect x='58' y='90' width='14' height='92' fill='#5a3a20'/><rect x='188' y='90' width='14' height='92' fill='#5a3a20'/>"
 "<rect x='20' y='90' width='220' height='92' rx='4' fill='none' stroke='#120a05' stroke-width='3'/>"
 "<path d='M20 100 V90 H34 M240 100 V90 H226 M20 172 V182 H34 M240 172 V182 H226' stroke='url(#brl)' stroke-width='6' fill='none'/>"
 "<rect x='118' y='96' width='24' height='30' rx='3' fill='url(#brl)'/><circle cx='130' cy='108' r='3' fill='#1a1008'/><path d='M130 110 V118' stroke='#1a1008' stroke-width='2.4'/>"
  # rusty chain hanging off the front
 + "".join(f"<ellipse cx='{f(78 + k*10)}' cy='{f(132 + 8*math.sin(k/2.2))}' rx='6' ry='3.4' fill='none' stroke='#6a5a4a' stroke-width='2.2'/>" for k in range(11)) +
 # lid: lifts a crack, holds, then slams down with a little jolt
 "<g><animateTransform attributeName='transform' type='translate' values='0 0;0 0;0 -16;0 -14;0 -16;0 0;0 1.5;0 0' keyTimes='0;.6;.65;.72;.8;.84;.86;1' dur='11s' repeatCount='indefinite'/>"
 "<path d='M16 92 V70 C16 46 60 38 130 38 C200 38 244 46 244 70 V92 Z' fill='url(#lid)'/>"
 "<path d='M58 92 V44 M202 92 V44' stroke='#5a3a20' stroke-width='14'/>"
 "<path d='M16 92 V70 C16 46 60 38 130 38 C200 38 244 46 244 70 V92 Z' fill='none' stroke='#120a05' stroke-width='3'/>"
 "<path d='M16 86 H244' stroke='url(#brl)' stroke-width='5'/><path d='M40 58 C80 48 180 48 220 58' stroke='#fff' stroke-opacity='.08' stroke-width='4' fill='none'/>"
 "<path d='M124 86 V96 H136 V86' fill='url(#brl)'/>" + web(16, 70, .5) + "</g>"
 "</svg>")

# ======================= AQUARIUM =======================
def jelly(cx, cy, s, c1, c2, dur, drift, begin):
    bell = f"M{-36} 0 C{-36} -40 36 -40 36 0 C26 6 18 2 12 6 C6 2 -6 2 -12 6 C-18 2 -26 6 -36 0 Z"
    tent = ""
    rr = random.Random(int(cx * 10 + cy))
    for k, x in enumerate((-26, -14, -4, 6, 16, 26)):
        L = rr.uniform(70, 110); a = rr.uniform(5, 9)
        d1 = f"M{x} 4 C{x+a} {f(L*.3)} {x-a} {f(L*.6)} {x+a*.5} {f(L)}"
        d2 = f"M{x} 4 C{x-a} {f(L*.3)} {x+a} {f(L*.6)} {x-a*.5} {f(L)}"
        tent += (f"<path d='{d1}' stroke='{c2}' stroke-opacity='.65' stroke-width='{1.8 if k % 2 else 1.2}' fill='none' stroke-linecap='round'>"
                 f"<animate attributeName='d' values='{d1};{d2};{d1}' dur='{f(dur*1.6 + k*.2)}s' begin='{begin}s' repeatCount='indefinite'/></path>")
    arms = "".join(f"<path d='M{x} 4 C{x-4} 20 {x+6} 34 {x} 48 C{x-3} 34 {x-8} 20 {x-4} 4 Z' fill='{c1}' opacity='.55'><animateTransform attributeName='transform' type='skewX' values='0;6;-6;0' dur='{f(dur*2)}s' begin='{begin}s' repeatCount='indefinite'/></path>" for x in (-8, 4, 14))
    return (f"<g transform='translate({cx} {cy}) scale({s})'>"
            f"<g><animateTransform attributeName='transform' type='translate' values='0 0;3 {-drift};0 0' dur='{f(dur*4)}s' begin='{begin}s' repeatCount='indefinite' {SPL}/>"
            f"<ellipse cx='0' cy='-10' rx='60' ry='50' fill='url(#jg{c1[1:]})' opacity='.55'><animate attributeName='opacity' values='.35;.7;.35' dur='{dur}s' begin='{begin}s' repeatCount='indefinite'/></ellipse>"
            + tent + arms +
            # the bell squeezes from the top, so the rim and everything under it stays attached
            f"<g><animateTransform attributeName='transform' type='scale' values='1 1;.86 1.1;1 1' dur='{dur}s' begin='{begin}s' repeatCount='indefinite' {SPL}/>"
            f"<clipPath id='bc{c1[1:]}'><path d='{bell}'/></clipPath>"
            f"<path d='{bell}' fill='url(#jb{c1[1:]})'/>"
            f"<g clip-path='url(#bc{c1[1:]})'><ellipse cx='-12' cy='-22' rx='12' ry='6' fill='#fff' opacity='.45' transform='rotate(-24 -12 -22)'/>"
            + "".join(f"<path d='M{x} -2 C{x*.8:.1f} -14 {x*.5:.1f} -24 0 -30' stroke='#fff' stroke-opacity='.25' fill='none'/>" for x in (-30, -18, -6, 6, 18, 30)) +
            f"<ellipse cx='0' cy='-6' rx='14' ry='6' fill='{c2}' opacity='.6'/></g>"
            f"<path d='{bell}' fill='none' stroke='#fff' stroke-opacity='.4' stroke-width='1'/></g></g></g>")
def jgrads(c1, c2):
    k = c1[1:]
    return (f"<radialGradient id='jb{k}' cx='.5' cy='.75' r='.8'><stop offset='0' stop-color='{c2}' stop-opacity='.95'/><stop offset='.6' stop-color='{c1}' stop-opacity='.75'/><stop offset='1' stop-color='{c1}' stop-opacity='.35'/></radialGradient>"
            f"<radialGradient id='jg{k}' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='{c1}' stop-opacity='.6'/><stop offset='1' stop-color='{c1}' stop-opacity='0'/></radialGradient>")
ART["jelly"] = (f"<svg {W} viewBox='0 0 220 330'><defs>{jgrads('#ff7ad9', '#ffe0f6')}{jgrads('#8ad7ff', '#e6fbff')}</defs>"
 + jelly(124, 70, 1.15, '#ff7ad9', '#ffe0f6', 2.6, 16, 0) + jelly(58, 196, .75, '#8ad7ff', '#e6fbff', 2.1, 12, -1.3) + "</svg>")

ART["chest"] = (f"<svg {W} viewBox='0 0 260 230'><defs>"
 "<linearGradient id='pl' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#6a4022'/><stop offset='1' stop-color='#3a2010'/></linearGradient>"
 "<linearGradient id='pl2' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#7a4c28'/><stop offset='1' stop-color='#4a2a14'/></linearGradient>"
 "<linearGradient id='ir' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#6f7a78'/><stop offset='.5' stop-color='#3e4644'/><stop offset='1' stop-color='#2a302e'/></linearGradient>"
 "<radialGradient id='gd' cx='.4' cy='.3' r='.8'><stop offset='0' stop-color='#fff4b0'/><stop offset='.45' stop-color='#f2c23a'/><stop offset='1' stop-color='#8a5a08'/></radialGradient>"
 "<radialGradient id='shine' cx='.5' cy='.7' r='.6'><stop offset='0' stop-color='#ffe27a' stop-opacity='.7'/><stop offset='1' stop-color='#ffe27a' stop-opacity='0'/></radialGradient>"
 "<linearGradient id='sd' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#d9c08a'/><stop offset='.55' stop-color='#b89a62' stop-opacity='.85'/><stop offset='1' stop-color='#a88a52' stop-opacity='0'/></linearGradient>"
 "<clipPath id='bx'><rect x='40' y='120' width='180' height='82'/></clipPath></defs>"
 # gold glow spilling from the chest
 "<ellipse cx='130' cy='112' rx='110' ry='60' fill='url(#shine)'><animate attributeName='opacity' values='.6;1;.6' dur='3.4s' repeatCount='indefinite'/></ellipse>"
 # sand drift it is half-buried in
 "<path d='M0 226 C30 206 70 198 130 200 C190 198 230 206 260 226 Z' fill='url(#sd)'/>"
 # open lid, tipped back (seen from below)
 "<g><animateTransform attributeName='transform' type='rotate' values='0 130 112;-3 130 112;0 130 112' dur='5s' repeatCount='indefinite' {SPL}/>"
 "<path d='M46 112 L52 60 C70 44 190 44 208 60 L214 112 Z' fill='#2a160a'/>"
 "<path d='M52 60 C70 44 190 44 208 60 L206 70 C188 56 72 56 54 70 Z' fill='url(#pl2)'/>"
 "<path d='M46 112 L52 60 M214 112 L208 60' stroke='url(#ir)' stroke-width='6'/><path d='M50 66 C70 50 190 50 210 66' stroke='url(#ir)' stroke-width='5' fill='none'/>"
 "<path d='M88 104 L90 54 M170 104 L168 54' stroke='url(#ir)' stroke-width='6'/></g>".replace("{SPL}", SPL) +
 # treasure heaped above the rim
 "<path d='M44 124 C60 100 80 96 100 102 C114 90 140 88 156 100 C176 94 200 102 216 124 Z' fill='url(#gd)'/>"
 + "".join(f"<ellipse cx='{x}' cy='{y}' rx='7' ry='3.2' fill='url(#gd)' stroke='#8a5a08' stroke-width='.8'/>" for x, y in [(62, 116), (78, 108), (96, 112), (118, 100), (138, 96), (152, 106), (172, 104), (190, 112), (204, 118), (108, 118), (164, 116), (130, 110)]) +
 "<path d='M120 102 l8 -22 l6 22 Z' fill='#e8e6f0' stroke='#9a98a8'/><circle cx='128' cy='78' r='4' fill='#e8e6f0' stroke='#9a98a8'/>"
 "<path d='M76 104 C72 92 96 86 108 94' stroke='#e8e2ff' stroke-width='3' fill='none' stroke-dasharray='.1 5' stroke-linecap='round'/>"
 # gems
 "<path d='M88 100 l6 -6 l6 6 l-6 7 Z' fill='#e0304a'/><path d='M160 98 l5 -6 l5 6 l-5 6 Z' fill='#30c070'/><path d='M180 108 l5 -5 l5 5 l-5 6 Z' fill='#4a7aff'/>"
 # chest body
 "<rect x='40' y='120' width='180' height='82' rx='3' fill='url(#pl)'/>"
 "<g clip-path='url(#bx)'>" + "".join(f"<path d='M40 {y} H220' stroke='#2a1408' stroke-width='1.5'/>" for y in (140, 160, 180)) +
 "<path d='M40 186 C80 176 180 176 220 186 V202 H40 Z' fill='#d9c08a' opacity='.9'/></g>"
 "<rect x='40' y='120' width='180' height='8' fill='url(#ir)'/><rect x='84' y='120' width='10' height='70' fill='url(#ir)'/><rect x='166' y='120' width='10' height='70' fill='url(#ir)'/>"
 "<rect x='118' y='124' width='24' height='28' rx='3' fill='url(#gd)' stroke='#6a4008'/><path d='M130 132 V144' stroke='#3a2008' stroke-width='3' stroke-linecap='round'/>"
 # weed growing on it
 "<path d='M212 200 C206 180 216 168 208 150 M220 200 C222 186 230 176 226 160' stroke='#3a9a5a' stroke-width='3' fill='none' stroke-linecap='round'><animateTransform attributeName='transform' type='skewX' values='0;5;-3;0' dur='5s' repeatCount='indefinite'/></path>"
 # sparkles that wink across the gold
 + "".join(f"<path d='M{x} {y-7} L{x+1.5} {y-1.5} L{x+7} {y} L{x+1.5} {y+1.5} L{x} {y+7} L{x-1.5} {y+1.5} L{x-7} {y} L{x-1.5} {y-1.5} Z' fill='#fff' opacity='0'><animate attributeName='opacity' values='0;1;0;0' keyTimes='0;.08;.16;1' dur='{d}s' begin='{b}s' repeatCount='indefinite'/></path>" for x, y, d, b in [(100, 100, 3.1, 0), (150, 96, 3.7, -1.2), (186, 110, 2.9, -2), (70, 112, 4.1, -.6), (128, 80, 3.3, -2.6)]) +
 # bubbles that escape every so often
 rise(130, 96, -10, 7, 5.5, 3, 1.5, 4, sway=8) + rise(84, 104, 0, 4, 6.5, 8, 1.2, 3) +
 "</svg>")

ART["helmet"] = (f"<svg {W} viewBox='0 0 220 300'><defs>"
 "<radialGradient id='bz' cx='.35' cy='.3' r='.8'><stop offset='0' stop-color='#ffe7a8'/><stop offset='.3' stop-color='#d39a3e'/><stop offset='.75' stop-color='#8a5a1e'/><stop offset='1' stop-color='#4a2e0c'/></radialGradient>"
 "<linearGradient id='bzl' x1='0' x2='1'><stop offset='0' stop-color='#6a4210'/><stop offset='.45' stop-color='#f0c470'/><stop offset='1' stop-color='#5a360c'/></linearGradient>"
 "<radialGradient id='pg' cx='.4' cy='.35' r='.75'><stop offset='0' stop-color='#3c8aa0'/><stop offset='.7' stop-color='#0d3646'/><stop offset='1' stop-color='#051a22'/></radialGradient>"
 "<linearGradient id='sd' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#d9c08a'/><stop offset='.55' stop-color='#b89a62' stop-opacity='.85'/><stop offset='1' stop-color='#a88a52' stop-opacity='0'/></linearGradient>"
 "<clipPath id='dome'><path d='M44 210 C34 150 48 96 110 92 C172 96 186 150 176 210 Z'/></clipPath>"
 "<clipPath id='port'><circle cx='110' cy='160' r='30'/></clipPath></defs>"
 + rise(110, 96, -10, 9, 6, 21, 1.6, 4.5, sway=10) +
 # breastplate
 "<path d='M22 270 C20 236 46 214 110 212 C174 214 200 236 198 270 Z' fill='url(#bz)'/>"
 "<path d='M22 270 C20 236 46 214 110 212 C174 214 200 236 198 270' fill='none' stroke='#4a2e0c' stroke-width='2'/>"
 + "".join(f"<circle cx='{f(110 + 78*math.cos(math.radians(a)))}' cy='{f(258 - 34*math.sin(math.radians(a)))}' r='3.6' fill='url(#bzl)' stroke='#3a2208'/>" for a in range(15, 170, 25)) +
 # collar ring
 "<ellipse cx='110' cy='212' rx='70' ry='12' fill='url(#bzl)'/><ellipse cx='110' cy='210' rx='62' ry='8' fill='#5a360c'/>"
 # dome, sheen only inside it
 "<path d='M44 210 C34 150 48 96 110 92 C172 96 186 150 176 210 Z' fill='url(#bz)'/>"
 "<g clip-path='url(#dome)'><ellipse cx='76' cy='128' rx='20' ry='38' fill='#fff' opacity='.28' transform='rotate(24 76 128)'><animate attributeName='opacity' values='.18;.34;.18' dur='4s' repeatCount='indefinite'/></ellipse>"
 "<path d='M40 196 C80 206 140 206 180 196' stroke='#000' stroke-opacity='.2' stroke-width='10' fill='none'/></g>"
 "<path d='M44 210 C34 150 48 96 110 92 C172 96 186 150 176 210' fill='none' stroke='#3a2208' stroke-width='2'/>"
 # side ports
 "<circle cx='54' cy='156' r='15' fill='url(#bzl)'/><circle cx='54' cy='156' r='10' fill='url(#pg)'/><circle cx='166' cy='156' r='15' fill='url(#bzl)'/><circle cx='166' cy='156' r='10' fill='url(#pg)'/>"
 # air valve on top
 "<rect x='100' y='80' width='20' height='16' rx='3' fill='url(#bzl)'/><rect x='96' y='76' width='28' height='7' rx='3' fill='url(#bzl)'/>"
 # front port with its grille
 "<circle cx='110' cy='160' r='38' fill='url(#bzl)' stroke='#3a2208' stroke-width='2'/>"
 + "".join(f"<circle cx='{f(110 + 34*math.cos(math.radians(a)))}' cy='{f(160 + 34*math.sin(math.radians(a)))}' r='2.6' fill='#ffe7a8' stroke='#3a2208' stroke-width='.8'/>" for a in range(0, 360, 45)) +
 "<circle cx='110' cy='160' r='30' fill='url(#pg)'/>"
 "<g clip-path='url(#port)'><path d='M80 150 L130 130 L140 138 L90 162 Z' fill='#cdf6ff' opacity='.25'/><circle cx='98' cy='146' r='4' fill='#fff' opacity='.5'/></g>"
 "<path d='M80 160 H140 M110 130 V190' stroke='url(#bzl)' stroke-width='4'/>"
 # little fish peeking in at the port
 "<g opacity='0'><animate attributeName='opacity' values='0;0;1;1;0;0' keyTimes='0;.5;.56;.8;.86;1' dur='12s' repeatCount='indefinite'/>"
 "<g><animateTransform attributeName='transform' type='translate' values='40 0;40 0;0 0;0 0;-50 0;-50 0' keyTimes='0;.5;.6;.76;.88;1' dur='12s' repeatCount='indefinite'/>"
 "<path d='M126 172 c6 -6 16 -6 20 0 c-4 6 -14 6 -20 0 Z M146 172 l7 -5 v10 Z' fill='#ffb02a'/><circle cx='130' cy='171' r='1.2' fill='#111'/></g></g>"
 # sand it rests on
 "<path d='M0 296 C30 270 70 264 110 266 C150 264 190 270 220 296 Z' fill='url(#sd)'/>"
 "</svg>")

# ======================= STARSHIP =======================
ART["console"] = (f"<svg {W} viewBox='0 0 260 330'><defs>"
 "<linearGradient id='hl' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3fd7ff' stop-opacity='0'/><stop offset='1' stop-color='#3fd7ff' stop-opacity='.32'/></linearGradient>"
 "<linearGradient id='mt' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#2b3750'/><stop offset='1' stop-color='#121a2a'/></linearGradient>"
 "<linearGradient id='mt2' x1='0' x2='1'><stop offset='0' stop-color='#151c2a'/><stop offset='.5' stop-color='#26324a'/><stop offset='1' stop-color='#111725'/></linearGradient>"
 "<radialGradient id='pl' cx='.4' cy='.35' r='.7'><stop offset='0' stop-color='#9ff0ff' stop-opacity='.55'/><stop offset='1' stop-color='#1a8ad0' stop-opacity='.15'/></radialGradient>"
 "<clipPath id='pc'><circle cx='130' cy='110' r='52'/></clipPath><clipPath id='rd'><circle cx='130' cy='268' r='20'/></clipPath>"
 "<filter id='gw' x='-30%' y='-30%' width='160%' height='160%'><feGaussianBlur stdDeviation='2.5' result='b'/><feMerge><feMergeNode in='b'/><feMergeNode in='SourceGraphic'/></feMerge></filter></defs>"
 # beam from the projector
 "<path d='M112 206 L66 50 H194 L148 206 Z' fill='url(#hl)'><animate attributeName='opacity' values='.8;1;.7;1;.8' dur='3s' repeatCount='indefinite'/></path>"
 # hologram planet: wire globe with turning meridians, a tilted ring and a moon
 "<g filter='url(#gw)'><animate attributeName='opacity' values='1;.85;1;.6;1;1' keyTimes='0;.3;.32;.34;.36;1' dur='5s' repeatCount='indefinite'/>"
 "<circle cx='130' cy='110' r='52' fill='url(#pl)' stroke='#7fe8ff' stroke-width='1.4'/>"
 "<g clip-path='url(#pc)' stroke='#7fe8ff' stroke-opacity='.75' fill='none' stroke-width='1'>"
 + "".join(f"<ellipse cx='130' cy='{f(110 + 52*math.sin(math.radians(a)))}' rx='{f(52*math.cos(math.radians(a)))}' ry='{f(8*math.cos(math.radians(a)))}'/>" for a in (-60, -30, 0, 30, 60)) +
 "".join(f"<ellipse cx='130' cy='110' ry='52' rx='52'><animate attributeName='rx' values='{v}' dur='8s' begin='{b}s' repeatCount='indefinite'/><animate attributeName='stroke-opacity' values='0;.9;0' dur='4s' begin='{b}s' repeatCount='indefinite'/></ellipse>" for v, b in [("52;0", 0), ("52;0", -2), ("52;0", -4), ("52;0", -6)]) +
 # continents sliding across
 "<g fill='#7fe8ff' fill-opacity='.35' stroke='none'><animateTransform attributeName='transform' type='translate' values='-60 0;60 0' dur='16s' repeatCount='indefinite'/>"
 "<path d='M110 90 c10 -8 26 -4 30 6 c4 10 -8 14 -4 24 c-10 6 -20 -2 -26 -10 c-6 -8 -6 -14 0 -20 Z'/><path d='M150 124 c8 -2 14 4 12 10 c-4 6 -12 6 -16 0 Z'/>"
 "<path d='M-10 90 c10 -8 26 -4 30 6 c4 10 -8 14 -4 24 c-10 6 -20 -2 -26 -10 c-6 -8 -6 -14 0 -20 Z' transform='translate(120 0)'/></g></g>"
 "<ellipse cx='130' cy='110' rx='84' ry='16' fill='none' stroke='#b6f4ff' stroke-width='2' stroke-opacity='.8' transform='rotate(-14 130 110)' stroke-dasharray='4 3'><animate attributeName='stroke-dashoffset' values='0;-70' dur='6s' repeatCount='indefinite'/></ellipse>"
 "<g><animateTransform attributeName='transform' type='rotate' values='0 130 110;360 130 110' dur='12s' repeatCount='indefinite'/><circle cx='206' cy='110' r='6' fill='#b6f4ff' fill-opacity='.6' stroke='#e6fbff'/></g>"
 # scan line rolling down
 "<rect x='70' y='56' width='120' height='3' fill='#e6fbff' opacity='.35'><animate attributeName='y' values='56;166' dur='2.6s' repeatCount='indefinite'/></rect></g>"
 # console body
 "<path d='M18 236 L36 206 H224 L242 236 Z' fill='url(#mt)' stroke='#3fd7ff' stroke-opacity='.6'/>"
 "<rect x='22' y='236' width='216' height='86' rx='4' fill='url(#mt2)' stroke='#3fd7ff' stroke-opacity='.5'/>"
 "<rect x='22' y='316' width='216' height='10' rx='2' fill='#0a0e18'/><path d='M30 326 H230' stroke='#3fd7ff' stroke-width='2' opacity='.8'/>"
 # projector disc
 "<ellipse cx='130' cy='208' rx='26' ry='6' fill='#0a0e18' stroke='#3fd7ff'/><ellipse cx='130' cy='207' rx='16' ry='3.4' fill='#bff6ff'><animate attributeName='opacity' values='.6;1;.6' dur='1.4s' repeatCount='indefinite'/></ellipse>"
 # buttons on the sloped desk
 + "".join(f"<rect x='{f(48 + c*12 + (c > 4)*48)}' y='{f(214 + r*9)}' width='10' height='5' rx='1.5' fill='{col}'><animate attributeName='opacity' values='{ops}' dur='{d}s' repeatCount='indefinite'/></rect>"
           for (r, c, col, ops, d) in [(rr, cc, ['#3fd7ff', '#ff4fa3', '#ffd23a', '#5cff9a'][(rr*7 + cc*3) % 4], ['1;.25;1', '.3;1;.3', '1;1;.2;1', '.2;.2;1;.2'][(rr + cc) % 4], [1.3, 1.9, 2.4, 0.9, 3.1][(rr*3 + cc) % 5]) for rr in range(2) for cc in range(10)]) +
 # radar sweep
 "<circle cx='130' cy='268' r='20' fill='#061420' stroke='#3fd7ff' stroke-opacity='.8'/><g clip-path='url(#rd)'><circle cx='130' cy='268' r='12' fill='none' stroke='#3fd7ff' stroke-opacity='.3'/><path d='M110 268 H150 M130 248 V288' stroke='#3fd7ff' stroke-opacity='.25'/>"
 "<g><animateTransform attributeName='transform' type='rotate' values='0 130 268;360 130 268' dur='3s' repeatCount='indefinite'/><path d='M130 268 L150 268 A20 20 0 0 0 144 254 Z' fill='#3fd7ff' opacity='.45'/></g>"
 "<circle cx='138' cy='260' r='1.8' fill='#5cff9a'><animate attributeName='opacity' values='0;1;0' dur='3s' repeatCount='indefinite'/></circle></g>"
 # two readout screens with scrolling bars
 + "".join(f"<rect x='{x}' y='252' width='54' height='32' rx='3' fill='#061420' stroke='#3fd7ff' stroke-opacity='.6'/>" + "".join(f"<rect x='{x+6+k*8}' y='262' width='5' height='18' fill='#3fd7ff' opacity='.75'><animate attributeName='height' values='{h1};{h2};{h1}' dur='{d}s' repeatCount='indefinite'/><animate attributeName='y' values='{280-h1};{280-h2};{280-h1}' dur='{d}s' repeatCount='indefinite'/></rect>" for k, (h1, h2, d) in enumerate([(6, 18, 1.1), (14, 4, .9), (10, 20, 1.4), (18, 8, 1.2), (4, 14, .8), (12, 6, 1.6)])) for x in (40, 166)) +
 "<path d='M40 300 H90 M170 300 H220' stroke='#3fd7ff' stroke-opacity='.35' stroke-width='3' stroke-dasharray='6 4'/>"
 "</svg>")

ART["droid"] = (f"<svg {W} viewBox='0 0 200 300'><defs>"
 "<linearGradient id='sh' x1='0' x2='1'><stop offset='0' stop-color='#8a96aa'/><stop offset='.4' stop-color='#eef3f8'/><stop offset='.7' stop-color='#cfd8e4'/><stop offset='1' stop-color='#6a768a'/></linearGradient>"
 "<linearGradient id='dk' x1='0' x2='1'><stop offset='0' stop-color='#1a2233'/><stop offset='.5' stop-color='#2b3750'/><stop offset='1' stop-color='#151c2a'/></linearGradient>"
 "<radialGradient id='ey' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='#fff'/><stop offset='.35' stop-color='#7fe8ff'/><stop offset='1' stop-color='#3fd7ff' stop-opacity='0'/></radialGradient>"
 "<clipPath id='vz'><rect x='68' y='70' width='64' height='22' rx='11'/></clipPath><clipPath id='bd'><rect x='54' y='128' width='92' height='110' rx='18'/></clipPath></defs>"
 "<ellipse cx='100' cy='294' rx='70' ry='5' fill='#000' opacity='.55'/><ellipse cx='100' cy='294' rx='60' ry='4' fill='#3fd7ff' opacity='.2'/>"
 # treads
 "<rect x='38' y='256' width='124' height='36' rx='18' fill='url(#dk)' stroke='#0a0e18' stroke-width='2'/>"
 ""
 "<rect x='44' y='262' width='112' height='24' rx='12' fill='none' stroke='#5a6a86' stroke-width='3' stroke-dasharray='6 5'><animate attributeName='stroke-dashoffset' values='0;22' dur='1.6s' repeatCount='indefinite'/></rect>"
 + "".join(f"<circle cx='{x}' cy='274' r='8' fill='#3a4660' stroke='#8a96aa'/><circle cx='{x}' cy='274' r='2.5' fill='#8a96aa'/>" for x in (58, 100, 142)) +
 # gentle hover-bob of everything above the treads
 f"<g><animateTransform attributeName='transform' type='translate' values='0 0;0 -3;0 0' dur='2.2s' repeatCount='indefinite' {SPL}/>"
 "<rect x='92' y='236' width='16' height='24' fill='#3a4660'/>"
 # arms: the left one waves now and then
 "<g><animateTransform attributeName='transform' type='rotate' values='0 52 150;0 52 150;-58 52 150;-40 52 150;-58 52 150;-40 52 150;0 52 150;0 52 150' keyTimes='0;.5;.58;.64;.7;.76;.84;1' dur='9s' repeatCount='indefinite'/>"
 "<path d='M52 150 L34 196' stroke='url(#sh)' stroke-width='10' stroke-linecap='round'/><circle cx='52' cy='150' r='8' fill='#5a6a86'/><path d='M34 196 l-8 12 M34 196 l6 13' stroke='#cfd8e4' stroke-width='4' stroke-linecap='round'/></g>"
 "<path d='M148 150 L164 196' stroke='url(#sh)' stroke-width='10' stroke-linecap='round'/><circle cx='148' cy='150' r='8' fill='#5a6a86'/><path d='M164 196 l-6 13 M164 196 l8 12' stroke='#cfd8e4' stroke-width='4' stroke-linecap='round'/>"
 # body
 "<rect x='54' y='128' width='92' height='110' rx='18' fill='url(#sh)'/>"
 "<g clip-path='url(#bd)'><rect x='54' y='128' width='92' height='110' fill='#000' opacity='0'/><path d='M54 222 H146' stroke='#3fd7ff' stroke-width='3' opacity='.7'/><path d='M66 128 V238' stroke='#fff' stroke-opacity='.4' stroke-width='6'/></g>"
 "<rect x='54' y='128' width='92' height='110' rx='18' fill='none' stroke='#5a6a86' stroke-width='1.5'/>"
 # chest screen with a heartbeat line and status lights
 "<rect x='70' y='142' width='60' height='34' rx='5' fill='#061420' stroke='#3fd7ff' stroke-opacity='.7'/>"
 "<path d='M72 160 H86 L90 150 L96 170 L100 156 L104 160 H128' stroke='#5cff9a' stroke-width='1.8' fill='none' stroke-dasharray='70 70'><animate attributeName='stroke-dashoffset' values='70;-70' dur='1.8s' repeatCount='indefinite'/></path>"
 + "".join(f"<circle cx='{x}' cy='194' r='4' fill='{c}'><animate attributeName='opacity' values='{o}' dur='{d}s' repeatCount='indefinite'/></circle>" for x, c, o, d in [(78, '#ff4f6a', '1;.2;1', 1.2), (92, '#ffd23a', '.2;1;.2', 1.7), (106, '#5cff9a', '1;1;.2;1', 2.3), (120, '#3fd7ff', '.3;1;.3', .9)]) +
 "<rect x='76' y='206' width='48' height='6' rx='3' fill='#2b3750'/>"
 # neck + head
 "<rect x='90' y='112' width='20' height='18' fill='#5a6a86'/><rect x='84' y='118' width='32' height='4' fill='#8a96aa'/>"
 "<g><animateTransform attributeName='transform' type='rotate' values='0 100 112;0 100 112;-6 100 112;-6 100 112;5 100 112;5 100 112;0 100 112' keyTimes='0;.2;.28;.45;.55;.75;1' dur='7s' repeatCount='indefinite'/>"
 "<rect x='56' y='50' width='88' height='64' rx='22' fill='url(#sh)' stroke='#5a6a86' stroke-width='1.5'/>"
 "<rect x='46' y='70' width='12' height='24' rx='4' fill='#5a6a86'/><rect x='142' y='70' width='12' height='24' rx='4' fill='#5a6a86'/>"
 "<path d='M100 50 V30' stroke='#8a96aa' stroke-width='3'/><circle cx='100' cy='26' r='5' fill='#ff4f6a'><animate attributeName='opacity' values='1;.2;1' dur='1.1s' repeatCount='indefinite'/></circle>"
 "<rect x='68' y='70' width='64' height='22' rx='11' fill='#061420'/>"
 "<g clip-path='url(#vz)'><g><animateTransform attributeName='transform' type='translate' values='-18 0;18 0;18 0;-18 0;-18 0' keyTimes='0;.35;.5;.85;1' dur='5s' repeatCount='indefinite' calcMode='spline' keySplines='.45 0 .55 1;0 0 1 1;.45 0 .55 1;0 0 1 1'/>"
 "<circle cx='100' cy='81' r='14' fill='url(#ey)'/><circle cx='100' cy='81' r='4' fill='#fff'/></g>"
 "<path d='M70 72 L96 72 L88 90 L70 90 Z' fill='#fff' opacity='.08'/></g>"
 "<rect x='68' y='70' width='64' height='22' rx='11' fill='none' stroke='#3fd7ff' stroke-opacity='.8'/>"
 "<path d='M66 56 C80 52 120 52 134 56' stroke='#fff' stroke-opacity='.5' stroke-width='3' fill='none'/></g>"
 "</g></svg>")

# ======================= CHRISTMAS =======================
ART["horse"] = (f"<svg {W} viewBox='0 0 300 240'><defs>"
 "<linearGradient id='rk' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#b8322a'/><stop offset='1' stop-color='#6a1410'/></linearGradient>"
 "<radialGradient id='hb' cx='.4' cy='.3' r='.8'><stop offset='0' stop-color='#fffaf0'/><stop offset='.7' stop-color='#efe4cf'/><stop offset='1' stop-color='#bfae90'/></radialGradient>"
 "<linearGradient id='gd' x1='0' x2='1'><stop offset='0' stop-color='#8a6a20'/><stop offset='.5' stop-color='#f6dc7a'/><stop offset='1' stop-color='#8a6a20'/></linearGradient>"
 "<clipPath id='hc'><path d='M70 120 C70 96 96 86 130 88 L190 90 C206 70 214 50 220 38 C224 30 236 28 244 34 L262 50 C268 56 266 64 258 66 L244 66 C238 80 232 102 222 120 C220 132 210 140 196 140 H96 C80 140 70 132 70 120 Z'/></clipPath></defs>"
 "<ellipse cx='150' cy='236' rx='120' ry='5' fill='#000' opacity='.45'/>"
 f"<g><animateTransform attributeName='transform' type='rotate' values='-6 150 228;6 150 228;-6 150 228' dur='3.2s' repeatCount='indefinite' {SPL}/>"
 # rockers
 "<path d='M14 196 C70 236 230 236 286 196' stroke='url(#rk)' stroke-width='12' fill='none' stroke-linecap='round'/>"
 "<path d='M20 200 C76 236 224 236 280 200' stroke='#fff' stroke-opacity='.25' stroke-width='2' fill='none'/>"
 # legs (far pair darker) splayed onto the rockers
 "<path d='M104 134 L80 214 M196 134 L222 214' stroke='#cbbca0' stroke-width='12' stroke-linecap='round'/>"
 "<path d='M118 134 L98 218 M184 134 L204 218' stroke='url(#hb)' stroke-width='13' stroke-linecap='round'/>"
 + "".join(f"<rect x='{x-9}' y='{y}' width='18' height='8' rx='2' fill='#2a1a10'/>" for x, y in [(80, 210), (98, 214), (222, 210), (204, 214)]) +
 # tail of yarn
 "<path d='M72 112 C52 112 42 130 46 158 C54 140 58 130 72 124 Z' fill='#5a3a20'/><path d='M72 116 C56 120 50 138 54 160' stroke='#3a2410' stroke-width='2' fill='none'/>"
 # body + head with dapples kept inside
 "<path d='M70 120 C70 96 96 86 130 88 L190 90 C206 70 214 50 220 38 C224 30 236 28 244 34 L262 50 C268 56 266 64 258 66 L244 66 C238 80 232 102 222 120 C220 132 210 140 196 140 H96 C80 140 70 132 70 120 Z' fill='url(#hb)'/>"
 "<g clip-path='url(#hc)' fill='#c8b89a' opacity='.55'>" + "".join(f"<circle cx='{x}' cy='{y}' r='{r}'/>" for x, y, r in [(92, 112, 6), (110, 124, 5), (124, 104, 7), (150, 118, 6), (172, 104, 5), (196, 120, 6), (210, 96, 5), (84, 128, 4), (140, 132, 4)]) + "</g>"
 "<path d='M70 120 C70 96 96 86 130 88 L190 90 C206 70 214 50 220 38 C224 30 236 28 244 34 L262 50 C268 56 266 64 258 66 L244 66 C238 80 232 102 222 120 C220 132 210 140 196 140 H96 C80 140 70 132 70 120 Z' fill='none' stroke='#9a8a6c' stroke-width='1.5'/>"
 # ear, eye, nostril
 "<path d='M224 34 L222 18 L234 30 Z' fill='url(#hb)' stroke='#9a8a6c'/><circle cx='238' cy='44' r='3' fill='#2a1a10'/><circle cx='239' cy='43' r='1' fill='#fff'/><circle cx='258' cy='58' r='1.6' fill='#7a6a50'/>"
 # mane
 "<path d='M222 30 C210 40 206 56 200 66 C196 76 190 84 184 90 C194 90 200 82 206 74 C212 62 214 50 226 40 Z' fill='#5a3a20'/>"
 "<path d='M216 36 C206 50 202 64 194 78 M222 38 C214 52 208 66 200 80' stroke='#3a2410' stroke-width='1.6' fill='none'/>"
 # bridle + reins
 "<path d='M228 34 L250 64 M226 52 L256 52' stroke='#b8322a' stroke-width='3'/><circle cx='250' cy='60' r='3' fill='url(#gd)'/>"
 "<path d='M250 62 C236 90 200 96 176 92' stroke='#b8322a' stroke-width='2.4' fill='none'/>"
 # saddle with gold trim + a holly sprig
 "<path d='M126 92 C140 84 168 84 182 92 L186 112 C170 118 140 118 122 112 Z' fill='#1f5a32'/><path d='M122 112 C140 118 170 118 186 112' stroke='url(#gd)' stroke-width='3' fill='none'/>"
 "<path d='M150 116 L150 136' stroke='url(#gd)' stroke-width='3'/><rect x='142' y='134' width='16' height='5' rx='2' fill='url(#gd)'/>"
 "<path d='M196 82 c6 -8 16 -6 14 2 c-6 0 -10 4 -14 -2 Z M196 82 c-2 -10 6 -14 10 -8 c-4 2 -6 6 -10 8 Z' fill='#1f6a3a'/><circle cx='198' cy='86' r='3' fill='#d8202a'/><circle cx='203' cy='88' r='2.6' fill='#d8202a'/>"
 "</g></svg>")

def star_points(cx, cy, R, r, n, rot=0):
    pts = []
    for k in range(2 * n):
        a = math.radians(rot + k * 180 / n - 90); rr = R if k % 2 == 0 else r
        pts.append(f"{f(cx + rr*math.cos(a))} {f(cy + rr*math.sin(a))}")
    return "M" + " L".join(pts) + " Z"
ART["star"] = (f"<svg {W} viewBox='-110 0 220 340'><defs>"
 "<radialGradient id='lt' cx='.5' cy='.5' r='.5'><stop offset='0' stop-color='#fff6c8' stop-opacity='.9'/><stop offset='.4' stop-color='#ffc24a' stop-opacity='.45'/><stop offset='1' stop-color='#ff8a1a' stop-opacity='0'/></radialGradient>"
 "<linearGradient id='p1' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='#fff8dc'/><stop offset='.5' stop-color='#ffd36a'/><stop offset='1' stop-color='#d88a1a'/></linearGradient>"
 "<linearGradient id='p2' x1='1' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#ffe9a8'/><stop offset='1' stop-color='#b8641a'/></linearGradient>"
 "<linearGradient id='rb' x1='0' x2='1'><stop offset='0' stop-color='#8a0f14'/><stop offset='.5' stop-color='#e0323a'/><stop offset='1' stop-color='#8a0f14'/></linearGradient></defs>"
 # sways on its ribbon from the very top
 f"<g><animateTransform attributeName='transform' type='rotate' values='-3 0 0;3 0 0;-3 0 0' dur='5s' repeatCount='indefinite' {SPL}/>"
 "<path d='M0 0 V128' stroke='url(#rb)' stroke-width='5'/>"
 "<path d='M0 118 C-22 100 -34 116 -20 128 C-12 134 -4 130 0 124 C4 130 12 134 20 128 C34 116 22 100 0 118 Z' fill='url(#rb)'/>"
 "<path d='M-2 124 L-14 156 L-6 152 L-2 160 Z M2 124 L14 156 L6 152 L2 160 Z' fill='#b81c24'/><circle cx='0' cy='122' r='5' fill='#e0323a'/>"
 "<path d='M0 128 V146' stroke='#d8a040' stroke-width='2'/>"
 # glow, breathing
 "<circle cx='0' cy='238' r='106' fill='url(#lt)'><animate attributeName='opacity' values='.7;1;.75;.95;.7' dur='3.2s' repeatCount='indefinite'/></circle>"
 # paper star: back points, then front points split into lit and shaded halves
 f"<path d='{star_points(0, 238, 84, 30, 8, 22.5)}' fill='#c97a1a' opacity='.85'/>"
 + "".join(f"<path d='M0 238 L{f(84*math.cos(math.radians(a-90)))} {f(238 + 84*math.sin(math.radians(a-90)))} L{f(30*math.cos(math.radians(a-90+22.5)))} {f(238 + 30*math.sin(math.radians(a-90+22.5)))} Z' fill='url(#p1)'/>"
           f"<path d='M0 238 L{f(84*math.cos(math.radians(a-90)))} {f(238 + 84*math.sin(math.radians(a-90)))} L{f(30*math.cos(math.radians(a-90-22.5)))} {f(238 + 30*math.sin(math.radians(a-90-22.5)))} Z' fill='url(#p2)'/>" for a in range(0, 360, 45)) +
 f"<path d='{star_points(0, 238, 84, 30, 8)}' fill='none' stroke='#8a4a10' stroke-opacity='.5' stroke-width='1'/>"
 # pierced pattern lets light out
 + "".join(f"<circle cx='{f(52*math.cos(math.radians(a-90)))}' cy='{f(238 + 52*math.sin(math.radians(a-90)))}' r='2.6' fill='#fffbe6'><animate attributeName='opacity' values='1;.5;1' dur='{1.6 + (a % 90)/60:.1f}s' repeatCount='indefinite'/></circle>" for a in range(0, 360, 45)) +
 "<circle cx='0' cy='238' r='12' fill='#fff8dc'/><circle cx='0' cy='238' r='22' fill='none' stroke='#fff3c0' stroke-opacity='.8' stroke-dasharray='2 4'/>"
 # twinkles
 + "".join(f"<path d='M{x} {y-8} L{x+1.6} {y-1.6} L{x+8} {y} L{x+1.6} {y+1.6} L{x} {y+8} L{x-1.6} {y+1.6} L{x-8} {y} L{x-1.6} {y-1.6} Z' fill='#fff' opacity='0'><animate attributeName='opacity' values='0;1;0;0' keyTimes='0;.1;.2;1' dur='{d}s' begin='{b}s' repeatCount='indefinite'/></path>" for x, y, d, b in [(-70, 180, 3.4, 0), (76, 214, 2.9, -1.1), (-58, 300, 3.8, -2.2), (64, 296, 3.1, -.5)]) +
 "</g></svg>")

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for k, v in ART.items():
        open(f"{out}/prop-{k}.svg", "w").write(v); print(k, len(v))
