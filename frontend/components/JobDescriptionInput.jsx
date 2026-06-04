// frontend/components/JobDescriptionInput.jsx
export default function JobDescriptionInput({ jobDesc, setJobDesc }) {
  return (
    <div className="card">
      <h3>📝 Job Description</h3>
      <textarea className="input" rows={7} value={jobDesc} onChange={(e) => setJobDesc(e.target.value)} placeholder="Paste job description here..." />
    </div>
  );
}
