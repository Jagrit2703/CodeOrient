export interface ModuleType {
  key: "frontend" | "backend" | "database" | "external" | "service";
  label: string;
  color: string;
}

export const MODULE_TYPES: ModuleType[] = [
  { key: "frontend", label: "Frontend", color: "#2563eb" },
  { key: "backend", label: "Backend", color: "#7c3aed" },
  { key: "database", label: "Database", color: "#d97706" },
  { key: "external", label: "External", color: "#dc2626" },
  { key: "service", label: "Service", color: "#059669" },
];

export function categoryColor(type: string): string {
  return MODULE_TYPES.find((t) => t.key === type)?.color ?? "#64748b";
}
