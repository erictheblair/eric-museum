/* Mummula arcade: two little games hidden in the Neon arcade room's cabinets.
   MummulaArcade.open("moon")   -> Mummula vs. The Moon Men (shoot the saucers before they land)
   MummulaArcade.open("island") -> Mummula vs. Monster Island (run the beach, jump the crabs and lava, dodge the fireballs)
   MummulaArcade.open("curse")  -> The Curse of Mummula (dodge the curses Old Man Mummula hurls down from his ledge) */
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
// Bright red with a dark outline and pale highlights, so it pops against the blue sea, the sand and the sunset.
const CRAB_PAL = {t:"#ff2b4a", C:"#ffd0d8"};
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
  const game = ({island:ISLAND, curse:CURSE})[which] || MOON;
  const ov = document.createElement("div");
  ov.className = "mm-arcade";
  ov.innerHTML = `<style>
    .mm-arcade{position:fixed;inset:0;z-index:300;background:radial-gradient(ellipse at 50% 40%,#28104a,#05020c);display:flex;align-items:center;justify-content:center;font-family:"Courier New",monospace;color:#fff;touch-action:none;user-select:none;-webkit-user-select:none}
    .mm-arcade .cab{display:flex;flex-direction:column;align-items:center;gap:10px;padding:12px}
    .mm-arcade .mq{font:900 clamp(20px,4.4vw,34px)/1 Impact,"Arial Black",sans-serif;letter-spacing:.06em;color:#fff7c2;text-shadow:0 0 10px ${game.glow},0 0 26px ${game.glow};text-align:center}
    .mm-arcade .mq img{display:block;height:clamp(30px,6.5vw,52px);width:auto;margin:0 auto 4px;filter:drop-shadow(0 0 2px #2a0b38) drop-shadow(0 0 10px ${game.glow}) drop-shadow(0 0 22px ${game.glow})}
    .mm-arcade .mq b{display:block;font:900 clamp(11px,2.2vw,15px)/1.2 "Arial Black",Arial,sans-serif;letter-spacing:.18em;color:#fff;margin-bottom:2px}
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
  <button class="x" aria-label="Close the game">✕</button>${game.song === null ? "" : `<button class="mu" aria-label="Music on or off">♪</button>`}
  <div class="cab"><div class="mq">${game.pre ? `<b>${game.pre}</b>` : ""}<img src="${new URL("mummula-wordmark.png?v=1", BASE).href}" alt="MUMMULA">${game.sub ? `<small>${game.sub}</small>` : ""}</div>
    <canvas width="${game.W}" height="${game.H}"></canvas>
    <div class="hud"><span class="sc">SCORE 0</span><span class="hi">HI ${hiGet(game.key)}</span></div>
    <div class="pad">${game.pad.map(([k, l]) => `<button data-k="${k}">${l}</button>`).join("")}</div>
    <div class="help">${game.help}${game.song === null ? "" : " · M for music"} · Esc to leave</div></div>`;
  document.body.appendChild(ov);
  // Music: loops while the game is open. Starts right away if the browser allows it, otherwise on the first key or tap.
  // A game without its own song (song:null) plays silently and has no music button.
  const song = game.song === null ? {paused:false, play(){ return Promise.resolve(); }, pause(){}, removeAttribute(){}, load(){}} : new Audio(new URL("music/" + (game.song || game.key) + ".mp3?v=1", BASE).href);
  song.loop = true; song.volume = .6;
  const muBtn = ov.querySelector(".mu") || document.createElement("button");
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
  if(window.__mmTest) window.__mmSt = st;
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
  function close(){ if(!alive) return; alive = false; cancelAnimationFrame(raf); removeEventListener("keydown", kd, true); removeEventListener("keyup", ku, true); removeEventListener("resize", fit); song.pause(); song.removeAttribute("src"); song.load(); ov.remove(); cur = null; dispatchEvent(new Event("mummula-closed")); }
  cur = {close};
}
// Eric's wordmark, tinted to each cabinet's glow for the title screen (falls back to text until it loads).
const WM = new Image(); WM.src = new URL("mummula-wordmark.png?v=1", BASE).href;
const wmTint = {};
function wordmark(col){
  if(!WM.complete || !WM.naturalWidth) return null;
  if(!wmTint[col]){ const c = document.createElement("canvas"); c.width = WM.naturalWidth; c.height = WM.naturalHeight; const x = c.getContext("2d");
    x.drawImage(WM, 0, 0); x.globalCompositeOperation = "source-in"; x.fillStyle = col; x.fillRect(0, 0, c.width, c.height); wmTint[col] = c; }
  return wmTint[col];
}
function overlayText(g, game, st){
  g.fillStyle = "rgba(0,0,0,.45)"; g.fillRect(0, 0, game.W, game.H);
  g.textAlign = "center"; g.fillStyle = "#fff"; g.font = "bold 12px 'Courier New',monospace";
  const cx = game.W / 2, cy = game.H / 2;
  if(st.mode === "title"){
    const wm = wordmark(game.glow), ww = Math.min(120, game.W - 40), wh = wm ? Math.round(ww * wm.height / wm.width) : 0;
    if(game.pre){ g.fillStyle = "#fff"; g.font = "bold 10px 'Courier New',monospace"; g.fillText(game.pre, cx, cy - 26 - (wm ? wh : 18)); }
    if(wm) g.drawImage(wm, Math.round(cx - ww / 2), cy - 22 - wh, ww, wh);
    else { g.fillStyle = game.glow; g.font = "bold 16px Impact,'Arial Black',sans-serif"; g.fillText("MUMMULA", cx, cy - 26); }
    g.fillStyle = "#fff"; g.font = "bold 10px 'Courier New',monospace"; if(game.sub) g.fillText(game.sub, cx, cy - 12);
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
    st.waves = Array.from({length:16}, (_, i) => ({x:i * 22, y:Math.round(rnd(GROUND - 13, GROUND - 4)), w:Math.round(rnd(5, 12))}));
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
    // once you drop below the lip you're in the hole: you ride along with it and can't climb out sideways
    if(!m.pit && !m.on && m.y > GROUND - 10) m.pit = st.obs.find(o => o.kind === "pit" && m.x + 5 > o.x && m.x + 5 < o.x + o.w);
    if(m.pit){ m.x = Math.max(m.pit.x + 1, Math.min(m.pit.x + m.pit.w - m.w - 1, m.x)); m.on = false; }
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
    for(const o of st.obs) if(o.kind !== "pit" && !o.gone && hit(box, o)){ o.gone = true; m.stun = .45; m.x -= 34; m.vy = -120; st.shake = .3; ISLAND.pop(st, o.x + 5, o.y + 3, o.kind === "crab" ? "#ff2b4a" : "#8a7a8a"); }
    for(const b of st.balls) if(hit(box, b)) return ISLAND.die(st, "burned");
    for(const a of st.ankhs) if(hit(box, a)){ a.got = true; st.coins++; ISLAND.pop(st, a.x + 2, a.y + 4, "#7dff5a"); }
    for(const w of st.waves){ w.x -= sp * dt * (.2 + (w.y - GROUND + 14) * .02); if(w.x < -20){ w.x += 16 * 22; w.y = Math.round(rnd(GROUND - 13, GROUND - 4)); w.w = Math.round(rnd(5, 12)); } }
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
    // the sea behind the beach: deeper toward the shore, sunset glints under the sun, rolling crests and foam
    const sea = g.createLinearGradient(0, GROUND - 15, 0, GROUND); sea.addColorStop(0, "#6a5aa8"); sea.addColorStop(.25, "#2f6fb0"); sea.addColorStop(1, "#174a86");
    g.fillStyle = sea; g.fillRect(-4, GROUND - 15, 328, 15);
    g.fillStyle = "#ffb07a"; g.fillRect(-4, GROUND - 15, 328, 1);
    for(let i = 0; i < 7; i++){ const yy = GROUND - 13 + i * 2, ww = 26 - i * 2 + Math.round(Math.sin(st.t * 3 + i * 1.7) * 4);
      g.fillStyle = i % 2 ? "rgba(255,208,74,.75)" : "rgba(255,138,58,.7)"; g.fillRect(250 - ww / 2 + Math.round(Math.sin(st.t * 2 + i) * 2), yy, ww, 1); }
    for(const w of st.waves){ const wx = Math.round(w.x); g.fillStyle = "#0f3a6e"; g.fillRect(wx + 1, w.y + 1, w.w, 1); g.fillStyle = "#9fd8ff"; g.fillRect(wx, w.y, w.w, 1); g.fillStyle = "#fff"; g.fillRect(wx + w.w - 2, w.y, 2, 1); }
    // surf: a foamy line that washes up and back
    const surf = Math.round(Math.sin(st.t * 1.6) * 1.5);
    g.fillStyle = "rgba(255,255,255,.85)";
    for(let x = -Math.round((st.dist * .5) % 8); x < 324; x += 8){ g.fillRect(x, GROUND - 2 + surf, 6, 1); g.fillRect(x + 2, GROUND - 3 + surf, 3, 1); }
    // sand runs to the bottom of the screen
    const sand = g.createLinearGradient(0, GROUND, 0, 180); sand.addColorStop(0, "#f2d488"); sand.addColorStop(.25, "#e0bd6c"); sand.addColorStop(1, "#a9803e");
    g.fillStyle = sand; g.fillRect(-4, GROUND, 328, 36);
    g.fillStyle = "#fff0b8"; g.fillRect(-4, GROUND, 328, 1);
    const off = Math.round(st.dist % 24);
    for(let x = -off; x < 330; x += 24){ g.fillStyle = "#c79a50"; g.fillRect(x, GROUND + 5, 3, 1); g.fillRect(x + 13, GROUND + 12, 2, 1); g.fillRect(x + 6, GROUND + 22, 3, 1); g.fillStyle = "#fbe3a0"; g.fillRect(x + 18, GROUND + 7, 2, 1); g.fillRect(x + 3, GROUND + 16, 2, 1); }
    // pits: real holes in the sand, crumbly lips, walls in shadow, darkness at the bottom
    for(const o of st.obs) if(o.kind === "pit"){
      const ox = Math.round(o.x), ow = Math.round(o.w);
      const hole = g.createLinearGradient(0, GROUND, 0, 180); hole.addColorStop(0, "#5a3a1c"); hole.addColorStop(.35, "#24140a"); hole.addColorStop(1, "#000");
      g.fillStyle = hole; g.fillRect(ox, GROUND, ow, 36);
      g.fillStyle = "#8a6232"; g.beginPath(); g.moveTo(ox, GROUND); g.lineTo(ox + 5, GROUND); g.lineTo(ox + 2, GROUND + 9); g.lineTo(ox, 180); g.fill();
      g.fillStyle = "#3a2410"; g.beginPath(); g.moveTo(ox + ow, GROUND); g.lineTo(ox + ow - 4, GROUND); g.lineTo(ox + ow - 1, GROUND + 10); g.lineTo(ox + ow, 180); g.fill();
      g.fillStyle = "#fff0b8"; g.fillRect(ox - 3, GROUND - 1, 3, 1); g.fillRect(ox + ow, GROUND - 1, 3, 1);
      g.fillStyle = "#c79a50"; g.fillRect(ox - 1, GROUND, 2, 2); g.fillRect(ox + ow - 1, GROUND, 2, 2);
    }
    for(const o of st.obs){
      const ox = Math.round(o.x);
      if(o.kind === "crab") draw(g, CRAB, ox - 1, o.y - 3 + (Math.floor(st.t * 8) & 1), CRAB_PAL);
      if(o.kind === "rock"){ g.fillStyle = "#5a4a5a"; g.beginPath(); g.moveTo(ox, o.y + o.h); g.lineTo(ox + 2, o.y + 2); g.lineTo(ox + 7, o.y); g.lineTo(ox + 12, o.y + 4); g.lineTo(ox + 12, o.y + o.h); g.fill(); g.fillStyle = "#8a7a8a"; g.fillRect(ox + 3, o.y + 3, 3, 2); }
    }
    // ankhs float steadily with a slow glint
    for(const a of st.ankhs){ for(const [dx, dy] of [[-1,0],[1,0],[0,-1],[0,1]]) draw(g, ANKH, a.x + dx, a.y + dy, {O:"#1a0a2a"}); draw(g, ANKH, a.x, a.y, {O:"#7dff5a"}); if(Math.floor(st.t * 3 + a.y) % 6 === 0){ g.fillStyle = "#fff"; g.fillRect(Math.round(a.x) + 1, a.y + 1, 1, 1); } }
    for(const b of st.balls){
      g.fillStyle = "rgba(0,0,0,.35)"; g.fillRect(Math.round(b.x) - 1, GROUND - 1, 9, 2);
      const bx = Math.round(b.x), by = Math.round(b.y);
      g.fillStyle = "#ff5a12"; g.fillRect(bx, by, 7, 7); g.fillStyle = "#ffd04a"; g.fillRect(bx + 2, by + 2, 3, 3);
      g.fillStyle = "rgba(255,120,30,.5)"; g.fillRect(bx + 2, by - 6, 3, 5);
    }
    const m = st.m;
    const pit = m.pit;
    if(pit){ g.save(); g.beginPath(); g.rect(Math.round(pit.x), -10, Math.round(pit.w), 200); g.clip(); }
    if(!(st.mode === "over" && st.how !== "fell")){ if(!(m.stun && Math.floor(st.t * 16) % 2)) draw(g, RUN[m.on ? Math.floor(st.t * 10) & 1 : 1], m.x, m.y); }
    if(pit) g.restore();
    if(m.y > GROUND - 12){
      if(pit){ g.save(); g.beginPath(); g.rect(Math.round(pit.x), GROUND, Math.round(pit.w), 40); g.clip();
        g.fillStyle = `rgba(0,0,0,${Math.min(.95, (m.y - GROUND + 12) / 26)})`; g.fillRect(Math.round(m.x) - 1, Math.round(m.y), 14, 14); g.restore(); } }
    ISLAND.monster(g, st);
    for(const b of st.boom){ g.fillStyle = b.col; g.fillRect(b.x | 0, b.y | 0, 2, 2); }
    g.fillStyle = "#fff"; g.font = "bold 8px 'Courier New',monospace"; g.fillText("☥ " + st.coins, 290, 12);
    g.restore();
  }
};
/* ---------- Game 3: The Curse of Mummula ---------- */
// Old Man Mummula paces a ledge at the top of his tomb and hurls curses down. Dodge them, cape-dash through them, grab the ankhs.
// Mummula with his tall vampire collar popping up behind his head (used in The Curse of Mummula).
const CMUM = MUM.map(f => { const r = f.map(x => x.slice()); r[0] = ".k..wwww..k.".split(""); r[1] = ".kvwbwwbwvk.".split(""); r[2] = ".kvwrwwrwvk.".split(""); return r; });
const OLD_PAL = {f:"#d01c3a", F:"#17121a", w:"#efe6cf", b:"#b9ae94", k:"#17121a", p:"#b45cff", s:"#f0b8a8", W:"#ffffff", c:"#17121a", r:"#b0101a", u:"#4a1a78", U:"#6a2aa8", G:"#1f6a3a", d:"#8a4a1c", P:"#f0d8ff", q:"#7a2ac8"};
// Old Man Mummula: red fez with a black tassel, gauze strips hanging down from his head either side of his face,
// round black sunglasses with purple lenses, a bandaged face with a toothy grin, tall black vampire collar with a red lining, purple velvet robe
// with a green sash, and a cane. Second frame: arm raised to throw.
const OLD = [spr([
  "......ffff......",
  "......fffffF....",
  ".....ffffffF....",
  ".....ffffffF....",
  "....wwwwwwww....",
  ".c.wwbwwwwbww.c.",
  ".crkkkkkkkkkrc..",
  ".crkPppkPppkrc..",
  ".crkqqqkqqqkrc..",
  ".crwkkkskkkwrc..",
  ".crw.wwwww.wrc..",
  ".crw.kWkWk.wrc..",
  ".crw.wwwww.wrc..",
  "cuuw.uuuuu.wuucd",
  "cuUw.uUuUu.wUusd",
  "cuUw.uuUuu.wUu.d",
  "cuUwuuuUuuuwUu.d",
  "cuUuuGGGGGuuUu.d",
  "c.uuuuGuGuuuu..d",
  "..uuuuUuUuuuu..d",
  "..uuuuuUuuuuu..d",
  "...kk.....kk...d"]), spr([
  "s.....ffff......",
  "s.....fffffF....",
  "u....ffffffF....",
  "u....ffffffF....",
  "u...wwwwwwww....",
  "uc.wwbwwwwbww.c.",
  "ucrkkkkkkkkkrc..",
  "ucrkPppkPppkrc..",
  "ucrkqqqkqqqkrc..",
  "ucrwkkkskkkwrc..",
  "ucrw.wwwww.wrc..",
  "ucrw.kWkWk.wrc..",
  "ucrw.wwwww.wrc..",
  "cuuw.uuuuu.wuucd",
  "cuUw.uUuUu.wUusd",
  "cuUw.uuUuu.wUu.d",
  "cuUwuuuUuuuwUu.d",
  "cuUuuGGGGGuuUu.d",
  "c.uuuuGuGuuuu..d",
  "..uuuuUuUuuuu..d",
  "..uuuuuUuuuuu..d",
  "...kk.....kk...d"])];
