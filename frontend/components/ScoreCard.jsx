// frontend/components/ScoreCard.jsx
export default function ScoreCard({ score }) {
  return (
    <div className="card" style={{ textAlign: "center" }}>
      <h3>📊 ATS Score</h3>
      <div style={{ fontSize: 36, fontWeight: 700, color: "#2563eb", marginTop: 8 }}>{score ?? "—"}%</div>
      <div className="small-muted" style={{ marginTop: 6 }}>Match with job description</div>
    </div>
  );
}
