#!/usr/bin/env python3
"""Discover and run ten reproducible Python fill-in-the-middle tasks.

Run --dry-run first. Target repository remains read-only. Exercises use AST
source ranges; each task calls rag_completion_benchmark.py independently.
"""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

KINDS = ("assignment", "return", "call", "conditional", "exception", "function",
         "cross_file_return", "cross_file_call", "cross_file_condition", "cross_file_function")


def kind_and_span(node: ast.AST, lines: list[str]):
    if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.lineno == node.end_lineno:
        return "assignment", node.lineno, 1
    if isinstance(node, ast.Return) and node.value is not None and node.lineno == node.end_lineno:
        return "return", node.lineno, 1
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and node.lineno == node.end_lineno:
        return "call", node.lineno, 1
    if isinstance(node, ast.If) and node.body:
        last = node.body[0]
        if node.lineno + 1 == last.lineno and last.end_lineno == last.lineno:
            return "conditional", node.lineno, 2
    if isinstance(node, ast.ExceptHandler) and node.body and node.end_lineno is not None:
        # Avoid blank lines and multi-line handlers; include its first statement.
        first = node.body[0]
        if first.end_lineno == first.lineno and first.lineno == node.lineno + 1:
            return "exception", node.lineno, 2
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.end_lineno:
        length = node.end_lineno - node.lineno + 1
        if 2 <= length <= 6 and not node.decorator_list:
            return "function", node.lineno, length
    return None


def discover(repo: Path):
    candidates = {k: [] for k in KINDS[:6]}
    for path in sorted(repo.rglob("*.py")):
        if any(x in {".git", ".venv", "venv", "__pycache__", "benchmark-runs"} for x in path.relative_to(repo).parts):
            continue
        if path.stat().st_size > 120_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=str(path))
        except (UnicodeError, SyntaxError):
            continue
        lines = text.splitlines()
        imports = any(isinstance(x, (ast.Import, ast.ImportFrom)) for x in tree.body)
        for node in ast.walk(tree):
            if not hasattr(node, "lineno"):
                continue
            result = kind_and_span(node, lines)
            if not result:
                continue
            kind, line, count = result
            if line <= 2 or line + count > len(lines):
                continue
            if not lines[line - 1].strip() or not lines[line + count - 1].strip():
                continue
            rel = path.relative_to(repo).as_posix()
            candidates[kind].append({"kind": kind, "file": rel, "line": line, "lines": count, "has_imports": imports})
    selected = []
    used = set()
    for kind in KINDS:
        base = kind.replace("cross_file_", "")
        if base == "condition":
            base = "conditional"
        options = candidates[base]
        # Cross-file tasks prioritize source files with imports; the benchmark
        # does not assume that a cross-file dependency is truly required.
        if kind.startswith("cross_file_"):
            options = sorted(options, key=lambda x: (not x["has_imports"], x["file"], x["line"]))
        for candidate in options:
            key = (candidate["file"], candidate["line"], candidate["lines"])
            if key in used:
                continue
            used.add(key)
            selected.append({**candidate, "kind": kind})
            break
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--model", default="gemma4:e2b")
    parser.add_argument("--embed-model", default="embeddinggemma:300m-qat-q4_0")
    parser.add_argument("--out", type=Path, default=Path("benchmark-runs"))
    parser.add_argument("--modes", default="0,2,4", help="Comma-separated RAG top-k settings")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    repo = args.repo.expanduser().resolve()
    if not (repo / ".git").exists():
        parser.error("--repo must be a Git clone")
    modes = [int(x) for x in args.modes.split(",")]
    if not modes or any(x < 0 for x in modes) or args.limit < 1:
        parser.error("Invalid --modes or --limit")
    sha = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    tasks = discover(repo)[:args.limit]
    if len(tasks) < args.limit:
        print(f"WARNING: found only {len(tasks)} distinct tasks (requested {args.limit})", file=sys.stderr)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    batch = args.out / ("batch-" + stamp)
    manifest = {"commit": sha, "repo": str(repo), "model": args.model,
                "embed_model": args.embed_model, "modes": modes, "tasks": tasks}
    print(json.dumps(manifest, indent=2))
    if args.dry_run:
        return
    batch.mkdir(parents=True, exist_ok=False)
    (batch / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    script = Path(__file__).with_name("rag_completion_benchmark.py")
    results = []
    for n, task in enumerate(tasks, 1):
        for top_k in modes:
            cmd = [sys.executable, str(script), "--repo", str(repo),
                   "--file", task["file"], "--line", str(task["line"]), "--lines", str(task["lines"]),
                   "--top-k", str(top_k), "--model", args.model, "--embed-model", args.embed_model,
                   "--out", str(args.out)]
            print(f"\n[{n}/{len(tasks)}] {task['kind']} / top-k={top_k}", flush=True)
            process = subprocess.run(cmd, capture_output=True, text=True)
            entry = {"task": task, "top_k": top_k, "exit_code": process.returncode,
                     "stdout": process.stdout, "stderr": process.stderr}
            results.append(entry)
            (batch / "runs.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(process.stdout[-1500:] if process.returncode == 0 else process.stderr[-1500:])
    print(f"\nBatch results: {batch / 'runs.json'}")


if __name__ == "__main__":
    main()