// Cursed things he throws. Bright fills, dark outlines (drawn by outl), so they pop off the dark stone.
const JAR = spr([
  "...ccc...",
  "...cCc...",
  "..LLLLL..",
  "...LgL...",
  "..LgWgL..",
  ".LgWgggL.",
  "LgWGGGGGL",
  "LGWGGGGGL",
  "LGGGGGGGL",
  ".LGGGGGL.",
  "..LLLLL.."]);
const SKULL = spr([
  ".WWWWW.",
  "WWWWWWW",
  "WkkWkkW",
  "WkkWkkW",
  "WWWkWWW",
  ".WkWkW.",
  ".WWWWW."]);
const SCARAB = [spr([
  "...ttttt...",
  "....ttt....",
  "....tSt....",
  ".GGtSSStGG.",
  "...tSSSt...",
  "GGtBBdBBtGG",
  "..tCBdCBt..",
  "..tBBdBBt..",
  "GGtBBdBBtGG",
  "..tBBdBBt..",
  "...tBdBt...",
  "....ttt...."]), spr([
  "...ttttt...",
  "....ttt....",
  "....tSt....",
  "...tSSSt...",
  ".GGtSSStGG.",
  "..tBBdBBt..",
  "GGtCBdCBtGG",
  "..tBBdBBt..",
  "..tBBdBBt..",
  "GGtBBdBBtGG",
  "...tBdBt...",
  "....ttt...."])];
