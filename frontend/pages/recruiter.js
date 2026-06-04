// frontend/pages/recruiter.js
import { useEffect, useState } from "react";
import RecruiterTable from "../components/RecruiterTable";
import axios from "axios";
import { useRouter } from "next/router";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Recruiter() {
  const router = useRouter();
  const [candidates, setCandidates] = useState([]);
  const [search, setSearch] = useState("");
  const [tags, setTags] = useState("");
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return router.push("/login");
    loadCandidates(token);
  }, []);

  const loadCandidates = async (token, query = "", tagFilter = "") => {
    try {
      let url = `${API_BASE}/recruiter/resumes?`;
      if (query) url += `q=${encodeURIComponent(query)}&`;
      if (tagFilter) url += `tags=${encodeURIComponent(tagFilter)}`;

      const res = await axios.get(url, { headers: { Authorization: `Bearer ${token}` } });
      setCandidates(res.data);
    } catch (err) {
      console.error(err);
      if (err?.response?.status === 401) router.push("/login");
    }
  };

  const handleSearch = () => {
    const token = localStorage.getItem("token");
    loadCandidates(token, search, tags);
  };

  const handleMatchUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      const token = localStorage.getItem("token");
      const form = new FormData();
      form.append("file", file);

      const res = await axios.post(`${API_BASE}/recruiter/match-resume`, form, {
        headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" }
      });
      setCandidates(res.data);
    } catch (err) {
      console.error(err);
      alert("Matching failed");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1>Recruiter Dashboard</h1>
          <div className="small-muted">Find the perfect candidate</div>
        </div>
        <div>
          <button className="button" onClick={() => { localStorage.clear(); router.push("/login"); }}>Logout</button>
        </div>
      </div>

      <div style={{ display: "grid", gap: 20 }}>

        {/* Search & Filter Section */}
        <div className="card" style={{ display: "flex", gap: 10, alignItems: "flex-end", flexWrap: "wrap" }}>
          <div style={{ flex: 1 }}>
            <label className="small-muted">Search Name/Email</label>
            <input
              className="input"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="e.g. John Doe"
              onKeyDown={e => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <div style={{ flex: 1 }}>
            <label className="small-muted">Filter by Tags</label>
            <input
              className="input"
              value={tags}
              onChange={e => setTags(e.target.value)}
              placeholder="e.g. Python, React"
              onKeyDown={e => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <button className="button" onClick={handleSearch}>Search</button>
        </div>

        {/* Resume Match Section */}
        <div className="card" style={{ background: "#f8fafc", border: "1px dashed #cbd5e1" }}>
          <div style={{ fontWeight: 600, marginBottom: 4 }}>📄 AI Resume Match</div>
          <div className="small-muted" style={{ marginBottom: 12 }}>Upload a Job Description or Ideal Resume to find similar candidates</div>
          <input type="file" onChange={handleMatchUpload} disabled={uploading} accept=".pdf,.txt,.doc,.docx" />
          {uploading && <span style={{ marginLeft: 10 }}>Matching...</span>}
        </div>

        <RecruiterTable candidates={candidates} />
      </div>
    </div>
  );
}
