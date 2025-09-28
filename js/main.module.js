import { Toast } from './toast.js';
import { initAnchorScroll } from './scroll.js';
import { initReveal } from './reveal.js';
import { initCounters } from './counters.js';
import { initTimeline } from './timeline.js';
import { initSound } from './sound.js';
import { initTyping } from './typing.js';
import { initParallax } from './parallax.js';
import { initTicker } from './ticker.js';
import { initGlossary } from './glossary.js';
import glossaryFallback from './fallback/glossary.js';
import heroesFallback from './fallback/heroes.js';

import { initParticles } from './particles.js';

function run(){
  document.documentElement.classList.remove('no-js');
  initAnchorScroll();
  initReveal();
  initCounters();
  initTimeline();
  initSound();
  initTyping();
  initTicker();
  initParticles();
  initGlossary({ url: 'data/glossary.json', fallbackData: glossaryFallback });
  initHeroes({ url: 'data/heroes.json', fallbackData: heroesFallback });
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', run, { once: true });
}else{
  run();
}
