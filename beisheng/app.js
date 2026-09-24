/* 背诵宝典 · 艾宾浩斯复习
   数据源: data_comm.js / data_gd.js / data_xd.js (window.BS_DECKS)
           ../data/sentences.json (英语作文15批, 与背作文模块同源)
   调度: localStorage bs_v1_<deckId>_<n> = {s:阶梯, t:到期ms, n:看过次数, k:认识次数}
   阶梯(天): 忘记→当天重现+1天(归0)  模糊→当天重现+2天(退1阶)  认识→升1阶 */
'use strict';

const LADDER = [0, 1, 2, 4, 7, 15, 30];          // 天; 0=当天收尾
const NEXTTXT = ['今天再来', '1天后', '2天后', '4天后', '7天后', '15天后', '30天后'];
const DAY = 86400000;
const LS = 'bs_v1_';

const $ = s => document.querySelector(s);
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

let DECKS = [];      // {id,name,em,subject,cards:[{f,b,batch?}]}
let state = null;    // {id, queue:[], idx, shown}
let tab = 'library';
let engLoading = false;

/* ---------- 英语作文: 从背作文数据动态生成卡 ---------- */
async function loadEnglish(){
  if (DECKS.some(d => d.id === 'eng')) return;
  if (engLoading) return; engLoading = true;
  try{
    const r = await fetch('../data/sentences.json?' + Date.now());
    const DATA = await r.json();
    const cards = [];
    (DATA.days || []).sort((a,b)=>a.day-b.day).forEach(d => {
      (d.sents || []).forEach(s => {
        cards.push({ f: s.zh.replace(/<[^>]+>/g,'').replace(/＿+/g,'____'),
                     b: '<div class="fl">'+s.en+'</div>' + (s.meta?'<div class="tip">'+esc(String(s.meta).replace(/<[^>]+>/g,''))+'</div>':''),
                     batch: d.day, tag: d.tag || '' });
      });
    });
    if (cards.length) DECKS.push({id:'eng', name:'英语作文背诵（15批）', em:'✍️', subject:'英语', cards});
    render();
  }catch(e){ /* 静默: 英语数据取不到时不阻塞其他牌库 */ }
}

/* ---------- 调度 ---------- */
const KEY = (d,i) => LS + d.id + '_' + i;
const getSt = (d,i) => { try{ return JSON.parse(localStorage.getItem(KEY(d,i))); }catch(e){ return null; } };
const setSt = (d,i,st) => st ? localStorage.setItem(KEY(d,i), JSON.stringify(st)) : localStorage.removeItem(KEY(d,i));
const due = (d,i) => { const s = getSt(d,i); return !s || s.t <= Date.now(); };
const deckDue = d => d.cards.reduce((n,_,i) => n + (due(d,i)?1:0), 0);
const deckNew = d => d.cards.reduce((n,_,i) => n + (getSt(d,i)?0:1), 0);
const deckDone = d => d.cards.reduce((n,_,i) => { const s=getSt(d,i); return n + (s && s.s >= LADDER.length-1 ? 1:0); }, 0);

function answer(d, i, kind){
  const st = getSt(d,i) || {s:0,t:0,n:0,k:0};
  st.n++;
  if (kind === 'no'){ st.s = 0; st.t = Date.now() + DAY; }
  else if (kind === 'mid'){ st.s = Math.max(0, st.s - 1); st.t = Date.now() + 2*DAY; st.k++; }
  else { st.s = Math.min(LADDER.length-1, st.s + 1); st.k++;
         st.t = Date.now() + (LADDER[st.s] || 0.007) * DAY; }
  setSt(d,i,st);
}

/* ---------- 视图 ---------- */
function render(){
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('on', b.dataset.tab === tab));
  $('#main').classList.toggle('cardmode', tab==='review' && !!state);
  $('#topsub').textContent = tab==='library' ? '艾宾浩斯复习' : tab==='review' ? (state ? deckName(state.d) : '今日到期') : '学习进度';
  if (tab === 'library') return renderLibrary();
  if (tab === 'review') return state ? renderCard() : renderPick();
  return renderStats();
}

