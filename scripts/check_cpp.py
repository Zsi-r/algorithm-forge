#!/usr/bin/env python3
# LeetCode C++ 骨架编译验证脚本
# 骨架中 LeetCode 提供的结构体定义（ListNode/TreeNode 等）被包在块注释里，
# 本脚本将其临时解开到 /tmp 再用 g++ -fsyntax-only 做语法检查，不改动原文件。
# 用法：python3 scripts/check_cpp.py <main.cpp> [<main.cpp> ...]

import re
import subprocess
import sys
from pathlib import Path


def unfold_block_comments(src: str) -> str:
    """解开包含 struct/class 定义的块注释，其余块注释（如用法说明）保留。"""

    def _unfold(match: re.Match) -> str:
        body = match.group(1)
        if "struct" in body or "class" in body:
            lines = []
            for line in body.splitlines():
                stripped = line.strip()
                if stripped.startswith("*"):
                    lines.append(stripped[1:].strip())
            return "\n".join(lines)
        return match.group(0)

    return re.sub(r"/\*\*(.*?)\*/", _unfold, src, flags=re.S)


def check_file(path: Path) -> tuple[bool, str]:
    src = path.read_text(encoding="utf-8")
    tmp = Path("/tmp/leetcode_check") / (path.parent.name + ".cpp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(unfold_block_comments(src), encoding="utf-8")
    proc = subprocess.run(
        ["g++", "-std=c++17", "-fsyntax-only", "-Wall", str(tmp)],
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0, proc.stderr.strip()


def main() -> int:
    files = [Path(p) for p in sys.argv[1:]]
    if not files:
        print("用法：python3 scripts/check_cpp.py <main.cpp> [...]", file=sys.stderr)
        return 2
    failed: list[Path] = []
    for f in files:
        ok, err = check_file(f)
        status = "OK  " if ok else "FAIL"
        print(f"[{status}] {f}")
        if not ok:
            failed.append(f)
            print(err)
    print(f"\n共 {len(files)} 个文件，通过 {len(files) - len(failed)}，失败 {len(failed)}")
    if failed:
        print("失败列表：", ", ".join(str(f) for f in failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
