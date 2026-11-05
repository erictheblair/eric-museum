/* Mummula arcade: two little games hidden in the Neon arcade room's cabinets.
   MummulaArcade.open("moon")   -> Mummula vs. The Moon Men (shoot the saucers before they land)
   MummulaArcade.open("island") -> Mummula vs. Monster Island (run the beach, jump the crabs and lava, dodge the fireballs) */
(function(){
"use strict";
const hiGet = k => { try{ return +localStorage.getItem("mummula.hi." + k) || 0; }catch(e){ return 0; } };
const hiSet = (k, v) => { try{ localStorage.setItem("mummula.hi." + k, String(v)); }catch(e){} };

/* ---------- pixel sprites ---------- */
const PAL = { v:"#b0101a", m:"#9aa5ae", M:"#eef2f5", n:"#5a636b", w:"#efe6cf", b:"#b9ae94", r:"#ff3b3b", k:"#17121a", c:"#9ff", C:"#e8ffff", y:"#ffef3a", g:"#2f8f4a", G:"#7dff5a", o:"#ff7a1a", O:"#ffd04a", s:"#e8c878", d:"#7a3a16", p:"#ff4fd8", t:"#3cf0ff", L:"#ff5a12" };
function spr(rows){ return rows.map(r => r.split("")); }
// Mummula: bandaged, red eyes, black vampire cape with a red lining and a tall collar. Two frames (legs / cape flutter).
const MUM = [spr([
  "....wwww....",
  "...wbwwbw...",
  "..kwrwwrwk..",
  ".kk.wwww.kk.",
  ".kvwwbbwwvk.",
  "kvwwwwwwwwvk",
  "kvw.wwww.wvk",
  "kv..wbbw..vk",
  "kv..wwww..vk",
  "kk..w..w..kk",
  ".k..w..w..k.",
  "...ww..ww..."]), spr([
  "....wwww....",
  "...wbwwbw...",
  "..kwrwwrwk..",
  ".kk.wwww.kk.",
  ".kvwwbbwwvk.",
  "kvwwwwwwwwvk",
  "kvw.wwww.wvk",
  "kv..wbbw..vk",
  ".kv.wwww.vk.",
  ".kk.w..ww.k.",
  "...ww....w..",
  "..ww.....ww."])];
// Side view for the beach run: cape streaming out behind.
const RUN = [spr([
  "......wwww..",
  ".....wwbwr..",
  "...kkwwwww..",
  "..kvvkwbw...",
  ".kvvvwwwww..",
  "kvvvkwwbw.w.",
  "kvvk.wwww...",
  "kkk..wbbw...",
  "kk...ww.ww..",
  "....ww...w..",
  "...ww....ww.",
  "............"]), spr([
  "......wwww..",
  ".....wwbwr..",
  "...kkwwwww..",
  ".kkvvkwbw...",
  "kvvvvwwwww..",
  "kvvvkwwbw.w.",
  ".kvk.wwww...",
  "..kk.wbbw...",
  "....wwww....",
  "....w..w....",
  "...ww..ww...",
  "............"])];
// Mummula's classic flying saucer: silver disc, glass dome with Mummula inside, running lights.
const SAUCER = spr([
  "......ccccc......",
  ".....cwwbwwc.....",
  "....cwrwwwrwc....",
  "....ckkwwwkkc....",
  "..mmmmmmmmmmmmm..",
  ".mMMMMMMMMMMMMMm.",
  "mmmmmmmmmmmmmmmmm",
  ".mymmmymmmymmmym.",
  "...nnnnnnnnnnn..."]);
// Player ship: a big Mummula head (with cape collar) popping out of the open-top saucer.
const SAUCER_BIG = spr([
  ".......wwbwwww.......",
  ".....wwwwwwbwwww.....",
  "....wbwwwwwwwwbww....",
  "....wwbbbwwwbbbww....",
  "....wwkrrwwwkrrbw....",
  "....bwkrrwbwkrrww....",
  "....wwwwwwkwwwwwb....",
  "..vv.wwkwkwkwkww.vv..",
  "..vvvwwwkkkkkwwwvvv..",
  "...vvkcwwwwwwwckvv...",
  "....ccCkkkkkkkCcc....",
  "...mmmmmmmmmmmmmmm...",
  ".mMMMMMMMMMMMMMMMMMm.",
  "mmmmmmmmmmmmmmmmmmmmm",
  ".mymmmymmmymmmymmmym.",
  "...nnnnnnnnnnnnnnn..."]);
const UFO = spr([
  "....ccc....",
  "...cCCCc...",
  ".mmmmmmmmm.",
  "mmymmymmymm",
  "..mmmmmmm.."]);
// Bright cyan with a dark outline so it pops against the orange sunset and sand.
const CRAB = spr([
  "kk.......kk",
  "ktk.w.w.ktk",
  "ktk.k.k.ktk",
  ".kkkkkkkkk.",
  "kktttttttkk",
  ".kCtttttCk.",
  "k.kkkkkkk.k",
  ".k.k...k.k."]);
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
  s = s || 1; x = Math.round(x); y = Math.round(y);
  for(let j = 0; j < rows.length; j++) for(let i = 0; i < rows[j].length; i++){
    const ch = rows[j][i]; if(ch === ".") continue;
    g.fillStyle = (pal && pal[ch]) || PAL[ch]; g.fillRect(x + Math.floor(i*s), y + Math.floor(j*s), Math.ceil(s), Math.ceil(s));
  }
}

/* ---------- shell: overlay, canvas, input ---------- */
let cur = null;
const BASE = (document.currentScript && document.currentScript.src) || location.href;
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
    .mm-arcade .mu{position:absolute;top:calc(12px + env(safe-area-inset-top));right:66px;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.4);background:rgba(0,0,0,.4);color:#fff;font-size:20px;cursor:pointer}
    .mm-arcade .mu.off{opacity:.45;text-decoration:line-through}
    @media (hover:none),(pointer:coarse){.mm-arcade .pad{display:flex}}
  </style>
  <button class="x" aria-label="Close the game">✕</button><button class="mu" aria-label="Music on or off">♪</button>
  <div class="cab"><div class="mq">MUMMULA<small>${game.sub}</small></div>
    <canvas width="${game.W}" height="${game.H}"></canvas>
    <div class="hud"><span class="sc">SCORE 0</span><span class="hi">HI ${hiGet(game.key)}</span></div>
    <div class="pad">${game.pad.map(([k, l]) => `<button data-k="${k}">${l}</button>`).join("")}</div>
    <div class="help">${game.help} · M for music · Esc to leave</div></div>`;
  document.body.appendChild(ov);
  // Music: loops while the game is open. Starts right away if the browser allows it, otherwise on the first key or tap.
  const song = new Audio(new URL("music/" + game.key + ".mp3?v=1", BASE).href); song.loop = true; song.volume = .6;
  const muBtn = ov.querySelector(".mu");
  let muted = false; try{ muted = localStorage.getItem("mummula.mute") === "1"; }catch(e){}
  const play = () => { if(!muted && alive && song.paused) song.play().catch(() => {}); };
  const setMute = m => { muted = m; muBtn.classList.toggle("off", m); try{ localStorage.setItem("mummula.mute", m ? "1" : "0"); }catch(e){} m ? song.pause() : play(); };
  muBtn.classList.toggle("off", muted);
  muBtn.onclick = e => { e.stopPropagation(); setMute(!muted); };
  ov.addEventListener("pointerdown", play, true);
  const cv = ov.querySelector("canvas"), g = cv.getContext("2d"), scEl = ov.querySelector(".sc"), hiEl = ov.querySelector(".hi");
  const fit = () => { const padH = matchMedia("(hover:none),(pointer:coarse)").matches ? 70 : 0;
    const s = Math.max(1, Math.min((innerWidth - 32) / game.W, (innerHeight - 170 - padH) / game.H));
    const k = s >= 2 ? Math.floor(s) : s; cv.style.width = game.W * k + "px"; cv.style.height = game.H * k + "px"; };
  fit(); addEventListener("resize", fit);
  const keys = {}, pressed = {};
  const map = e => ({ArrowLeft:"left", a:"left", A:"left", ArrowRight:"right", d:"right", D:"right", ArrowUp:"up", w:"up", W:"up", " ":"fire", Enter:"fire", ArrowDown:"down", s:"down", S:"down"})[e.key];
  const kd = e => { if(e.key === "Escape"){ e.preventDefault(); e.stopPropagation(); close(); return; }
    if(e.key === "m" || e.key === "M"){ e.preventDefault(); e.stopPropagation(); setMute(!muted); return; }
    play();
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
  let alive = true; play();
  const st = {mode:"title", t:0, score:0, hi:hiGet(game.key)};
  game.reset(st);
  let last = performance.now(), raf = 0;
  const frame = now => {
    if(!alive) return;
    const dt = Math.max(0, Math.min(.05, (now - last) / 1000)); last = now; st.t += dt;
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
  function close(){ if(!alive) return; alive = false; cancelAnimationFrame(raf); removeEventListener("keydown", kd, true); removeEventListener("keyup", ku, true); removeEventListener("resize", fit); song.pause(); song.removeAttribute("src"); song.load(); ov.remove(); cur = null; }
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
    st.p = {x:103, y:264, w:17, h:9, inv:0}; st.lives = 3; st.wave = 0; st.shots = []; st.zaps = []; st.boom = []; st.saved = false; st.newHi = false;
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
    p.x += ((k.right ? 1 : 0) - (k.left ? 1 : 0)) * 100 * dt; p.x = Math.max(2, Math.min(205, p.x));
    st.cool -= dt;
    if((k.fire || k.tap) && st.cool <= 0 && st.shots.length < 3){ st.shots.push({x:p.x + 7.5, y:p.y - 12, w:2, h:6}); st.cool = .32; }
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
    if(p.inv <= 0) for(const z of st.zaps) if(hit(z, p)){ z.y = 999; st.lives--; p.inv = 1.6; MOON.pop(st, p.x + 8, p.y + 4, "#eef2f5"); if(st.lives <= 0) st.mode = "over"; }
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
    if(!(p.inv > 0 && Math.floor(st.t * 12) % 2) && st.mode !== "title") draw(g, SAUCER_BIG, p.x - 2, p.y - 7, {y:Math.floor(st.t * 6) % 2 ? "#ffef3a" : "#ff3b3b"});
    for(const b of st.boom){ g.fillStyle = b.col; g.fillRect(b.x | 0, b.y | 0, 2, 2); }
    g.fillStyle = "#fff"; g.font = "bold 8px 'Courier New',monospace";
    g.fillText("WAVE " + st.wave, 4, 10);
    for(let i = 0; i < st.lives; i++) draw(g, SAUCER, 166 + i * 19, 3, null, 1);
    if(st.banner > 0 && st.mode === "play"){ g.textAlign = "center"; g.fillStyle = "#ffef3a"; g.font = "bold 14px Impact,'Arial Black',sans-serif"; g.fillText("WAVE " + st.wave, 112, 150); g.textAlign = "left"; }
  }
};

/* ---------- Game 2: Mummula vs. Monster Island ---------- */
const GROUND = 148;
const ISLAND = {
  key:"island", W:320, H:180, glow:"#3cff7a", sub:"vs. MONSTER ISLAND",
  help:"Space, ↑ or tap to jump (hold for a bigger jump) · ← → to run ahead or ease back · don't let the monster catch you", start:"PRESS START", pad:[["left","◀"],["fire","JUMP"],["right","▶"]],
  reset(st){
    st.m = {x:110, y:GROUND - 12, w:10, h:12, vy:0, on:true, stun:0}; st.obs = []; st.balls = []; st.ankhs = []; st.boom = [];
    st.speed = 110; st.dist = 0; st.next = 1.2; st.nextBall = 4; st.nextAnkh = 2; st.shake = 0; st.saved = false; st.newHi = false; st.coins = 0;
    // the monster: its snout tip is at mon.x; it creeps forward, lunges now and then, and gains on you when you stumble
    st.mon = {x:60, base:60, lunge:0, nextLunge:3.5, step:0, jaw:0};
    st.waves = Array.from({length:14}, (_, i) => ({x:i * 26, y:rnd(GROUND + 10, 176)}));
  },
  update(st, dt, k, pr){
    const m = st.m, mon = st.mon;
    st.speed = Math.min(250, 105 + st.t * 3); const sp = st.speed;
    st.dist += sp * dt; st.score = Math.floor(st.dist / 6) + st.coins * 50;
    // run ahead / ease back (limited), jump, short hop on early release
    m.stun = Math.max(0, m.stun - dt);
    if(!m.stun) m.x += ((k.right ? 1 : 0) - (k.left ? 1 : 0)) * 80 * dt;
    m.x = Math.min(250, m.x);
    if((pr.fire || pr.tap || pr.up) && m.on && !m.stun){ m.vy = -300; m.on = false; }
    if(!(k.fire || k.tap || k.up) && m.vy < -120) m.vy = -120;
    m.vy += 900 * dt; m.y += m.vy * dt;
    const overPit = st.obs.some(o => o.kind === "pit" && m.x + 3 > o.x && m.x + m.w - 3 < o.x + o.w);
    if(m.y >= GROUND - 12 && !overPit && m.y < GROUND){ m.y = GROUND - 12; m.vy = 0; m.on = true; } else m.on = false;
    if(m.y > 190) return ISLAND.die(st, "fell");
    // the monster: slow creep toward a resting spot, plus lunges that get closer over time
    mon.base = Math.min(124, 60 + st.t * .55);
    mon.nextLunge -= dt;
    if(mon.nextLunge <= 0){ mon.lunge = 1; mon.nextLunge = rnd(2.6, 4.6) * Math.max(.55, 1 - st.t * .006); st.shake = .3; }
    if(mon.lunge > 0) mon.lunge = Math.max(0, mon.lunge - dt * 1.4);
    const reach = Math.sin(Math.min(1, mon.lunge) * Math.PI) * 34;
    mon.x += ((mon.base + reach) - mon.x) * Math.min(1, dt * 6);
    mon.step += dt * (2 + sp / 90); mon.jaw = (Math.sin(st.t * 9) + 1) / 2;
    if(Math.floor(mon.step) !== mon.lastStep){ mon.lastStep = Math.floor(mon.step); st.shake = Math.max(st.shake, .08); }
    if(m.x < mon.x - 2) return ISLAND.die(st, "caught");
    // spawn
    st.next -= dt;
    if(st.next <= 0){
      const r = Math.random(), x = 330;
      if(r < .4) st.obs.push({kind:"crab", x, y:GROUND - 5, w:9, h:5, ph:Math.random() * 6});
      else if(r < .7) st.obs.push({kind:"rock", x, y:GROUND - 9, w:12, h:9});
      else st.obs.push({kind:"pit", x, y:GROUND, w:rnd(22, 30 + sp * .05), h:40});
      st.next = rnd(.8, 1.6) * (140 / sp) + .4;
    }
    st.nextAnkh -= dt;
    if(st.nextAnkh <= 0){ st.ankhs.push({x:330, y:Math.round(rnd(GROUND - 58, GROUND - 22)), w:5, h:8}); st.nextAnkh = rnd(1.4, 3); }
    st.nextBall -= dt;
    if(st.nextBall <= 0){ const tx = rnd(m.x - 20, 300); st.balls.push({x:tx, y:-10, w:7, h:7, vy:rnd(70, 95)}); st.nextBall = Math.max(1, 3.2 - st.t * .03) * rnd(.7, 1.3); }
    for(const o of st.obs){ o.x -= sp * dt; if(o.kind === "crab") o.x -= Math.sin(st.t * 6 + o.ph) * 10 * dt; }
    for(const a of st.ankhs) a.x -= sp * dt;
    for(const b of st.balls){ b.y += b.vy * dt; b.x -= sp * dt * .35; }
    st.obs = st.obs.filter(o => o.x > -40 && !o.gone); st.ankhs = st.ankhs.filter(a => a.x > -10 && !a.got);
    for(const b of st.balls) if(b.y > GROUND - 7 && !b.done){ b.done = true; st.shake = .25; ISLAND.pop(st, b.x + 3, GROUND - 2, "#ff7a1a"); }
    st.balls = st.balls.filter(b => !b.done);
    // collisions: crabs and rocks trip you back toward the monster; fireballs and pits are the end
    const box = {x:m.x + 2, y:m.y + 1, w:m.w - 4, h:m.h - 1};
    for(const o of st.obs) if(o.kind !== "pit" && !o.gone && hit(box, o)){ o.gone = true; m.stun = .45; m.x -= 34; m.vy = -120; st.shake = .3; ISLAND.pop(st, o.x + 5, o.y + 3, o.kind === "crab" ? "#3cf0ff" : "#8a7a8a"); }
    for(const b of st.balls) if(hit(box, b)) return ISLAND.die(st, "burned");
    for(const a of st.ankhs) if(hit(box, a)){ a.got = true; st.coins++; ISLAND.pop(st, a.x + 2, a.y + 4, "#ffd04a"); }
    for(const w of st.waves){ w.x -= sp * dt * .5; if(w.x < -20){ w.x += 14 * 26; w.y = rnd(GROUND + 10, 176); } }
    st.shake = Math.max(0, st.shake - dt);
    for(const b of st.boom){ b.x += b.vx * dt; b.y += b.vy * dt; b.vy += 120 * dt; b.life -= dt; }
    st.boom = st.boom.filter(b => b.life > 0);
  },
  die(st, how){ st.how = how; ISLAND.pop(st, st.m.x + 5, st.m.y + 6, "#efe6cf"); st.shake = .5; st.mode = "over"; if(how === "caught") st.mon.lunge = 1; },
  pop(st, x, y, col){ for(let i = 0; i < 10; i++){ const a = Math.random() * 6.28, v = rnd(20, 60); st.boom.push({x, y, vx:Math.cos(a)*v, vy:Math.sin(a)*v - 30, life:rnd(.3, .6), col}); } },
  monster(g, st){
    // A huge green lizard right behind you, running on the sand. Its snout tip is at mon.x.
    const mon = st.mon, x = Math.round(mon.x), bob = Math.round(Math.sin(mon.step * Math.PI) * 2), stride = Math.sin(mon.step * Math.PI);
    const jaw = 3 + mon.jaw * 9 + (mon.lunge > 0 ? 6 : 0), hy = GROUND - 44 + bob;
    g.fillStyle = "#1f6a36";
    // far leg
    g.fillRect(x - 70 - stride * 8, GROUND - 30 + bob, 14, 30 - Math.max(0, -stride) * 6);
    // body leaning forward, tail off-screen left
    g.fillStyle = "#2f8f4a";
    g.beginPath(); g.moveTo(-10, GROUND - 20 + bob); g.lineTo(-10, GROUND - 96 + bob); g.bezierCurveTo(x - 90, GROUND - 120 + bob, x - 40, GROUND - 76 + bob, x - 26, hy + 6);
    g.lineTo(x - 30, GROUND - 26 + bob); g.bezierCurveTo(x - 60, GROUND - 14 + bob, x - 100, GROUND - 16 + bob, -10, GROUND - 20 + bob); g.fill();
    // back spikes
    g.fillStyle = "#7dff5a";
    for(let i = 0; i < 6; i++){ const sx = x - 120 + i * 14, sy = GROUND - 104 + bob + i * 6; g.beginPath(); g.moveTo(sx - 5, sy + 8); g.lineTo(sx + 1, sy - 8); g.lineTo(sx + 6, sy + 8); g.fill(); }
    // belly
    g.fillStyle = "#b8d68a"; g.beginPath(); g.moveTo(x - 34, hy + 16); g.bezierCurveTo(x - 50, GROUND - 26 + bob, x - 80, GROUND - 22 + bob, x - 96, GROUND - 26 + bob); g.lineTo(x - 90, GROUND - 40 + bob); g.bezierCurveTo(x - 70, GROUND - 40 + bob, x - 50, GROUND - 50 + bob, x - 38, hy + 4); g.fill();
    // near leg + claws
    g.fillStyle = "#2a7c40"; g.fillRect(x - 52 + stride * 8, GROUND - 32 + bob, 16, 32 - Math.max(0, stride) * 6);
    g.fillStyle = "#fff"; for(let i = 0; i < 3; i++) g.fillRect(x - 52 + stride * 8 + 16, GROUND - 3 - i * 2 + bob, 3, 1);
    // little arm reaching
    g.fillStyle = "#2f8f4a"; g.fillRect(x - 34, hy + 22, 12, 4); g.fillStyle = "#fff"; g.fillRect(x - 22, hy + 22, 2, 1); g.fillRect(x - 22, hy + 25, 2, 1);
    // head: upper jaw + lower jaw opening and snapping, teeth, eye
    g.fillStyle = "#2f8f4a";
    g.beginPath(); g.moveTo(x - 30, hy - 10); g.lineTo(x - 6, hy - 6); g.lineTo(x, hy + 2); g.lineTo(x - 30, hy + 4); g.fill();
    g.beginPath(); g.moveTo(x - 30, hy + 6); g.lineTo(x - 4, hy + 6 + jaw * .6); g.lineTo(x - 6, hy + 10 + jaw); g.lineTo(x - 30, hy + 14); g.fill();
    g.fillStyle = "#5a0a10"; g.beginPath(); g.moveTo(x - 28, hy + 4); g.lineTo(x - 2, hy + 3); g.lineTo(x - 5, hy + 7 + jaw * .6); g.lineTo(x - 28, hy + 7); g.fill();
    g.fillStyle = "#fff"; for(let i = 0; i < 5; i++){ g.fillRect(x - 26 + i * 5, hy + 2, 2, 3); g.fillRect(x - 24 + i * 5, hy + 5 + jaw * .5 * (i / 5), 2, 2); }
    g.fillStyle = "#ffef3a"; g.fillRect(x - 20, hy - 6, 4, 3); g.fillStyle = "#000"; g.fillRect(x - 17, hy - 6, 1, 3);
    // warning glow when it's about to lunge
    if(mon.nextLunge < .5 && st.mode === "play"){ g.fillStyle = "rgba(255,60,40," + (.25 + .25 * Math.sin(st.t * 30)) + ")"; g.fillRect(x - 21, hy - 7, 6, 5); }
  },
  render(g, st){
    g.save();
    if(st.shake > 0) g.translate(Math.round(rnd(-2, 2)), Math.round(rnd(-2, 2)));
    const sky = g.createLinearGradient(0, 0, 0, GROUND); sky.addColorStop(0, "#3a1050"); sky.addColorStop(.6, "#c8366a"); sky.addColorStop(1, "#ff8a3a");
    g.fillStyle = sky; g.fillRect(-4, -4, 328, GROUND + 4);
    g.fillStyle = "#ffd04a"; g.beginPath(); g.arc(250, 96, 22, 0, 6.28); g.fill();
    const vx = 230 - (st.dist * .04) % 420;
    for(const ox of [vx, vx + 420]){
      g.fillStyle = "#2a1a2e"; g.beginPath(); g.moveTo(ox - 60, GROUND); g.lineTo(ox - 8, 70); g.lineTo(ox + 8, 70); g.lineTo(ox + 70, GROUND); g.fill();
      g.fillStyle = "#ff4a1a"; g.fillRect(ox - 6, 68, 12, 4);
      g.fillStyle = "rgba(90,80,90,.7)"; for(let i = 0; i < 3; i++){ const t = (st.t * .6 + i / 3) % 1; g.beginPath(); g.arc(ox + Math.sin(t * 6) * 4, 64 - t * 40, 3 + t * 7, 0, 6.28); g.fill(); }
    }
    g.fillStyle = "#1b4f8a"; g.fillRect(-4, GROUND, 328, 40);
    g.fillStyle = "#7cc4ff"; for(const w of st.waves) g.fillRect(Math.round(w.x), Math.round(w.y), 10, 1);
    g.fillStyle = "#e8c878"; g.fillRect(-4, GROUND, 328, 6);
    g.fillStyle = "#c9a85a"; for(let x = -Math.round(st.dist % 16); x < 324; x += 16) g.fillRect(x, GROUND + 2, 3, 1);
    for(const o of st.obs) if(o.kind === "pit"){
      const ox = Math.round(o.x), ow = Math.round(o.w);
      g.fillStyle = "#1b4f8a"; g.fillRect(ox, GROUND, ow, 6);
      g.fillStyle = Math.floor(st.t * 8) % 2 ? "#ff5a12" : "#ffb02a"; g.fillRect(ox + 2, GROUND + 2, ow - 4, 4);
    }
    for(const o of st.obs){
      const ox = Math.round(o.x);
      if(o.kind === "crab") draw(g, CRAB, ox - 1, o.y - 3 + (Math.floor(st.t * 8) & 1));
      if(o.kind === "rock"){ g.fillStyle = "#5a4a5a"; g.beginPath(); g.moveTo(ox, o.y + o.h); g.lineTo(ox + 2, o.y + 2); g.lineTo(ox + 7, o.y); g.lineTo(ox + 12, o.y + 4); g.lineTo(ox + 12, o.y + o.h); g.fill(); g.fillStyle = "#8a7a8a"; g.fillRect(ox + 3, o.y + 3, 3, 2); }
    }
    // ankhs float steadily with a slow glint
    for(const a of st.ankhs){ draw(g, ANKH, a.x, a.y); if(Math.floor(st.t * 3 + a.y) % 6 === 0){ g.fillStyle = "#fff"; g.fillRect(Math.round(a.x) + 1, a.y + 1, 1, 1); } }
    for(const b of st.balls){
      g.fillStyle = "rgba(0,0,0,.35)"; g.fillRect(Math.round(b.x) - 1, GROUND - 1, 9, 2);
      const bx = Math.round(b.x), by = Math.round(b.y);
      g.fillStyle = "#ff5a12"; g.fillRect(bx, by, 7, 7); g.fillStyle = "#ffd04a"; g.fillRect(bx + 2, by + 2, 3, 3);
      g.fillStyle = "rgba(255,120,30,.5)"; g.fillRect(bx + 2, by - 6, 3, 5);
    }
    const m = st.m;
    if(!(st.mode === "over" && st.how !== "fell")){ if(!(m.stun && Math.floor(st.t * 16) % 2)) draw(g, RUN[m.on ? Math.floor(st.t * 10) & 1 : 1], m.x, m.y); }
    ISLAND.monster(g, st);
    for(const b of st.boom){ g.fillStyle = b.col; g.fillRect(b.x | 0, b.y | 0, 2, 2); }
    g.fillStyle = "#fff"; g.font = "bold 8px 'Courier New',monospace"; g.fillText("☥ " + st.coins, 290, 12);
    g.restore();
  }
};
window.MummulaArcade = {open};
})();