// Mummula shielding: a Dracula pose, cape swept up across his body (red lining showing where he holds the edge),
// tall pointed collar popping up behind his head, eyes peeking over the top.
const SHIELD = spr([
  ".k............k.",
  ".kk...wwww...kk.",
  ".kvk.wbwwbw.kvk.",
  "..kvkwrwwrwkvk..",
  "..kvkkkkkkkkvkww",
  "..kkkkkkkkkkkkvw",
  ".kkMkkkkMkkkkkv.",
  ".kMkkkkMkkkkkkv.",
  "kMkkkkMkkkkkkkv.",
  "kkkkkMkkkkkMkkv.",
  "kkkkMkkkkkMkkkv.",
  "kkkMkkkkkMkkkkv.",
  "kk.kkk.kkk.kkkv.",
  "k...k...k...kk..",
  ".....ww..ww....."]);
// Curse bolt: a slim lightning bolt, sharp at both ends, drawn pointing down (+y) and turned along its flight path.
const BOLT = [[3.3, -11.7], [-6, 2.1], [.7, .3], [-3.4, 11.7], [6, -2.6], [1.4, -1.3]];
const HEART = spr([".rr.rr.", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."]);
function outl(g, rows, x, y, pal, s, oc){
  s = s || 1; const o = Math.max(1, Math.round(s));
  for(const [dx, dy] of [[-o,0],[o,0],[0,-o],[0,o]]) draw(g, rows, x + dx, y + dy, new Proxy({}, {get:() => oc || "#0a0612"}), s);
  draw(g, rows, x, y, pal, s);
}
const CFLOOR = 270, LEDGE = 58;
const TAUNTS = ["CURSE YOU!", "BAH!", "KIDS THESE DAYS!", "OFF MY PYRAMID!", "IN MY DAY...", "HEH HEH HEH", "MY BACK!", "BEGONE!"];
const CURSE = {
  key:"curse", W:224, H:288, glow:"#b45cff", pre:"THE CURSE OF", sub:"", song:"curse",
  help:"← → dodge · Space, ↑ or tap to cape-dash · hold ↓ to shield (it runs out) · grab ankhs",
  start:"PRESS START", pad:[["left","◀"],["fire","DASH"],["down","SHIELD"],["right","▶"]],
  reset(st){
    st.p = {x:100, y:CFLOOR - 24, w:24, h:24, inv:0, dash:0, cool:0, face:1, trail:[], sh:1, shT:0, shield:false, shLock:false}; st.texts = []; st.notes = [];
    st.old = {x:100, tx:100, wind:0, tt:1.6, face:1, say:"", sayT:0, sayNext:2.5};
    st.lives = 3; st.lvl = 1; st.surv = 0; st.bonus = 0; st.curse = 0; st.banner = 1.6; st.shake = 0;
    st.things = []; st.puffs = []; st.boom = []; st.nextAnkh = 3; st.saved = false; st.newHi = false;
    st.dust = Array.from({length:24}, () => ({x:rnd(0, 224), y:rnd(60, 270), v:rnd(3, 9)}));
  },
  kinds(lvl){ return ["jar", "skull", "jar", "skull", "record", "record"].concat(lvl >= 2 ? ["scarab", "scarab"] : [], lvl >= 3 ? ["bolt", "bolt"] : [], lvl >= 4 ? ["hex"] : []); },
  throw(st){
    const o = st.old, p = st.p, hx = o.x + (o.face > 0 ? 28 : 4), hy = LEDGE - 42;
    const ks = CURSE.kinds(st.lvl), k = ks[Math.floor(Math.random() * ks.length)];
    const aim = (p.x + 12 + rnd(-30, 30)) - hx;
    if(k === "jar") st.things.push({k, x:hx - 9, y:hy, w:18, h:22, vx:aim * .55, vy:-40});
    if(k === "skull") st.things.push({k, x:hx - 7, y:hy, w:14, h:14, vx:rnd(40, 75) * (aim < 0 ? -1 : 1), vy:-20, n:0});
    if(k === "scarab") st.things.push({k, x:hx - 11, y:hy, w:22, h:24, x0:hx - 11 + aim * .5, ph:Math.random() * 6, vy:62 + st.lvl * 5});
    if(k === "bolt"){ const dx = p.x + 12 - hx, dy = p.y + 12 - hy, d = Math.hypot(dx, dy), v = 120 + st.lvl * 8;
      // lobbed in an arc that still comes down where Mummula is standing
      const T = Math.max(.55, Math.min(1.5, d / v)); st.things.push({k, x:hx - 3, y:hy, w:6, h:6, vx:dx / T, vy:dy / T - 80 * T}); }
    // a vinyl record, flung like a frisbee: it sails down in an arc, lands on its edge and rolls away across the floor
    if(k === "record") st.things.push({k, x:hx - 9, y:hy, w:18, h:9, vx:Math.sign(aim || 1) * rnd(55, 85), vy:-30, spin:0, roll:false});
    if(k === "hex") st.things.push({k, x:hx - 7, y:hy, w:14, h:14, x0:hx - 7 + aim * .6, ph:Math.random() * 6, vy:48});
  },
  update(st, dt, k, pr){
    const p = st.p, o = st.old;
    st.surv += dt;
    const lvl = 1 + Math.floor(st.surv / 20);
    if(lvl !== st.lvl){ st.lvl = lvl; st.banner = 1.6; st.bonus += 100 * (lvl - 1); }
    st.banner = Math.max(0, st.banner - dt); st.shake = Math.max(0, st.shake - dt);
    st.score = Math.floor(st.surv * 10) + st.bonus;
    for(const d of st.dust){ d.y += d.v * dt; d.x += Math.sin(st.t + d.v) * 2 * dt; if(d.y > 270){ d.y = 62; d.x = rnd(0, 224); } }
    // Mummula: left/right (swapped while hexed), dash = a quick, untouchable swoop of the cape
    st.curse = Math.max(0, st.curse - dt);
    let dir = (k.right ? 1 : 0) - (k.left ? 1 : 0); if(st.curse > 0) dir = -dir;
    if(dir) p.face = dir;
    p.cool -= dt; p.inv -= dt;
    if((pr.fire || pr.tap || pr.up) && p.cool <= 0){ p.dash = .18; p.cool = .8; }
    // Shield: hold ↓ to wrap the cape round. He can't move while it's up; the meter lasts 1.5s and refills in 4s once it's down.
    // Run it dry and you have to let go of ↓ before it comes back up.
    if(!k.down) p.shLock = false;
    p.shield = !!k.down && !p.shLock && p.sh > 0 && p.dash <= 0;
    if(p.shield){ p.sh = Math.max(0, p.sh - dt / 1.5); p.shT += dt; if(p.sh <= 0){ p.shLock = true; p.shield = false; } }
    else { p.shT = 0; if(!k.down || p.shLock) p.sh = Math.min(1, p.sh + dt / 4); }
    if(p.dash > 0){ p.dash -= dt; p.x += p.face * 330 * dt; p.trail.push({x:p.x, life:.25}); }
    else if(!p.shield) p.x += dir * 110 * dt;
    p.x = Math.max(0, Math.min(200, p.x));
    for(const t of p.trail) t.life -= dt; p.trail = p.trail.filter(t => t.life > 0);
    // Old Man Mummula shuffles along the ledge, winds up, throws. Faster and meaner each level; doubles up from level 5.
    if(o.wind > 0){ o.wind -= dt; if(o.wind <= 0){ CURSE.throw(st); if(st.lvl >= 5 && Math.random() < Math.min(.6, .15 * (st.lvl - 4))) CURSE.throw(st); } }
    else {
      const sp = 26 + st.lvl * 5;
      if(Math.abs(o.tx - o.x) < 2) o.tx = rnd(8, 184);
      o.face = o.tx > o.x ? 1 : -1; o.x += o.face * Math.min(sp * dt, Math.abs(o.tx - o.x));
      o.tt -= dt; if(o.tt <= 0){ o.wind = .4; o.tt = Math.max(.42, 1.45 - st.lvl * .13) * rnd(.75, 1.25); }
    }
    o.sayT -= dt; o.sayNext -= dt;
    if(o.sayNext <= 0){ o.say = TAUNTS[Math.floor(Math.random() * TAUNTS.length)]; o.sayT = 1.6; o.sayNext = rnd(5, 9); }
    // ankhs and the odd heart drop from cracks in the ceiling
    st.nextAnkh -= dt;
    if(st.nextAnkh <= 0){ const heart = st.lives < 3 && Math.random() < .18;
      st.things.push({k:heart ? "heart" : "ankh", x:rnd(10, 200), y:LEDGE + 4, w:heart ? 14 : 10, h:heart ? 12 : 16, vy:45, good:true}); st.nextAnkh = rnd(2.5, 4.5); }
    // move the curses
    for(const t of st.things){
      if(t.k === "jar"){ t.vy += 240 * dt; t.x += t.vx * dt; t.y += t.vy * dt;
        if(t.y + t.h >= CFLOOR){ t.gone = true; st.shake = .18; st.puffs.push({x:t.x - 4, y:CFLOOR - 16, w:26, h:16, life:.8, max:.8}); CURSE.pop(st, t.x + 6, CFLOOR - 4, "#7dff5a", 14); } }
      if(t.k === "skull"){ t.vy += 300 * dt; t.x += t.vx * dt; t.y += t.vy * dt;
        if(t.x < 0 || t.x > 210){ t.vx = -t.vx; t.x = Math.max(0, Math.min(210, t.x)); }
        if(t.y + t.h >= CFLOOR){ t.y = CFLOOR - t.h; t.n++; t.vy = -[210, 150, 0][Math.min(2, t.n - 1)]; if(t.n >= 3){ t.gone = true; CURSE.pop(st, t.x + 7, t.y + 7, "#fff", 10); } } }
      if(t.k === "scarab" || t.k === "hex"){ t.y += t.vy * dt; t.ph += dt * (t.k === "hex" ? 2.4 : 4); t.x = Math.max(0, Math.min(210, t.x0 + Math.sin(t.ph) * (t.k === "hex" ? 22 : 34))); if(t.y > CFLOOR - t.h){ t.gone = true; CURSE.pop(st, t.x + 7, t.y + 7, t.k === "hex" ? "#d27bff" : "#3cf0ff", 10); } }
      if(t.k === "record"){ t.spin += dt * 14; t.nt = (t.nt || 0) - dt;
        if(t.nt <= 0){ t.nt = .11; st.notes.push({x:t.x + t.w / 2 - Math.sign(t.vx) * 8, y:t.y + rnd(-2, 4), vx:-t.vx * .15, life:.8, c:["#ffef3a", "#3cf0ff", "#ff4fd8"][Math.floor(Math.random() * 3)], two:Math.random() < .4}); }
        if(!t.roll){ t.vy += 150 * dt; t.x += t.vx * dt; t.y += t.vy * dt; if(t.x < 0 || t.x > 210){ t.vx = -t.vx; t.x = Math.max(0, Math.min(210, t.x)); }
          if(t.y + t.h >= CFLOOR){ t.roll = true; t.y = CFLOOR - 15; t.x += 2; t.w = 14; t.h = 15; t.vx = Math.sign(t.vx) * 95; st.shake = .12; CURSE.pop(st, t.x + 3, CFLOOR - 2, "#3cf0ff", 8); } }
        else { t.x += t.vx * dt; if(t.x < -20 || t.x > 240) t.gone = true; } }
      if(t.k === "bolt"){ t.vy += 160 * dt; t.x += t.vx * dt; t.y += t.vy * dt; if(t.y > CFLOOR - 4 || t.x < -10 || t.x > 234){ t.gone = true; CURSE.pop(st, t.x + 3, Math.min(t.y, CFLOOR - 3), "#7dff5a", 8); } }
      if(t.good){ t.y += t.vy * dt; if(t.y > CFLOOR - t.h) t.vy = 0, t.life = (t.life ?? 2.5) - dt; if(t.life <= 0) t.gone = true; }
    }
    for(const u of st.puffs) u.life -= dt;
    st.puffs = st.puffs.filter(u => u.life > 0);
    // collisions
    const box = {x:p.x + 5, y:p.y + 4, w:14, h:20};
    for(const t of st.things){
      if(t.gone || !hit(box, t)) continue;
      if(t.k === "ankh"){ t.gone = true; st.bonus += 50; CURSE.pop(st, t.x + 5, t.y + 8, "#ffcf3a", 10); continue; }
      if(t.k === "heart"){ t.gone = true; st.lives = Math.min(3, st.lives + 1); CURSE.pop(st, t.x + 3, t.y + 3, "#ff3b3b", 10); continue; }
      if(p.dash > 0 || p.inv > 0) continue;
      t.gone = true;
      // the cape blocks everything; a block in the first instant is a perfect block
      if(p.shield){
        CURSE.pop(st, t.x + t.w / 2, t.y + t.h / 2, "#ffffff", 10); CURSE.pop(st, t.x + t.w / 2, t.y + t.h / 2, "#d27bff", 8); st.shake = .1;
        if(p.shT < .2){ st.bonus += 25; st.texts.push({x:p.x + 12, y:p.y - 10, s:"PERFECT +25", life:.9}); }
        continue; }
      if(t.k === "hex"){ st.curse = 4; st.shake = .3; CURSE.pop(st, p.x + 12, p.y + 12, "#d27bff", 18); continue; }
      CURSE.hurt(st);
    }
    if(p.dash <= 0 && p.inv <= 0 && !p.shield) for(const u of st.puffs) if(u.life > .15 && hit(box, u)){ CURSE.hurt(st); break; }
    st.things = st.things.filter(t => !t.gone);
    for(const n of st.notes){ n.x += n.vx * dt; n.y -= 14 * dt; n.life -= dt; } st.notes = st.notes.filter(n => n.life > 0);
    for(const x of st.texts){ x.y -= 18 * dt; x.life -= dt; } st.texts = st.texts.filter(x => x.life > 0);
    for(const b of st.boom){ b.x += b.vx * dt; b.y += b.vy * dt; b.vy += 90 * dt; b.life -= dt; }
    st.boom = st.boom.filter(b => b.life > 0);
  },
  hurt(st){ const p = st.p; st.lives--; p.inv = 1.6; st.shake = .4; CURSE.pop(st, p.x + 12, p.y + 12, "#efe6cf", 16);
    if(st.lives <= 0){ st.mode = "over"; st.old.say = "HEH HEH HEH!"; st.old.sayT = 9; } },
  pop(st, x, y, col, n){ for(let i = 0; i < (n || 12); i++){ const a = Math.random() * 6.28, v = rnd(20, 70); st.boom.push({x, y, vx:Math.cos(a)*v, vy:Math.sin(a)*v - 20, life:rnd(.3, .7), col}); } },
  render(g, st){
    g.save();
    if(st.shake > 0) g.translate(Math.round(rnd(-2, 2)), Math.round(rnd(-2, 2)));
    // the tomb: dim sandstone blocks with faint hieroglyphs, torchlight from both sides
    g.fillStyle = "#1a0f22"; g.fillRect(-4, -4, 232, 296);
    for(let r = 0; r < 20; r++) for(let c = -1; c < 8; c++){
      const x = c * 32 + (r % 2 ? 16 : 0), y = 60 + r * 11;
      g.fillStyle = (r * 7 + c * 3) % 5 ? "#2a1a2c" : "#2f1e30"; g.fillRect(x + 1, y + 1, 30, 9);
    }
    g.fillStyle = "#3a2738";
    const gl = ["☥", "◉", "△", "≋", "☥", "◎"];
    g.font = "9px serif"; g.textAlign = "center";
    for(let i = 0; i < 12; i++) g.fillText(gl[i % gl.length], 22 + (i % 6) * 36, 110 + Math.floor(i / 6) * 70);
    g.textAlign = "left";
    for(const tx of [10, 214]){
      const fl = Math.sin(st.t * 17 + tx) * .5 + Math.sin(st.t * 9.3 + tx) * .5;
      const lg = g.createRadialGradient(tx, 150, 2, tx, 150, 70 + fl * 6); lg.addColorStop(0, "rgba(255,150,60,.35)"); lg.addColorStop(1, "rgba(255,150,60,0)");
      g.fillStyle = lg; g.fillRect(tx - 80, 70, 160, 160);
      g.fillStyle = "#5a3a1c"; g.fillRect(tx - 2, 152, 4, 12); g.fillStyle = "#8a6232"; g.fillRect(tx - 4, 150, 8, 3);
      g.fillStyle = "#ff7a1a"; g.fillRect(tx - 3, 143 - Math.round(fl), 6, 7 + Math.round(fl)); g.fillStyle = "#ffd04a"; g.fillRect(tx - 1, 145, 3, 5);
    }
    // floating dust in the torchlight
    g.fillStyle = "rgba(255,220,170,.35)"; for(const d of st.dust) g.fillRect(d.x | 0, d.y | 0, 1, 1);
    // ceiling + ledge Old Man Mummula walks on
    g.fillStyle = "#0e0814"; g.fillRect(-4, -4, 232, LEDGE + 4);
    g.fillStyle = "#3b2440"; for(let x = 0; x < 224; x += 16){ g.fillRect(x + 1, 6, 14, 10); g.fillRect(x + 9, 18, 14, 10); }
    g.fillStyle = "#5a3c3a"; g.fillRect(-4, LEDGE, 232, 6); g.fillStyle = "#ffcf3a"; g.fillRect(-4, LEDGE, 232, 1); g.fillStyle = "#2a1520"; g.fillRect(-4, LEDGE + 6, 232, 2);
    // floor
    g.fillStyle = "#3a2430"; g.fillRect(-4, CFLOOR, 232, 22); g.fillStyle = "#c89a5a"; g.fillRect(-4, CFLOOR, 232, 1);
    g.fillStyle = "#2a1820"; for(let x = 0; x < 224; x += 28) g.fillRect(x, CFLOOR + 1, 1, 18);
    // Old Man Mummula
    const o = st.old, ox = Math.round(o.x), bob = o.wind > 0 ? 0 : (Math.floor(st.t * 5) % 2);
    const oldRows = (o.wind > 0 ? OLD[1] : OLD[0]).map(r => o.face > 0 ? r.slice().reverse() : r);
    const glow = o.wind > 0 ? (Math.floor(st.t * 20) % 2 ? "#7dff5a" : "#e8ffd8") : null;
    outl(g, oldRows, ox, LEDGE - 44 + bob, glow ? Object.assign({}, OLD_PAL, {p:glow, q:glow}) : OLD_PAL, 2, "#5a3a80");
    if(o.wind > 0){ g.fillStyle = "rgba(125,255,90," + (.4 + .3 * Math.sin(st.t * 40)) + ")"; g.beginPath(); g.arc(ox + (o.face > 0 ? 28 : 4), LEDGE - 42, 5, 0, 6.28); g.fill(); }
    if(o.sayT > 0){
      g.font = "bold 7px 'Courier New',monospace"; const tw = g.measureText(o.say).width + 8;
      const bx = ox > 112 ? Math.max(2, ox - tw - 2) : Math.min(222 - tw, ox + 34), by = LEDGE - 44;
      g.fillStyle = "#fff"; g.fillRect(bx, by, tw, 11); g.fillRect(ox > 112 ? bx + tw - 3 : bx, by + 11, 3, 3);
      g.fillStyle = "#1a0f22"; g.fillText(o.say, bx + 4, by + 8);
    }
    // curse clouds left by shattered jars
    for(const u of st.puffs){ const a = Math.min(1, u.life / u.max * 1.6);
      for(let i = 0; i < 5; i++){ g.fillStyle = `rgba(${i % 2 ? "125,255,90" : "60,200,80"},${.55 * a})`; g.beginPath(); g.arc(u.x + 4 + i * 4.5, u.y + 10 - Math.sin(st.t * 8 + i) * 2 - (i % 2) * 3, 5 + (i % 3), 0, 6.28); g.fill(); }
      g.fillStyle = `rgba(230,255,220,${a})`; g.fillRect(Math.round(u.x + 8), Math.round(u.y + 4 - st.t * 3 % 3), 1, 1); g.fillRect(Math.round(u.x + 16), Math.round(u.y + 7), 1, 1); }
    // the curses
    const fl = Math.floor(st.t * 8) % 2;
    // little music notes trailing out behind flying records
    for(const n of st.notes){ const nx = Math.round(n.x), ny = Math.round(n.y); g.globalAlpha = Math.min(1, n.life * 2);
      for(const c of ["#0a0612", n.c]){ const o = c === n.c ? 0 : 1;
        g.fillStyle = c; g.fillRect(nx - o, ny + 4 - o, 3 + 2 * o, 2 + 2 * o); g.fillRect(nx + 2 - o, ny - o, 1 + 2 * o, 5 + 2 * o);
        if(n.two){ g.fillRect(nx + 4 - o, ny + 3 - o, 3 + 2 * o, 2 + 2 * o); g.fillRect(nx + 6 - o, ny - 1 - o, 1 + 2 * o, 5 + 2 * o); g.fillRect(nx + 2 - o, ny - 1 - o, 5 + 2 * o, 1 + 2 * o); }
        else g.fillRect(nx + 3 - o, ny + 1 - o, 1 + 2 * o, 1 + 2 * o); } }
    g.globalAlpha = 1;
    for(const t of st.things){
      const tx = Math.round(t.x), ty = Math.round(t.y);
      if(t.good && t.life < 1 && fl) continue;
      if(t.k === "jar"){ g.fillStyle = "rgba(125,255,90,.25)"; g.beginPath(); g.arc(tx + 9, ty + 14, 13, 0, 6.28); g.fill();
        outl(g, JAR, tx, ty, {c:"#b07a44", C:"#d8a868", L:"#d8f0ff", g:"#5a8a98", W:"#ffffff", G:fl ? "#7dff5a" : "#5ae04a"}, 2); }
      if(t.k === "skull"){ outl(g, SKULL, tx, ty, {W:"#ffffff", k:"#1a0f22"}, 2); if(fl){ g.fillStyle = "#7dff5a"; g.fillRect(tx + 2, ty + 4, 2, 2); g.fillRect(tx + 8, ty + 4, 2, 2); } }
      if(t.k === "scarab") outl(g, SCARAB[fl], tx, ty, {t:"#3a2a1e", S:"#8a6a48", B:"#7a5a3a", C:"#b89870", d:"#2a1e14", G:"#4a3828"}, 2, "#d8c8a8");
      if(t.k === "bolt"){ const cx = tx + 3, cy = ty + 3;
        g.fillStyle = `rgba(125,255,90,${fl ? .35 : .2})`; g.beginPath(); g.arc(cx, cy, 10, 0, 6.28); g.fill();
        g.save(); g.translate(cx, cy); g.rotate(Math.atan2(t.vy, t.vx) - Math.PI / 2);
        const path = k => { g.beginPath(); BOLT.forEach(([x, y], n) => n ? g.lineTo(x * k * 1.25, y * k * 1.25) : g.moveTo(x * k * 1.25, y * k * 1.25)); g.closePath(); };
        g.lineJoin = "miter"; path(1); g.strokeStyle = "#0a0612"; g.lineWidth = 2.5; g.stroke(); g.fillStyle = "#7dff5a"; g.fill();
        path(.55); g.fillStyle = fl ? "#ffffff" : "#e8ff8a"; g.fill(); g.restore(); }
      if(t.k === "record"){
        if(!t.roll){ // a flying disc seen at an angle, wobbling: black vinyl, a pale rim, groove rings, red label, glint
          const cx = tx + 9, cy = ty + 4, ry = 3.4 + Math.sin(t.spin * .5) * 1.4;
          g.fillStyle = "#c8c8d8"; g.beginPath(); g.ellipse(cx, cy, 10, ry + 1, 0, 0, 6.28); g.fill();
          g.fillStyle = "#111"; g.beginPath(); g.ellipse(cx, cy, 9, ry, 0, 0, 6.28); g.fill();
          g.strokeStyle = "#4a4a58"; g.lineWidth = 1; g.beginPath(); g.ellipse(cx, cy, 6.5, ry * .7, 0, 0, 6.28); g.stroke(); g.beginPath(); g.ellipse(cx, cy, 4.5, ry * .5, 0, 0, 6.28); g.stroke();
          g.fillStyle = "#ff3b3b"; g.beginPath(); g.ellipse(cx, cy, 2.6, Math.max(1, ry * .35), 0, 0, 6.28); g.fill(); g.fillStyle = "#fff"; g.fillRect(cx, cy, 1, 1);
          g.fillStyle = "#fff"; g.fillRect(Math.round(cx + Math.cos(t.spin) * 7), Math.round(cy + Math.sin(t.spin) * ry * .8), 2, 1);
        } else { // rolling across the floor: a round disc, face on, turning as it goes
          const cx = tx + 7, cy = ty + 7, a = t.x / 7 * Math.sign(t.vx);
          g.fillStyle = "#c8c8d8"; g.beginPath(); g.arc(cx, cy, 8, 0, 6.28); g.fill();
          g.fillStyle = "#111"; g.beginPath(); g.arc(cx, cy, 7, 0, 6.28); g.fill();
          g.strokeStyle = "#4a4a58"; g.lineWidth = 1; g.beginPath(); g.arc(cx, cy, 5, 0, 6.28); g.stroke(); g.beginPath(); g.arc(cx, cy, 3.6, 0, 6.28); g.stroke();
          g.fillStyle = "#ff3b3b"; g.beginPath(); g.arc(cx, cy, 2.4, 0, 6.28); g.fill();
          g.fillStyle = "#ffcf3a"; g.fillRect(Math.round(cx + Math.cos(a) * 1.4) - 1, Math.round(cy + Math.sin(a) * 1.4) - 1, 1, 1); g.fillStyle = "#000"; g.fillRect(cx, cy, 1, 1);
          g.fillStyle = "#fff"; g.fillRect(Math.round(cx + Math.cos(a) * 6) - 1, Math.round(cy + Math.sin(a) * 6) - 1, 2, 2);
        } }
      if(t.k === "hex"){ g.save(); g.translate(tx + 7, ty + 7); g.rotate(st.t * 5);
        g.fillStyle = "rgba(210,123,255,.3)"; g.beginPath(); g.arc(0, 0, 10, 0, 6.28); g.fill();
        g.strokeStyle = "#0a0612"; g.lineWidth = 4; g.beginPath(); for(let a = 0; a < 12; a += .3) g.lineTo(Math.cos(a) * a * .6, Math.sin(a) * a * .6); g.stroke();
        g.strokeStyle = "#e08cff"; g.lineWidth = 2; g.beginPath(); for(let a = 0; a < 12; a += .3) g.lineTo(Math.cos(a) * a * .6, Math.sin(a) * a * .6); g.stroke(); g.restore(); }
      if(t.k === "ankh"){ outl(g, ANKH, tx, ty, {O:"#ffcf3a"}, 2); if(Math.floor(st.t * 3 + t.x) % 5 === 0){ g.fillStyle = "#fff"; g.fillRect(tx + 2, ty + 2, 2, 2); } }
      if(t.k === "heart") outl(g, HEART, tx, ty, null, 2);
    }
    // Mummula (cape trail while dashing, flicker while recovering, purple while hexed)
    const p = st.p, hexed = st.curse > 0;
    const mpal = hexed ? {w:"#d9b8ff", b:"#9a6ad0", v:"#7a1ab0"} : null;
    for(const t of p.trail){ g.globalAlpha = t.life * 2; draw(g, CMUM[0], t.x, p.y, {w:"#6a3a9a", b:"#6a3a9a", r:"#6a3a9a", k:"#3a1a5a", v:"#6a3a9a"}, 2); }
    g.globalAlpha = 1;
    if(p.shield && st.mode === "play"){ g.fillStyle = `rgba(210,123,255,${.22 + .1 * Math.sin(st.t * 30)})`; g.beginPath(); g.arc(p.x + 12, p.y + 12, 19, Math.PI, 0); g.fill();
      outl(g, SHIELD, p.x - 4, p.y - 6, Object.assign({M:"#3a2a5a"}, mpal), 2, "#d27bff"); }
    else if(!(p.inv > 0 && Math.floor(st.t * 12) % 2) && st.mode !== "title") outl(g, CMUM[(Math.floor(st.t * 8) % 2) * ((st.mode === "play" && p.dash <= 0) ? 1 : 0)], p.x, p.y, mpal, 2, "#6a4a90");
    if(p.sh < 1 && st.mode === "play"){ g.fillStyle = "#1a2a3a"; g.fillRect(p.x + 6, p.y - 9, 12, 2); g.fillStyle = p.shLock ? "#ff4f4f" : "#3cf0ff"; g.fillRect(p.x + 6, p.y - 9, Math.round(12 * p.sh), 2); }
    g.textAlign = "center"; g.font = "bold 8px 'Courier New',monospace";
    for(const x of st.texts){ g.fillStyle = "#0a0612"; g.fillText(x.s, x.x + 1, x.y + 1); g.fillStyle = "#ffcf3a"; g.fillText(x.s, x.x, x.y); }
    g.textAlign = "left";
    if(p.cool > 0 && st.mode === "play"){ g.fillStyle = "#3a2440"; g.fillRect(p.x + 6, p.y - 5, 12, 2); g.fillStyle = "#b45cff"; g.fillRect(p.x + 6, p.y - 5, Math.round(12 * (1 - p.cool / .8)), 2); }
    for(const b of st.boom){ g.fillStyle = b.col; g.fillRect(b.x | 0, b.y | 0, 2, 2); }
    // HUD
    g.fillStyle = "#fff"; g.font = "bold 8px 'Courier New',monospace"; g.fillText("CURSE " + st.lvl, 4, 284);
    for(let i = 0; i < st.lives; i++) outl(g, HEART, 196 + i * 9 - 9, 278, null);
    if(hexed){ g.fillStyle = `rgba(180,92,255,${.12 + .08 * Math.sin(st.t * 10)})`; g.fillRect(-4, -4, 232, 296);
      if(Math.floor(st.t * 4) % 2){ g.textAlign = "center"; g.fillStyle = "#e08cff"; g.font = "bold 12px Impact,'Arial Black',sans-serif"; g.fillText("HEXED! CONTROLS FLIPPED", 112, 82); g.textAlign = "left"; } }
    if(st.banner > 0 && st.mode === "play"){ g.textAlign = "center"; g.fillStyle = "#ffcf3a"; g.font = "bold 14px Impact,'Arial Black',sans-serif"; g.fillText("CURSE LEVEL " + st.lvl, 112, 150);
      const note = ["", "", "WATCH FOR SCARABS", "CURSE BOLTS AIM AT YOU", "BEWARE THE PURPLE HEX", "DOUBLE CURSES!"][st.lvl] || "";
      if(note){ g.fillStyle = "#fff"; g.font = "bold 9px 'Courier New',monospace"; g.fillText(note, 112, 164); } g.textAlign = "left"; }
    g.restore();
  }
};
window.MummulaArcade = {open};
})();
