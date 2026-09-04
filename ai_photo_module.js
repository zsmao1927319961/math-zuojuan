/* ===== 问AI + 解答照片（独立模块，两版通用）===== */
(function () {
  const AI_URL = 'https://open.bigmodel.cn/api/paas/v4/chat/completions';
  const css = document.createElement('style');
  css.textContent = [
    '#btn-ai,#btn-photo{flex:1}',
    '#media-box{margin:10px 0 2px}',
    '#media-box .today-reason-title{display:flex;align-items:center;justify-content:space-between}',
    '#ph-add,#btn-ai-set{border:none;background:#eef1f6;border-radius:8px;padding:4px 10px;font-size:12px;cursor:pointer}',
    '#ph-grid{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}',
    '.ph-thumb{position:relative;width:86px;height:86px;border-radius:8px;overflow:hidden;cursor:zoom-in;border:1px solid #e3e6ec}',
    '.ph-thumb img{width:100%;height:100%;object-fit:cover}',
    '.ph-del{position:absolute;top:2px;right:2px;width:18px;height:18px;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;font-size:11px;line-height:18px;text-align:center;cursor:pointer}',
    '#aipanel{position:fixed;inset:0;z-index:10000;background:#f6f7fa;display:none;flex-direction:column}',
    '#ai-head{display:flex;align-items:center;gap:8px;padding:10px 14px;background:#1f2430;color:#fff;font-size:15px;font-weight:600}',
    '#ai-head .sp{flex:1}',
    '#ai-set-btn{background:rgba(255,255,255,.14);border:none;color:#fff;border-radius:8px;padding:4px 10px;font-size:12px;cursor:pointer}',
    '#ai-close{background:none;border:none;color:#fff;font-size:22px;cursor:pointer;line-height:1}',
    '#ai-settings{display:none;background:#fff;border-bottom:1px solid #e5e8ee;padding:10px 14px;font-size:13px}',
    '#ai-settings input{width:100%;box-sizing:border-box;border:1px solid #d8dce4;border-radius:8px;padding:7px 9px;margin:4px 0 8px;font-size:13px}',
    '#ai-settings .row{display:flex;gap:8px}',
    '#ai-settings .row>*{flex:1}',
    '#ai-save{background:#2f6bff;color:#fff;border:none;border-radius:8px;padding:7px 0;cursor:pointer}',
    '#ai-test{background:#eef1f6;border:1px solid #d8dce4;border-radius:8px;padding:7px 0;cursor:pointer}',
    '#ai-msgs{flex:1;overflow-y:auto;padding:12px 14px;-webkit-overflow-scrolling:touch}',
    '.ai-msg{max-width:88%;margin-bottom:10px;padding:9px 12px;border-radius:12px;font-size:14px;line-height:1.65;white-space:pre-wrap;word-break:break-word}',
    '.ai-msg.u{background:#2f6bff;color:#fff;margin-left:auto}',
    '.ai-msg.a{background:#fff;border:1px solid #e5e8ee}',
    '.ai-msg.err{background:#fdecec;color:#b42318;border:1px solid #f5c2c0}',
    '#ai-chips{display:flex;gap:8px;padding:8px 14px 0}',
    '.ai-chip{flex:1;border:1px solid #2f6bff;color:#2f6bff;background:#fff;border-radius:10px;padding:8px 0;font-size:14px;cursor:pointer}',
    '.ai-chip.on{background:#2f6bff;color:#fff}',
    '#ai-inputrow{display:flex;gap:8px;padding:10px 14px calc(12px + env(safe-area-inset-bottom))}',
    '#ai-input{flex:1;border:1px solid #d8dce4;border-radius:10px;padding:10px 12px;font-size:14px}',
    '#ai-send{background:#2f6bff;color:#fff;border:none;border-radius:10px;padding:10px 18px;font-size:14px;cursor:pointer}',
    '#ai-send:disabled{opacity:.5}'
  ].join('');
  document.head.appendChild(css);

  /* ---------- IndexedDB：解答照片 ---------- */
  function idb() {
    return new Promise((res, rej) => {
      const r = indexedDB.open('zuoti_media', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('photos', { keyPath: 'id' });
      r.onsuccess = () => res(r.result);
      r.onerror = () => rej(r.error);
    });
  }
  function photosFor(qid) {
    return idb().then(db => new Promise((res, rej) => {
      const rq = db.transaction('photos').objectStore('photos').getAll();
      rq.onsuccess = () => res((rq.result || []).filter(p => p.qid === qid).sort((a, b) => a.ts - b.ts));
      rq.onerror = () => rej(rq.error);
    }));
  }
  function photoAdd(qid, dataURL) {
    return idb().then(db => new Promise((res, rej) => {
      const t = db.transaction('photos', 'readwrite');
      t.objectStore('photos').add({ id: qid + '#' + Date.now(), qid, ts: Date.now(), data: dataURL });
      t.oncomplete = res; t.onerror = () => rej(t.error);
    }));
  }
  function photoDel(id) {
    return idb().then(db => new Promise((res, rej) => {
      const t = db.transaction('photos', 'readwrite');
      t.objectStore('photos').delete(id);
      t.oncomplete = res; t.onerror = () => rej(t.error);
    }));
  }
  function fileToDataURL(file) {
    return new Promise((res, rej) => {
      const img = new Image();
      img.onload = () => {
        const sc = Math.min(1, 1400 / Math.max(img.width, img.height));
        const cv = document.createElement('canvas');
        cv.width = Math.round(img.width * sc); cv.height = Math.round(img.height * sc);
        cv.getContext('2d').drawImage(img, 0, 0, cv.width, cv.height);
        res(cv.toDataURL('image/jpeg', 0.72));
      };
      img.onerror = () => rej(new Error('图片读取失败'));
      img.src = URL.createObjectURL(file);
    });
  }

  /* ---------- AI 调用 ---------- */
  function aiKey() { return localStorage.getItem('glm_key') || ''; }
  function aiModel() { return localStorage.getItem('glm_model') || 'glm-5.3-flash'; }
  function histKey(qid) { return 'ai_chat_' + qid; }
  function histLoad(qid) { try { return JSON.parse(localStorage.getItem(histKey(qid)) || '[]'); } catch (e) { return []; } }
  function histSave(qid, h) { try { localStorage.setItem(histKey(qid), JSON.stringify(h.slice(-30))); } catch (e) {} }

  async function imagePart(q) {
    const src = q.question_img || (q.answer_img || '');
    if (!src) return null;
    const r = await fetch(src.startsWith('data/') ? src : 'data/' + src);
    const blob = await r.blob();
    const dataURL = await new Promise((res, rej) => {
      const fr = new FileReader();
      fr.onload = () => res(fr.result); fr.onerror = () => rej(fr.error);
      fr.readAsDataURL(blob);
    });
    return { type: 'image_url', image_url: { url: dataURL } };
  }

  async function aiStream(msgs, onDelta) {
    const res = await fetch(AI_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + aiKey() },
      body: JSON.stringify({ model: aiModel(), messages: msgs, stream: true, max_tokens: 2048, temperature: 0.4 })
    });
    if (!res.ok) {
      const t = await res.text().catch(() => '');
      throw new Error('API ' + res.status + (t ? '：' + t.slice(0, 160) : ''));
    }
    const reader = res.body.getReader(); const dec = new TextDecoder(); let buf = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let i;
      while ((i = buf.indexOf('\n')) >= 0) {
        const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
        if (!line.startsWith('data:')) continue;
        const d = line.slice(5).trim();
        if (d === '[DONE]') return;
        try {
          const j = JSON.parse(d);
          const c = j.choices && j.choices[0] && j.choices[0].delta && j.choices[0].delta.content;
          if (c) onDelta(c);
        } catch (e) {}
      }
    }
  }

  /* ---------- 弹窗注入（照片区 + 问AI按钮）---------- */
  window.__curQ = null;
  const _showModal = window.showModal;
  if (typeof _showModal === 'function') {
    window.showModal = function (q) {
      window.__curQ = q;
      const r = _showModal.apply(this, arguments);
      setTimeout(() => {
        const m = document.querySelector('#modal');
        if (m && !m.hidden) injectMedia(m, q);
      }, 0);
      return r;
    };
  }

  function injectMedia(m, q) {
    if (m.querySelector('#media-box')) { refreshThumbs(m, q); return; }
    const box = document.createElement('div');
    box.id = 'media-box';
    box.innerHTML =
      '<div class="today-reason-title"><span>我的解答照片（仅存本机）</span><span>' +
      '<button id="btn-ai" type="button">🤖 问AI</button> ' +
      '<button id="btn-photo" type="button">📷 ＋拍照/相册</button></span></div>' +
      '<div id="ph-grid"><span style="font-size:12px;color:#98a0ad">做错的题可拍下纸上过程，复习时对照</span></div>' +
      '<input type="file" id="ph-file" accept="image/*" capture="environment" multiple hidden>';
    const anchor = m.querySelector('#modal-actions');
    if (anchor) anchor.parentNode.insertBefore(box, anchor);
    else m.querySelector('#modal-box').appendChild(box);
    box.querySelector('#btn-photo').onclick = () => box.querySelector('#ph-file').click();
    box.querySelector('#btn-ai').onclick = () => openAI(q);
    box.querySelector('#ph-file').onchange = async (e) => {
      const files = Array.from(e.target.files || []);
      for (const f of files) {
        try { await photoAdd(q.id, await fileToDataURL(f)); } catch (err) { alert('照片保存失败：' + err.message); }
      }
      e.target.value = '';
      refreshThumbs(m, q);
    };
    refreshThumbs(m, q);
  }

  function refreshThumbs(m, q) {
    const grid = m.querySelector('#ph-grid');
    if (!grid) return;
    photosFor(q.id).then(list => {
      grid.innerHTML = '';
      list.forEach(p => {
        const d = document.createElement('div');
        d.className = 'ph-thumb';
        const img = document.createElement('img');
        img.src = p.data; img.alt = '解答照片';
        img.onclick = () => { if (window.zoomImg) window.zoomImg(p.data); };
        const x = document.createElement('span');
        x.className = 'ph-del'; x.textContent = '×';
        x.onclick = (e) => { e.stopPropagation(); if (confirm('删除这张解答照片？')) photoDel(p.id).then(() => refreshThumbs(m, q)); };
        d.appendChild(img); d.appendChild(x);
        grid.appendChild(d);
      });
    });
  }

  /* ---------- AI 面板 ---------- */
  const panel = document.createElement('div');
  panel.id = 'aipanel';
  panel.innerHTML =
    '<div id="ai-head"><span id="ai-title">问AI</span><span class="sp"></span>' +
    '<button id="ai-set-btn">设置</button><button id="ai-close">×</button></div>' +
    '<div id="ai-settings">' +
    '<label>智谱 API Key（仅存本机 localStorage）</label><input id="ai-key-in" type="password" placeholder="粘贴你的 API Key">' +
    '<div class="row"><input id="ai-model-in" placeholder="模型，默认 glm-5.3-flash">' +
    '<button id="ai-save">保存</button><button id="ai-test">测连通</button></div>' +
    '<div id="ai-test-out" style="margin-top:6px;color:#666"></div></div>' +
    '<div id="ai-chips">' +
    '<button class="ai-chip" data-mode="hint">💡 给我提示（不给答案）</button>' +
    '<button class="ai-chip" data-mode="full">📖 完整讲解</button></div>' +
    '<div id="ai-msgs"></div>' +
    '<div id="ai-inputrow"><input id="ai-input" placeholder="追问…（回车发送）"><button id="ai-send">发送</button></div>';
  document.body.appendChild(panel);

  let curQ = null, busy = false;
  function openAI(q) {
    curQ = q;
    document.getElementById('ai-title').textContent = '问AI · ' + (q.label || q.id);
    document.getElementById('ai-key-in').value = aiKey();
    document.getElementById('ai-model-in').value = aiModel();
    document.getElementById('ai-settings').style.display = aiKey() ? 'none' : 'block';
    renderHist();
    panel.style.display = 'flex';
  }
  function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function addMsg(role, text) {
    const d = document.createElement('div');
    d.className = 'ai-msg ' + (role === 'user' ? 'u' : role === 'err' ? 'err' : 'a');
    d.innerHTML = esc(text);
    const box = document.getElementById('ai-msgs');
    box.appendChild(d); box.scrollTop = box.scrollHeight;
    return d;
  }
  function renderHist() {
    const box = document.getElementById('ai-msgs');
    box.innerHTML = '';
    histLoad(curQ.id).forEach(m => addMsg(m.role, m.text));
    if (!histLoad(curQ.id).length) addMsg('assistant', '我是你的考研数学老师。选「给我提示」引导你自己想，或「完整讲解」看全过程；也可以直接输入问题追问。');
  }
  function setBusy(b) {
    busy = b;
    document.getElementById('ai-send').disabled = b;
    document.querySelectorAll('.ai-chip').forEach(c => c.disabled = b);
  }
  async function send(userText, mode) {
    if (busy || !curQ) return;
    if (!aiKey()) { document.getElementById('ai-settings').style.display = 'block'; return; }
    const h = histLoad(curQ.id);
    const sys = mode === 'hint'
      ? '你是考研数学老师。图中是一道考研数学题。不要给出完整解答！只给2-3步递进式提示（先方向、再关键步骤、最后易错点），引导学生自己想出来。中文，简洁。'
      : mode === 'full'
        ? '你是考研数学老师。图中是一道考研数学题。请给出完整严谨的解答，分步骤书写，末尾用一两句点出易错点。中文。'
        : '你是考研数学老师，正在就图中这道题继续为学生答疑。中文回答。';
    let userContent;
    if (h.length === 0) {
      const img = await imagePart(curQ).catch(() => null);
      userContent = img ? [img, { type: 'text', text: userText }] : userText;
    } else {
      userContent = userText;
    }
    const msgs = [{ role: 'system', content: sys }];
    h.forEach(m => msgs.push({ role: m.role, content: m.text }));
    msgs.push({ role: 'user', content: userContent });
    h.push({ role: 'user', text: userText });
    addMsg('user', userText);
    const bubble = addMsg('assistant', '…');
    setBusy(true);
    let acc = '';
    try {
      await aiStream(msgs, (delta) => {
        acc += delta;
        bubble.innerHTML = esc(acc);
        const box = document.getElementById('ai-msgs');
        box.scrollTop = box.scrollHeight;
      });
      if (!acc) acc = '（无返回内容）';
      bubble.innerHTML = esc(acc);
      h.push({ role: 'assistant', text: acc });
      histSave(curQ.id, h);
    } catch (e) {
      bubble.remove();
      addMsg('err', '出错：' + e.message + (e.message.indexOf('401') >= 0 ? '（Key 无效或过期）' : e.message.indexOf('Failed to fetch') >= 0 ? '（网络不通）' : ''));
    }
    setBusy(false);
  }

  document.getElementById('ai-close').onclick = () => panel.style.display = 'none';
  document.getElementById('ai-set-btn').onclick = () => {
    const s = document.getElementById('ai-settings');
    s.style.display = s.style.display === 'block' ? 'none' : 'block';
    document.getElementById('ai-key-in').value = aiKey();
    document.getElementById('ai-model-in').value = aiModel();
  };
  document.getElementById('ai-save').onclick = () => {
    localStorage.setItem('glm_key', document.getElementById('ai-key-in').value.trim());
    localStorage.setItem('glm_model', document.getElementById('ai-model-in').value.trim() || 'glm-5.3-flash');
    document.getElementById('ai-test-out').textContent = '已保存 ✓';
    setTimeout(() => { document.getElementById('ai-settings').style.display = 'none'; }, 600);
  };
  document.getElementById('ai-test').onclick = async () => {
    localStorage.setItem('glm_key', document.getElementById('ai-key-in').value.trim());
    localStorage.setItem('glm_model', document.getElementById('ai-model-in').value.trim() || 'glm-5.3-flash');
    const out = document.getElementById('ai-test-out');
    out.textContent = '测试中…';
    try {
      const res = await fetch(AI_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + aiKey() },
        body: JSON.stringify({ model: aiModel(), messages: [{ role: 'user', content: '回复：OK' }], max_tokens: 8, stream: false })
      });
      const j = await res.json().catch(() => ({}));
      out.textContent = res.ok ? '✓ 连通正常，模型已响应' : '✗ ' + res.status + ' ' + ((j.error && j.error.message) || '').slice(0, 120);
    } catch (e) { out.textContent = '✗ ' + e.message; }
  };
  document.querySelectorAll('.ai-chip').forEach(c => {
    c.onclick = () => {
      document.querySelectorAll('.ai-chip').forEach(x => x.classList.remove('on'));
      c.classList.add('on');
      send(c.dataset.mode === 'hint' ? '请给我提示，不要直接给答案。' : '请给出完整讲解。', c.dataset.mode);
    };
  });
  document.getElementById('ai-send').onclick = () => {
    const inp = document.getElementById('ai-input');
    const t = inp.value.trim();
    if (!t) return;
    inp.value = '';
    send(t, 'chat');
  };
  document.getElementById('ai-input').onkeydown = (e) => { if (e.key === 'Enter') document.getElementById('ai-send').click(); };
})();
