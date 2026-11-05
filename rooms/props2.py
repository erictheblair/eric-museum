# More room props. Run: python3 props2.py <outdir>  (also writes everything from props.py)
import sys, os, math, random
from props import ART, W, f

# ======================= MUSEUM =======================
marble = ("<linearGradient id='mb' x1='0' x2='1'><stop offset='0' stop-color='#8d887e'/><stop offset='.3' stop-color='#efeae0'/><stop offset='.55' stop-color='#fbf8f2'/><stop offset='.8' stop-color='#cfc8bb'/><stop offset='1' stop-color='#7c776d'/></linearGradient>"
          "<radialGradient id='mh' cx='.4' cy='.35' r='.7'><stop offset='0' stop-color='#fffdf8'/><stop offset='.6' stop-color='#e2dccf'/><stop offset='1' stop-color='#9c968a'/></radialGradient>"
          "<filter id='vein'><feTurbulence type='fractalNoise' baseFrequency='.02 .08' numOctaves='3' seed='4'/><feColorMatrix values='0 0 0 0 .45  0 0 0 0 .43  0 0 0 0 .4  0 0 0 -2.2 1.25'/><feComposite in2='SourceGraphic' operator='in'/></filter>")
def pedestal(top, w=84, cx=100, h=None):
    # column pedestal from y=top to 396
    x0 = cx - w/2
    return (f"<rect x='{x0-10}' y='{top}' width='{w+20}' height='14' rx='2' fill='url(#mb)'/><rect x='{x0-6}' y='{top+14}' width='{w+12}' height='6' fill='#a49e92'/>"
            f"<rect x='{x0}' y='{top+20}' width='{w}' height='{372-top-20}' fill='url(#mb)'/>"
            f"<rect x='{x0}' y='{top+20}' width='{w}' height='{372-top-20}' fill='#000' filter='url(#vein)'/>"
            + "".join(f"<path d='M{f(x0 + w*k/6)} {top+24} V{368}' stroke='#8a8478' stroke-opacity='.35' stroke-width='2'/>" for k in range(1, 6)) +
            f"<rect x='{x0-6}' y='372' width='{w+12}' height='8' fill='#a49e92'/><rect x='{x0-12}' y='380' width='{w+24}' height='16' rx='2' fill='url(#mb)'/>")
ART["bust"] = (f"<svg {W} viewBox='0 0 200 400'><defs>{marble}</defs>"
 "<ellipse cx='100' cy='396' rx='80' ry='6' fill='#000' opacity='.35'/>" + pedestal(200) +
 # bust: socle, chest with drape, neck, head with curls
 "<path d='M84 200 L116 200 L112 188 L88 188 Z' fill='url(#mb)'/><rect x='80' y='182' width='40' height='7' rx='2' fill='url(#mh)'/>"
 "<path d='M52 182 C52 150 68 136 86 132 L114 132 C132 136 148 150 148 182 Z' fill='url(#mh)'/>"
 "<path d='M60 182 C70 160 84 150 112 142 C122 148 132 160 140 182 Z' fill='#d8d1c3' opacity='.7'/>"
 "<path d='M70 182 C80 166 96 156 118 150 M84 182 C92 170 104 162 124 158 M100 182 C106 174 116 168 132 166' stroke='#a8a194' stroke-width='1.6' fill='none'/>"
 "<path d='M88 136 C88 124 90 116 92 112 L108 112 C110 116 112 124 112 136 Z' fill='url(#mh)'/>"
 "<path d='M80 84 C78 62 90 50 102 50 C116 50 124 62 122 84 C121 98 114 110 104 114 C96 116 84 108 81 96 Z' fill='url(#mh)'/>"
 # nose/brow shading (3/4 view to the left)
 "<path d='M88 80 C86 88 84 92 87 95 L92 95' stroke='#a39c8e' stroke-width='1.6' fill='none'/>"
 "<path d='M84 74 C88 71 92 71 95 74 M100 73 C104 70 108 70 111 73' stroke='#9c958a' stroke-width='1.4' fill='none'/>"
 "<path d='M88 102 C92 104 96 104 99 102' stroke='#9c958a' stroke-width='1.3' fill='none'/>"
 "<path d='M112 84 C116 80 120 84 118 92 C116 96 113 96 112 92' fill='#d4cdbf' stroke='#a39c8e' stroke-width='1'/>"
 # curls + laurel
 + "".join(f"<circle cx='{f(102 + 22*math.cos(math.radians(a)))}' cy='{f(70 - 22*math.sin(math.radians(a))*1.05)}' r='6' fill='url(#mh)' stroke='#aaa294' stroke-width='.8'/>" for a in range(10, 180, 18)) +
 "".join(f"<ellipse cx='{f(102 + 20*math.cos(math.radians(a)))}' cy='{f(68 - 20*math.sin(math.radians(a)))}' rx='5' ry='2.2' transform='rotate({-a+90} {f(102 + 20*math.cos(math.radians(a)))} {f(68 - 20*math.sin(math.radians(a)))})' fill='#c9c1b2'/>" for a in range(30, 160, 22)) +
 "</svg>")
