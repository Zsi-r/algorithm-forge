#!/usr/bin/env python3
"""Fetch a LeetCode (CN) problem and scaffold the solution directory.

Usage:
    python3 fetch_problem.py <number_or_slug> [--name <snake_name>] [--workspace <path>]

Examples:
    python3 fetch_problem.py 1                   # -> leetcode/0001_two_sum/
    python3 fetch_problem.py two-sum             # -> leetcode/0001_two_sum/
    python3 fetch_problem.py 1 --name two_sum    # override directory name
    python3 fetch_problem.py 1 --workspace /path/to/algorithm-forge

LeetCode 题目是函数/类题，不需要 main() 和 stdin/stdout。
脚本从 LeetCode API 直接拉取题目代码骨架（codeSnippets），包含正确的函数/类签名。

The script creates the following structure under <workspace>/leetcode/:
    0001_two_sum/
    ├── statement.md   # 题面（描述、示例）
    ├── main.cpp       # LeetCode 代码骨架（含类/函数签名）
    └── main.rs        # LeetCode 代码骨架
"""
import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

GRAPHQL_URL = "https://leetcode.cn/graphql/"
PROBLEMS_API = "https://leetcode.cn/api/problems/all/"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) algorithm-forge/1.0"

# LeetCode langSlug → 文件名 + 前缀
LANG_MAP = {
    "cpp":  ("main.cpp", "cpp"),
    "rust": ("main.rs", "rust"),
}


# ---------- HTTP helpers ----------

