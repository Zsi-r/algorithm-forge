---
name: hot100-picker
description: 从 references/leetcode_hot_100.md（LeetCode 热题 100 题单）中随机挑选一道未完成的题目，并调用 leetcode-fetcher 拉取到 leetcode/ 目录。当用户说"随机来一道 Hot 100"、"随机刷道 LC 题"、"随机开一道没做过的 LeetCode 题"等时，应使用此 skill。
---

# Hot 100 随机选题器

## 概述

从 LeetCode 热题 100 题单中随机挑选一道**未完成**的题目，并拉取到 `leetcode/` 目录下，形成"随机抽题 → 建目录骨架"的一键流程。

- 题单来源：`references/leetcode_hot_100.md`（17 个专题、100 道题，含题号、标题、slug、难度）
- 完成判定：`leetcode/` 下存在以该题号（4 位零填充）开头的目录，如 `0146_lru_cache/`
- 拉取动作：复用 `leetcode-fetcher` skill 的脚本

## 何时使用

当用户想要以下操作时触发此 skill：

- 随机来一道 / 抽一道 Hot 100（热题 100）题目
- 随机刷一道没做过的 LeetCode 题
- 随机开一道 LeetCode 题

典型用户用语："随机来一道 hot 100"、"随机抽道 LC 题做做"、"来一道没做过的热题"。

## 工作流程

### 第一步：随机选题

```bash
python3 .codebuddy/skills/hot100-picker/scripts/pick_random.py
```

脚本输出：题单进度统计（总数 / 已完成 / 待完成）及随机选中题目的题号、标题、slug、专题、难度。

可选参数：

- `--workspace <路径>` — 工作区根路径（默认当前目录）
- `--count N` — 一次随机选 N 道（默认 1）
- `--seed <种子>` — 固定随机种子以复现结果

若脚本提示"已全部完成"，直接告知用户即可，流程结束。

### 第二步：拉取题目

用第一步输出的 **slug**（比题号更可靠）调用 leetcode-fetcher 的脚本：

```bash
python3 .codebuddy/skills/leetcode-fetcher/scripts/fetch_problem.py <slug>
```

这会在 `leetcode/{4位零填充题号}_{蛇形名}/` 下创建 `statement.md`、`main.cpp`、`main.rs`。详细约定与降级方案见 `leetcode-fetcher` skill。

### 第三步：收尾

1. 告知用户选中了哪道题（标题、专题、难度）及目录位置
2. 刷新 rust-analyzer 项目描述：

```bash
python3 scripts/gen_rust_project.py
```

## 示例

```
用户："随机来一道 hot 100"
→ 运行：python3 .codebuddy/skills/hot100-picker/scripts/pick_random.py
→ 输出：题号 11，slug container-with-most-water，专题 双指针，难度 中等
→ 运行：python3 .codebuddy/skills/leetcode-fetcher/scripts/fetch_problem.py container-with-most-water
→ 创建：leetcode/0011_container_with_most_water/
→ 运行：python3 scripts/gen_rust_project.py
```
