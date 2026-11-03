import numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
OUT = "/home/claude/eric-museum/rooms/"

def noise(h, w, beta=2.0, seed=None, aniso=(1,1)):
    """Periodic (tileable) fractal noise via FFT; returns [0,1]."""
    r = np.random.default_rng(seed)
    fy = np.fft.fftfreq(h)[:,None]*aniso[0]; fx = np.fft.fftfreq(w)[None,:]*aniso[1]
    f = np.sqrt(fx**2 + fy**2); f[0,0] = 1
    spec = (r.normal(size=(h,w)) + 1j*r.normal(size=(h,w))) / f**(beta/2)
    spec[0,0] = 0
    n = np.real(np.fft.ifft2(spec))
    n = (n - n.min())/(n.max()-n.min()); return n

def shade(height, light=(-1,-1.4,1.6), strength=6.0):
    gy, gx = np.gradient(height*strength)
    nx, ny, nz = -gx, -gy, np.ones_like(height)
    l = np.array(light, float); l /= np.linalg.norm(l)
    d = (nx*l[0] + ny*l[1] + nz*l[2]) / np.sqrt(nx**2+ny**2+nz**2)
    return np.clip(d, 0, 1)

def save(arr, name, q=80):
    Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8)).save(OUT+name, quality=q, optimize=True, progressive=True)

# ---------- Castle stone wall ----------
def castle():
    W, H = 1024, 768
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    wx = (noise(H,W,3.0,1)-.5)*40; wy = (noise(H,W,3.0,2)-.5)*34
    X = (xx + wx) % W; Y = (yy + wy) % H
    rows = []; y = 0
    hs = [150,128,170,140,180]; hs[-1] = H - sum(hs[:-1])
    sid = np.zeros((H,W),int); dist = np.zeros((H,W)); k = 0
    base = np.zeros((H,W))
    for rh in hs:
        widths = []; tot = 0
        while tot < W - 360:
            wdt = int(rng.integers(150, 330)); widths.append(wdt); tot += wdt
        widths.append(W - tot)
        off = int(rng.integers(0, W))
        x0 = off
        for wdt in widths:
            inrow = (Y >= y) & (Y < y + rh)
            rel = (X - x0) % W
            m = inrow & (rel < wdt)
            sid[m] = k
            dx = np.minimum(rel, wdt - rel); dy = np.minimum(Y - y, y + rh - Y)
            dist[m] = np.minimum(dx, dy)[m]
            base[m] = rng.uniform(-.16, .08)
            k += 1; x0 += wdt
        y += rh
    mortar = 5.0
    edge = np.clip((dist - mortar) / 16.0, 0, 1)
    bump = noise(H,W,3.0,3); fine = noise(H,W,2.7,4); chip = noise(H,W,2.8,5)
    rough = noise(H,W,2.8,9)
    height = np.where(dist > mortar, edge**.5 * (0.6 + .6*bump) + .12*rough + .015*fine, 0.02*fine)
    height = np.where((dist > mortar) & (chip < .1), height*.6, height)
    L = shade(height, strength=9)
    col_stone = np.stack([.50,.47,.42])
    tint = (noise(H,W,3.2,6)-.5)*.12
    c = np.zeros((H,W,3))
    warm = np.zeros((H,W)); 
    for i,ch in enumerate([.47,.44,.40]):
        c[...,i] = ch + base + tint*(1.3 if i==0 else (.9 if i==1 else .5)) + (fine-.5)*.14 + (rough-.5)*.10
    c = np.where((dist > mortar)[...,None], c, np.stack([.26,.24,.21])[None,None,:] + (fine[...,None]-.5)*.08)
    soot = noise(H,W,3.3,8)
    pits = noise(H,W,2.3,10)
    c *= (1 - .35*np.clip((pits-.72)*6,0,1))[...,None]
    c *= (0.92 + .16*(noise(H,W,2.4,19)[...,None]-.5))
    ao = np.where(dist > mortar, 0.6 + 0.4*np.clip((dist-mortar)/10,0,1), 0.5)
    c *= (0.45 + 0.85*L)[...,None] * (0.72 + .35*soot)[...,None] * ao[...,None]
    save(c, "castle-stone.jpg")

