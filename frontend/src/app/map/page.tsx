"use client";

import { useEffect, useState } from "react";
import ReactFlow, { Background, Controls, Edge, Node } from "reactflow";
import "reactflow/dist/style.css";
import Shell from "@/components/Shell";
import MapNode from "@/components/map/MapNode";
import { analyzeRepo, ArchitectureMap, GraphNode } from "@/lib/api";

const nodeTypes = { module: MapNode };

export default function MapPage() {
  const [map, setMap] = useState<ArchitectureMap | null>(null);
  const [selected, setSelected] = useState<GraphNode | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const repoUrl = window.localStorage.getItem("co_repo_url");
    if (!repoUrl) {
      setError("No repo selected yet — go back and analyze one.");
      setLoading(false);
      return;
    }
    analyzeRepo(repoUrl)
      .then(setMap)
      .catch((err) => setError(err?.response?.data?.detail ?? "Failed to analyze repo"))
      .finally(() => setLoading(false));
  }, []);

  const nodes: Node[] = (map?.nodes ?? []).map((n, i) => ({
    id: n.id,
    type: "module",
    data: { label: n.label, type: n.type },
    position: { x: (i % 4) * 220, y: Math.floor(i / 4) * 140 },
  }));

  const edges: Edge[] = (map?.edges ?? []).map((e, i) => ({
    id: `${e.source}-${e.target}-${i}`,
    source: e.source,
    target: e.target,
  }));

  return (
    <Shell>
      <h1 className="text-xl font-semibold text-slate-900">Architecture &amp; Impact Map</h1>
      {loading && <p className="mt-4 text-slate-500">Analyzing repo…</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
      {map && (
        <div className="mt-4 flex gap-4">
          <div style={{ height: 560 }} className="flex-1 rounded-lg border border-slate-200 bg-white">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              onNodeClick={(_, node) => setSelected(map.nodes.find((n) => n.id === node.id) ?? null)}
              fitView
            >
              <Background />
              <Controls />
            </ReactFlow>
          </div>
          <div className="w-80 shrink-0 rounded-lg border border-slate-200 bg-white p-4">
            {selected ? (
              <>
                <h2 className="font-medium text-slate-800">{selected.label}</h2>
                <p className="mt-2 text-sm text-slate-600">{selected.summary}</p>
                <p className="mt-3 text-xs font-medium uppercase text-slate-400">Key files</p>
                <ul className="mt-1 space-y-1 text-xs text-slate-500">
                  {selected.key_files.map((f) => (
                    <li key={f}>{f}</li>
                  ))}
                </ul>
              </>
            ) : (
              <p className="text-sm text-slate-400">Click a node to see its summary.</p>
            )}
          </div>
        </div>
      )}
    </Shell>
  );
}
