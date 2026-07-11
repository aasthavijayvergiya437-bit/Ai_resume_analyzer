const form = document.getElementById('analyzeForm');
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('resumeFile');
const dzText = document.getElementById('dzText');
const analyzeBtn = document.getElementById('analyzeBtn');
const errMsg = document.getElementById('errMsg');
const results = document.getElementById('results');
const scanline = document.getElementById('scanline');
const stamp = document.getElementById('stamp');

// --- drag & drop niceties ---
['dragenter', 'dragover'].forEach(evt =>
  dropzone.addEventListener(evt, e => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  })
);
['dragleave', 'drop'].forEach(evt =>
  dropzone.addEventListener(evt, e => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
  })
);
dropzone.addEventListener('drop', e => {
  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    updateFileLabel(file);
  }
});
fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) updateFileLabel(fileInput.files[0]);
});
function updateFileLabel(file) {
  dzText.innerHTML = `<strong>${file.name}</strong><br><small>${(file.size / 1024).toFixed(0)} KB — ready to scan</small>`;
}

function chip(text, tone) {
  const span = document.createElement('span');
  span.className = `chip chip-${tone}`;
  span.textContent = text;
  return span;
}

function renderChips(containerId, items, tone) {
  const el = document.getElementById(containerId);
  el.innerHTML = '';
  if (!items || items.length === 0) {
    const empty = document.createElement('span');
    empty.className = 'chip-empty';
    empty.textContent = '— none —';
    el.appendChild(empty);
    return;
  }
  items.forEach(item => el.appendChild(chip(item, tone)));
}

function scoreTone(score) {
  if (score >= 70) return { cls: '', label: 'STRONG MATCH' };
  if (score >= 40) return { cls: 'tone-gold', label: 'PARTIAL MATCH' };
  return { cls: 'tone-red', label: 'WEAK MATCH' };
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errMsg.textContent = '';

  const jd = document.getElementById('jdText').value.trim();
  if (!jd) {
    errMsg.textContent = 'Paste a job description before running the match.';
    return;
  }

  analyzeBtn.disabled = true;
  analyzeBtn.querySelector('span').textContent = 'Scanning...';

  try {
    const formData = new FormData(form);
    const res = await fetch('/api/analyze', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) {
      errMsg.textContent = data.error || 'Something went wrong. Try again.';
      return;
    }

    renderResults(data);
  } catch (err) {
    errMsg.textContent = 'Could not reach the server. Please try again.';
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.querySelector('span').textContent = 'Run the Match';
  }
});

function renderResults(data) {
  results.hidden = false;

  // scanline sweep
  scanline.classList.remove('active');
  void scanline.offsetWidth; // restart animation
  scanline.classList.add('active');

  // stamp
  stamp.classList.remove('pop', 'tone-red', 'tone-gold');
  const tone = scoreTone(data.final_score);
  if (tone.cls) stamp.classList.add(tone.cls);
  document.getElementById('stampScore').textContent = `${data.final_score}%`;
  document.getElementById('stampLabel').textContent = tone.label;
  void stamp.offsetWidth;
  stamp.classList.add('pop');

  // bars
  setTimeout(() => {
    document.getElementById('barOverlap').style.width = `${data.overlap_pct}%`;
    document.getElementById('barSemantic').style.width = `${data.semantic_score}%`;
    const expPct = data.jd_years > 0 ? Math.min((data.resume_years / data.jd_years) * 100, 100) : (data.resume_years > 0 ? 100 : 0);
    document.getElementById('barExp').style.width = `${expPct}%`;
  }, 50);

  document.getElementById('valOverlap').textContent = `${data.overlap_pct}%`;
  document.getElementById('valSemantic').textContent = `${data.semantic_score}%`;
  document.getElementById('valExp').textContent = data.jd_years
    ? `${data.resume_years}/${data.jd_years}yr`
    : (data.resume_years ? `${data.resume_years}yr` : '—');

  // chips
  renderChips('matchedChips', data.matched_skills, 'green');
  renderChips('missingChips', data.missing_skills, 'red');
  renderChips('extraChips', data.extra_skills, 'blue');

  // suggestions
  const list = document.getElementById('suggestionsList');
  list.innerHTML = '';
  data.suggestions.forEach(s => {
    const li = document.createElement('li');
    li.textContent = s;
    list.appendChild(li);
  });

  results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
