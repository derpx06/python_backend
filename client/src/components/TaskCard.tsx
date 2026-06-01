"use client";

import { useAuth } from "@/context/AuthContext";

export default function TaskCard({ task, onEdit, onDelete }: { task: any, onEdit: () => void, onDelete: () => void }) {
  const { user } = useAuth();
  const date = new Date(task.updated_at).toLocaleDateString(undefined, { 
    year: 'numeric', month: 'short', day: 'numeric' 
  });

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "TODO": return <span className="badge badge-todo">To Do</span>;
      case "IN_PROGRESS": return <span className="badge badge-progress">In Progress</span>;
      case "DONE": return <span className="badge badge-done">Done</span>;
      default: return null;
    }
  };

  const isAdmin = user?.role === 'ADMIN';

  return (
    <div className="glass animate-in" style={{ padding: "24px", display: "flex", flexDirection: "column", height: "100%", gap: "16px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <h3 style={{ fontSize: "1.2rem", fontWeight: 600, color: "var(--text-primary)", flex: 1 }}>{task.title}</h3>
        {getStatusBadge(task.status)}
      </div>
      
      <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem", flex: 1, whiteSpace: "pre-wrap" }}>
        {task.description || <span style={{ fontStyle: "italic", opacity: 0.5 }}>No description</span>}
      </p>
      
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: "auto", paddingTop: "16px", borderTop: "1px solid rgba(255,255,255,0.05)" }}>
        <span style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>{date}</span>
        
        <div style={{ display: "flex", gap: "8px" }}>
          <button onClick={onEdit} className="btn-secondary" style={{ padding: "4px 12px", fontSize: "0.85rem", border: "none", background: "rgba(255,255,255,0.05)" }}>
            Edit
          </button>
          <button onClick={onDelete} className="btn-danger" style={{ padding: "4px 12px", fontSize: "0.85rem" }}>
            Delete
          </button>
        </div>
      </div>
      {isAdmin && task.owner_id !== user?.id && (
        <div style={{ fontSize: "0.75rem", color: "var(--warning)", marginTop: "-8px" }}>
          Owned by user ID: {task.owner_id}
        </div>
      )}
    </div>
  );
}
