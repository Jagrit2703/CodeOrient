import { Handle, Position } from "reactflow";
import { categoryColor } from "./catalog";

export default function MapNode({ data, selected }: { data: { label: string; type: string }; selected: boolean }) {
  const color = categoryColor(data.type);
  return (
    <div
      className="rounded-lg border-2 bg-white px-4 py-2 text-sm shadow-sm"
      style={{ borderColor: selected ? color : "#e2e8f0", minWidth: 170 }}
    >
      <Handle type="target" position={Position.Top} style={{ background: color }} />
      <div className="flex items-center gap-2">
        <span className="h-2 w-2 rounded-full" style={{ background: color }} />
        <span className="font-medium text-slate-800">{data.label}</span>
      </div>
      <p className="mt-0.5 text-xs text-slate-400">{data.type}</p>
      <Handle type="source" position={Position.Bottom} style={{ background: color }} />
    </div>
  );
}
