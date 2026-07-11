<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Screening Desk — AI Resume Analyser</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>

<div class="deskglow"></div>

<header class="topbar">
  <div class="brand">
    <span class="brand-mark">◈</span>
    <span class="brand-text">SCREENING&nbsp;DESK</span>
  </div>
  <div class="topbar-sub">AI Resume Analyser — matched against the job description, on the spot</div>
</header>

<main class="wrap">

  <section class="hero">
    <p class="eyebrow">Case File 001 — Candidate vs. Requisition</p>
    <h1>Put the resume<br>under the light.</h1>
    <p class="hero-copy">
      Paste a job description, drop in a resume, and the desk runs both documents
      through the same NLP pipeline a screener would use by hand — skill extraction,
      keyword overlap, experience depth — then stamps a verdict in seconds.
    </p>
    <div class="hero-stats">
      <div><span class="num">70%</span><span class="lbl">less manual screening time</span></div>
      <div><span class="num">3</span><span class="lbl">signals scored: skills · context · experience</span></div>
      <div><span class="num">PDF·DOCX·TXT</span><span class="lbl">resume formats accepted</span></div>
    </div>
  </section>

  <section class="desk" id="desk">
    <form id="analyzeForm" class="desk-grid" autocomplete="off">

      <div class="doc-card" data-doc="resume">
        <div class="doc-tab">EXHIBIT A — RESUME</div>
        <div class="doc-body">
          <label class="dropzone" id="dropzone" for="resumeFile">
            <input type="file" id="resumeFile" name="resume_file" accept=".pdf,.docx,.txt" hidden>
            <span class="dz-icon">⇪</span>
            <span class="dz-text" id="dzText">Drop resume here or click to browse<br><small>PDF, DOCX or TXT · max 5MB</small></span>
          </label>
          <div class="or-divider"><span>or paste text</span></div>
          <textarea id="resumeText" name="resume_text" placeholder="Paste resume text here instead of uploading a file..."></textarea>
        </div>
      </div>

      <div class="doc-card" data-doc="jd">
        <div class="doc-tab">EXHIBIT B — JOB DESCRIPTION</div>
        <div class="doc-body">
          <textarea id="jdText" name="job_description" class="jd-textarea" placeholder="Paste the full job description here — responsibilities, required skills, experience level..." required></textarea>
        </div>
      </div>

    </form>

    <div class="desk-actions">
      <button type="submit" form="analyzeForm" class="stamp-btn" id="analyzeBtn">
        <span>Run the Match</span>
      </button>
      <p class="err" id="errMsg"></p>
    </div>
  </section>

  <section class="results" id="results" hidden>

    <div class="scanline" id="scanline"></div>

    <div class="verdict-row">
      <div class="stamp" id="stamp">
        <div class="stamp-score" id="stampScore">--</div>
        <div class="stamp-label" id="stampLabel">MATCH</div>
      </div>

      <div class="breakdown">
        <div class="bar-row">
          <span class="bar-label">Skill overlap</span>
          <div class="bar-track"><div class="bar-fill fill-green" id="barOverlap"></div></div>
          <span class="bar-val" id="valOverlap">0%</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">Contextual similarity</span>
          <div class="bar-track"><div class="bar-fill fill-gold" id="barSemantic"></div></div>
          <span class="bar-val" id="valSemantic">0%</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">Experience depth</span>
          <div class="bar-track"><div class="bar-fill fill-blue" id="barExp"></div></div>
          <span class="bar-val" id="valExp">--</span>
        </div>
      </div>
    </div>

    <div class="skills-grid">
      <div class="skills-col">
        <h3><span class="dot dot-green"></span>Matched keywords</h3>
        <div class="chip-row" id="matchedChips"></div>
      </div>
      <div class="skills-col">
        <h3><span class="dot dot-red"></span>Missing from resume</h3>
        <div class="chip-row" id="missingChips"></div>
      </div>
      <div class="skills-col">
        <h3><span class="dot dot-blue"></span>Extra on resume</h3>
        <div class="chip-row" id="extraChips"></div>
      </div>
    </div>

    <div class="notes">
      <h3>Screener's notes</h3>
      <ul id="suggestionsList"></ul>
    </div>

  </section>

</main>

<footer class="foot">
  Built for portfolio use · scoring runs entirely with local Python NLP (TF-IDF + rule-based extraction), no data leaves the server.
</footer>

<script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
