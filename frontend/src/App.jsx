import React, { useEffect, useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "/api";

function getClientId() {
  const key = "midra_client_id";
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const id = crypto.randomUUID();
  localStorage.setItem(key, id);
  return id;
}

async function api(path, options = {}) {
  const cid = getClientId();
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Midra-Client-Id": cid,
      ...(options.headers || {}),
    },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();
  return res;
}

export function App() {
  const [prompt, setPrompt] = useState("");
  const [tasks, setTasks] = useState([]);
  const [runtime, setRuntime] = useState({ busy: false, quota: { count: 0, limit: 100, remaining: 100 } });
  const [error, setError] = useState("");
  const clientId = useMemo(() => getClientId(), []);

  async function refresh() {
    try {
      const [rt, t] = await Promise.all([api("/runtime"), api("/tasks")]);
      setRuntime(rt);
      setTasks(t.tasks || []);
      setError("");
    } catch (e) {
      setError(String(e.message || e));
    }
  }

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 2000);
    return () => clearInterval(id);
  }, []);

  const runningTask = useMemo(() => tasks.find((t) => t.status === "running"), [tasks]);

  function fmtTime(v) {
    if (!v) return "-";
    const d = new Date(v);
    if (Number.isNaN(d.getTime())) return String(v);
    return d.toLocaleString();
  }

  function artifactHref(taskId, ext) {
    return `${API_BASE}/tasks/${taskId}/download/${ext}?client_id=${encodeURIComponent(clientId)}`;
  }

  async function submitTask(e) {
    e.preventDefault();
    if (!prompt.trim()) return;
    try {
      await api("/tasks", { method: "POST", body: JSON.stringify({ prompt: prompt.trim() }) });
      setPrompt("");
      refresh();
    } catch (e2) {
      setError(String(e2.message || e2));
    }
  }

  async function retryTask(taskId) {
    try {
      await api(`/tasks/${taskId}/retry`, { method: "POST", body: "{}" });
      refresh();
    } catch (e) {
      setError(String(e.message || e));
    }
  }

  return (
    <div className="page">
      <header className="card">
        <h1>Midra</h1>
        <p className="hero-subtitle">Agentic prompt-to-MIDI composition for editable, controllable music workflows.</p>
      </header>

      <section className="card">
        <h2>Runtime</h2>
        <div className="runtime-grid">
          <div>
            <p className="label">Global status</p>
            <p className="value">{runtime.busy ? "Busy" : "Idle"}</p>
            <p>Stage: {runtime.stage_index ?? 0}/{runtime.stage_total ?? 9} · {runtime.stage_name ?? "idle"}</p>
            <p>Substage (tracks): {runtime.track_completed ?? 0}/{runtime.track_total ?? 0}</p>
          </div>
          <div>
            <p className="label">Daily quota</p>
            <p className="value">{runtime.quota?.count ?? 0}/{runtime.quota?.limit ?? 100}</p>
            <p>Remaining: {runtime.quota?.remaining ?? 0}</p>
          </div>
        </div>
      </section>

      <section className="card">
        <h2>Create Task</h2>
        <form onSubmit={submitTask}>
          <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Describe your music prompt..." />
          <button type="submit" disabled={!!runningTask}>Generate</button>
        </form>
        {error ? <pre className="error">{error}</pre> : null}
      </section>

      <section className="card">
        <h2>My Tasks</h2>
        <div className="stack">
          {tasks.map((t) => (
            <article className="task" key={t.id}>
              <div className="task-head">
                <h3>{t.id.slice(0, 8)}…</h3>
                <span className={`badge badge-${t.status}`}>{t.status}</span>
              </div>
              <p className="label">Prompt</p>
              <p className="prompt-text">{t.prompt || "-"}</p>
              <p>Created: {fmtTime(t.created_at)}</p>
              <p>Updated: {fmtTime(t.updated_at)}</p>
              <p>Stage: {t.stage_index}/{t.stage_total} · {t.stage_name}</p>
              <p>Track substage: {t.track_completed}/{t.track_total}</p>
              {t.status === "failed" ? <button onClick={() => retryTask(t.id)}>Retry</button> : null}
              {t.status === "succeeded" ? (
                <div className="downloads">
                  <audio controls src={artifactHref(t.id, "mp3")} />
                  <div className="download-actions">
                    <a href={artifactHref(t.id, "mid")} target="_blank" rel="noreferrer">
                      Download MID
                    </a>
                    <a href={artifactHref(t.id, "wav")} target="_blank" rel="noreferrer">
                      Download WAV
                    </a>
                    <a href={artifactHref(t.id, "mp3")} target="_blank" rel="noreferrer">
                      Download MP3
                    </a>
                  </div>
                </div>
              ) : null}
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