ART["amphora"] = (f"<svg {W} viewBox='0 0 200 400'><defs>{marble}"
 "<linearGradient id='tc' x1='0' x2='1'><stop offset='0' stop-color='#6b2a10'/><stop offset='.35' stop-color='#c9682c'/><stop offset='.55' stop-color='#e08a48'/><stop offset='1' stop-color='#5a220c'/></linearGradient>"
 "<clipPath id='bd'><path d='M70 120 C46 150 50 196 78 216 L122 216 C150 196 154 150 130 120 Z'/></clipPath></defs>"
 "<ellipse cx='100' cy='396' rx='80' ry='6' fill='#000' opacity='.35'/>" + pedestal(232) +
 "<ellipse cx='100' cy='230' rx='22' ry='4' fill='#3a1606'/><path d='M86 230 L88 218 L112 218 L114 230 Z' fill='url(#tc)'/>"
 "<path d='M88 60 L112 60 L110 76 C110 92 132 104 140 130 C152 168 140 200 112 218 L88 218 C60 200 48 168 60 130 C68 104 90 92 90 76 Z' fill='url(#tc)'/>"
 "<ellipse cx='100' cy='60' rx='18' ry='4' fill='#2a0e04'/><ellipse cx='100' cy='58' rx='20' ry='4.5' fill='none' stroke='#c9682c' stroke-width='3'/>"
 "<path d='M90 82 C70 80 64 100 72 116' stroke='#8a3a16' stroke-width='5' fill='none'/><path d='M110 82 C130 80 136 100 128 116' stroke='#8a3a16' stroke-width='5' fill='none'/>"
 # black-figure band
 "<g clip-path='url(#bd)'><rect x='40' y='140' width='120' height='46' fill='#1a0d08'/><rect x='40' y='138' width='120' height='3' fill='#e08a48'/><rect x='40' y='185' width='120' height='3' fill='#e08a48'/>"
 "<g fill='#e08a48'><circle cx='82' cy='152' r='4'/><path d='M80 156 L76 172 L72 182 M80 156 L86 172 L90 182 M80 160 L70 164 M80 160 L94 154' stroke='#e08a48' stroke-width='2.6' fill='none'/>"
 "<circle cx='118' cy='152' r='4'/><path d='M118 156 L114 172 L110 182 M118 156 L124 172 L128 182 M118 160 L104 156 M118 160 L128 166' stroke='#e08a48' stroke-width='2.6' fill='none'/>"
 "<path d='M100 146 L100 184' stroke='#e08a48' stroke-width='1.4' stroke-dasharray='3 3'/></g></g>"
 + "".join(f"<path d='M{70 + k*8} 196 l4 -6 l4 6' stroke='#1a0d08' stroke-width='1.6' fill='none'/>" for k in range(8)) +
 "<path d='M66 130 C60 160 66 190 84 208' stroke='#fff' stroke-opacity='.18' stroke-width='5' fill='none'/>"
 "</svg>")

# ======================= MODERN GALLERY =======================
def arm(len_l, len_r, children_l, children_r, dur, amp, begin=0):
    # balanced arm hanging from (0,0): string down 30, bar across, children at each end
    return (f"<g><animateTransform attributeName='transform' type='rotate' values='{-amp} 0 0;{amp} 0 0;{-amp} 0 0' dur='{dur}s' begin='{begin}s' repeatCount='indefinite' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1'/>"
            f"<path d='M0 0 V30' stroke='#222' stroke-width='1'/><path d='M{-len_l} 30 H{len_r}' stroke='#111' stroke-width='2.2' stroke-linecap='round'/>"
            f"<g transform='translate({-len_l} 30)'>{children_l}</g><g transform='translate({len_r} 30)'>{children_r}</g></g>")
disc = lambda r, c, dy=26: f"<path d='M0 0 V{dy-r}' stroke='#222' stroke-width='1'/><ellipse cy='{dy}' rx='{r}' ry='{r*.9}' fill='{c}'/>"
leaf = lambda r, c, dy=24: f"<path d='M0 0 V{dy-r*.6}' stroke='#222' stroke-width='1'/><path d='M0 {dy-r} C{r} {dy-r} {r*1.2} {dy+r*.6} 0 {dy+r} C{-r*.4} {dy+r*.2} {-r*.6} {dy-r*.4} 0 {dy-r}Z' fill='{c}'/>"
mob = arm(70, 60,
          arm(36, 30, disc(14, '#d72a1f'), arm(18, 22, disc(9, '#111'), leaf(10, '#f2c230'), 5.5, 9, -1), 7.5, 7, -2),
          arm(26, 40, leaf(13, '#1d4fa3'), arm(20, 16, disc(10, '#f2c230'), disc(7, '#d72a1f'), 4.8, 10, -3), 6.4, 8, -1.2),
          11, 5)