def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _post(url: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "User-Agent": UA,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------- Slug resolution ----------

def slug_from_number(number: int) -> str:
    """Map a frontend question ID to its title slug via the problems list API."""
    data = _get(PROBLEMS_API)
    for p in data.get("stat_status_pairs", []):
        if p["stat"]["frontend_question_id"] == number:
            return p["stat"]["question__title_slug"]
    raise ValueError(f"LeetCode problem #{number} not found")


# ---------- Problem fetch ----------

def fetch_problem(slug: str) -> dict:
    query = """
    query getQuestion($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
        titleSlug
        difficulty
        topicTags { name translatedName }
        content
        sampleTestCase
        exampleTestcases
        codeSnippets { lang langSlug code }
      }
    }
    """
    resp = _post(GRAPHQL_URL, {"query": query.strip(), "variables": {"titleSlug": slug}})
    q = (resp.get("data") or {}).get("question")
    if not q:
        raise ValueError(f"Problem '{slug}' not found on LeetCode CN")
    return q


# ---------- Text helpers ----------

def snake_case(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def html_to_markdown(html: str) -> str:
    """Lightweight HTML→markdown conversion for LeetCode content."""
    if not html:
        return ""
    # Decode HTML entities helper
    def _decode(text: str) -> str:
        for entity, char in [("&nbsp;", " "), ("&lt;", "<"), ("&gt;", ">"),
                             ("&amp;", "&"), ("&#39;", "'"), ("&quot;", '"')]:
            text = text.replace(entity, char)
        return text
    # Preserve code blocks first — strip inner tags & decode entities
    blocks = []
    def _save_block(m):
        inner = m.group(1).strip()
        inner = re.sub(r"<[^>]+>", "", inner)  # strip tags inside code
        inner = _decode(inner)
        blocks.append(inner)
        return f"\x00BLOCK{len(blocks) - 1}\x00"
    html = re.sub(r"<pre[^>]*>(.*?)</pre>", _save_block, html, flags=re.DOTALL | re.IGNORECASE)
    # Inline code
    html = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", html, flags=re.DOTALL | re.IGNORECASE)
    # Superscript / subscript (before stripping all tags)
    html = re.sub(r"<sup[^>]*>(.*?)</sup>", r"^\1", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<sub[^>]*>(.*?)</sub>", r"_\1", html, flags=re.DOTALL | re.IGNORECASE)
    # Bold / italic
    html = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", r"**\2**", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", r"*\2*", html, flags=re.DOTALL | re.IGNORECASE)
    # List items
    html = re.sub(r"<li[^>]*>", "\n- ", html, flags=re.IGNORECASE)
    # Block-level → newlines
    html = re.sub(r"</?(p|div|ul|ol|table|tr|td|th|h[1-6])[^>]*>", "\n", html, flags=re.IGNORECASE)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    # Strip remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Decode entities
    html = _decode(html)
    # Restore code blocks
    def _restore(m):
        return f"```\n{blocks[int(m.group(1))]}\n```"
    html = re.sub(r"\x00BLOCK(\d+)\x00", _restore, html)
    # Tidy whitespace
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()


# ---------- File builders ----------

def build_statement(q: dict) -> str:
    fid = q.get("questionFrontendId", "")
    title = q.get("title", "")
    slug = q.get("titleSlug", "")
    tags = [t.get("translatedName") or t.get("name", "") for t in q.get("topicTags", [])]
    lines = [
        f"# [{fid}. {title}](https://leetcode.cn/problems/{slug}/)",
        "",
        "- 来源：LeetCode",
        f"- 难度：{q.get('difficulty', '未知')}",
    ]
    if tags:
        lines.append(f"- 标签：{', '.join(tags)}")
    lines += ["", "## 题目描述", "", html_to_markdown(q.get("content") or ""), ""]
    # Examples
    examples = q.get("exampleTestcases") or q.get("sampleTestCase") or ""
    if examples:
        lines += ["## 示例", "", "```text", examples.strip(), "```", ""]
    return "\n".join(lines)


def build_code_file(lang_slug: str, snippet_code: str, url: str, header_title: str) -> str:
    """将 LeetCode 代码骨架包装成完整文件。

    LeetCode 题目是函数/类题，不需要 main() 和 stdin/stdout。
    代码骨架直接来自 LeetCode API，已含正确的类/函数签名。
    """
    snippet = snippet_code or ""
    if lang_slug == "cpp":
        prefix = (
            f"// {header_title}\n"
            f"// {url}\n"
            f"#include <bits/stdc++.h>\n"
            f"using namespace std;\n"
        )
        return prefix + snippet + "\n"
    elif lang_slug == "rust":
        prefix = (
            f"// {header_title}\n"
            f"// {url}\n"
        )
        return prefix + snippet + "\n"
    else:
        return snippet


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser(description="Fetch a LeetCode CN problem and scaffold the directory.")
    ap.add_argument("identifier", help="Problem number (e.g. 1) or title slug (e.g. two-sum)")
    ap.add_argument("--name", help="Override the snake_case directory name (e.g. two_sum)")
    ap.add_argument("--workspace", default=".", help="Workspace root (default: current directory)")
    args = ap.parse_args()

    ws = Path(args.workspace).resolve()

    # Resolve slug
    if args.identifier.isdigit():
        print(f"Looking up slug for LeetCode #{args.identifier} ...")
        try:
            slug = slug_from_number(int(args.identifier))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            print("Hint: provide the title slug directly, e.g. 'two-sum'.", file=sys.stderr)
            sys.exit(1)
    else:
        slug = args.identifier

    # Fetch
    print(f"Fetching LeetCode problem '{slug}' ...")
    try:
        q = fetch_problem(slug)
    except urllib.error.URLError as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)

    fid = q.get("questionFrontendId", "0")
    title = q.get("title", slug)
    url = f"https://leetcode.cn/problems/{q.get('titleSlug', slug)}/"

    # Directory name
    dir_name = args.name or snake_case(title)
    try:
        padded = f"{int(fid):04d}"
    except ValueError:
        padded = fid
    dir_name = f"{padded}_{dir_name}"

    problem_dir = ws / "leetcode" / dir_name
    if problem_dir.exists():
        print(f"Error: directory already exists → {problem_dir}", file=sys.stderr)
        sys.exit(1)

    # Build code snippets map: langSlug -> code
    snippets = {s["langSlug"]: s.get("code", "") for s in q.get("codeSnippets", []) or []}
    header = f"{fid}. {title}"

    # Create directory + files
    problem_dir.mkdir(parents=True)
    (problem_dir / "statement.md").write_text(build_statement(q), encoding="utf-8")

    created_files = ["statement.md"]
    for lang_slug, (filename, _) in LANG_MAP.items():
        code = snippets.get(lang_slug, "")
        if code:
            content = build_code_file(lang_slug, code, url, header)
            (problem_dir / filename).write_text(content, encoding="utf-8")
            created_files.append(filename)
        else:
            print(f"Warning: no {lang_slug} code snippet available, skipping {filename}", file=sys.stderr)

    print(f"\n✅ Created: {problem_dir}")
    for f in created_files:
        print(f"   {f}")


if __name__ == "__main__":
    main()
