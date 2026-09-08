#!/usr/bin/env python3
"""Fetch a Luogu problem and scaffold the solution directory.

Usage:
    python3 fetch_problem.py <problem_id> <english_name> [--workspace <path>]

Examples:
    python3 fetch_problem.py P1226 quick_power            # -> luogu/P1226_quick_power/
    python3 fetch_problem.py B2001 hello_world            # -> luogu/B2001_hello_world/
    python3 fetch_problem.py P1001 --workspace /path      # -> luogu/P1001/ (name fallback)

The script creates the following structure under <workspace>/luogu/:
    P1226_quick_power/
    ├── statement.md   # problem statement (background, description, I/O, samples)
    ├── main.cpp       # copied from templates/cpp/template.cpp
    └── main.rs        # copied from templates/rust/template.rs
"""
import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_BASE = "https://www.luogu.com.cn/problem/{pid}?_contentOnly=true"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) algorithm-forge/1.0"

DIFF_MAP = {
    1: "暂无评定", 2: "入门", 3: "普及-", 4: "普及/提高-",
    5: "普及+/提高", 6: "提高+/省选-", 7: "省选/NOI-", 8: "NOI/NOI+/CTSC",
}


# ---------- HTTP ----------

def fetch_problem(pid: str) -> dict:
    url = API_BASE.format(pid=pid)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("code") != 200:
        raise ValueError(f"Luogu API error: {data.get('currentData', 'unknown')}")
    problem = (data.get("currentData") or {}).get("problem")
    if not problem:
        raise ValueError(f"Problem {pid} not found on Luogu")
    return problem


# ---------- Helpers ----------

def snake_case(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def luogu_md(text: str) -> str:
    """Light cleanup of Luogu markdown (strip KaTeX wrappers, trim)."""
    if not text:
        return ""
    # Remove empty paragraphs / excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------- File builders ----------

def build_statement(p: dict) -> str:
    pid = p.get("pid", "")
    title = p.get("title", "")
    diff = DIFF_MAP.get(p.get("difficulty", 0), "未知")
    tags_raw = p.get("tags", [])
    # tags may be list of ints (IDs) or dicts; show what we have
    if tags_raw and isinstance(tags_raw[0], dict):
        tags = [t.get("title", str(t.get("id", ""))) for t in tags_raw]
    else:
        tags = [str(t) for t in tags_raw]

    lines = [
        f"# [{pid} {title}](https://www.luogu.com.cn/problem/{pid})",
        "",
        "- 来源：洛谷",
        f"- 难度：{diff}",
    ]
    if tags:
        lines.append(f"- 标签：{', '.join(tags)}")
    lines.append("")

    background = luogu_md(p.get("background", ""))
    if background:
        lines += ["## 题目背景", "", background, ""]

    desc = luogu_md(p.get("description", ""))
    lines += ["## 题目描述", "", desc, ""]

    inp = luogu_md(p.get("inputFormat", ""))
    lines += ["## 输入格式", "", inp, ""]

    out = luogu_md(p.get("outputFormat", ""))
    lines += ["## 输出格式", "", out, ""]

    samples = p.get("samples", [])
    if samples:
        lines.append("## 样例")
        for i, (s_in, s_out) in enumerate(samples, 1):
            lines += [f"### 样例 {i}", "", "输入：", "", "```text", s_in.strip(), "```", ""]
            lines += ["输出：", "", "```text", s_out.strip(), "```", ""]

    hint = luogu_md(p.get("hint", ""))
    if hint:
        lines += ["## 提示", "", hint, ""]

    return "\n".join(lines)


def copy_template(template: Path, dest: Path, url: str, header_title: str):
    content = template.read_text(encoding="utf-8")
    prefix = f"// {header_title}\n// {url}\n"
    dest.write_text(prefix + content, encoding="utf-8")


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="Fetch a Luogu problem and scaffold the directory.")
    ap.add_argument("pid", help="Problem ID, e.g. P1226, B2001")
    ap.add_argument("name", nargs="?", default="", help="English snake_case name, e.g. quick_power")
    ap.add_argument("--workspace", default=".", help="Workspace root (default: current directory)")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()

    print(f"Fetching Luogu problem {args.pid} ...")
    try:
        p = fetch_problem(args.pid)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    pid = p.get("pid", args.pid)
    title = p.get("title", "")
    url = f"https://www.luogu.com.cn/problem/{pid}"

    # Directory name
    if args.name:
        dir_name = f"{pid}_{snake_case(args.name)}"
    else:
        # Fallback: use PID only (SKILL.md recommends always providing a name)
        dir_name = pid
        print(f"Warning: no English name provided, using '{dir_name}' as directory name.", file=sys.stderr)
        print("Hint: pass an English name, e.g.  python3 fetch_problem.py {pid} quick_power", file=sys.stderr)

    problem_dir = ws / "luogu" / dir_name
    if problem_dir.exists():
        print(f"Error: directory already exists → {problem_dir}", file=sys.stderr)
        sys.exit(1)

    # Templates
    templates = ws / "templates"
    tpl_files = {
        "main.cpp": templates / "cpp" / "template.cpp",
        "main.rs": templates / "rust" / "template.rs",
    }
    missing = [name for name, path in tpl_files.items() if not path.exists()]
    if missing:
        print(f"Warning: missing template files: {', '.join(missing)}", file=sys.stderr)

    # Create directory + files
    problem_dir.mkdir(parents=True)
    (problem_dir / "statement.md").write_text(build_statement(p), encoding="utf-8")
    header = f"{pid} {title}"
    for name, tpl in tpl_files.items():
        if tpl.exists():
            copy_template(tpl, problem_dir / name, url, header)

    print(f"\n✅ Created: {problem_dir}")
    for f in ["statement.md", "main.cpp", "main.rs"]:
        print(f"   {f}")


if __name__ == "__main__":
    main()