ART["mobile"] = (f"<svg {W} viewBox='-140 0 280 300'><path d='M0 0 V40' stroke='#222' stroke-width='1'/><g transform='translate(0 40)'>{mob}</g></svg>")
ART["sculpture"] = (f"<svg {W} viewBox='0 0 200 400'><defs>"
 "<linearGradient id='pl' x1='0' x2='1'><stop offset='0' stop-color='#d9d9d6'/><stop offset='.5' stop-color='#fbfbfa'/><stop offset='1' stop-color='#c4c4c0'/></linearGradient>"
 "<linearGradient id='br' x1='0' x2='1'><stop offset='0' stop-color='#6a4510'/><stop offset='.4' stop-color='#f2c766'/><stop offset='.6' stop-color='#fff1c0'/><stop offset='1' stop-color='#7a5014'/></linearGradient>"
 "<radialGradient id='bs' cx='.35' cy='.35' r='.7'><stop offset='0' stop-color='#fff'/><stop offset='.5' stop-color='#d9d9d9'/><stop offset='1' stop-color='#555'/></radialGradient></defs>"
 "<ellipse cx='100' cy='396' rx='70' ry='5' fill='#000' opacity='.18'/>"
 "<rect x='50' y='250' width='100' height='146' fill='url(#pl)'/><rect x='50' y='250' width='100' height='4' fill='#fff'/><rect x='50' y='392' width='100' height='4' fill='#bdbdb8'/>"
 # big brass ring that turns (fake 3D via scaleX), chrome sphere inside, black slab base
 "<rect x='76' y='238' width='48' height='12' fill='#1b1b1b'/>"
 "<g transform='translate(100 170)'><g><animateTransform attributeName='transform' type='scale' values='1 1;.18 1;1 1;.18 1;1 1' dur='14s' repeatCount='indefinite' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1;.45 0 .55 1;.45 0 .55 1'/>"
 "<circle r='62' fill='none' stroke='url(#br)' stroke-width='12'/></g>"
 "<circle cy='18' r='24' fill='url(#bs)'/><path d='M0 42 V68' stroke='#1b1b1b' stroke-width='6'/></g>"
 "</svg>")

# ======================= LIBRARY =======================
cont = ("<path d='M10 20 C20 8 40 10 46 22 C50 32 40 40 44 52 C36 60 24 52 20 44 C12 40 4 30 10 20Z'/>"
        "<path d='M58 14 C70 8 92 12 98 20 C104 30 90 34 84 30 C78 40 82 52 74 60 C66 56 70 44 62 38 C54 32 52 22 58 14Z'/>"
        "<path d='M30 62 C38 58 46 64 44 74 C42 84 34 90 30 84 C26 76 24 68 30 62Z'/><path d='M86 66 C94 62 104 66 102 74 C98 80 90 78 86 66Z'/>")
ART["globe"] = (f"<svg {W} viewBox='0 0 200 400'><defs>"
 "<radialGradient id='sea' cx='.38' cy='.35' r='.75'><stop offset='0' stop-color='#f3e2b4'/><stop offset='.7' stop-color='#d8bd82'/><stop offset='1' stop-color='#7d6438'/></radialGradient>"
 "<radialGradient id='sh' cx='.35' cy='.32' r='.75'><stop offset='.45' stop-color='#000' stop-opacity='0'/><stop offset='1' stop-color='#000' stop-opacity='.55'/></radialGradient>"
 "<linearGradient id='wd' x1='0' x2='1'><stop offset='0' stop-color='#3a1d0c'/><stop offset='.5' stop-color='#8a4f22'/><stop offset='1' stop-color='#341a0a'/></linearGradient>"
 "<linearGradient id='bz' x1='0' x2='1'><stop offset='0' stop-color='#7a5418'/><stop offset='.5' stop-color='#f5d27a'/><stop offset='1' stop-color='#6b4612'/></linearGradient>"
 "<clipPath id='gb'><circle cx='100' cy='160' r='62'/></clipPath></defs>"
 "<ellipse cx='100' cy='394' rx='70' ry='6' fill='#000' opacity='.4'/>"
 # tripod stand
 "<path d='M100 250 V392' stroke='#5a3216' stroke-width='9'/><path d='M96 250 L56 392 M104 250 L144 392' stroke='url(#wd)' stroke-width='9' stroke-linecap='round'/>"
 "<path d='M70 340 H130' stroke='#5a3216' stroke-width='6'/><ellipse cx='100' cy='250' rx='70' ry='12' fill='url(#wd)'/><ellipse cx='100' cy='246' rx='70' ry='11' fill='#9a5c2a'/>"
 # sphere with drifting map
 "<circle cx='100' cy='160' r='62' fill='url(#sea)'/>"
 f"<g clip-path='url(#gb)'><g fill='#6e8b4a' stroke='#4a5e30' stroke-width='.8' transform='translate(0 120)'><g><animateTransform attributeName='transform' type='translate' values='0 0;-110 0' dur='22s' repeatCount='indefinite'/>"
 + "".join(f"<g transform='translate({x} 0)'>{cont}</g>" for x in (40, 150, 260)) + "</g></g>"
 "<g stroke='#8a6a3a' stroke-width='.6' fill='none' opacity='.6'><ellipse cx='100' cy='160' rx='62' ry='14'/><ellipse cx='100' cy='160' rx='62' ry='34'/><path d='M38 160 H162'/><ellipse cx='100' cy='160' rx='22' ry='62'/><ellipse cx='100' cy='160' rx='46' ry='62'/></g></g>"
 "<circle cx='100' cy='160' r='62' fill='url(#sh)'/><ellipse cx='80' cy='132' rx='16' ry='10' fill='#fff' opacity='.25' transform='rotate(-30 80 132)'/>"
 # brass meridian ring
 "<path d='M100 88 A72 72 0 1 1 99.9 88' fill='none' stroke='url(#bz)' stroke-width='6' transform='rotate(-20 100 160)'/>"
 "<circle cx='100' cy='160' r='4' fill='url(#bz)'/><path d='M100 232 V248' stroke='#c9a24a' stroke-width='7'/>"
 "</svg>")
