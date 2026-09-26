"""Clones a repo (or reads a local path) and detects candidate modules/services
for the architecture-map and starter-task pipelines to build on.
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST_FILES = {
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "Cargo.toml",
    "composer.json",
}

IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".next", "venv", ".venv", "dist", "build"}

CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".rb", ".rs", ".php"}


@dataclass
class ModuleInfo:
    name: str
    path: str
    files: list[str] = field(default_factory=list)


@dataclass
class RepoContext:
    repo_url: str
    local_path: Path
    modules: list[ModuleInfo]


def _is_local_path(repo_url: str) -> bool:
    return Path(repo_url).expanduser().exists()


def _clone(repo_url: str) -> Path:
    dest = Path(tempfile.mkdtemp(prefix="codebase-orientation-"))
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(dest)],
        check=True,
        capture_output=True,
        timeout=120,
    )
    return dest


def _walk_files(root: Path) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in CODE_EXTENSIONS:
            files.append(path)
    return files


def _detect_modules(root: Path) -> list[ModuleInfo]:
    candidates: dict[str, ModuleInfo] = {}

    for manifest in root.rglob("*"):
        if manifest.name in MANIFEST_FILES and not any(p in IGNORED_DIRS for p in manifest.parts):
            module_dir = manifest.parent
            rel = module_dir.relative_to(root)
            name = str(rel) if str(rel) != "." else root.name
            candidates[name] = ModuleInfo(name=name, path=str(module_dir))

    if not candidates:
        # No manifests found (e.g. a monolith without per-service package files) —
        # fall back to the top-level directories with the most code files.
        top_dirs: dict[str, int] = {}
        for f in _walk_files(root):
            rel = f.relative_to(root)
            top = rel.parts[0] if len(rel.parts) > 1 else "root"
            top_dirs[top] = top_dirs.get(top, 0) + 1
        for name, _ in sorted(top_dirs.items(), key=lambda kv: -kv[1])[:6]:
            module_path = root / name if name != "root" else root
            candidates[name] = ModuleInfo(name=name, path=str(module_path))

    for module in candidates.values():
        module_files = _walk_files(Path(module.path))
        module.files = [str(f.relative_to(root)) for f in module_files[:25]]

    return list(candidates.values())


def ingest_repo(repo_url: str) -> RepoContext:
    local_path = (
        Path(repo_url).expanduser().resolve() if _is_local_path(repo_url) else _clone(repo_url)
    )
    modules = _detect_modules(local_path)
    return RepoContext(repo_url=repo_url, local_path=local_path, modules=modules)
