"""
AI Resume Analyser
-------------------
Flask backend that scores a candidate resume against a job description
using classic Python NLP techniques:

  * TF-IDF + cosine similarity            -> overall semantic match score
  * Regex / dictionary keyword matching   -> skill extraction (matched + missing)
  * Regex pattern mining                  -> years-of-experience depth
  * Rule-based generator                  -> actionable improvement suggestions

No external ML API calls -- everything runs locally so it works offline
and is fast enough for real-time screening.
"""

import io
import os
import re
import uuid

from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import PyPDF2
import docx

from skills_data import SKILL_TAXONOMY, FLAT_SKILLS

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload cap

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


# --------------------------------------------------------------------------
# File parsing
# --------------------------------------------------------------------------

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(file_stream) -> str:
    reader = PyPDF2.PdfReader(file_stream)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)


def extract_text_from_docx(file_stream) -> str:
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(file_storage) -> str:
    filename = file_storage.filename
    ext = filename.rsplit(".", 1)[1].lower()
    data = file_storage.read()
    stream = io.BytesIO(data)

    if ext == "pdf":
        return extract_text_from_pdf(stream)
    if ext == "docx":
        return extract_text_from_docx(stream)
    if ext == "txt":
        return data.decode("utf-8", errors="ignore")
    return ""


# --------------------------------------------------------------------------
# NLP helpers
# --------------------------------------------------------------------------

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"[^a-z0-9\+\#\.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(clean: str):
    """Dictionary-based keyword matching over the skill taxonomy."""
    found = {}
    for skill, category in FLAT_SKILLS.items():
        # word-boundary aware search; handles multi-word & symbol skills (c++, c#)
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, clean):
            found.setdefault(category, []).append(skill)
    return found


def extract_experience_years(raw_text: str) -> float:
    """Pulls the highest 'N years' style mention as a proxy for experience depth."""
    matches = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs|year)\b", raw_text.lower())
    years = [float(m) for m in matches]
    return max(years) if years else 0.0


def compute_similarity_score(resume_clean: str, jd_clean: str) -> float:
    """TF-IDF cosine similarity between resume and job description, 0-100."""
    if not resume_clean.strip() or not jd_clean.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf = vectorizer.fit_transform([resume_clean, jd_clean])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(sim * 100, 1)


def compute_skill_overlap(resume_skills: dict, jd_skills: dict):
    resume_flat = {s for skills in resume_skills.values() for s in skills}
    jd_flat = {s for skills in jd_skills.values() for s in skills}

    matched = sorted(resume_flat & jd_flat)
    missing = sorted(jd_flat - resume_flat)
    extra = sorted(resume_flat - jd_flat)

    overlap_pct = round((len(matched) / len(jd_flat)) * 100, 1) if jd_flat else 0.0
    return matched, missing, extra, overlap_pct


def generate_suggestions(missing, overlap_pct, semantic_score, resume_years, jd_years):
    tips = []

    if missing:
        top_missing = ", ".join(missing[:6])
        tips.append(
            f"Add or highlight these job-description keywords if you genuinely have them: {top_missing}."
        )

    if overlap_pct < 50:
        tips.append(
            "Your listed skills cover less than half of what the job description asks for. "
            "Consider re-reading the JD and mirroring its exact terminology in your Skills section."
        )

    if semantic_score < 40:
        tips.append(
            "Overall content overlap with the job description is low. Rewrite your summary and "
            "bullet points using language closer to the JD so ATS keyword scanners pick it up."
        )
    elif semantic_score < 70:
        tips.append(
            "Overall alignment is decent but not strong. Tie 2-3 of your project bullets directly "
            "to responsibilities mentioned in the job description."
        )

    if jd_years and resume_years < jd_years:
        tips.append(
            f"The role expects roughly {jd_years:g}+ years of experience; your resume shows about "
            f"{resume_years:g}. If you have relevant internship or project experience, quantify it "
            "explicitly to close that gap."
        )

    if not re.search(r"\d", "".join(missing)):
        tips.append(
            "Quantify achievements with numbers (%, time saved, users impacted) wherever possible -- "
            "recruiters and ATS scoring both weight measurable impact highly."
        )

    if not tips:
        tips.append("Strong match! Fine-tune formatting and keep keyword phrasing consistent with the JD.")

    return tips


def analyse(resume_raw: str, jd_raw: str) -> dict:
    resume_clean = clean_text(resume_raw)
    jd_clean = clean_text(jd_raw)

    resume_skills = extract_skills(resume_clean)
    jd_skills = extract_skills(jd_clean)

    matched, missing, extra, overlap_pct = compute_skill_overlap(resume_skills, jd_skills)
    semantic_score = compute_similarity_score(resume_clean, jd_clean)

    resume_years = extract_experience_years(resume_raw)
    jd_years = extract_experience_years(jd_raw)

    # Weighted final score: keyword overlap carries more weight (ATS-style),
    # semantic similarity captures phrasing/context match.
    final_score = round((overlap_pct * 0.6) + (semantic_score * 0.4), 1)

    suggestions = generate_suggestions(missing, overlap_pct, semantic_score, resume_years, jd_years)

    return {
        "final_score": final_score,
        "semantic_score": semantic_score,
        "overlap_pct": overlap_pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "resume_years": resume_years,
        "jd_years": jd_years,
        "resume_skill_categories": resume_skills,
        "jd_skill_categories": jd_skills,
        "suggestions": suggestions,
    }


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    jd_text = request.form.get("job_description", "").strip()
    resume_file = request.files.get("resume_file")
    resume_text_input = request.form.get("resume_text", "").strip()

    if not jd_text:
        return jsonify({"error": "Job description is required."}), 400

    resume_raw = ""
    if resume_file and resume_file.filename:
        if not allowed_file(resume_file.filename):
            return jsonify({"error": "Unsupported file type. Use PDF, DOCX, or TXT."}), 400
        resume_raw = extract_text(resume_file)
    elif resume_text_input:
        resume_raw = resume_text_input

    if not resume_raw.strip():
        return jsonify({"error": "Please upload a resume file or paste resume text."}), 400

    result = analyse(resume_raw, jd_text)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
