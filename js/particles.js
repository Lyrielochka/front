export function initParticles(){
  const wrap = document.getElementById('particles');
  if(!wrap) return;
  wrap.innerHTML = '';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce) return;
  const count = Math.max(48, Math.min(110, Math.floor(window.innerWidth / 14)));
  for(let i=0;i<count;i++){
    const el = document.createElement('span');
    el.className = 'particle' + (Math.random() < 0.3 ? ' spark' : '');
    const left = Math.random() * 100;
    const delay = (Math.random() * -18).toFixed(2) + 's';
    const dur = (12 + Math.random() * 12).toFixed(2) + 's';
    const size = (0.26 + Math.random() * 0.32).toFixed(2) + 'rem';
    const alpha = (0.55 + Math.random() * 0.25).toFixed(2);
    const drift = (Math.random() * 12 - 6).toFixed(2) + 'vw';
    el.style.left = `${left}vw`;
    el.style.setProperty('--dur', dur);
    el.style.setProperty('--size', size);
    el.style.setProperty('--alpha', alpha);
    el.style.setProperty('--drift', drift);
    el.style.animationDelay = delay;
    wrap.appendChild(el);
  }
}
