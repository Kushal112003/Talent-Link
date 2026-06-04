// frontend/components/RecruiterTable.jsx
export default function RecruiterTable({ candidates = [] }) {
  const rows = [...candidates].sort((a, b) => (b.match_score || 0) - (a.match_score || 0));
  return (
    <div className="card">
      <h3>📋 Candidates</h3>
      <table style={{ width: "100%", marginTop: 12, borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #eef2f6" }}>
            <th style={{ padding: 8 }}>Name</th>
            <th style={{ padding: 8 }}>Email</th>
            <th style={{ padding: 8 }}>Tags</th>
            <th style={{ padding: 8 }}>Match Score</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} style={{ borderBottom: "1px solid #f1f5f9" }}>
              <td style={{ padding: 8, fontWeight: 500 }}>{r.full_name || "—"}</td>
              <td style={{ padding: 8 }}>{r.email}</td>
              <td style={{ padding: 8 }}>
                {r.tags ? (
                  <div style={{ display: "flex", gap: 4, flexWrap: "wrap" }}>
                    {r.tags.split(",").map(t => (
                      <span key={t} style={{ background: "#eef2ff", color: "#3730a3", padding: "2px 6px", borderRadius: 4, fontSize: 12 }}>{t}</span>
                    ))}
                  </div>
                ) : <span style={{ color: "#94a3b8" }}>—</span>}
              </td>
              <td style={{ padding: 8, color: r.match_score ? "#2563eb" : "#94a3b8", fontWeight: 600 }}>
                {r.match_score ? `${r.match_score}%` : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