function renderLibrary(){
  const groups = [['数学',['gd','xd']], ['专业课',['comm']], ['英语',['eng']]];
  let html = '';
  groups.forEach(([g, ids]) => {
    html += `<div class="group-h">${g}</div>`;
    ids.forEach(id => {
      const d = DECKS.find(x => x.id === id); if (!d) return;
      const dueN = deckDue(d), tot = d.cards.length, done = deckDone(d);
      html += `<div class="deck" data-deck="${id}">
        <div class="em">${d.em}</div>
        <div class="info"><div class="nm">${esc(d.name)}</div>
        <div class="meta">${tot} 卡 · 背熟 <b>${done}</b> · 新卡 ${deckNew(d)}</div></div>
        ${dueN?`<div class="due">${dueN>99?'99+':dueN}</div>`:''}
        <div class="go">›</div></div>`;
    });
  });
  if (!DECKS.some(d=>d.id==='eng'))
    html += `<div class="notice">英语作文牌库加载中…（若长时间为空，检查网络后刷新）</div>`;
  html += `<div class="notice">点击牌组开始复习；算法为艾宾浩斯曲线：<b style="color:var(--green)">认识</b>间隔 1→2→4→7→15→30 天递增，<b style="color:var(--orange)">模糊</b>退 1 阶+2 天，<b style="color:var(--red)">忘记</b>归零+1 天。进度保存在本设备浏览器。</div>`;
  $('#main').innerHTML = html;
  document.querySelectorAll('[data-deck]').forEach(el =>
    el.addEventListener('click', () => startDeck(el.dataset.deck)));
  updateBadge();
}

function startDeck(id){
  const d = DECKS.find(x => x.id === id); if (!d) return;
  const q = [];
  d.cards.forEach((_, i) => { if (due(d, i)) q.push(i); });
  // 新卡排前, 到期旧卡按到期时间排后
  q.sort((a,b) => (getSt(d,a)?getSt(d,a).t:0) - (getSt(d,b)?getSt(d,b).t:0));
  state = { d, queue: q, idx: 0, shown: 0 };
  tab = 'review'; render();
}

function renderPick(){
  const tot = DECKS.reduce((n,d)=>n+deckDue(d),0);
  $('#main').innerHTML = tot
    ? `<div class="empty"><div class="big">◔</div>今天还有 ${tot} 张到期<br>回牌库选一个牌组开始</div>`
    : `<div class="empty"><div class="big">🎉</div>全部背完，今天没有到期的了<br>明天再来</div>`;
}

function renderCard(){
  const {d, queue, idx} = state;
  $('#main').classList.add('cardmode');
  if (idx >= queue.length){
    $('#main').innerHTML = `<div class="empty"><div class="big">✅</div>本组完成！<br>${state.shown} 张已过
      <div style="margin-top:16px"><button class="flipbtn" style="width:auto;padding:10px 26px" id="goLib">回牌库</button></div></div>`;
    $('#goLib').addEventListener('click', ()=>{ tab='library'; state=null; render(); });
    updateBadge(); return;
  }
  const i = queue[idx], c = d.cards[i], st = getSt(d,i);
  const isNew = !st;
  const chip = (d.id==='eng' && c.batch) ? `<span class="chip">第 ${c.batch} 批</span>` : '';
  $('#main').innerHTML = `
    <div class="rvhead"><span class="cnt">${chip}${idx+1} / ${queue.length}${isNew?' · 新卡':''}</span>
      <button class="backbtn" id="quit">‹ 牌库</button></div>
    <div class="qcard" id="qcard">
      <div class="q">${c.f}</div>
      <div class="a" id="ans" style="display:none">${c.b}</div>
      <div class="hint" id="hint">点击卡片显示答案</div>
    </div>
    <div class="btns" id="btns" style="display:none">
      <button class="abtn no" data-k="no"><span class="lab">忘记</span><span class="next">今日/1天后</span></button>
      <button class="abtn mid" data-k="mid"><span class="lab">模糊</span><span class="next">今日/2天后</span></button>
      <button class="abtn ok" data-k="ok"><span class="lab">认识</span><span class="next">${NEXTTXT[Math.min(LADDER.length-1,(st?st.s:0)+1)]}</span></button>
    </div>
    <div id="flipwrap"><button class="flipbtn" id="flip">显示答案</button></div>`;
  $('#quit').addEventListener('click', ()=>{ tab='library'; state=null; render(); });
  const flip = () => {
    $('#ans').style.display='block'; $('#hint').style.display='none';
    $('#btns').style.display='flex'; $('#flipwrap').style.display='none';
    renderMath($('#ans'));
    if (window.renderMathInElement) renderMathInElement($('#qcard'), DELIMS);
  };
  $('#qcard').addEventListener('click', flip);
  $('#flip').addEventListener('click', flip);
  document.querySelectorAll('.abtn').forEach(b => b.addEventListener('click', e => {
    e.stopPropagation();
    answer(d, i, b.dataset.k); state.shown++;
    render(); window.scrollTo(0,0);
  }));
  renderMath($('#main'));
}

