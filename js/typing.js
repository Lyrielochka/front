export function initTyping(){
  const el = document.getElementById('typeTarget');
  if(!el) return;
  const text = 'Первая мировая\nна землях Беларуси';
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce){ el.textContent = text; el.classList.add('done'); return; }
  let i = 0; const total = text.length; const duration = 2800; const start = performance.now();
  function step(t){ const p = Math.min(1, (t - start)/duration); i = Math.max(i, Math.floor(total * p)); el.textContent = text.slice(0, i); if(i < total){ requestAnimationFrame(step); } else { el.classList.add('done'); } }
  requestAnimationFrame(step);
}