ART["lamp"] = (f"<svg {W} viewBox='0 0 220 400'><defs>"
 "<radialGradient id='lg' cx='.5' cy='.4' r='.5'><stop offset='0' stop-color='#ffe2a0' stop-opacity='.7'/><stop offset='1' stop-color='#ffb84a' stop-opacity='0'/></radialGradient>"
 "<linearGradient id='gs' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#3d8a52'/><stop offset='.6' stop-color='#14532a'/><stop offset='1' stop-color='#0c3a1c'/></linearGradient>"
 "<linearGradient id='bz' x1='0' x2='1'><stop offset='0' stop-color='#7a5418'/><stop offset='.5' stop-color='#f5d27a'/><stop offset='1' stop-color='#6b4612'/></linearGradient>"
 "<linearGradient id='wd' x1='0' x2='1'><stop offset='0' stop-color='#2e1608'/><stop offset='.5' stop-color='#7a4420'/><stop offset='1' stop-color='#2a1407'/></linearGradient></defs>"
 "<ellipse cx='110' cy='200' rx='110' ry='150' fill='url(#lg)'><animate attributeName='opacity' values='1;.85;1;.95;1' dur='4s' repeatCount='indefinite'/></ellipse>"
 "<ellipse cx='110' cy='394' rx='86' ry='6' fill='#000' opacity='.45'/>"
 # table
 "<rect x='30' y='250' width='160' height='14' rx='3' fill='url(#wd)'/><rect x='38' y='264' width='144' height='26' fill='#4a260f'/><rect x='96' y='270' width='28' height='5' rx='2' fill='url(#bz)'/>"
 "<path d='M44 290 L50 392 M176 290 L170 392' stroke='url(#wd)' stroke-width='10' stroke-linecap='round'/>"
 # books
 "<rect x='120' y='232' width='62' height='18' rx='2' fill='#7a1d1d'/><rect x='124' y='216' width='54' height='16' rx='2' fill='#1d3a6a'/><rect x='118' y='202' width='58' height='14' rx='2' fill='#2d5a2a'/>"
 "<path d='M120 238 H182 M124 222 H178 M118 208 H176' stroke='#e2c27a' stroke-width='1.2'/>"
 # lamp
 "<rect x='48' y='238' width='56' height='12' rx='5' fill='url(#bz)'/><path d='M76 238 V180' stroke='#c9a24a' stroke-width='5'/>"
 "<path d='M40 182 C40 166 52 160 76 160 C100 160 112 166 112 182 Z' fill='url(#gs)'/><path d='M40 182 H112' stroke='url(#bz)' stroke-width='3'/>"
 "<path d='M48 168 C56 163 68 162 80 162' stroke='#fff' stroke-opacity='.35' stroke-width='2' fill='none'/>"
 "<ellipse cx='76' cy='184' rx='32' ry='4' fill='#fff3c4'/><path d='M100 184 V204' stroke='#c9a24a' stroke-width='1.4'/><circle cx='100' cy='206' r='2.2' fill='url(#bz)'/>"
 # open book + teacup
 "<path d='M8 250 L44 246 L80 250 L80 244 L44 240 L8 244 Z' fill='#f4ead2'/><path d='M44 240 V246' stroke='#b9a986' stroke-width='1'/>"
 "</svg>")

# ======================= CASTLE =======================
st = ("<linearGradient id='st' x1='0' x2='1'><stop offset='0' stop-color='#3a3f44'/><stop offset='.35' stop-color='#c9d0d6'/><stop offset='.5' stop-color='#f4f7f9'/><stop offset='.7' stop-color='#9aa3aa'/><stop offset='1' stop-color='#2f3438'/></linearGradient>"
      "<radialGradient id='sr' cx='.38' cy='.32' r='.75'><stop offset='0' stop-color='#f4f7f9'/><stop offset='.55' stop-color='#9aa3aa'/><stop offset='1' stop-color='#30353a'/></radialGradient>")
