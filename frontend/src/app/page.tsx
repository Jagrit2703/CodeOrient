"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import Shell from "@/components/Shell";

export default function Home() {
  const router = useRouter();
  const [repoUrl, setRepoUrl] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!repoUrl.trim()) return;
    window.localStorage.setItem("co_repo_url", repoUrl.trim());
    router.push("/map");
  }

  return (
    <Shell>
      <div className="mx-auto max-w-xl">
        <h1 className="text-2xl font-semibold text-slate-900">Codebase Orientation</h1>
        <p className="mt-2 text-slate-500">
          Point this at a repo. Get an architecture map and a starter task list back.
        </p>
        <form onSubmit={handleSubmit} className="mt-6 flex gap-2">
          <input
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/org/repo or a local path"
            className="flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm"
          />
          <button
            type="submit"
            className="rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Analyze
          </button>
        </form>
      </div>
    </Shell>
  );
}
