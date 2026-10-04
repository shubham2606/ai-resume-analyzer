import { useMemo, useState } from "react";
import {
  BriefcaseBusiness,
  CheckCircle2,
  FileText,
  LoaderCircle,
  Sparkles,
  UploadCloud,
} from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function ScoreRing({ score }) {
  return (
    <div className="score-ring" style={{ "--score": `${score * 3.6}deg` }}>
      <div>
        <strong>{score}</strong>
        <span>/100</span>
      </div>
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const canAnalyze = useMemo(() => Boolean(file) && !loading, [file, loading]);

  async function analyzeResume() {
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);

    const form = new FormData();
    form.append("file", file);

    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: "POST",
        body: form,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Resume analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message.includes("Failed to fetch")
          ? "Cannot connect to the backend. Make sure FastAPI is running on port 8000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div className="eyebrow">
          <Sparkles size={16} />
          Phase 1 POC
        </div>
        <h1>ResumeLens AI</h1>
        <p>
          Upload a PDF or DOCX resume to extract skills, review resume quality,
          identify improvement opportunities, and discover matching job roles.
        </p>
      </section>

      <section className="upload-card">
        <label className="drop-zone">
          <UploadCloud size={36} />
          <strong>{file ? file.name : "Choose a resume"}</strong>
          <span>PDF or DOCX • Maximum 5 MB</span>
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(event) => {
              setFile(event.target.files?.[0] || null);
              setResult(null);
              setError("");
            }}
          />
        </label>

        <button disabled={!canAnalyze} onClick={analyzeResume}>
          {loading ? <LoaderCircle className="spin" size={18} /> : <FileText size={18} />}
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {error && <div className="error">{error}</div>}
      </section>

      {result && (
        <section className="results">
          <div className="summary-grid">
            <article className="panel score-panel">
              <div>
                <p className="panel-kicker">Resume score</p>
                <h2>{result.filename}</h2>
                <p>{result.estimated_experience}</p>
              </div>
              <ScoreRing score={result.score} />
            </article>

            <article className="panel">
              <p className="panel-kicker">Detected skills</p>
              <div className="chips">
                {result.skills.length ? (
                  result.skills.map((skill) => <span key={skill}>{skill}</span>)
                ) : (
                  <em>No predefined skills detected.</em>
                )}
              </div>
            </article>
          </div>

          <div className="content-grid">
            <article className="panel">
              <div className="panel-title">
                <CheckCircle2 size={20} />
                <h3>Improvement suggestions</h3>
              </div>
              <ul className="suggestions">
                {result.suggestions.map((suggestion) => (
                  <li key={suggestion}>{suggestion}</li>
                ))}
              </ul>
            </article>

            <article className="panel">
              <div className="panel-title">
                <BriefcaseBusiness size={20} />
                <h3>Role matches</h3>
              </div>
              <div className="roles">
                {result.job_matches.map((job) => (
                  <div className="role" key={job.role}>
                    <div className="role-top">
                      <strong>{job.role}</strong>
                      <span>{job.match_percent}%</span>
                    </div>
                    <div className="progress">
                      <i style={{ width: `${job.match_percent}%` }} />
                    </div>
                    <small>
                      Matched: {job.matched_skills.join(", ") || "No core skills yet"}
                    </small>
                  </div>
                ))}
              </div>
            </article>
          </div>

          <article className="panel">
            <p className="panel-kicker">Score breakdown</p>
            <div className="breakdown">
              {result.score_breakdown.map((item) => (
                <div key={item.name}>
                  <span>{item.name}</span>
                  <strong>{item.score}/{item.max}</strong>
                </div>
              ))}
            </div>
          </article>
        </section>
      )}

      <footer>
        Phase 1 uses rule-based analysis, so no paid AI key is required.
        LLM-based semantic analysis is planned for Phase 2.
      </footer>
    </main>
  );
}

export default App;
