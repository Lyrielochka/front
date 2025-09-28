export function initSound(){
  const btn = document.getElementById('soundToggle');
  if(!btn) return;
  let ctx, source, gain, lp, hp;
  const PREF_KEY = 'ww1-sound-on';
  function createNoiseBuffer(context, seconds=2){
    const rate = context.sampleRate;
    const length = seconds * rate;
    const buffer = context.createBuffer(1, length, rate);
    const data = buffer.getChannelData(0);
    let b0=0,b1=0,b2=0,b3=0,b4=0,b5=0,b6=0;
    for (let i=0;i<length;i++){
      const white = Math.random()*2-1;
      b0 = 0.99886*b0 + white*0.0555179;
      b1 = 0.99332*b1 + white*0.0750759;
      b2 = 0.96900*b2 + white*0.1538520;
      b3 = 0.86650*b3 + white*0.3104856;
      b4 = 0.55000*b4 + white*0.5329522;
      b5 = -0.7616*b5 - white*0.0168980;
      const pink = b0+b1+b2+b3+b4+b5+b6 + white*0.5362;
      b6 = white*0.115926;
      data[i] = pink * 0.12;
    }
    return buffer;
  }
  function buildGraph(){
    ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
    gain = ctx.createGain();
    lp = ctx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value = 1400; lp.Q.value = 0.4;
    hp = ctx.createBiquadFilter(); hp.type='highpass'; hp.frequency.value = 60;
    source = ctx.createBufferSource();
    source.buffer = createNoiseBuffer(ctx, 4);
    source.loop = true;
    source.connect(hp).connect(lp).connect(gain).connect(ctx.destination);
    gain.gain.value = 0.0;
    source.start(0);
  }
  function fade(to=0.08, ms=600){
    if(!ctx || !gain) return;
    const now = ctx.currentTime;
    const target = Math.max(0, Math.min(0.25, to));
    gain.gain.cancelScheduledValues(now);
    gain.gain.setValueAtTime(gain.gain.value, now);
    gain.gain.linearRampToValueAtTime(target, now + ms/1000);
  }
  function fadeOut(ms=500){
    if(!ctx || !gain) return;
    const now = ctx.currentTime;
    gain.gain.cancelScheduledValues(now);
    gain.gain.setValueAtTime(gain.gain.value, now);
    gain.gain.linearRampToValueAtTime(0.0, now + ms/1000);
  }
  async function ensureStarted(){
    if(!ctx){ buildGraph(); }
    else if (ctx.state === 'suspended'){ try{ await ctx.resume(); }catch{} }
  }
  function setUI(on){
    btn.setAttribute('aria-pressed', on?'true':'false');
    btn.querySelector('.label').textContent = on ? 'Звук: вкл' : 'Звук: выкл';
    btn.setAttribute('aria-label', on ? 'Выключить фоновый шум' : 'Включить фоновый шум');
  }
  async function turnOn(){ await ensureStarted(); setUI(true); localStorage.setItem(PREF_KEY, '1'); fade(0.08, 700); }
  function turnOff(){ setUI(false); localStorage.setItem(PREF_KEY, '0'); fadeOut(500); }
  btn.addEventListener('click', async ()=>{ const on = btn.getAttribute('aria-pressed')==='true'; if(on){ turnOff(); } else { await turnOn(); } });
  document.addEventListener('visibilitychange', ()=>{ if(!ctx) return; const wantOn = localStorage.getItem(PREF_KEY)==='1'; if(document.hidden){ fadeOut(300); } else if(wantOn){ fade(0.08, 500); } });
  function telegraphClick({vol=0.02, freq=1200, dur=0.09}={}){
    if(!ctx){ buildGraph(); }
    const o = ctx.createOscillator(); const g = ctx.createGain();
    o.type = 'square'; o.frequency.value = freq; o.connect(g).connect(ctx.destination);
    const t = ctx.currentTime; g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol, t+0.01); g.gain.exponentialRampToValueAtTime(0.0001, t+dur); o.start(t); o.stop(t+dur+0.01);
  }
  const hoverSel = '.nav a, .tl-btn, details.q summary, .down, .term, .permalink';
  document.addEventListener('mouseover', (e)=>{ if(e.target.closest(hoverSel)) telegraphClick(); }, {passive:true});
  document.addEventListener('focusin',   (e)=>{ if(e.target.closest(hoverSel)) telegraphClick(); });
}
