// frontend/pages/index.js
import Link from "next/link";

export default function Home() {
  return (
    <div className="container fade-in">
      <div className="header fade-in">
        <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
          <img src="/logo.png" alt="TalentLink" style={{ width: 48, height: 48 }} className="hover-scale" />
          <div>
            <h1 style={{ margin: 0, fontSize: '1.5rem', background: 'linear-gradient(to right, #1e293b, #3b82f6)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>TalentLink</h1>
            <div className="small-muted">AI-driven campus recruitment & resume screening</div>
          </div>
        </div>
        <div>
          <Link href="/login"><a className="button">Sign in</a></Link>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 350px", gap: 32 }}>
        <div className="card fade-in delay-100">
          <h2>What TalentLink does</h2>
          <p className="small-muted" style={{ marginBottom: '1.5rem' }}>Upload resumes, match with job descriptions using TF-IDF + cosine similarity, get suggestions, and track progress over time. Recruiters can shortlist candidates quickly using score-sorted dashboards.</p>
          <ul style={{ paddingLeft: '20px', lineHeight: '1.8' }}>
            <li>ATS scoring (semantic)</li>
            <li>AI-powered suggestions (local heuristics)</li>
            <li>Resume history and progress graphs</li>
            <li>Recruiter dashboards and role-based access</li>
          </ul>
        </div>

        <div>
          <div className="card fade-in delay-200" style={{ marginBottom: 24 }}>
            <h3>Get started</h3>
            <p className="small-muted" style={{ marginBottom: '1.5rem' }}>Create an account on the login page and choose candidate or recruiter role.</p>
            <Link href="/login"><a className="button" style={{ display: 'block', textAlign: 'center' }}>Login / Register</a></Link>
          </div>

          <div className="card fade-in delay-300">
            <h3>Developer notes</h3>
            <p className="small-muted">Backend at <code>http://localhost:8000</code>, Frontend <code>http://localhost:3000</code>. Use the register endpoint to create users.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
