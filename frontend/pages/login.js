// frontend/pages/login.js
import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/router";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export default function Login() {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState("candidate");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isRegister) {
        await axios.post(`${API_BASE}/auth/register`, { email, password, full_name: fullName, role });
      }
      const res = await axios.post(`${API_BASE}/auth/login_json`, { email, password });
      const token = res.data.access_token;
      localStorage.setItem("token", token);
      // get user to find role
      const me = await axios.get(`${API_BASE}/users/me`, { headers: { Authorization: `Bearer ${token}` } });
      localStorage.setItem("role", me.data.role);
      if (me.data.role === "recruiter") router.push("/recruiter");
      else router.push("/candidate");
    } catch (err) {
      alert(err?.response?.data?.detail || "Auth failed");
    }
  };

  return (
    <div className="container">
      <div style={{ maxWidth: 520, margin: "auto" }}>
        <div className="card">
          <h2>{isRegister ? "Register" : "Login"}</h2>
          <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
            {isRegister && (
              <>
                <input className="input" placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} />
                <select className="input" value={role} onChange={(e) => setRole(e.target.value)} style={{ background: "white" }}>
                  <option value="candidate">Candidate</option>
                  <option value="recruiter">Recruiter</option>
                </select>
              </>
            )}
            <input className="input" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            <input className="input" placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            <button className="button" type="submit">{isRegister ? "Register" : "Login"}</button>
          </form>
          <div style={{ marginTop: 12 }}>
            <button className="button" onClick={() => setIsRegister(!isRegister)} style={{ background: "transparent", color: "#2563eb", border: "1px solid #e6eefc" }}>
              {isRegister ? "Have account? Login" : "New? Register"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
