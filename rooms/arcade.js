/* Mummula arcade: two little games hidden in the Neon arcade room's cabinets.
   MummulaArcade.open("moon")   -> Mummula vs. The Moon Men (shoot the saucers before they land)
   MummulaArcade.open("island") -> Mummula vs. Monster Island (run the beach, jump the crabs and lava, dodge the fireballs) */
(function(){
"use strict";
const hiGet = k => { try{ return +localStorage.getItem("mummula.hi." + k) || 0; }catch(e){ return 0; } };
const hiSet = (k, v) => { try{ localStorage.setItem("mummula.hi." + k, String(v)); }catch(e){} };

/* ---------- pixel sprites ---------- */
const PAL = { w:"#efe6cf", b:"#b9ae94", r:"#ff3b3b", k:"#1a1410", c:"#9ff", C:"#e8ffff", y:"#ffef3a", g:"#2f8f4a", G:"#7dff5a", o:"#ff7a1a", O:"#ffd04a", s:"#e8c878", d:"#7a3a16", p:"#ff4fd8", t:"#3cf0ff", L:"#ff5a12" };
function spr(rows){ return rows.map(r => r.split("")); }
const MUM = [spr([
  "...wwww...",
  "..wbwwbw..",
  "..wrwwrw..",
  "..wwwwww..",
  "...wbbw...",
  ".wwwwwwww.",
  "w.bwwwwb.w",
  "w.wwwwww.w",
  "..wbbbbw..",
  "..ww..ww..",
  "..ww..ww..",
  ".www..www."]), spr([
  "...wwww...",
  "..wbwwbw..",
  "..wrwwrw..",
  "..wwwwww..",
  "...wbbw...",
  ".wwwwwwww.",
  "w.bwwwwb.w",
  "w.wwwwww.w",
  "..wbbbbw..",
  "..ww.ww...",
  ".ww...ww..",
  "ww.....ww."])];
const UFO = spr([
  "....ccc....",
  "...cCCCc...",
  ".mmmmmmmmm.",
  "mmymmymmymm",
  "..mmmmmmm.."]);
const CRAB = spr([
  "o.......o",
  "oo.o.o.oo",
  ".ooooooo.",
  "o.ooooo.o",
  ".o.....o."]);
const ANKH = spr([
  ".OOO.",
  "O...O",
  "O...O",
  ".OOO.",
  "OOOOO",
  "..O..",
  "..O..",
  "..O.."]);
function draw(g, rows, x, y, pal, s){
  s = s || 1;
  for(let j = 0; j < rows.length; j++) for(let i = 0; i < rows[j].length; i++){
    const ch = rows[j][i]; if(ch === ".") continue;
    g.fillStyle = (pal && pal[ch]) || PAL[ch]; g.fillRect(Math.round(x + i*s), Math.round(y + j*s), s, s);
  }
}

/* ---------- shell: overlay, canvas, input ---------- */
let cur = null;
function open(which){
  if(cur) cur.close();
  const game = which === "island" ? ISLAND : MOON;
  const ov = document.createElement("div");
  ov.className = "mm-arcade";
  ov.innerHTML = `<style>
    .mm-arcade{position:fixed;inset:0;z-index:300;background:radial-gradient(ellipse at 50% 40%,#28104a,#05020c);display:flex;align-items:center;justify-content:center;font-family:"Courier New",monospace;color:#fff;touch-action:none;user-select:none;-webkit-user-select:none}
    .mm-arcade .cab{display:flex;flex-direction:column;align-items:center;gap:10px;padding:12px}
    .mm-arcade .mq{font:900 clamp(20px,4.4vw,34px)/1 Impact,"Arial Black",sans-serif;letter-spacing:.06em;color:#fff7c2;text-shadow:0 0 10px ${game.glow},0 0 26px ${game.glow};text-align:center}
    .mm-arcade .mq small{display:block;font:900 clamp(11px,2.2vw,15px)/1.4 "Arial Black",Arial,sans-serif;letter-spacing:.12em;color:#fff}
    .mm-arcade canvas{display:block;image-rendering:pixelated;image-rendering:crisp-edges;border-radius:10px;box-shadow:0 0 0 3px #05020a,0 0 0 6px ${game.glow},0 0 40px ${game.glow}}
    .mm-arcade .hud{display:flex;gap:18px;font-weight:700;font-size:14px;color:#ffe3f7}
    .mm-arcade .help{font-size:12px;color:#b9a6d8;text-align:center;max-width:90vw}
    .mm-arcade .pad{display:none;gap:10px}
    .mm-arcade .pad button{font:700 16px "Courier New",monospace;color:#fff;background:#24104a;border:2px solid ${game.glow};border-radius:12px;min-width:64px;height:54px;touch-action:none}
    .mm-arcade .pad button:active{background:${game.glow};color:#000}
    .mm-arcade .x{position:absolute;top:calc(12px + env(safe-area-inset-top));right:14px;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.4);background:rgba(0,0,0,.4);color:#fff;font-size:20px;cursor:pointer}
    @media (hover:none),(pointer:coarse){.mm-arcade .pad{display:flex}}
  </style>
  <button class="x" aria-label="Close the game">✕</button>
  <div class="cab"><div class="mq">MUMMULA<small>${game.sub}</small></div>
    <canvas width="${game.W}" height="${game.H}"></canvas>
    <div class="hud"><span class="sc">SCORE 0</span><span class="hi">HI ${hiGet(game.key)}</span></div>
    <div class="pad">${game.pad.map(([k, l]) => `<button data-k="${k}">${l}</button>`).join("")}</div>
    <div class="help">${game.help} · Esc to leave</div></div>`;
  document.body.appendChild(ov);
  const cv = ov.querySelector("canvas"), g = cv.getContext("2d"), scEl = ov.querySelector(".sc"), hiEl = ov.querySelector(".hi");
  const fit = () => { const padH = matchMedia("(hover:none),(pointer:coarse)").matches ? 70 : 0;
    const s = Math.max(1, Math.min((innerWidth - 32) / game.W, (innerHeight - 170 - padH) / game.H));
    const k = s >= 2 ? Math.floor(s) : s; cv.style.width = game.W * k + "px"; cv.style.height = game.H * k + "px"; };
  fit(); addEventListener("resize", fit);
  const keys = {}, pressed = {};
  const map = e => ({ArrowLeft:"left", a:"left", A:"left", ArrowRight:"right", d:"right", D:"right", ArrowUp:"up", w:"up", W:"up", " ":"fire", Enter:"fire", ArrowDown:"down", s:"down", S:"down"})[e.key];
  const kd = e => { if(e.key === "Escape"){ e.preventDefault(); e.stopPropagation(); close(); return; }
    const k = map(e); if(!k) return; e.preventDefault(); e.stopPropagation(); if(!keys[k]) pressed[k] = true; keys[k] = true; };
  const ku = e => { const k = map(e); if(!k) return; e.preventDefault(); e.stopPropagation(); keys[k] = false; };
  addEventListener("keydown", kd, true); addEventListener("keyup", ku, true);
  ov.querySelectorAll(".pad button").forEach(b => {
    const k = b.dataset.k;
    b.addEventListener("pointerdown", e => { e.preventDefault(); if(!keys[k]) pressed[k] = true; keys[k] = true; b.setPointerCapture(e.pointerId); });
    const up = () => { keys[k] = false; }; b.addEventListener("pointerup", up); b.addEventListener("pointercancel", up);
  });
  cv.addEventListener("pointerdown", e => { e.preventDefault(); pressed.tap = true; keys.tap = true; });
  addEventListener("pointerup", () => { keys.tap = false; });
  ov.querySelector(".x").onclick = () => close();
  const st = {mode:"title", t:0, score:0, hi:hiGet(game.key)};
  game.reset(st);
  let last = performance.now(), raf = 0, alive = true;
  const frame = now => {
    if(!alive) return;
    const dt = Math.min(.05, (now - last) / 1000); last = now; st.t += dt;
    const go = pressed.fire || pressed.tap || pressed.up;
    if(st.mode === "title" || st.mode === "over"){
      if(go && st.t > .4){ game.reset(st); st.mode = "play"; st.score = 0; st.t = 0; }
    } else game.update(st, dt, keys, pressed);
    if(st.mode === "over" && !st.saved){ st.saved = true; if(st.score > st.hi){ st.hi = st.score; hiSet(game.key, st.hi); st.newHi = true; } st.t = 0; }
    game.render(g, st);
    if(st.mode !== "play") overlayText(g, game, st);
    scEl.textContent = "SCORE " + st.score; hiEl.textContent = "HI " + Math.max(st.hi, st.score);
    for(const k in pressed) delete pressed[k];
    raf = requestAnimationFrame(frame);
  };
  raf = requestAnimationFrame(frame);
  function close(){ if(!alive) return; alive = false; cancelAnimationFrame(raf); removeEventListener("keydown", kd, true); removeEventListener("keyup", ku, true); removeEventListener("resize", fit); ov.remove(); cur = null; }
  cur = {close};
}
function overlayText(g, game, st){
  g.fillStyle = "rgba(0,0,0,.45)"; g.fillRect(0, 0, game.W, game.H);
  g.textAlign = "center"; g.fillStyle = "#fff"; g.font = "bold 12px 'Courier New',monospace";
  const cx = game.W / 2, cy = game.H / 2;
  if(st.mode === "title"){
    g.fillStyle = game.glow; g.font = "bold 16px Impact,'Arial Black',sans-serif"; g.fillText("MUMMULA", cx, cy - 26);
    g.fillStyle = "#fff"; g.font = "bold 10px 'Courier New',monospace"; g.fillText(game.sub, cx, cy - 12);
    if(Math.floor(st.t * 2) % 2 === 0){ g.fillStyle = "#ffef3a"; g.font = "bold 12px 'Courier New',monospace"; g.fillText(game.start, cx, cy + 14); }
  } else {
    g.fillStyle = "#ff4f4f"; g.font = "bold 18px Impact,'Arial Black',sans-serif"; g.fillText("GAME OVER", cx, cy - 8);
    g.fillStyle = "#fff"; g.font = "bold 11px 'Courier New',monospace"; g.fillText("SCORE " + st.score + (st.newHi ? "  NEW HIGH!" : ""), cx, cy + 10);
    if(st.t > .6 && Math.floor(st.t * 2) % 2 === 0){ g.fillStyle = "#ffef3a"; g.fillText(game.start.replace("START", "PLAY AGAIN"), cx, cy + 30); }
  }
  g.textAlign = "left";
}
const rnd = (a, b) => a + Math.random() * (b - a);
const hit = (a, b) => a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;

/* ---------- Game 1: Mummula vs. The Moon Men ---------- */
const MOON = {
  key:"moon", W:224, H:288, glow:"#ff3cc8", sub:"vs. THE MOON MEN",
  help:"← → to move · Space to fire bandage bolts", start:"PRESS START", pad:[["left","◀"],["fire","FIRE"],["right","▶"]],
  reset(st){
    st.p = {x:107, y:262, w:10, h:12, inv:0}; st.lives = 3; st.wave = 0; st.shots = []; st.zaps = []; st.boom = []; st.saved = false; st.newHi = false;
    st.stars = Array.from({length:60}, () => ({x:rnd(0, 224), y:rnd(0, 288), v:rnd(4, 18)}));
    MOON.wave(st);
  },
  wave(st){
    st.wave++; st.ufos = []; st.dir = 1; st.banner = 1.6;
    const cols = ["#7dff5a", "#3cf0ff", "#ff4fd8", "#ffcf3a"];
    for(let r = 0; r < 4; r++) for(let c = 0; c < 7; c++) st.ufos.push({x:18 + c*26, y:34 + r*18, w:11, h:5, row:r, col:cols[r]});
    st.total = st.ufos.length; st.zapT = 1; st.cool = 0; st.boss = null; st.bossT = rnd(8, 14);
  },
  update(st, dt, k, pr){
    const p = st.p;
    for(const s of st.stars){ s.y += s.v * dt; if(s.y > 288) { s.y = 0; s.x = rnd(0, 224); } }
    if(st.banner > 0){ st.banner -= dt; }
    p.x += ((k.right ? 1 : 0) - (k.left ? 1 : 0)) * 100 * dt; p.x = Math.max(2, Math.min(212, p.x));
    st.cool -= dt;
    if((k.fire || k.tap) && st.cool <= 0 && st.shots.length < 3){ st.shots.push({x:p.x + 4, y:p.y - 4, w:2, h:6}); st.cool = .32; }
    for(const s of st.shots) s.y -= 230 * dt;
    st.shots = st.shots.filter(s => s.y > -8);
    // formation
    const alive = st.ufos.length;
    const sp = (12 + st.wave * 4) * (1 + (1 - alive / st.total) * 2.2);
    let edge = false;
    for(const u of st.ufos){ u.x += st.dir * sp * dt; if(u.x < 3 || u.x > 210) edge = true; }
    if(edge){ st.dir *= -1; for(const u of st.ufos){ u.y += 7; u.x += st.dir * 2; } }
    // zaps
    st.zapT -= dt;
    if(st.zapT <= 0 && alive){ const u = st.ufos[Math.floor(Math.random() * alive)]; st.zaps.push({x:u.x + 5, y:u.y + 5, w:2, h:5}); st.zapT = Math.max(.35, 1.25 - st.wave * .1) * rnd(.6, 1.3); }
    for(const z of st.zaps) z.y += (75 + st.wave * 6) * dt;
    st.zaps = st.zaps.filter(z => z.y < 300);
    // bonus moon base saucer
    st.bossT -= dt;
    if(!st.boss && st.bossT <= 0){ const l = Math.random() < .5; st.boss = {x:l ? -20 : 230, y:20, w:18, h:7, v:l ? 46 : -46}; }
    if(st.boss){ st.boss.x += st.boss.v * dt; if(st.boss.x < -30 || st.boss.x > 250){ st.boss = null; st.bossT = rnd(10, 16); } }
    // hits
    for(const s of st.shots){
      for(const u of st.ufos) if(!u.dead && hit(s, u)){ u.dead = true; s.y = -99; st.score += (4 - u.row) * 10; MOON.pop(st, u.x + 5, u.y + 2, u.col); break; }
      if(st.boss && hit(s, st.boss)){ st.score += [100, 150, 300][Math.floor(Math.random() * 3)]; MOON.pop(st, st.boss.x + 9, st.boss.y + 3, "#ffef3a"); st.boss = null; st.bossT = rnd(10, 16); s.y = -99; }
    }
    st.ufos = st.ufos.filter(u => !u.dead);
    p.inv -= dt;
    if(p.inv <= 0) for(const z of st.zaps) if(hit(z, p)){ z.y = 999; st.lives--; p.inv = 1.6; MOON.pop(st, p.x + 5, p.y + 6, "#efe6cf"); if(st.lives <= 0) st.mode = "over"; }
    if(st.ufos.some(u => u.y > 250)){ st.lives = 0; st.mode = "over"; }
    if(!st.ufos.length){ st.score += 50 * st.wave; MOON.wave(st); st.zaps = []; }
    for(const b of st.boom){ b.x += b.vx * dt; b.y += b.vy * dt; b.life -= dt; }
    st.boom = st.boom.filter(b => b.life > 0);
  },
  pop(st, x, y, col){ for(let i = 0; i < 12; i++){ const a = Math.random() * 6.28, v = rnd(20, 70); st.boom.push({x, y, vx:Math.cos(a)*v, vy:Math.sin(a)*v, life:rnd(.3, .7), col}); } },
  render(g, st){
    g.fillStyle = "#06031a"; g.fillRect(0, 0, 224, 288);
    for(const s of st.stars){ g.fillStyle = s.v > 12 ? "#fff" : "#8a86b8"; g.fillRect(s.x | 0, s.y | 0, 1, 1); }
    g.fillStyle = "#e8e4c8"; g.beginPath(); g.arc(186, 46, 16, 0, 6.28); g.fill(); g.fillStyle = "#c8c2a0"; g.fillRect(178, 40, 4, 4); g.fillRect(190, 50, 3, 3); g.fillRect(184, 54, 2, 2);
    g.fillStyle = "#3a3a52"; g.fillRect(0, 276, 224, 12); g.fillStyle = "#7b7ba3"; g.fillRect(0, 276, 224, 1);
    const flap = Math.floor(st.t * 4) % 2;
    for(const u of st.ufos) draw(g, UFO, u.x, u.y, {m:u.col, y:flap ? "#ffef3a" : "#fff"});
    if(st.boss){ draw(g, UFO, st.boss.x, st.boss.y, {m:"#ff3b3b", y:"#fff"}, 1.6); }
    g.fillStyle = "#ffef3a"; for(const s of st.shots) g.fillRect(s.x, s.y, 2, 6);
    g.fillStyle = "#7dff5a"; for(const z of st.zaps){ g.fillRect(z.x, z.y, 2, 2); g.fillRect(z.x + (Math.floor(st.t * 20) % 2 ? 1 : -1), z.y + 2, 2, 3); }
    const p = st.p;
    if(!(p.inv > 0 && Math.floor(st.t * 12) % 2) && st.mode !== "title") draw(g, MUM[Math.floor(st.t * 6) % 2 && (st.keysMoving) ? 1 : 0], p.x, p.y);
    for(const b of st.boom){ g.fillStyle = b.col; g.fillRect(b.x | 0, b.y | 0, 2, 2); }
    g.fillStyle = "#fff"; g.font = "bold 8px 'Courier New',monospace";
    g.fillText("WAVE " + st.wave, 4, 10);
    for(let i = 0; i < st.lives; i++) draw(g, MUM[0], 180 + i * 12, 2, null, .7);
    if(st.banner > 0 && st.mode === "play"){ g.textAlign = "center"; g.fillStyle = "#ffef3a"; g.font = "bold 14px Impact,'Arial Black',sans-serif"; g.fillText("WAVE " + st.wave, 112, 150); g.textAlign = "left"; }
  }
};

/* ---------- Game 2: Mummula vs. Monster Island ---------- */
const GROUND = 148;
const ISLAND = {
  key:"island", W:320, H:180, glow:"#3cff7a", sub:"vs. MONSTER ISLAND",
  help:"Space, ↑ or tap to jump (hold for a bigger jump) · grab the ankhs, dodge the fireballs", start:"PRESS START", pad:[["fire","JUMP"]],
  reset(st){
    st.m = {x:56, y:GROUND - 12, w:8, h:12, vy:0, on:true}; st.obs = []; st.balls = []; st.ankhs = []; st.boom = [];
    st.speed = 110; st.dist = 0; st.next = 1; st.nextBall = 3; st.nextAnkh = 2; st.shake = 0; st.roar = 4; st.saved = false; st.newHi = false; st.coins = 0;
    st.waves = Array.from({length:14}, (_, i) => ({x:i * 26, y:rnd(GROUND + 10, 176)}));
  },
  update(st, dt, k, pr){
    const m = st.m;
    st.speed = Math.min(270, 110 + st.t * 3.2); const sp = st.speed;
    st.dist += sp * dt; st.score = Math.floor(st.dist / 6) + st.coins * 50;
    // jump: press to leave the ground, let go early for a short hop
    if((pr.fire || pr.tap || pr.up) && m.on){ m.vy = -300; m.on = false; }
    if(!(k.fire || k.tap || k.up) && m.vy < -120) m.vy = -120;
    m.vy += 900 * dt; m.y += m.vy * dt;
    const overPit = st.obs.some(o => o.kind === "pit" && m.x + 2 > o.x && m.x + m.w - 2 < o.x + o.w);
    if(m.y >= GROUND - 12 && !overPit && m.y < GROUND){ m.y = GROUND - 12; m.vy = 0; m.on = true; } else m.on = false;
    if(m.y > 190){ ISLAND.die(st); return; }
    // spawn
    st.next -= dt;
    if(st.next <= 0){
      const r = Math.random(), x = 330;
      if(r < .4) st.obs.push({kind:"crab", x, y:GROUND - 5, w:9, h:5, ph:Math.random() * 6});
      else if(r < .7) st.obs.push({kind:"rock", x, y:GROUND - 9, w:12, h:9});
      else st.obs.push({kind:"pit", x, y:GROUND, w:rnd(22, 30 + sp * .06), h:40});
      st.next = rnd(.75, 1.5) * (140 / sp) + .35;
    }
    st.nextAnkh -= dt;
    if(st.nextAnkh <= 0){ st.ankhs.push({x:330, y:rnd(GROUND - 60, GROUND - 22), w:5, h:8}); st.nextAnkh = rnd(1.4, 3); }
    st.nextBall -= dt;
    if(st.nextBall <= 0){ const tx = rnd(70, 300); st.balls.push({x:tx, y:-10, w:7, h:7, tx, vy:rnd(70, 95)}); st.nextBall = Math.max(.9, 3 - st.t * .03) * rnd(.7, 1.3); }
    for(const o of st.obs){ o.x -= sp * dt; if(o.kind === "crab") o.x -= Math.sin(st.t * 6 + o.ph) * 10 * dt; }
    for(const a of st.ankhs) a.x -= sp * dt;
    for(const b of st.balls){ b.y += b.vy * dt; b.x -= sp * dt * .35; b.tx = b.x; }
    st.obs = st.obs.filter(o => o.x > -40); st.ankhs = st.ankhs.filter(a => a.x > -10 && !a.got);
    for(const b of st.balls) if(b.y > GROUND - 7 && !b.done){ b.done = true; st.shake = .25; ISLAND.pop(st, b.x + 3, GROUND - 2, "#ff7a1a"); }
    st.balls = st.balls.filter(b => !b.done);
    // collisions
    const box = {x:m.x + 1, y:m.y + 1, w:m.w - 2, h:m.h - 1};
    for(const o of st.obs) if(o.kind !== "pit" && hit(box, o)) return ISLAND.die(st);
    for(const b of st.balls) if(hit(box, b)) return ISLAND.die(st);
    for(const a of st.ankhs) if(hit(box, a)){ a.got = true; st.coins++; ISLAND.pop(st, a.x + 2, a.y + 4, "#ffd04a"); }
    for(const w of st.waves){ w.x -= sp * dt * .5; if(w.x < -20){ w.x += 14 * 26; w.y = rnd(GROUND + 10, 176); } }
    st.roar -= dt; if(st.roar <= 0){ st.roar = rnd(5, 9); st.shake = .5; }
    st.shake = Math.max(0, st.shake - dt);
    for(const b of st.boom){ b.x += b.vx * dt; b.y += b.vy * dt; b.vy += 120 * dt; b.life -= dt; }
    st.boom = st.boom.filter(b => b.life > 0);
  },
  die(st){ ISLAND.pop(st, st.m.x + 4, st.m.y + 6, "#efe6cf"); st.shake = .4; st.mode = "over"; },
  pop(st, x, y, col){ for(let i = 0; i < 10; i++){ const a = Math.random() * 6.28, v = rnd(20, 60); st.boom.push({x, y, vx:Math.cos(a)*v, vy:Math.sin(a)*v - 30, life:rnd(.3, .6), col}); } },
  render(g, st){
    g.save();
    if(st.shake > 0) g.translate(rnd(-2, 2), rnd(-2, 2));
    // sunset sky, sun, volcano
    const sky = g.createLinearGradient(0, 0, 0, GROUND); sky.addColorStop(0, "#3a1050"); sky.addColorStop(.6, "#c8366a"); sky.addColorStop(1, "#ff8a3a");
    g.fillStyle = sky; g.fillRect(-4, -4, 328, GROUND + 4);
    g.fillStyle = "#ffd04a"; g.beginPath(); g.arc(250, 96, 22, 0, 6.28); g.fill();
    const vx = 210 - (st.dist * .04) % 420;
    for(const ox of [vx, vx + 420]){
      g.fillStyle = "#2a1a2e"; g.beginPath(); g.moveTo(ox - 60, GROUND); g.lineTo(ox - 8, 70); g.lineTo(ox + 8, 70); g.lineTo(ox + 70, GROUND); g.fill();
      g.fillStyle = "#ff4a1a"; g.fillRect(ox - 6, 68, 12, 4);
      g.fillStyle = "rgba(90,80,90,.7)"; for(let i = 0; i < 3; i++){ const t = (st.t * .6 + i / 3) % 1; g.beginPath(); g.arc(ox + Math.sin(t * 6) * 4, 64 - t * 40, 3 + t * 7, 0, 6.28); g.fill(); }
    }
    // the giant lizard wading behind, roaring now and then
    const kx = 18 + Math.sin(st.t * .7) * 6, ky = 62 + Math.sin(st.t * 1.4) * 3, roar = st.roar < .6;
    g.fillStyle = "#2f8f4a";
    g.beginPath(); g.moveTo(kx - 20, GROUND); g.bezierCurveTo(kx - 22, ky + 40, kx - 6, ky + 8, kx + 12, ky + 4); g.lineTo(kx + 34, ky - 2); g.lineTo(kx + 40, ky + (roar ? 14 : 8)); g.lineTo(kx + 26, ky + 14); g.bezierCurveTo(kx + 30, ky + 40, kx + 34, ky + 70, kx + 40, GROUND); g.fill();
    g.fillStyle = "#7dff5a"; for(let i = 0; i < 5; i++){ g.beginPath(); g.moveTo(kx - 14 + i * 4, ky + 30 - i * 5); g.lineTo(kx - 20 + i * 4, ky + 24 - i * 6); g.lineTo(kx - 10 + i * 4, ky + 26 - i * 5); g.fill(); }
    g.fillStyle = "#ffef3a"; g.fillRect(kx + 22, ky + 2, 4, 3);
    if(roar){ g.fillStyle = "#fff"; g.fillRect(kx + 30, ky + 6, 6, 2); g.strokeStyle = "rgba(255,255,255,.6)"; for(let i = 1; i < 4; i++){ g.beginPath(); g.arc(kx + 42, ky + 9, i * 6, -.6, .6); g.stroke(); } }
    // sea
    g.fillStyle = "#1b4f8a"; g.fillRect(-4, GROUND, 328, 40);
    g.fillStyle = "#7cc4ff"; for(const w of st.waves) g.fillRect(w.x | 0, w.y | 0, 10, 1);
    // beach strip with pits
    g.fillStyle = "#e8c878"; g.fillRect(-4, GROUND, 328, 6);
    g.fillStyle = "#c9a85a"; for(let x = -((st.dist * 1) % 16); x < 324; x += 16) g.fillRect(x, GROUND + 2, 3, 1);
    for(const o of st.obs) if(o.kind === "pit"){
      g.fillStyle = "#1b4f8a"; g.fillRect(o.x, GROUND, o.w, 6);
      g.fillStyle = Math.floor(st.t * 8) % 2 ? "#ff5a12" : "#ffb02a"; g.fillRect(o.x + 2, GROUND + 2, o.w - 4, 4);
    }
    for(const o of st.obs){
      if(o.kind === "crab") draw(g, CRAB, o.x, o.y + (Math.floor(st.t * 8) % 2));
      if(o.kind === "rock"){ g.fillStyle = "#5a4a5a"; g.beginPath(); g.moveTo(o.x, o.y + o.h); g.lineTo(o.x + 2, o.y + 2); g.lineTo(o.x + 7, o.y); g.lineTo(o.x + 12, o.y + 4); g.lineTo(o.x + 12, o.y + o.h); g.fill(); g.fillStyle = "#8a7a8a"; g.fillRect(o.x + 3, o.y + 3, 3, 2); }
    }
    for(const a of st.ankhs) draw(g, ANKH, a.x, a.y + Math.sin(st.t * 5 + a.x) * 1.5);
    for(const b of st.balls){
      g.fillStyle = "rgba(0,0,0,.35)"; g.fillRect(b.x - 1, GROUND - 1, 9, 2);
      g.fillStyle = "#ff5a12"; g.fillRect(b.x, b.y, 7, 7); g.fillStyle = "#ffd04a"; g.fillRect(b.x + 2, b.y + 2, 3, 3);
      g.fillStyle = "rgba(255,120,30,.5)"; g.fillRect(b.x + 2, b.y - 6, 3, 5);
    }
    const m = st.m;
    if(st.mode !== "over") draw(g, MUM[m.on ? Math.floor(st.t * 10) % 2 : 1], m.x - 1, m.y);
    for(const b of st.boom){ g.fillStyle = b.col; g.fillRect(b.x | 0, b.y | 0, 2, 2); }
    g.fillStyle = "#fff"; g.font = "bold 8px 'Courier New',monospace"; g.fillText("☥ " + st.coins, 6, 12);
    g.restore();
  }
};
window.MummulaArcade = {open};
})();