ART["armor"] = (f"<svg {W} viewBox='0 0 200 420'><defs>{st}</defs>"
 "<ellipse cx='100' cy='414' rx='70' ry='6' fill='#000' opacity='.45'/>"
 # halberd behind
 "<path d='M160 24 V410' stroke='#4a2e16' stroke-width='5'/><path d='M160 30 L176 46 L176 74 L160 66 Z M160 40 L144 50 L148 58 L160 54 Z' fill='url(#st)'/><path d='M160 6 L164 30 L156 30 Z' fill='url(#st)'/>"
 # base plinth
 "<rect x='52' y='396' width='96' height='16' rx='2' fill='#2a2522'/>"
 # legs
 "<path d='M78 260 L72 330 L70 392 L92 392 L94 330 L98 262 Z' fill='url(#st)'/><path d='M122 260 L128 330 L130 392 L108 392 L106 330 L102 262 Z' fill='url(#st)'/>"
 "<ellipse cx='82' cy='326' rx='12' ry='10' fill='url(#sr)'/><ellipse cx='118' cy='326' rx='12' ry='10' fill='url(#sr)'/>"
 "<path d='M66 392 L96 392 L98 400 L60 400 Z M104 392 L134 392 L140 400 L102 400 Z' fill='url(#st)'/>"
 # tassets/skirt
 "<path d='M68 230 L132 230 L138 262 L62 262 Z' fill='url(#st)'/><path d='M66 244 H134 M64 254 H136' stroke='#3a3f44' stroke-width='1'/>"
 # torso
 "<path d='M64 140 C64 126 80 118 100 118 C120 118 136 126 136 140 L132 230 L68 230 Z' fill='url(#st)'/>"
 "<path d='M100 122 V226' stroke='#5a6168' stroke-width='1.2'/><path d='M72 200 H128 M74 214 H126' stroke='#3a3f44' stroke-width='1'/>"
 # pauldrons + arms (gauntlet resting on halberd)
 "<ellipse cx='60' cy='136' rx='20' ry='16' fill='url(#sr)'/><ellipse cx='140' cy='136' rx='20' ry='16' fill='url(#sr)'/>"
 "<path d='M48 146 L44 204 L56 206 L62 150 Z' fill='url(#st)'/><path d='M44 204 L46 240 L58 240 L56 206 Z' fill='url(#st)'/><ellipse cx='52' cy='246' rx='9' ry='11' fill='url(#sr)'/>"
 "<path d='M150 146 L156 180 L160 178 L152 144 Z' fill='url(#st)'/><path d='M156 180 L160 126 L168 126 L164 182 Z' fill='url(#st)'/><ellipse cx='163' cy='122' rx='8' ry='9' fill='url(#sr)'/>"
 # helmet with visor slits and plume
 "<path d='M78 112 C74 82 84 62 100 62 C116 62 126 82 122 112 C116 120 84 120 78 112 Z' fill='url(#sr)'/>"
 "<path d='M80 92 H120 M80 98 H120' stroke='#111' stroke-width='2.4'/><path d='M100 64 V116' stroke='#5a6168' stroke-width='1.2'/>"
 "<path d='M100 62 C96 40 110 26 128 28 C116 34 112 44 116 56 C110 50 106 54 104 62 Z' fill='#9a1c22'><animateTransform attributeName='transform' type='rotate' values='0 100 62;4 100 62;0 100 62' dur='5s' repeatCount='indefinite'/></path>"
 # glint that slides down the armor now and then
 "<rect x='60' y='-40' width='90' height='14' fill='#fff' opacity='.0' transform='skewY(-20)'><animate attributeName='y' values='40;420' dur='6s' repeatCount='indefinite'/><animate attributeName='opacity' values='0;.35;0;0' keyTimes='0;.15;.3;1' dur='6s' repeatCount='indefinite'/></rect>"
 "</svg>")
def banner(bg, fg, emblem):
    return (f"<svg {W} viewBox='0 0 140 340'><defs><linearGradient id='fold' x1='0' x2='1'><stop offset='0' stop-color='#000' stop-opacity='.35'/><stop offset='.2' stop-color='#000' stop-opacity='0'/><stop offset='.5' stop-color='#fff' stop-opacity='.08'/><stop offset='.8' stop-color='#000' stop-opacity='0'/><stop offset='1' stop-color='#000' stop-opacity='.35'/></linearGradient>"
            "<linearGradient id='gd' x1='0' x2='1'><stop offset='0' stop-color='#7a5418'/><stop offset='.5' stop-color='#f5d27a'/><stop offset='1' stop-color='#6b4612'/></linearGradient></defs>"
            "<path d='M8 14 H132' stroke='#3a2410' stroke-width='7' stroke-linecap='round'/><circle cx='8' cy='14' r='6' fill='url(#gd)'/><circle cx='132' cy='14' r='6' fill='url(#gd)'/>"
            "<g><animateTransform attributeName='transform' type='skewX' values='0;1.6;0;-1.2;0' dur='7s' repeatCount='indefinite'/>"
            f"<path d='M18 18 H122 V300 L70 330 L18 300 Z' fill='{bg}'/>"
            f"<path d='M26 26 H114 V294 L70 320 L26 294 Z' fill='none' stroke='{fg}' stroke-width='3'/>"
            f"{emblem}"
            "<path d='M18 18 H122 V300 L70 330 L18 300 Z' fill='url(#fold)'/>"
            + "".join(f"<path d='M{x} 300 l0 0' />" for x in ()) +
            "</g></svg>")
crown = ("<g fill='url(#gd)'><path d='M44 118 L50 86 L60 104 L70 80 L80 104 L90 86 L96 118 Z'/><rect x='44' y='118' width='52' height='9' rx='2'/>"
         "<circle cx='50' cy='84' r='4'/><circle cx='70' cy='78' r='4'/><circle cx='90' cy='84' r='4'/></g>"
         "<g stroke='url(#gd)' stroke-width='6' stroke-linecap='round'><path d='M48 150 L92 214 M92 150 L48 214'/></g>"
         "<g fill='url(#gd)'><circle cx='48' cy='150' r='9'/><circle cx='92' cy='150' r='9'/><rect x='84' y='206' width='18' height='8' transform='rotate(55 92 214)'/><rect x='38' y='206' width='18' height='8' transform='rotate(-55 48 214)'/></g>")
tower = ("<g fill='url(#gd)'><path d='M46 230 V140 H54 V128 H62 V140 H78 V128 H86 V140 H94 V230 Z'/><path d='M64 230 V196 C64 186 76 186 76 196 V230 Z' fill='#1d2a5a'/></g>"
         "<g fill='url(#gd)'><path d='M70 70 L76 86 L94 86 L80 96 L85 112 L70 102 L55 112 L60 96 L46 86 L64 86 Z'/></g>")
