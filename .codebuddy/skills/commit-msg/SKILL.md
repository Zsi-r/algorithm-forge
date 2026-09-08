---
name: commit-msg
description: 按项目约定快速生成 Git commit message 并完成提交。当用户要求"提交"、"commit"、"写 commit msg"、"快速 commit"时使用。规则：题目相关（leetcode/luogu/codeforces 等目录）的变更为 [YYYY-MM-DD] 平台: 子目录名 格式，其余变更为 feat: 前缀；两类混合时拆成多个 commit。
---

# Commit 信息生成器

## 概述

按项目约定为当前工作区变更生成 commit message 并完成提交，用户无需手动写信息。

## 提交信息规范

### 1. 题目相关变更

范围：`leetcode/`、`luogu/`、`codeforces/` 等 OJ 目录下新增/修改题目的变更。

格式：

```
[YYYY-MM-DD] 平台: 子目录名
```

- 日期：提交当天日期
- 平台：题目所属的一级目录名，全小写（`leetcode` / `luogu` / `codeforces` / `atcoder` 等）
- 子目录名：题目目录名原样保留，含题号前缀
  - `leetcode/0146_lru_cache/` → `[2026-09-09] leetcode: 0146_lru_cache`
  - `luogu/P1226_quick_power/` → `[2026-09-09] luogu: P1226_quick_power`

### 2. 工程类变更

题目目录之外的一切变更（模板、脚本、配置、文档、`.codebuddy/` 等）。

格式：

```
feat: 中文简述
```

- 一行概括本次变更，必要时附加多行 body 列出细节
- 默认用 `feat:`；用户明确指定其他前缀（`fix:` / `docs:` / `chore:`）时从其要求

## 工作流程

### 第一步：分析变更

```bash
git status --short
git diff --stat
```

将每个变更归类为"题目"或"工程"。`.gitignore` 已排除的文件（如 `.vscode/`）不会出现，无需关心。

### 第二步：拆分与暂存

- 两类混合时拆成多个 commit：先提交题目，再提交工程
- 同类变更默认合为一个 commit，除非用户要求按语义再拆

```bash
git add leetcode/0146_lru_cache/
git commit -m "[2026-09-09] leetcode: 0146_lru_cache"
git add -A
git commit -m "feat: xxx"
```

### 第三步：提炼工程类 msg

根据 diff 内容写一句话概括，变更较多时补 body：

```
feat: 重构三语言竞赛模板并完善工程化配置

- 新增 .clang-format 格式化配置
- 新增 rust-project 生成脚本
```

### 第四步：提交并汇报

依次执行提交，最后汇报每个 commit 的 hash、msg 及包含的文件概要。

> 注意：若变更中有大量删除或语义不明确的内容，先向用户展示拆分方案，确认后再提交。

## 示例

```
用户："帮我 commit"
→ git status 发现 leetcode/0146_lru_cache/（新题）和 templates/、.clang-format（工程）
→ commit 1: [2026-09-09] leetcode: 0146_lru_cache  （只含 leetcode/0146_lru_cache/）
→ commit 2: feat: 重构模板与工程化配置               （其余全部）

用户："写个 commit msg，只看 luogu 那道新题"
→ 只对 luogu/P1226_quick_power/ 生成：[2026-09-09] luogu: P1226_quick_power
```
