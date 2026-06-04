// frontend/components/UploadResume.jsx
import { useState } from "react";

export default function UploadResume({ onUpload }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);
  const handleSubmit = (e) => {
    e.preventDefault();
    if (file) onUpload(file);
  };

  return (
    <div className="card">
      <h3>📄 Upload Resume</h3>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12, marginTop: 12 }}>
        <input className="input" type="file" accept="application/pdf" onChange={handleFileChange} />
        <button className="button" type="submit" disabled={!file}>Upload & Analyze</button>
      </form>
    </div>
  );
}
