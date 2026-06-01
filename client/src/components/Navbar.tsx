"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  if (!user) return null;

  return (
    <nav style={{ 
      background: "var(--bg-card)", 
      borderBottom: "1px solid var(--border-color)",
      padding: "16px 32px",
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      backdropFilter: "blur(12px)",
      position: "sticky",
      top: 0,
      zIndex: 50
    }}>
      <div className="gradient-text" style={{ fontSize: "1.5rem", fontWeight: "bold" }}>
        TaskFlow
      </div>
      
      <div style={{ display: "flex", alignItems: "center", gap: "24px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span style={{ fontWeight: 500 }}>{user.name}</span>
          <span className={`badge ${user.role === 'ADMIN' ? 'badge-admin' : 'badge-user'}`}>
            {user.role}
          </span>
        </div>
        <button onClick={handleLogout} className="btn-secondary" style={{ padding: "6px 12px", fontSize: "0.85rem" }}>
          Logout
        </button>
      </div>
    </nav>
  );
}