const DELIMS = {delimiters:[{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}], throwOnError:false};
function renderMath(el){ if (window.renderMathInElement) renderMathInElement(el, DELIMS); }

function renderStats(){
  let html = '';
  DECKS.forEach(d => {
    const tot = d.cards.length;
    let seen=0, ok=0, dueN=0;
    d.cards.forEach((_,i)=>{ const s=getSt(d,i); if(s){seen++; ok+=s.k;} if(due(d,i)) dueN++; });
    const pct = tot? Math.round(seen/tot*100) : 0;
    html += `<div class="stat"><div class="nm">${d.em} ${esc(d.name)}</div>
      <div class="bar"><i style="width:${pct}%"></i></div>
      <div class="row"><span>已学 ${seen} / ${tot}（${pct}%）</span><span>背熟 <b>${deckDone(d)}</b></span></div>
      <div class="row"><span>今日到期 <b>${dueN}</b></span><span>累计认识 <b>${ok}</b> 次</span></div></div>`;
  });
  html += `<div class="notice">「背熟」= 认识满 6 阶（30 天间隔）。更换手机/浏览器或清理浏览器数据会丢进度。</div>`;
  $('#main').innerHTML = html;
}

function deckName(d){ return d.name; }
function updateBadge(){
  const n = DECKS.reduce((s,d)=>s+deckDue(d),0);
  const b = $('#dueBadge');
  b.textContent = n>99?'99+':n; b.classList.toggle('show', n>0);
}

/* ---------- init ---------- */
document.querySelectorAll('.tab').forEach(b => b.addEventListener('click', () => {
  tab = b.dataset.tab; if (tab!=='review') state=null; render(); window.scrollTo(0,0);
}));
(function init(){
  if (window.BS_DECKS) DECKS.push(...BS_DECKS);
  loadEnglish().then(()=>updateBadge());
  render();
  // 调试/直达: ?d=牌组id 直接开始复习; ?flip=1 自动翻第一张
  const q = new URLSearchParams(location.search);
  if (q.get('debug')){
    setTimeout(()=>{
      let w = 0, who = '';
      document.querySelectorAll('#app *').forEach(el=>{
        if (el.scrollWidth > w){ w = el.scrollWidth; who = el.tagName + '.' + el.className; }
      });
      const dv = document.createElement('div'); dv.id = 'dbg';
      dv.textContent = 'DBG body=' + document.body.scrollWidth + ' doc=' + document.documentElement.clientWidth + ' max=' + w + ' @' + who;
      document.body.appendChild(dv);
    }, 800);
  }
  if (q.get('d') && DECKS.some(x=>x.id===q.get('d'))){
    setTimeout(()=>{ startDeck(q.get('d'));
      if (q.get('flip')) setTimeout(()=>{ const f=$('#flip'); if(f) f.click(); }, 300);
    }, 200);
  }
})();