ART["banner1"] = banner('#8f1720', '#e6b84a', crown)
ART["banner2"] = banner('#1d2a5a', '#e6b84a', tower)

# ======================= CABIN =======================
def flame(cx, base, h, w, col, dur, begin):
    return (f"<g transform='translate({cx} {base})'><path d='M{-w} 0 C{-w} {-h*.5} {-w*.2} {-h*.6} 0 {-h} C{w*.3} {-h*.6} {w} {-h*.5} {w} 0 Z' fill='{col}'>"
            f"<animateTransform attributeName='transform' type='scale' values='1 1;1.06 .82;.94 1.12;1.04 .9;1 1' dur='{dur}s' begin='{begin}s' repeatCount='indefinite'/>"
            f"<animateTransform attributeName='transform' type='skewX' additive='sum' values='0;4;-5;3;0' dur='{dur*1.3:.2f}s' begin='{begin}s' repeatCount='indefinite'/></path></g>")
rs = random.Random(11)
stones = "".join(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{min(w,h)*.4:.1f}' fill='{c}' stroke='#2a2420' stroke-width='1.2'/>"
                 for x, y, w, h, c in [(rs.randint(6, 214), rs.randint(70, 380), rs.randint(18, 34), rs.randint(12, 20), rs.choice(['#7a6e62', '#8d8174', '#6a5f55', '#9a8d7d', '#5f554c'])) for _ in range(150)])
ART["fireplace"] = (f"<svg {W} viewBox='0 0 240 400'><defs>"
 "<radialGradient id='glow' cx='.5' cy='.78' r='.6'><stop offset='0' stop-color='#ffb04a' stop-opacity='.65'/><stop offset='1' stop-color='#ff6a1a' stop-opacity='0'/></radialGradient>"
 "<radialGradient id='hole' cx='.5' cy='.9' r='.9'><stop offset='0' stop-color='#4a1a06'/><stop offset='.6' stop-color='#120604'/><stop offset='1' stop-color='#050202'/></radialGradient>"
 "<linearGradient id='mt' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#7a4420'/><stop offset='1' stop-color='#3a1d0c'/></linearGradient>"
 "<clipPath id='fc'><rect x='6' y='70' width='228' height='326'/></clipPath><clipPath id='hc'><path d='M58 392 V290 C58 258 86 244 120 244 C154 244 182 258 182 290 V392 Z'/></clipPath></defs>"
 "<ellipse cx='120' cy='330' rx='150' ry='120' fill='url(#glow)'><animate attributeName='opacity' values='.9;.7;1;.8;.9' dur='1.7s' repeatCount='indefinite'/></ellipse>"
 f"<rect x='6' y='70' width='228' height='326' fill='#6a5f55'/><g clip-path='url(#fc)'>{stones}</g>"
 "<rect x='6' y='70' width='228' height='326' fill='#000' opacity='.15'/>"
 # mantel with candles + clock
 "<rect x='0' y='196' width='240' height='18' rx='2' fill='url(#mt)'/><rect x='6' y='214' width='228' height='6' fill='#2a1407'/>"
 "<rect x='30' y='168' width='10' height='28' fill='#f2ead6'/><path d='M35 168 V165' stroke='#2a1a10' stroke-width='1'/><g transform='translate(35 166)'><ellipse cy='-6' rx='7' ry='9' fill='#ffcf5a' opacity='.25'/><path d='M0 0 C-3.6 -3 -2.6 -9 0 -15 C2.6 -9 3.6 -3 0 0Z' fill='#ffcf5a'><animateTransform attributeName='transform' type='skewX' values='0;6;-4;0' dur='1.3s' repeatCount='indefinite'/><animateTransform attributeName='transform' type='scale' additive='sum' values='1 1;.92 1.12;1.05 .9;1 1' dur='0.91s' repeatCount='indefinite'/></path><path d='M0 -1 C-1.4 -3 -1 -6 0 -8 C1 -6 1.4 -3 0 -1Z' fill='#fff6d0'/></g>"
 "<rect x='200' y='176' width='10' height='20' fill='#f2ead6'/><path d='M205 176 V173' stroke='#2a1a10' stroke-width='1'/><g transform='translate(205 174)'><ellipse cy='-6' rx='7' ry='9' fill='#ffcf5a' opacity='.25'/><path d='M0 0 C-3.6 -3 -2.6 -9 0 -15 C2.6 -9 3.6 -3 0 0Z' fill='#ffcf5a'><animateTransform attributeName='transform' type='skewX' values='0;-5;5;0' dur='1.1s' repeatCount='indefinite'/><animateTransform attributeName='transform' type='scale' additive='sum' values='1 1;.92 1.12;1.05 .9;1 1' dur='0.77s' repeatCount='indefinite'/></path><path d='M0 -1 C-1.4 -3 -1 -6 0 -8 C1 -6 1.4 -3 0 -1Z' fill='#fff6d0'/></g>"
 "<path d='M104 196 V160 C104 146 136 146 136 160 V196 Z' fill='#5a3216'/><circle cx='120' cy='166' r='11' fill='#f4ead2' stroke='#c9a24a' stroke-width='2'/><path d='M120 166 V158 M120 166 L126 168' stroke='#222' stroke-width='1.4'/>"
 # firebox
 "<path d='M50 396 V290 C50 252 82 236 120 236 C158 236 190 252 190 290 V396 Z' fill='#3a312b'/>"
 "<path d='M58 392 V290 C58 258 86 244 120 244 C154 244 182 258 182 290 V392 Z' fill='url(#hole)'/>"
 "<g clip-path='url(#hc)'>"
 + flame(120, 378, 92, 40, '#ff5a12', 1.3, 0) + flame(98, 380, 64, 22, '#ff7a1a', 1.05, -.4) + flame(144, 380, 70, 24, '#ff7a1a', 1.2, -.7)
 + flame(120, 380, 60, 24, '#ffb02a', .9, -.2) + flame(108, 380, 36, 12, '#ffe07a', .7, -.3) + flame(132, 380, 40, 12, '#ffe07a', .8, -.5) +
 "".join(f"<circle cx='{x}' cy='370' r='1.6' fill='#ffd06a'><animate attributeName='cy' values='370;250' dur='{d}s' begin='{b}s' repeatCount='indefinite'/><animate attributeName='opacity' values='1;0' dur='{d}s' begin='{b}s' repeatCount='indefinite'/><animate attributeName='cx' values='{x};{x+12};{x-6}' dur='{d}s' begin='{b}s' repeatCount='indefinite'/></circle>" for x, d, b in [(110, 2.2, 0), (130, 2.6, -1), (120, 1.9, -1.4), (100, 2.4, -.6)]) +
 "</g>"
 # logs + grate
 "<g><rect x='72' y='372' width='96' height='14' rx='7' fill='#4a2a14' transform='rotate(-6 120 379)'/><rect x='72' y='374' width='96' height='14' rx='7' fill='#5a3418' transform='rotate(7 120 381)'/>"
 "<circle cx='76' cy='380' r='6' fill='#c9965a'/><circle cx='164' cy='382' r='6' fill='#c9965a'/></g>"
 "<path d='M64 390 H176' stroke='#111' stroke-width='5'/>" + "".join(f"<path d='M{x} 390 V378' stroke='#111' stroke-width='3'/>" for x in range(72, 176, 14)) +
 "<rect x='40' y='388' width='160' height='12' fill='#4a413a'/>"
 "</svg>")
