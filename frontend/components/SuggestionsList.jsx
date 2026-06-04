// frontend/components/SuggestionsList.jsx
export default function SuggestionsList({ suggestions = [] }) {
  return (
    <div className="card">
      <h3>💡 Suggestions</h3>
      {suggestions.length === 0 ? (
        <div className="small-muted" style={{ marginTop: 8 }}>No suggestions yet.</div>
      ) : (
        <ul style={{ marginTop: 10 }}>
          {suggestions.map((s, i) => <li key={i} style={{ margin: "8px 0" }}>{s}</li>)}
        </ul>
      )}
    </div>
  );
}
