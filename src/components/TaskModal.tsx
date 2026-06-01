"use client";

import { useState, useEffect } from "react";

export default function TaskModal({ task, onClose, onSubmit }: { task?: any, onClose: () => void, onSubmit: (data: any) => void }) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [status, setStatus] = useState(task?.status || "TODO");

  // Prevent background scrolling
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ title, description, status });
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="glass animate-in" 
        style={{ width: "100%", maxWidth: "500px", padding: "32px", margin: "16px", position: "relative" }}
        onClick={(e) => e.stopPropagation()}
      >
        <button 
          onClick={onClose} 
          style={{ position: "absolute", top: "16px", right: "16px", background: "none", border: "none", color: "var(--text-secondary)", fontSize: "1.5rem", cursor: "pointer" }}
        >
          &times;
        </button>
        
        <h2 style={{ fontSize: "1.5rem", fontWeight: "bold", marginBottom: "24px" }}>
          {task ? "Edit Task" : "Create New Task"}
        </h2>
        
        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontSize: "0.9rem", color: "var(--text-secondary)" }}>Title</label>
            <input
              type="text"
              className="input-field"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              autoFocus
            />
          </div>
          
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontSize: "0.9rem", color: "var(--text-secondary)" }}>Description</label>
            <textarea
              className="input-field"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              style={{ resize: "vertical" }}
            />
          </div>
          
          <div>
            <label style={{ display: "block", marginBottom: "8px", fontSize: "0.9rem", color: "var(--text-secondary)" }}>Status</label>
            <select
              className="input-field"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              <option value="TODO">To Do</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="DONE">Done</option>
            </select>
          </div>
          
          <div style={{ display: "flex", gap: "12px", marginTop: "8px", justifyContent: "flex-end" }}>
            <button type="button" onClick={onClose} className="btn-secondary">Cancel</button>
            <button type="submit" className="btn-primary" style={{ width: "auto" }}>
              {task ? "Save Changes" : "Create Task"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