ART["rocker"] = (f"<svg {W} viewBox='0 0 200 300'><defs><linearGradient id='wd' x1='0' x2='1'><stop offset='0' stop-color='#4a2510'/><stop offset='.5' stop-color='#8a4f22'/><stop offset='1' stop-color='#3a1d0c'/></linearGradient>"
 "<pattern id='pl' width='20' height='20' patternUnits='userSpaceOnUse'><rect width='20' height='20' fill='#a8231e'/><rect width='20' height='7' y='7' fill='#1d2a1a' opacity='.55'/><rect height='20' width='7' x='7' fill='#1d2a1a' opacity='.55'/><path d='M0 3 H20 M3 0 V20' stroke='#e2c27a' stroke-width='1' opacity='.6'/></pattern></defs>"
 "<ellipse cx='100' cy='292' rx='74' ry='5' fill='#000' opacity='.45'/>"
 # side profile, facing right; rocks about the point where the rocker touches the floor
 "<g><animateTransform attributeName='transform' type='rotate' values='-7 100 288;6 100 288;-7 100 288' dur='3.6s' repeatCount='indefinite' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1'/>"
 # far-side parts, darker
 "<g stroke='#3a1d0c' stroke-linecap='round' fill='none'><path d='M74 274 L80 196 L58 44' stroke-width='7'/><path d='M150 274 L146 196' stroke-width='7'/><path d='M66 146 H156' stroke-width='6'/></g>"
 # rocker runner
 "<path d='M14 262 C50 290 140 292 192 266' stroke='url(#wd)' stroke-width='9' fill='none' stroke-linecap='round'/>"
 # back post (leans back), front leg, seat, arm
 "<path d='M66 280 L72 196 L46 40' stroke='#6a3a18' stroke-width='10' fill='none' stroke-linecap='round' stroke-linejoin='round'/>"
 "<path d='M44 34 C42 28 52 26 54 32' stroke='#6a3a18' stroke-width='9' fill='none' stroke-linecap='round'/>"
 "<path d='M146 282 L142 196' stroke='#6a3a18' stroke-width='10' stroke-linecap='round'/>"
 "<path d='M60 190 L156 186 L156 198 L62 202 Z' fill='url(#wd)'/>"
 "<path d='M56 140 C90 136 130 136 158 140' stroke='#7a4420' stroke-width='8' fill='none' stroke-linecap='round'/><path d='M150 140 L146 188' stroke='#6a3a18' stroke-width='7'/>"
 "<path d='M70 232 L144 230' stroke='#5a3216' stroke-width='5'/>"
 # back spindles seen edge-on
 + "".join(f"<path d='M{f(72 - k*4.2)} {196 - k*30} l-1 -6' stroke='#5a3216' stroke-width='3'/>" for k in range(1, 5)) +
 # plaid blanket draped over the back and onto the seat
 "<path d='M40 46 C50 40 60 44 60 52 L72 120 C76 150 80 176 98 186 L104 206 L84 214 L80 202 C66 196 58 170 54 140 C48 110 42 80 40 46 Z' fill='url(#pl)'/>"
 "<path d='M40 46 C50 40 60 44 60 52 L72 120 C76 150 80 176 98 186 L104 206 L84 214 L80 202 C66 196 58 170 54 140 C48 110 42 80 40 46 Z' fill='none' stroke='#5a100c' stroke-width='1.5'/>"
 "<path d='M50 70 C56 110 62 150 76 190' stroke='#000' stroke-opacity='.2' stroke-width='5' fill='none'/>"
 "</g></svg>")

