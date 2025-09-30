const DEFAULT_DATA_URL = "map-data.json";
const YEAR_COLORS = { 1914: "#b000c8", 1915: "#d80000", 1916: "#f08c00", 1917: "#a07800" };

export function initMap(options = {}){
  const root = options.section || document.querySelector('#map');
  if (!root) return;

  const container = root.querySelector('.interactive-map') || root.querySelector('[data-map-stage]')?.closest('.map');
  const stage = container?.querySelector('[data-map-stage]');
  const canvas = stage?.querySelector('[data-map-canvas]');
  const tooltip = stage?.querySelector('[data-map-infobox]');
  const toolbar = container?.querySelector('[data-map-toolbar]');
  const hint = container?.querySelector('[data-map-hint]');

  if (!container || !stage || !canvas || !tooltip){
    console.warn('[map] markup is incomplete');
    return;
  }

  const ctx = canvas.getContext('2d');
  const natWidth = canvas.width;
  const natHeight = canvas.height;

  const shapes = { points: [], lines: [], arrows: [], fills: [] };
  let filterYear = null;
  const activeClass = options.yearActiveClass || 'is-active';
  const yearButtons = toolbar ? Array.from(toolbar.querySelectorAll('[data-year]')) : [];
  const defaultHint = hint ? hint.textContent.trim() : '';

  function parseYear(value){
    if (value === null || value === undefined || value === '') return null;
    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric : null;
  }

  function yearVisible(sourceYear){
    if (filterYear === null) return true;
    const normalized = parseYear(sourceYear);
    return normalized === null ? true : normalized === filterYear;
  }

  function toInternalPoint(event){
    const rect = stage.getBoundingClientRect();
    const scaleX = natWidth / rect.width;
    const scaleY = natHeight / rect.height;
    return {
      x: (event.clientX - rect.left) * scaleX,
      y: (event.clientY - rect.top) * scaleY,
    };
  }

  function clearCanvas(){
    ctx.clearRect(0, 0, natWidth, natHeight);
  }

  function draw(){
    clearCanvas();
    shapes.fills.forEach(fill => { if (yearVisible(fill.year)) drawFill(fill); });
    shapes.lines.forEach(line => { if (yearVisible(line.year)) drawLine(line); });
    shapes.arrows.forEach(arrow => { if (yearVisible(arrow.year)) drawArrow(arrow); });
    shapes.points.forEach(point => { if (yearVisible(point.year)) drawPoint(point); });
  }

  function drawPoint(point){
    ctx.fillStyle = '#000';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = '20px system-ui, sans-serif';
    ctx.fillText(point.icon || '•', point.x, point.y);
    if (point.label){
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.font = '12px system-ui, sans-serif';
      const label = point.label + (point.year ? ` (${point.year})` : '');
      ctx.fillText(label, point.x + 12, point.y);
    }
  }

  function drawLine(line){
    const pts = line?.points;
    if (!Array.isArray(pts) || pts.length === 0) return;
    ctx.strokeStyle = pickYearColor(line.year);
    ctx.lineWidth = 3;
    ctx.beginPath();
    pts.forEach((pt, index) => index === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y));
    ctx.stroke();
    if (line.label){
      const mid = pts[Math.floor(pts.length / 2)];
      if (mid){
        ctx.fillStyle = '#000';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        ctx.font = '14px system-ui, sans-serif';
        const text = line.label + (line.year ? ` ${line.year}` : '');
        ctx.fillText(text, mid.x, mid.y - 6);
      }
    }
  }

  function drawArrow(arrow){
    const pts = arrow?.points;
    if (!Array.isArray(pts) || pts.length === 0) return;
    ctx.strokeStyle = pickYearColor(arrow.year);
    ctx.lineWidth = 3;
    ctx.beginPath();
    pts.forEach((pt, index) => index === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y));
    ctx.stroke();
    if (pts.length >= 2){
      const from = pts[pts.length - 2];
      const to = pts[pts.length - 1];
      const angle = Math.atan2(to.y - from.y, to.x - from.x);
      const len = 12;
      ctx.beginPath();
      ctx.moveTo(to.x, to.y);
      ctx.lineTo(to.x - len * Math.cos(angle - Math.PI / 6), to.y - len * Math.sin(angle - Math.PI / 6));
      ctx.moveTo(to.x, to.y);
      ctx.lineTo(to.x - len * Math.cos(angle + Math.PI / 6), to.y - len * Math.sin(angle + Math.PI / 6));
      ctx.stroke();
    }
    if (arrow.label){
      const mid = pts[Math.floor(pts.length / 2)];
      if (mid){
        ctx.fillStyle = '#000';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        ctx.font = '14px system-ui, sans-serif';
        const text = arrow.label + (arrow.year ? ` ${arrow.year}` : '');
        ctx.fillText(text, mid.x, mid.y - 6);
      }
    }
  }

  function drawFill(fill){
    const pts = fill?.points;
    if (!Array.isArray(pts) || pts.length === 0) return;
    const alpha = Number(fill.alpha ?? 0.35);
    ctx.fillStyle = hexToRgba(fill.color || '#60a5fa', alpha);
    ctx.strokeStyle = pickYearColor(fill.year);
    ctx.lineWidth = 2;
    ctx.beginPath();
    pts.forEach((pt, index) => index === 0 ? ctx.moveTo(pt.x, pt.y) : ctx.lineTo(pt.x, pt.y));
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    if (fill.label){
      const mid = pts[Math.floor(pts.length / 2)];
      if (mid){
        ctx.fillStyle = '#000';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        ctx.font = '14px system-ui, sans-serif';
        const text = fill.label + (fill.year ? ` ${fill.year}` : '');
        ctx.fillText(text, mid.x, mid.y - 6);
      }
    }
  }

  function pickYearColor(year){
    const key = parseYear(year);
    return YEAR_COLORS[key] || '#000';
  }

  function hexToRgba(hex, alpha){
    const clean = String(hex || '').replace('#', '');
    const r = parseInt(clean.slice(0, 2) || '00', 16);
    const g = parseInt(clean.slice(2, 4) || '00', 16);
    const b = parseInt(clean.slice(4, 6) || '00', 16);
    const a = Number.isFinite(alpha) ? Math.max(0, Math.min(1, alpha)) : 0.35;
    return `rgba(${r},${g},${b},${a})`;
  }

  function nearPoint(point, radius = 12){
    for (let i = 0; i < shapes.points.length; i += 1){
      const candidate = shapes.points[i];
      if (Math.hypot(candidate.x - point.x, candidate.y - point.y) <= radius) return i;
    }
    return -1;
  }

  function segmentDistance(a, b, p){
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const length = dx * dx + dy * dy;
    if (length === 0) return Math.hypot(p.x - a.x, p.y - a.y);
    const ratio = Math.max(0, Math.min(1, ((p.x - a.x) * dx + (p.y - a.y) * dy) / length));
    const projX = a.x + ratio * dx;
    const projY = a.y + ratio * dy;
    return Math.hypot(p.x - projX, p.y - projY);
  }

  function findShape(point, tolerance = 6){
    const pool = [
      ...shapes.lines.map(obj => ({ obj, type: 'Линия' })),
      ...shapes.arrows.map(obj => ({ obj, type: 'Стрелка' })),
      ...shapes.fills.map(obj => ({ obj, type: 'Контур' })),
    ];
    for (const item of pool){
      if (!yearVisible(item.obj.year)) continue;
      const pts = item.obj.points || [];
      for (let i = 1; i < pts.length; i += 1){
        if (segmentDistance(pts[i - 1], pts[i], point) <= tolerance) return item;
      }
    }
    return null;
  }

  function clampTooltip(left, top){
    const rect = stage.getBoundingClientRect();
    const width = tooltip.offsetWidth;
    const height = tooltip.offsetHeight;
    const clampedLeft = Math.min(Math.max(8, left), Math.max(8, rect.width - width - 8));
    const clampedTop = Math.min(Math.max(8, top), Math.max(8, rect.height - height - 8));
    tooltip.style.left = `${clampedLeft}px`;
    tooltip.style.top = `${clampedTop}px`;
  }

  function showInfo(payload, internalPoint){
    const rect = stage.getBoundingClientRect();
    const scaleX = rect.width / natWidth;
    const scaleY = rect.height / natHeight;
    const left = internalPoint.x * scaleX + 16;
    const top = internalPoint.y * scaleY + 16;

    tooltip.innerHTML = '';
    let hasContent = false;

    if (payload && typeof payload === 'object' && !Array.isArray(payload)){
      const title = payload.title ?? payload.label ?? '';
      const body = payload.body ?? payload.description ?? payload.desc ?? payload.text ?? '';
      if (title){
        const titleEl = document.createElement('div');
        titleEl.className = 'map__tooltip-title';
        titleEl.textContent = title;
        tooltip.appendChild(titleEl);
        hasContent = true;
      }
      const segments = Array.isArray(body) ? body : String(body || '').split(/\r?\n\s*\r?\n/);
      segments.forEach(segment => {
        const trimmed = String(segment || '').trim();
        if (!trimmed) return;
        const bodyEl = document.createElement('div');
        bodyEl.className = 'map__tooltip-body';
        bodyEl.textContent = trimmed;
        tooltip.appendChild(bodyEl);
        hasContent = true;
      });
    } else if (typeof payload === 'string'){
      tooltip.textContent = payload;
      hasContent = Boolean(payload);
    }

    if (!hasContent){
      tooltip.textContent = 'Нет данных';
    }

    tooltip.style.display = 'block';
    tooltip.style.left = '0px';
    tooltip.style.top = '0px';
    clampTooltip(left, top);
  }

  function hideInfo(){
    tooltip.style.display = 'none';
  }

  function applyData(data){
    if (!data || typeof data !== 'object') return;
    shapes.points = Array.isArray(data.points) ? data.points : (Array.isArray(data.markers) ? data.markers : []);
    shapes.lines = Array.isArray(data.lines) ? data.lines : [];
    shapes.arrows = Array.isArray(data.arrows) ? data.arrows : [];
    shapes.fills = Array.isArray(data.fills) ? data.fills : [];
    hideInfo();
    draw();
  }

  function updateHint(message, status){
    if (!hint) return;
    if (message){
      hint.textContent = message;
    } else if (defaultHint){
      hint.textContent = defaultHint;
    }
    if (status){
      hint.dataset.status = status;
    } else {
      delete hint.dataset.status;
    }
  }

  function onCanvasClick(event){
    const internal = toInternalPoint(event);
    const pointIndex = nearPoint(internal);
    if (pointIndex >= 0){
      const marker = shapes.points[pointIndex];
      const icon = marker.icon || '\u0007';
      const titleParts = [icon];
      if (marker.label) titleParts.push(String(marker.label));
      if (marker.year) titleParts.push(String(marker.year));
      const heading = titleParts.join(' ').replace(/\s+/g, ' ').trim();
      const rawDescription = marker.desc ?? marker.description ?? marker.text ?? '';
      const description = typeof rawDescription === 'string' ? rawDescription.trim() : String(rawDescription || '').trim();
      const payload = description ? { title: heading || 'Точка', body: description } : (heading || 'Точка');
      showInfo(payload, marker);
      return;
    }
    const shape = findShape(internal);
    if (shape){
      const obj = shape.obj;
      const base = obj.label || shape.type || '';
      const textLabel = `${base}${obj.year ? ` ${obj.year}` : ''}`.trim();
      const rawDescription = obj.desc ?? obj.description ?? obj.text ?? '';
      const description = typeof rawDescription === 'string' ? rawDescription.trim() : String(rawDescription || '').trim();
      const payload = description ? { title: heading || 'Точка', body: description } : (heading || 'Точка');
      showInfo(payload, internal);
    } else {
      hideInfo();
    }
  }

  function bindFilters(){
    yearButtons.forEach(button => {
      button.addEventListener('click', () => {
        yearButtons.forEach(item => item.classList.remove(activeClass));
        button.classList.add(activeClass);
        filterYear = parseYear(button.dataset.year);
        hideInfo();
        draw();
      });
    });
  }

  function resolveDataUrl(){
    if (typeof options.url === 'string') return options.url;
    if (container?.dataset.mapUrl) return container.dataset.mapUrl;
    return DEFAULT_DATA_URL;
  }

  async function loadData(){
    const inline = options.data || globalThis.APP_MAP_DATA;
    if (inline){
      applyData(inline);
      updateHint(defaultHint, null);
      return;
    }
    const url = resolveDataUrl();
    if (!url) return;
    updateHint(defaultHint || 'Загружаем карту…', null);
    try{
      const response = await fetch(url, { cache: 'no-store' });
      if (!response.ok) throw new Error(`${response.status} ${response.statusText}`.trim());
      const payload = await response.json();
      applyData(payload);
      updateHint(defaultHint, null);
    }catch(error){
      console.warn('[map] data request failed', error);
      updateHint(`Не удалось загрузить ${url}: ${error.message}`, 'error');
    }
  }

  canvas.addEventListener('click', onCanvasClick);
  stage.addEventListener('pointerleave', hideInfo);
  stage.addEventListener('pointerdown', hideInfo);

  bindFilters();
  draw();
  loadData();

  return {
    redraw: draw,
    setYear(value){
      filterYear = parseYear(value);
      draw();
    },
    setData(data){
      applyData(data);
      updateHint(defaultHint, null);
    },
  };
}