# ---------- Cabin log wall ----------
def cabin():
    W, H = 1024, 696  # 6 logs of 116
    logh, gap = 116, 12
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    grain = noise(H, W, 3.0, 11, aniso=(1, 14))   # long streaks along x
    grain2 = noise(H, W, 2.8, 12, aniso=(1, 8))
    blot = noise(H, W, 3.0, 13)
    wav = (noise(H,W,3.4,14)-.5)*10
    yl = (yy + wav) % logh
    v = (yl - gap/2) / (logh - gap) * 2 - 1      # -1..1 across log
    inlog = np.abs(v) <= 1
    cyl = np.sqrt(np.clip(1 - v**2, 0, 1))
    logi = ((yy + wav) // logh).astype(int)
    tone = np.array([rng.uniform(-.09,.05) for _ in range(10)])[logi % 10]
    rings = np.sin((grain*55 + v*3) * 2.2)*.5+.5
    crack_n = noise(H, W, 3.0, 16, aniso=(1, 22))
    cracks = np.exp(-((crack_n-.5)/.006)**2) * (noise(H,W,3.0,17) > .55)
    wood = np.stack([.50,.34,.20])[None,None,:] * (0.62 + .38*rings[...,None]) * (0.8 + .45*(grain2[...,None]-.5)) + tone[...,None]
    wood *= (1 - .55*cracks)[...,None]
    wood *= (0.9 + .2*(blot[...,None]-.5))
    # knots
    for _ in range(9):
        cx, cy = rng.uniform(0,W), (rng.integers(0,6)+.5)*logh + rng.uniform(-18,18)
        rx, ry = rng.uniform(10,20), rng.uniform(6,11)
        ddx = np.minimum(np.abs(xx-cx), W-np.abs(xx-cx))/rx; ddy = (yy-cy)/ry
        d = np.sqrt(ddx**2+ddy**2)
        k = np.exp(-d**2*1.4)
        wood *= (1 - .45*k)[...,None]
        wood *= (1 - .12*np.exp(-((d-1.6)**2)*3))[...,None]
    light = 0.22 + 0.78*cyl**.8 + 0.15*np.clip(-v,0,1)*cyl
    wood *= light[...,None]
    chink = np.stack([.62,.58,.50])[None,None,:] * (0.75 + .3*(noise(H,W,1.3,15)[...,None]))
    shadow = np.clip(1 - (np.abs(v)-1)*0, 0, 1)
    c = np.where(inlog[...,None], wood, chink*0.8)
    # shadow under each log onto chinking
    under = (~inlog) & (v > 1)
    c = np.where(under[...,None], c*0.55, c)
    save(c, "cabin-logs.jpg")

# ---------- Library bookshelves ----------
def library():
    W, H = 1024, 640  # 3 shelves of 213
    img = np.zeros((H,W,3))
    sh = 213; board = 24
    back = noise(H,W,2.2,21, aniso=(1,6))
    img[...] = (np.stack([.20,.12,.07])[None,None,:]*(0.7+.5*back[...,None]))
    palette = [(.42,.08,.07),(.10,.20,.12),(.08,.12,.25),(.35,.22,.10),(.45,.32,.18),(.18,.08,.10),(.55,.45,.30),(.12,.10,.08),(.30,.05,.05),(.20,.26,.20)]
    fn = noise(H,W,1.2,22)
    for s in range(3):
        y1 = s*sh + sh - board; x = 0
        books = []
        while x < W:
            bw = int(rng.integers(16, 44)); books.append(bw); x += bw
        books[-1] -= (x - W)
        x = 0
        for bw in books:
            if bw < 6: x += bw; continue
            bh = int(rng.integers(130, 182))
            lean = 0
            col = np.array(palette[rng.integers(0,len(palette))]) * rng.uniform(.8,1.2)
            y0 = y1 - bh
            u = (np.arange(bw) + .5)/bw*2-1
            prof = (0.55 + .45*np.sqrt(1-u**2))
            block = col[None,None,:] * prof[None,:,None] * (0.85 + .3*(fn[y0:y1, x:x+bw, None]-.5))
            # gold bands
            for by in [int(bh*.12), int(bh*.18), int(bh*.82), int(bh*.88)]:
                if rng.random() < .8:
                    block[by:by+3] = np.array([.75,.6,.3])*prof[None,:,None]
            # title block
            if rng.random() < .6:
                t0 = int(bh*.3); t1 = int(bh*.55)
                block[t0:t1, max(1,bw//4):bw-max(1,bw//4)] *= .7
            img[y0:y1, x:x+bw] = block
            # gap shadow
            img[y0:y1, x:x+1] *= .4
            x += bw
        # shelf board
        bg = noise(board, W, 1.8, 30+s, aniso=(1,14))
        boardc = np.stack([.42,.26,.14])[None,None,:]*(0.8+.4*bg[...,None])
        boardc[:3] *= 1.25; boardc[-4:] *= .6
        img[y1:y1+board] = boardc
        img[y1+board: min(H, y1+board+10)] *= .55
    save(img, "library-shelves.jpg")

# ---------- Sand (aquarium floor) ----------
def sand():
    W, H = 512, 256
    n = noise(H,W,1.0,41); r = noise(H,W,2.4,42, aniso=(1,.3))
    h = .7*r + .3*n
    L = shade(h, strength=5)
    c = np.stack([.78,.68,.48])[None,None,:]*(0.6+.5*L[...,None])*(0.9+.2*(n[...,None]-.5))
    save(c, "sand.jpg")

# ---------- Old floorboards (haunted / library / diner none) ----------
def boards():
    W, H = 512, 512
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    bw = 64
    g = noise(H,W,2.0,51, aniso=(.05,1))
    idx = (xx//bw).astype(int)
    tone = np.array([rng.uniform(-.07,.07) for _ in range(8)])[idx%8]
    c = np.stack([.36,.24,.15])[None,None,:]*(0.75+.5*g[...,None]) + tone[...,None]
    c[(xx % bw) < 2] *= .35
    save(c, "boards.jpg")

castle(); cabin(); library(); sand(); boards()
print("ok")

# ---------- Aquarium caustics ----------
def caustics():
    W = H = 512
    n1 = noise(H,W,3.2,61); n2 = noise(H,W,3.2,62)
    a = (1-np.abs(np.sin(n1*22)))**10; b = (1-np.abs(np.sin(n2*19)))**10
    v = np.clip(a+b, 0, 1)
    img = np.stack([v*.75, v*.95, v], -1)
    save(img, "caustics.jpg", 75)

# ---------- Greenhouse foliage ----------
def foliage():
    from PIL import ImageDraw
    W, H = 1200, 800
    im = Image.new("RGB", (W,H), (150,190,150)); d = ImageDraw.Draw(im, "RGBA")
    r = np.random.default_rng(71)
    # sky light at top
    for i in range(H):
        t = i/H; d.line([(0,i),(W,i)], fill=(int(205-70*t), int(225-50*t), int(205-80*t), 255))
    for layer, (n, size, cols, alpha) in enumerate([(260, (60,160), [(40,90,45),(55,110,50),(70,125,60)], 210),
                                                   (220, (40,120), [(60,130,60),(80,150,70),(95,160,80)], 220),
                                                   (160, (30,90), [(110,170,90),(130,185,100),(70,140,70)], 230)]):
        for _ in range(n):
            x, y = r.uniform(-50,W+50), r.uniform(H*.15, H+50)
            L = r.uniform(*size); Wd = L*r.uniform(.3,.5); ang = r.uniform(0, np.pi)
            c = cols[r.integers(0,len(cols))]
            pts = []
            for t in np.linspace(0, 2*np.pi, 24):
                px, py = np.cos(t)*L/2, np.sin(t)*Wd/2*(1-.3*np.cos(t))
                pts.append((x + px*np.cos(ang) - py*np.sin(ang), y + px*np.sin(ang) + py*np.cos(ang)))
            d.polygon(pts, fill=c + (alpha,))
            d.line([pts[0], pts[12]], fill=(30,70,35,120), width=2)
    im = im.filter(ImageFilter.GaussianBlur(5))
    im.save(OUT+"foliage.jpg", quality=72, optimize=True, progressive=True)

# ---------- Grime (haunted wallpaper ageing) ----------
def grime():
    W, H = 512, 512
    a = noise(H,W,3.2,81); b = noise(H,W,2.6,82, aniso=(.12,1)); c = noise(H,W,2.2,83)
    v = 1 - .55*np.clip((a-.55)*2.2,0,1) - .25*np.clip((b-.6)*3,0,1) - .12*(c-.5)
    v = np.clip(v, 0, 1)
    save(np.stack([v, v*.97, v*.92], -1), "grime.jpg", 72)

caustics(); foliage(); grime()
print("more ok")

# ---------- Library: raised walnut wall panels ----------
def panels():
    W, H = 600, 720
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    grain = noise(H, W, 3.0, 91, aniso=(14, 1))      # vertical grain
    fine = noise(H, W, 2.6, 92, aniso=(6, 1))
    rings = np.sin(grain*60)*.5+.5
    wood = np.stack([.30,.17,.09])[None,None,:]*(0.7+.3*rings[...,None])*(0.85+.3*(fine[...,None]-.5))
    # panel layout: 2 columns x 2 rows of raised panels with stiles/rails
    h = np.zeros((H,W))
    for (x0,x1) in [(40,280),(320,560)]:
        for (y0,y1) in [(40,420),(460,680)]:
            dx = np.minimum(xx-x0, x1-xx); dy = np.minimum(yy-y0, y1-yy); d = np.minimum(dx,dy)
            inside = (d > 0)
            bevel = np.clip(d/22, 0, 1)
            h = np.where(inside, -0.15 + .45*bevel, h)
            mould = np.exp(-((d+4)/3)**2)*.25
            h += mould
    L = shade(h, light=(-1,-1.5,1.2), strength=14)
    c = wood*(0.45+0.85*L[...,None])
    save(c, "panels.jpg")

# ---------- Library: tall bookcase column ----------
def bookcase():
    sh = np.asarray(Image.open(OUT+"library-shelves.jpg")).astype(float)/255
    H = sh.shape[0]; inner = 190; post = 16; W = inner + 2*post
    c = np.zeros((H, W, 3))
    c[:, post:post+inner] = sh[:, 100:100+inner]
    g = noise(H, post, 3.0, 95, aniso=(14,1))
    pc = np.stack([.36,.21,.11])[None,None,:]*(0.75+.4*g[...,None])
    prof = (0.55 + .45*np.sin(np.linspace(0, np.pi, post)))[None,:,None]
    c[:, :post] = pc*prof; c[:, -post:] = pc*prof
    c[:, post:post+8] *= np.linspace(.35, 1, 8)[None,:,None]
    c[:, post+inner-8:post+inner] *= np.linspace(1, .35, 8)[None,:,None]
    save(c, "bookcase.jpg")

# ---------- Diner: glazed mint subway tile ----------
def tile():
    W, H = 480, 240   # tiles 120x60, 3px grout, offset rows
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    tw, th, g = 120, 60, 3
    row = (yy//th).astype(int); xo = (xx + (row % 2)*tw/2) % tw; yo = yy % th
    d = np.minimum(np.minimum(xo, tw-xo), np.minimum(yo, th-yo))
    inside = d > g/2
    rnd = np.random.default_rng(3); tone = rnd.uniform(-.03,.03,(H//th+1, W//tw+2))
    col = (( xx + (row%2)*tw/2)//tw).astype(int) % (W//tw+1)
    t = tone[row, col]
    bevel = np.clip((d-g/2)/5, 0, 1)
    gloss = np.exp(-((yo-th*.28)/(th*.18))**2)*.10 * np.clip(bevel,0,1)
    base = np.stack([.58,.78,.70])[None,None,:] + t[...,None] + (noise(H,W,2.4,101)[...,None]-.5)*.04
    c = base*(0.8+.2*bevel[...,None]) + gloss[...,None]
    c = np.where(inside[...,None], c, np.stack([.78,.80,.76])[None,None,:]*(0.9+.15*noise(H,W,1.6,102)[...,None]))
    save(c, "diner-tile.jpg")

# ---------- Diner: brushed stainless steel ----------
def steel():
    W, H = 512, 256
    n = noise(H, W, 2.2, 111, aniso=(1, 30))   # horizontal brushing
    m = noise(H, W, 3.2, 112)
    v = .62 + .18*(n-.5) + .12*(m-.5)
    c = np.stack([v*.97, v*.99, v*1.02], -1)
    save(c, "steel.jpg")

# ---------- Diner: worn checkerboard floor ----------
def checker():
    W = H = 512; s = 64
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    blk = ((xx//s + yy//s) % 2).astype(bool)
    d = np.minimum(np.minimum(xx % s, s - xx % s), np.minimum(yy % s, s - yy % s))
    rnd = np.random.default_rng(5); tone = rnd.uniform(-.04,.04,(H//s, W//s))
    t = tone[(yy//s).astype(int), (xx//s).astype(int)]
    scuff = noise(H, W, 2.4, 121); dirt = noise(H, W, 3.2, 122)
    white = np.stack([.90,.88,.82])[None,None,:]; black = np.stack([.09,.09,.10])[None,None,:]
    c = np.where(blk[...,None], black, white) + t[...,None]
    c = c*(0.92 + .1*(scuff[...,None]-.5)) - .06*np.clip(dirt-.6,0,1)[...,None]
    c = np.where((d < 1.5)[...,None], c*.75, c)
    save(c, "checker.jpg")

panels(); bookcase(); tile(); steel(); checker()
print("lib+diner ok")
