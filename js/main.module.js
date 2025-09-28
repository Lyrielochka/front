import { Toast } from './toast.js';
import { initAnchorScroll } from './scroll.js';
import { initReveal } from './reveal.js';
import { initCounters } from './counters.js';
import { initTimeline } from './timeline.js';
import { initSound } from './sound.js';
import { initTyping } from './typing.js';
import { initParallax } from './parallax.js';
import { initTicker } from './ticker.js';
import { initHeroes } from './heroes.js';
import { initGlossary } from './glossary.js';
import glossaryFallback from './fallback/glossary.js';
import heroesFallback from './fallback/heroes.js';
import { initParticles } from './particles.js';

async function run(){
  document.documentElement.classList.add('js');
  document.documentElement.classList.remove('no-js');
  try{
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
  }catch(err){
    console.error('[init error]', err);
    document.documentElement.classList.remove('js');
    document.documentElement.classList.add('no-js');
  }
}

if(document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', run, { once: true });
}else{
  run();
}
