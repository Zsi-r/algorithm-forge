#!/usr/bin/env python3
"""从 LeetCode 热题 100 清单中随机挑选一道未完成的题目。

用法：
    python3 pick_random.py [--workspace <路径>] [--count N] [--seed <种子>]

流程：
    1. 解析 references/leetcode_hot_100.md，提取全部题目（题号、标题、slug、难度、专题）
    2. 扫描 leetcode/ 目录，以目录名前 4 位零填充题号判断哪些题已完成
    3. 从未完成的题目中随机挑选并输出
"""

import argparse
import random
import re
import sys
from pathlib import Path

# 题单文档相对路径
PROBLEMS_MD = Path("references/leetcode_hot_100.md")
# 题目目录相对路径
LEETCODE_DIR = Path("leetcode")

# 表格行：| 1 | [两数之和](https://leetcode.cn/problems/two-sum/) | 简单 |
ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*\[([^\]]+)\]\(https://leetcode\.cn/problems/([^/)]+)/?\)\s*\|\s*(简单|中等|困难)\s*\|"
)
# 专题标题：## 哈希（3 题）
TOPIC_RE = re.compile(r"^##\s+(.+?)（\d+\s*题）")
# 已建目录名前缀：4 位零填充题号，如 0146_lru_cache
DONE_DIR_RE = re.compile(r"^(\d{4})_")


def parse_problems(md_path: Path) -> list[dict]:
    """解析题单 markdown，返回题目列表。"""
    problems = []
    topic = ""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = TOPIC_RE.match(line)
        if m:
            topic = m.group(1).strip()
            continue
        m = ROW_RE.match(line)
        if m:
            num, title, slug, difficulty = m.groups()
            problems.append(
                {
                    "num": int(num),
                    "title": title.strip(),
                    "slug": slug.strip(),
                    "difficulty": difficulty,
                    "topic": topic,
                }
            )
    return problems


def done_numbers(workspace: Path) -> set[int]:
    """扫描 leetcode/ 目录，返回已完成的题号集合。"""
    done = set()
    lc_dir = workspace / LEETCODE_DIR
    if not lc_dir.is_dir():
        return done
    for child in lc_dir.iterdir():
        if not child.is_dir():
            continue
        m = DONE_DIR_RE.match(child.name)
        if m:
            done.add(int(m.group(1)))
    return done


def main() -> int:
    parser = argparse.ArgumentParser(description="随机挑选一道未完成的 Hot 100 题目")
    parser.add_argument("--workspace", default=".", help="工作区根路径（默认当前目录）")
    parser.add_argument("--count", type=int, default=1, help="随机挑选的题目数量（默认 1）")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（用于复现）")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    md_path = workspace / PROBLEMS_MD
    if not md_path.is_file():
        print(f"错误：找不到题单文件 {md_path}", file=sys.stderr)
        return 1

    problems = parse_problems(md_path)
    if not problems:
        print(f"错误：未能从 {md_path} 解析出任何题目", file=sys.stderr)
        return 1

    done = done_numbers(workspace)
    todo = [p for p in problems if p["num"] not in done]

    print(f"题单总数：{len(problems)}，已完成：{len(done)}，待完成：{len(todo)}")

    if not todo:
        print("🎉 热题 100 已全部完成！")
        return 0

    rng = random.Random(args.seed)
    picks = rng.sample(todo, min(args.count, len(todo)))

    for i, p in enumerate(picks, 1):
        print(f"\n--- 第 {i} 道 ---")
        print(f"题号：{p['num']}")
        print(f"标题：{p['title']}")
        print(f"slug：{p['slug']}")
        print(f"专题：{p['topic']}")
        print(f"难度：{p['difficulty']}")
        print(f"链接：https://leetcode.cn/problems/{p['slug']}/")

    return 0


if __name__ == "__main__":
    sys.exit(main())
