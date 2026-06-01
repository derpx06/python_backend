"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Link from "next/link";
import Toast from "@/components/Toast";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || err.response?.data?.error || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", padding: "16px" }}>
      {error && <Toast message={error} type="error" onClose={() => setError(null)} />}
      <div className="glass animate-in" style={{ width: "100%", maxWidth: "400px", padding: "32px", textAlign: "center" }}>
        <h1 className="gradient-text" style={{ fontSize: "2rem", marginBottom: "8px", fontWeight: "bold" }}>Welcome Back</h1>
        <p style={{ color: "var(--text-secondary)", marginBottom: "32px" }}>Sign in to manage your tasks</p>
        
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <div>
            <input
              type="email"
              className="input-field"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <input
              type="password"
              className="input-field"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: "8px" }}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
        
        <p style={{ marginTop: "24px", color: "var(--text-secondary)", fontSize: "0.9rem" }}>
          Don't have an account? <Link href="/register" style={{ color: "var(--accent)", textDecoration: "none" }}>Register</Link>
        </p>
      </div>
    </div>
  );
}
