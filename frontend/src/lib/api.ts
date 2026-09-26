import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
});

export type NodeType = "frontend" | "backend" | "database" | "external" | "service";

export interface GraphNode {
  id: string;
  label: string;
  type: NodeType;
  summary: string;
  key_files: string[];
}

export interface GraphEdge {
  source: string;
  target: string;
  type: string;
}

export interface ArchitectureMap {
  repo_url: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface StarterTask {
  title: string;
  description: string;
  difficulty: "easy" | "medium" | "hard";
  target_files: string[];
  why_this_teaches_the_system: string;
}

export interface StarterTaskList {
  repo_url: string;
  tasks: StarterTask[];
}

export async function analyzeRepo(repoUrl: string): Promise<ArchitectureMap> {
  const { data } = await api.post<ArchitectureMap>("/api/analyze", { repo_url: repoUrl });
  return data;
}

export async function fetchStarterTasks(repoUrl: string): Promise<StarterTaskList> {
  const { data } = await api.post<StarterTaskList>("/api/tasks", { repo_url: repoUrl });
  return data;
}
