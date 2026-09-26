"use client";

import { useEffect, useState } from "react";
import Shell from "@/components/Shell";
import { fetchStarterTasks, StarterTask } from "@/lib/api";

export default function TasksPage() {
  const [tasks, setTasks] = useState<StarterTask[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const repoUrl = window.localStorage.getItem("co_repo_url");
    if (!repoUrl) {
      setError("No repo selected yet — go back and analyze one.");
      setLoading(false);
      return;
    }
    fetchStarterTasks(repoUrl)
      .then((result) => setTasks(result.tasks))
      .catch((err) => setError(err?.response?.data?.detail ?? "Failed to generate tasks"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Shell>
      <h1 className="text-xl font-semibold text-slate-900">Starter Tasks</h1>
      {loading && <p className="mt-4 text-slate-500">Generating tasks…</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
      {!loading && !error && tasks.length === 0 && (
        <p className="mt-4 text-slate-500">No TODO/FIXME signals found in this repo yet.</p>
      )}
      <div className="mt-4 grid gap-3">
        {tasks.map((task, i) => (
          <div key={i} className="rounded-lg border border-slate-200 bg-white p-4">
            <div className="flex items-center justify-between">
              <h2 className="font-medium text-slate-800">{task.title}</h2>
              <span className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-500">{task.difficulty}</span>
            </div>
            <p className="mt-2 text-sm text-slate-600">{task.description}</p>
            <p className="mt-2 text-xs text-slate-400">{task.target_files.join(", ")}</p>
            <p className="mt-1 text-xs italic text-slate-400">{task.why_this_teaches_the_system}</p>
          </div>
        ))}
      </div>
    </Shell>
  );
}
