// frontend/components/ScoreHistoryChart.jsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ScoreHistoryChart({ history = [] }) {
  if (!history || history.length < 2) {
    return <div className="card"><div className="small-muted">Upload more resumes to see progress.</div></div>;
  }
  return (
    <div className="card">
      <h3>📈 Progress</h3>
      <div style={{ width: "100%", height: 260 }}>
        <ResponsiveContainer>
          <LineChart data={history}>
            <XAxis dataKey="timestamp" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#2563eb" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
