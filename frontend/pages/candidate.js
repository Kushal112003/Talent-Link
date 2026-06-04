// frontend/pages/candidate.js
import { useEffect, useState } from "react";
import UploadResume from "../components/UploadResume";
import JobDescriptionInput from "../components/JobDescriptionInput";
import ScoreCard from "../components/ScoreCard";
import SuggestionsList from "../components/SuggestionsList";
import ScoreHistoryChart from "../components/ScoreHistoryChart";
import axios from "axios";
import { useRouter } from "next/router";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Candidate() {
  const router = useRouter();
  const [jobDesc, setJobDesc] = useState("");
  const [score, setScore] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return router.push("/login");
    loadHistory(token);
  }, []);

  const loadHistory = async (token) => {
    try {
      const res = await axios.get(`${API_BASE}/users/me/resumes`, { headers: { Authorization: `Bearer ${token}` } });
      const formatted = res.data.map(r => ({ timestamp: r.timestamp, score: r.score }));
      setHistory(formatted);
    } catch (err) {
      console.error(err);
    }
  };

  const [tags, setTags] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) loadProfile(token);
  }, []);

  const loadProfile = async (token) => {
    try {
      const res = await axios.get(`${API_BASE}/users/me`, { headers: { Authorization: `Bearer ${token}` } });
      setTags(res.data.tags || "");
    } catch (err) {
      console.error(err);
    }
  };

  const saveTags = async () => {
    try {
      const token = localStorage.getItem("token");
      await axios.put(`${API_BASE}/users/me`, { tags }, { headers: { Authorization: `Bearer ${token}` } });
      alert("Tags updated!");
    } catch (err) {
      alert("Failed to update tags");
    }
  };

  const handleUpload = async (file) => {
    try {
      const token = localStorage.getItem("token");
      const form = new FormData();
      form.append("file", file);
      form.append("job_description", jobDesc);
      const res = await axios.post(`${API_BASE}/resumes/upload_sync`, form, { headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" } });
      setScore(res.data.score);
      setSuggestions(res.data.suggestions || []);
      await loadHistory(token);
    } catch (err) {
      alert("Upload failed");
    }
  };

  return (
    <div className="container">
      <div className="header">
        <div>
          <h1>Candidate Dashboard</h1>
          <div className="small-muted">Upload, analyze, and improve your resume</div>
        </div>
        <div>
          <button className="button" onClick={() => { localStorage.clear(); router.push("/login"); }}>Logout</button>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 360px", gap: 20 }}>
        <div style={{ display: "grid", gap: 12 }}>
          <JobDescriptionInput jobDesc={jobDesc} setJobDesc={setJobDesc} />

          <div className="card">
            <h3>My Profile Tags</h3>
            <div className="small-muted" style={{ marginBottom: 10 }}>Add tags to help recruiters find you (comma separated)</div>
            <div style={{ display: "flex", gap: 10 }}>
              <input
                type="text"
                className="input"
                placeholder="e.g. Python, React, Data Science"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
              />
              <button className="button" onClick={saveTags}>Save</button>
            </div>
          </div>

          <UploadResume onUpload={handleUpload} />
          <SuggestionsList suggestions={suggestions} />
        </div>

        <div style={{ display: "grid", gap: 12 }}>
          <ScoreCard score={score} />
          <ScoreHistoryChart history={history} />
        </div>
      </div>
    </div>
  );
}
