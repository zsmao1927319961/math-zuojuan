/* 知识图库 · 通信原理必背公式（大观园式知识树, 纯浏览速查）
   数据源: data_comm.js (32卡, 按正面 chip 专题组分 7 组)
   交互: 组展开收起 / 卡片点击展开公式内容 / 搜索过滤 / 手动掌握标记 (localStorage kg_v1) */
'use strict';

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const strip = s => String(s).replace(/<span class='chip'>[^<]*<\/span>/,'').replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim();
const LSK = 'kg_v1';

let D = null, GROUPS = [], openG = {}, openC = {}, KW = '';
let MAST = null;
try { MAST = JSON.parse(localStorage.getItem(LSK)) || {}; } catch(e){ MAST = {}; }
function saveM(){ try{ localStorage.setItem(LSK, JSON.stringify(MAST)); }catch(e){} }

/* 分组: 按卡正面 chip 专题 */
function buildGroups(){
  const map = new Map();
  D.cards.forEach((c, i) => {
    const m = String(c.f).match(/<span class='chip'>([^<]+)<\/span>/);
    const g = m ? m[1].trim() : '其他';
    if (!map.has(g)) map.set(g, []);
    map.get(g).push(i);
  });
  GROUPS = [...map.entries()].map(([name, idxs]) => ({name, idxs}));
}
const gMastered = g => g.idxs.filter(i => MAST[i]).length;

/* 渲染 */
function render(){
  let mastered = 0;
  D.cards.forEach((_, i) => { if (MAST[i]) mastered++; });
  let h = `<div class="card root">
    <div class="root-h"><span class="root-em">📡</span>
      <div class="root-nm"><b>${esc(D.name)}</b><div class="root-meta">${D.cards.length} 张公式卡 · 已掌握 ${mastered}</div></div>
    </div>
    <input id="kw" placeholder="🔍 搜索公式关键词…" value="${esc(KW)}">
  </div>`;
  const kw = KW.trim().toLowerCase();
  let shown = 0;
  GROUPS.forEach((g, gi) => {
    const idxs = g.idxs.filter(i => {
      if (!kw) return true;
      return (strip(c(i).f) + ' ' + strip(c(i).b)).toLowerCase().indexOf(kw) >= 0;
    });
    if (kw && !idxs.length) return;
    shown += idxs.length;
    const open = kw ? true : !!openG[gi];
    const mas = gMastered(g);
    h += `<div class="card gcard">
      <div class="g-h" onclick="toggleG(${gi})">
        <span class="tw">${open?'▾':'▸'}</span>
        <span class="g-nm">${esc(g.name)}</span>
        <span class="g-meta">${idxs.length}卡 · 掌握 ${mas}</span>
      </div>`;
    if (open){
      g.idxs.forEach(i => {
        const cdi = c(i);
        const front = strip(cdi.f);
        const open2 = kw ? true : !!openC[i];
        h += `<div class="leaf ${open2?'open':''}">
          <div class="leaf-h" onclick="toggleC(${i})">
            <span class="tw">${open2?'▾':'▸'}</span>
            <span class="leaf-nm">${esc(front.slice(0, 46))}${front.length>46?'…':''}</span>
            <span class="mast ${MAST[i]?'on':''}" onclick="event.stopPropagation();toggleM(${i})">${MAST[i]?'✓ 掌握':'标记掌握'}</span>
          </div>
          <div class="leaf-b" style="display:${open2?'block':'none'}">
            <div class="q">${cdi.f.replace(/<span class='chip'>[^<]*<\/span>/,'')}</div>
            <div class="a">${cdi.b}</div>
          </div>
        </div>`;
      });
    }
    h += `</div>`;
  });
  if (kw) h += `<div class="notice">搜索“${esc(KW)}”：命中 ${shown} 张卡</div>`;
  $('#main').innerHTML = h;
  const kwEl = $('#kw');
  kwEl.addEventListener('input', () => {
    KW = kwEl.value; render();
    const el = $('#kw'); el.focus(); el.setSelectionRange(el.value.length, el.value.length);
  });
  renderMath($('#main'));
}
function c(i){ return D.cards[i]; }
function toggleG(gi){ openG[gi] = !openG[gi]; render(); }
function toggleC(i){ openC[i] = !openC[i]; render(); }
function toggleM(i){ MAST[i] = !MAST[i]; if (!MAST[i]) delete MAST[i]; saveM(); render(); }
function renderMath(el){ if (window.renderMathInElement) renderMathInElement(el, {delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}], throwOnError:false}); }

/* init */
(function(){
  if (window.BS_DECKS) D = window.BS_DECKS.find(x => x.id === 'comm') || window.BS_DECKS[0];
  buildGroups();
  render();
})();
