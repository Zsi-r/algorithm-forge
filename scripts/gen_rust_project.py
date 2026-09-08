#!/usr/bin/env python3
"""扫描仓库内所有独立 Rust 源文件，生成 rust-analyzer 的 rust-project.json。

本仓库是算法刷题仓库：每个题目目录含一个独立的 main.rs（无 Cargo.toml），
部分（如 LeetCode）只有类/函数骨架、无 main()，无法纳入 Cargo workspace。
改用 rust-project.json 让 rust-analyzer 逐文件做语义分析。

每次新增/删除题目后运行：
    python3 scripts/gen_rust_project.py
"""
import json
import subprocess
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


def crate_name(path: Path) -> str:
    """取目录名作为 crate 名，模板文件取文件名。"""
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if len(parts) >= 2 and parts[-1] == "main.rs":
        return parts[-2]
    return path.stem


def detect_sysroot():
    """探测 rustc sysroot 与 std 源码路径；sysroot 留 null 会导致 std 符号全部无法解析。"""
    sysroot = subprocess.run(
        ["rustc", "--print", "sysroot"], capture_output=True, text=True, check=True
    ).stdout.strip()
    sysroot_src = Path(sysroot) / "lib" / "rustlib" / "src" / "rust" / "library"
    return {
        "sysroot": sysroot,
        # rust-src 组件缺失时置 null，rust-analyzer 会降级为仅二进制分析
        "sysroot_src": str(sysroot_src) if sysroot_src.is_dir() else None,
    }


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
            # target 字段是平台三元组（如 x86_64-unknown-linux-gnu）而非 crate 类型，
            # 留 null 让 rust-analyzer 用默认宿主平台
            "target": None,
            "is_proc_macro": False,
        })
    # 按 root_module 排序，保证生成结果稳定
    crates.sort(key=lambda c: c["root_module"])

    # 显式写入 sysroot，避免自动探测失败导致 std 未解析
    sysroot = detect_sysroot()
    project = {**sysroot, "crates": crates}

    out_path = ROOT / "rust-project.json"
    out_path.write_text(
        json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"已生成 {out_path.relative_to(ROOT)}：{len(crates)} 个 crate")
    for c in crates:
        print(f"  - {c['display_name']:<24} <- {c['root_module']}")


if __name__ == "__main__":
    main()
