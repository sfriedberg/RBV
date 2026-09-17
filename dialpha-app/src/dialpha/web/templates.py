"""HTML template for the dialpha local dashboard."""

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deal Alpha — Local Dashboard</title>
<style>
  :root { --bg:#0f1117; --panel:#171a23; --accent:#4f8cff; --ok:#3fbf7f; --warn:#e0a430; --bad:#e05b5b; --text:#e8eaf0; --muted:#9aa1b2; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:var(--bg); color:var(--text); padding:24px; max-width:1100px; margin:0 auto; }
  h1 { font-size:1.5rem; margin-bottom:4px; }
  .sub { color:var(--muted); font-size:0.9rem; margin-bottom:20px; }
  .panel { background:var(--panel); border-radius:10px; padding:20px; margin-bottom:20px; }
  .panel h2 { font-size:1.05rem; margin-bottom:12px; }
  textarea, input[type=text] { width:100%; background:#0c0e14; color:var(--text); border:1px solid #2a2f3d; border-radius:6px; padding:10px; font-size:0.9rem; font-family:ui-monospace,monospace; }
  textarea { min-height:120px; resize:vertical; }
  label { display:block; font-size:0.85rem; color:var(--muted); margin:10px 0 4px; }
  button { background:var(--accent); color:#fff; border:none; border-radius:6px; padding:9px 18px; font-size:0.9rem; cursor:pointer; margin-top:12px; }
  button:hover { opacity:0.9; }
  button.secondary { background:#2a2f3d; }
  .score-row { display:flex; align-items:center; gap:10px; margin-bottom:6px; font-size:0.88rem; }
  .badge { padding:2px 8px; border-radius:4px; font-weight:600; font-size:0.78rem; min-width:46px; text-align:center; }
  .PASS { background:rgba(63,191,127,0.18); color:var(--ok); }
  .FAIL { background:rgba(224,91,91,0.18); color:var(--bad); }
  .composite { font-size:2.4rem; font-weight:700; }
  .recommendation { font-size:1.1rem; font-weight:600; }
  .AVOID { color:var(--bad); } .WATCH { color:var(--warn); } .STRONG { color:var(--ok); }
  .evidence { color:var(--muted); font-size:0.82rem; margin-top:10px; line-height:1.7; font-family:ui-monospace,monospace; }
  #loading { color:var(--muted); font-style:italic; margin-top:10px; }
  .hidden { display:none; }
  .error { color:var(--bad); margin-top:10px; font-size:0.9rem; }
</style>
</head>
<body>
<h1>Deal Alpha</h1>
<div class="sub">Local dashboard — score deal documents against alpha-generating patterns. Nothing leaves this machine.</div>

<div class="panel">
  <h2>Score a Deal</h2>
  <label for="deal-text">Paste deal text (CIM excerpt, 10-K snippet, transcript, memo…)</label>
  <textarea id="deal-text" placeholder="Paste text here…"></textarea>
  <button onclick="submitScore()">Score This Deal</button>
  <button class="secondary" onclick="clearAll()">Clear</button>
  <div id="loading" class="hidden">Scoring…</div>
  <div id="result"></div>
</div>

<div class="panel">
  <h2>Research a Ticker</h2>
  <label for="ticker">Public company ticker (pulls latest SEC EDGAR 10-K, scores it)</label>
  <input type="text" id="ticker" placeholder="e.g. AAPL" style="max-width:180px;">
  <button onclick="submitResearch()">Fetch &amp; Score</button>
  <div id="research-result"></div>
</div>

<script>
async function submitScore() {
  const text = document.getElementById('deal-text').value.trim();
  const res = document.getElementById('result');
  const loading = document.getElementById('loading');
  if (!text) { res.innerHTML = '<div class="error">Paste some deal text first.</div>'; return; }
  loading.classList.remove('hidden'); res.innerHTML = '';
  try {
    const r = await fetch('/api/score', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text})
    });
    const data = await r.json();
    loading.classList.add('hidden');
    if (data.error) { res.innerHTML = '<div class="error">' + data.error + '</div>'; return; }
    renderResult(data, res);
  } catch (e) {
    loading.classList.add('hidden');
    res.innerHTML = '<div class="error">Request failed: ' + e + '</div>';
  }
}

async function submitResearch() {
  const ticker = document.getElementById('ticker').value.trim();
  const res = document.getElementById('research-result');
  if (!ticker) { res.innerHTML = '<div class="error">Enter a ticker.</div>'; return; }
  res.innerHTML = '<div class="evidence">Fetching EDGAR filing and scoring… (may take ~20s first time)</div>';
  try {
    const r = await fetch('/api/research', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ticker})
    });
    const arr = await r.json();
    if (arr.error) { res.innerHTML = '<div class="error">' + arr.error + '</div>'; return; }
    renderResult(arr[0], res);
  } catch (e) {
    res.innerHTML = '<div class="error">Request failed: ' + e + '</div>';
  }
}

function clearAll() {
  document.getElementById('deal-text').value = '';
  document.getElementById('result').innerHTML = '';
}

function renderResult(data, res) {
  const recClass = data.recommendation.startsWith('STRONG') ? 'STRONG' : data.recommendation;
  let html = `
    <hr style="border-color:#2a2f3d;margin:16px 0;">
    <div style="display:flex;align-items:baseline;gap:16px;">
      <div class="composite">${(data.composite_score*100).toFixed(0)}%</div>
      <div class="recommendation ${recClass}">${data.recommendation}</div>
    </div>
    <div style="margin-top:14px;">`;
  for (const [pn, pd] of Object.entries(data.pattern_scores)) {
    const val = pd.direction === 'binary' ? (pd.value ? 'Yes' : 'No') : (pd.value*100).toFixed(1) + '%';
    const thr = pd.direction === 'binary' ? '' : ' (threshold ' + (pd.threshold*100).toFixed(0) + '%)';
    html += `
      <div class="score-row">
        <span class="badge ${pd.is_positive ? 'PASS' : 'FAIL'}">${pd.is_positive ? 'PASS' : 'FAIL'}</span>
        <span>${pn}</span>
        <span style="color:var(--muted);">${val}${thr}</span>
      </div>`;
  }
  html += '</div><div class="evidence">';
  for (const [pn, ev] of Object.entries(data.evidence_summary)) {
    html += pn + ': ' + ev + '<br>';
  }
  res.innerHTML = html + '</div>';
}
</script>
</body>
</html>
"""
