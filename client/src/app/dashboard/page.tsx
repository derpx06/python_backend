"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import Navbar from "@/components/Navbar";
import TaskCard from "@/components/TaskCard";
import TaskModal from "@/components/TaskModal";
import Toast from "@/components/Toast";

export default function Dashboard() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  
  const [tasks, setTasks] = useState<any[]>([]);
  const [tasksLoading, setTasksLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<any | null>(null);
  
  const [toast, setToast] = useState<{message: string, type: 'success'|'error'} | null>(null);

  const fetchTasks = async () => {
    setTasksLoading(true);
    try {
      const res = await api.get("/api/v1/tasks");
      setTasks(res.data.data.tasks);
    } catch (err) {
      showToast("Failed to fetch tasks", "error");
    } finally {
      setTasksLoading(false);
    }
  };

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    } else if (user) {
      fetchTasks();
    }
  }, [user, isLoading, router]);

  const showToast = (message: string, type: 'success'|'error') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleCreate = async (data: any) => {
    try {
      await api.post("/api/v1/tasks", data);
      showToast("Task created successfully", "success");
      fetchTasks();
      setIsModalOpen(false);
    } catch (err) {
      showToast("Failed to create task", "error");
    }
  };

  const handleUpdate = async (id: number, data: any) => {
    try {
      await api.put(`/api/v1/tasks/${id}`, data);
      showToast("Task updated successfully", "success");
      fetchTasks();
      setIsModalOpen(false);
      setEditingTask(null);
    } catch (err) {
      showToast("Failed to update task", "error");
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    try {
      await api.delete(`/api/v1/tasks/${id}`);
      showToast("Task deleted successfully", "success");
      fetchTasks();
    } catch (err) {
      showToast("Failed to delete task", "error");
    }
  };

  const openEditModal = (task: any) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  if (isLoading || !user) return null;

  return (
    <div>
      <Navbar />
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
      
      <main style={{ maxWidth: "1200px", margin: "0 auto", padding: "32px 16px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "32px" }}>
          <div>
            <h1 style={{ fontSize: "2rem", fontWeight: "bold" }}>Your Tasks</h1>
            <p style={{ color: "var(--text-secondary)" }}>Manage and organize your work</p>
          </div>
          <button 
            className="btn-primary" 
            style={{ width: "auto" }}
            onClick={() => { setEditingTask(null); setIsModalOpen(true); }}
          >
            + New Task
          </button>
        </div>

        {tasksLoading ? (
          <p style={{ textAlign: "center", color: "var(--text-secondary)", marginTop: "64px" }}>Loading tasks...</p>
        ) : tasks.length === 0 ? (
          <div className="glass" style={{ padding: "64px 32px", textAlign: "center", borderRadius: "16px" }}>
            <h3 style={{ fontSize: "1.2rem", marginBottom: "8px" }}>No tasks found</h3>
            <p style={{ color: "var(--text-secondary)", marginBottom: "24px" }}>Create your first task to get started.</p>
            <button className="btn-secondary" onClick={() => { setEditingTask(null); setIsModalOpen(true); }}>Create Task</button>
          </div>
        ) : (
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))", gap: "24px" }}>
            {tasks.map((task) => (
              <TaskCard 
                key={task.id} 
                task={task} 
                onEdit={() => openEditModal(task)} 
                onDelete={() => handleDelete(task.id)} 
              />
            ))}
          </div>
        )}
      </main>

      {isModalOpen && (
        <TaskModal 
          task={editingTask} 
          onClose={() => { setIsModalOpen(false); setEditingTask(null); }} 
          onSubmit={(data) => editingTask ? handleUpdate(editingTask.id, data) : handleCreate(data)} 
        />
      )}
    </div>
  );
}
