#!/usr/bin/env python3
"""扫描仓库内所有独立 Rust 源文件，生成 rust-analyzer 的 rust-project.json。

本仓库是算法刷题仓库：每个题目目录含一个独立的 main.rs（无 Cargo.toml），
部分（如 LeetCode）只有类/函数骨架、无 main()，无法纳入 Cargo workspace。
改用 rust-project.json 让 rust-analyzer 逐文件做语义分析。

每次新增/删除题目后运行：
    python3 scripts/gen_rust_project.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 题目根目录（每个子目录视为一个独立 crate）
PROBLEM_DIRS = ["luogu", "leetcode", "codeforces"]
# 额外的独立源文件（模板等）
EXTRA_FILES = [ROOT / "templates" / "rust" / "template.rs"]

EDITION = "2021"


def find_rust_files():
    """收集所有需要分析的 .rs 文件。"""
    files = [f for f in EXTRA_FILES if f.exists()]
    for d in PROBLEM_DIRS:
        base = ROOT / d
        if base.is_dir():
            files.extend(sorted(base.glob("*/main.rs")))
    return files


def detect_target(path: Path) -> str:
    """含 fn main 视为可执行，否则视为库（LeetCode 类骨架无 main）。"""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return "bin" if "fn main" in text else "lib"


def crate_name(path: Path) -> str:
    """取目录名作为 crate 名，模板文件取文件名。"""
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 2 and parts[-1] == "main.rs":
        return parts[-2]
    return path.stem


def main():
    crates = []
    for f in find_rust_files():
        rel = f.relative_to(ROOT).as_posix()
        crates.append({
            "display_name": crate_name(f),
            "root_module": rel,
            "edition": EDITION,
            "cfg": [],
            "deps": [],
            "target": detect_target(f),
            "is_proc_macro": False,
        })
    # 按 root_module 排序，保证生成结果稳定
    crates.sort(key=lambda c: c["root_module"])

    # sysroot 留 null，由 rust-analyzer 自动探测，避免硬编码绝对路径
    project = {"sysroot": None, "crates": crates}

    out_path = ROOT / "rust-project.json"
    out_path.write_text(
        json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"已生成 {out_path.relative_to(ROOT)}：{len(crates)} 个 crate")
    for c in crates:
        print(f"  - {c['display_name']:<24} ({c['target']:<3}) <- {c['root_module']}")


if __name__ == "__main__":
    main()