# ======================= GREENHOUSE =======================
ART["planter"] = (f"<svg {W} viewBox='0 0 200 360'><defs><linearGradient id='tc' x1='0' x2='1'><stop offset='0' stop-color='#7a3416'/><stop offset='.4' stop-color='#d0703a'/><stop offset='1' stop-color='#6a2c12'/></linearGradient></defs>"
 "<g><animateTransform attributeName='transform' type='rotate' values='-3 100 0;3 100 0;-3 100 0' dur='6s' repeatCount='indefinite' calcMode='spline' keySplines='.45 0 .55 1;.45 0 .55 1'/>"
 "<path d='M100 0 L64 150 M100 0 L136 150 M100 0 V146' stroke='#c9b48a' stroke-width='2'/>"
 # trailing vines
 + "".join(
   f"<g><animateTransform attributeName='transform' type='rotate' values='{-a} {x} 170;{a} {x} 170;{-a} {x} 170' dur='{d}s' repeatCount='indefinite'/>"
   f"<path d='M{x} 170 C{x+sx} {170+L*.3} {x-sx} {170+L*.7} {x+sx*.4} {170+L}' stroke='#2f6a2a' stroke-width='2' fill='none'/>"
   + "".join(f"<ellipse cx='{f(x + sx*math.sin(t*3.1)*.6)}' cy='{f(170 + L*t)}' rx='{f(9 - t*3)}' ry='{f(5 - t*1.5)}' fill='{c}' transform='rotate({(-1)**k * 35} {f(x + sx*math.sin(t*3.1)*.6)} {f(170 + L*t)})'/>"
             for k, t in enumerate([i/9 for i in range(1, 10)]) for c in [['#3f8a3a', '#56a64a', '#2f7a30'][k % 3]]) + "</g>"
   for x, L, sx, a, d in [(70, 150, 10, 3, 5.2), (92, 180, -8, 2, 6.1), (112, 130, 9, 3, 4.7), (132, 160, -10, 2.5, 5.6)]) +
 "<path d='M60 146 H140 L132 196 C120 204 80 204 68 196 Z' fill='url(#tc)'/><rect x='56' y='140' width='88' height='12' rx='3' fill='#c0602e'/>"
 # leaves spilling over the rim
 + "".join(f"<ellipse cx='{x}' cy='{y}' rx='14' ry='7' fill='{c}' transform='rotate({r} {x} {y})'/>" for x, y, r, c in [(66, 138, -30, '#3f8a3a'), (84, 132, -10, '#56a64a'), (104, 130, 8, '#2f7a30'), (124, 134, 26, '#56a64a'), (138, 140, 40, '#3f8a3a'), (94, 124, -60, '#4c9a40'), (114, 122, 60, '#3f8a3a')]) +
 "<g fill='#f06a9a'><circle cx='80' cy='128' r='4'/><circle cx='118' cy='126' r='4'/><circle cx='100' cy='118' r='3.4' fill='#ffd04a'/></g>"
 "</g></svg>")
def butterfly(c1, c2, flap):
    return (f"<g><g><animateTransform attributeName='transform' type='scale' values='1 1;.2 1;1 1' dur='{flap}s' repeatCount='indefinite'/>"
            f"<path d='M0 0 C-14 -16 -24 -6 -18 4 C-14 10 -6 6 0 2 Z' fill='{c1}'/><path d='M0 2 C-10 6 -14 16 -6 16 C-2 14 0 8 0 4 Z' fill='{c2}'/>"
            f"<path d='M0 0 C14 -16 24 -6 18 4 C14 10 6 6 0 2 Z' fill='{c1}'/><path d='M0 2 C10 6 14 16 6 16 C2 14 0 8 0 4 Z' fill='{c2}'/>"
            "<circle cx='-12' cy='-4' r='2' fill='#fff' opacity='.7'/><circle cx='12' cy='-4' r='2' fill='#fff' opacity='.7'/></g>"
            "<path d='M0 -4 V14' stroke='#222' stroke-width='2.4' stroke-linecap='round'/><path d='M0 -4 L-4 -10 M0 -4 L4 -10' stroke='#222' stroke-width='.8'/></g>")
ART["butterflies"] = (f"<svg {W} viewBox='0 0 300 300'>"
 "<g><animateMotion dur='16s' repeatCount='indefinite' rotate='0' path='M40 220 C60 120 160 160 150 90 C140 30 250 40 250 120 C250 200 180 160 150 230 C120 290 30 300 40 220 Z'/>"
 + "<g transform='scale(1.9)'>" + butterfly('#ff8a1a', '#2a1a10', .32) + "</g>" + "</g>"
 "<g transform='scale(.8)'><animateMotion dur='13s' begin='-5s' repeatCount='indefinite' rotate='0' path='M300 120 C240 60 150 140 120 80 C90 20 20 60 50 140 C80 220 170 160 220 230 C260 290 340 200 300 120 Z'/>"
 + "<g transform='scale(1.9)'>" + butterfly('#4ab8ff', '#16305a', .26) + "</g>" + "</g></svg>")

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for k, v in ART.items():
        open(f"{out}/prop-{k}.svg", "w").write(v); print(k, len(v))
