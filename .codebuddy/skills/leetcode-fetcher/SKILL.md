---
name: leetcode-fetcher
description: 通过题号或 slug 从 LeetCode（力扣中国）拉取题目，并创建包含 statement.md 及 C++/Rust 两语言代码骨架（直接从 LeetCode API 获取函数/类签名）的解题目录。LeetCode 是函数/类题，代码骨架不含 main() 和 I/O。当用户想要拉取 LeetCode 题目、开一道新的 LeetCode 题目、或搭建 LeetCode 题目目录骨架时，应使用此 skill。
---

# LeetCode 拉取器

## 概述

从 LeetCode（力扣中国）拉取一道题目，在 `leetcode/` 下按项目命名规范创建可直接开始编码的目录：`{4位零填充题号}_{小写蛇形英文标题}/`。每个题目目录包含 `statement.md`、`main.cpp`、`main.rs` 三个文件。

## 何时使用

当用户想要以下操作时触发此 skill：
- 拉取 / 抓取 / 导入一道 LeetCode 题目
- 开一道新的 LeetCode 题
- 创建 LeetCode 题目目录骨架

典型用户用语："拉一道 LC 题"、"拉取 LeetCode 1"、"开一道 LeetCode 题"、"fetch leetcode two-sum"。

## 目录约定

```
leetcode/0146_lru_cache/
├── statement.md   # 题面（中文）：来源链接、描述、示例
├── main.cpp       # LeetCode 代码骨架（含类/函数签名，无 main()）
└── main.rs        # LeetCode 代码骨架
```

- 目录名：`{4位零填充题号}_{小写蛇形英文标题}`，如 `0001_two_sum`、`0146_lru_cache`
- 代码骨架直接来自 LeetCode API 的 `codeSnippets`，已含正确的类/函数签名
- LeetCode 是函数/类题，不需要 `main()` 和 stdin/stdout，与洛谷/Codeforces 的竞赛模板不同
- **题面语言**：`statement.md` 一律使用中文。脚本优先取力扣官方中文翻译（`translatedTitle` / `translatedContent`），难度也输出中文（简单/中等/困难）；目录名仍用英文蛇形名

## 工作流程

### 第一步：确定题目

确定题目标识符——可以是**题号**（如 `1`、`53`）或 **title slug**（如 `two-sum`）。脚本两种都接受。

> 注意：题号→slug 的映射依赖 `leetcode.cn/api/problems/all/` 接口，该接口可能不稳定或限流。若题号查询失败，改用 slug 直接拉取更可靠。

### 第二步：运行拉取脚本

```bash
python3 .codebuddy/skills/leetcode-fetcher/scripts/fetch_problem.py <题号或slug>
```

可选参数：
- `--name <蛇形名>` — 覆盖自动生成的目录名（如 `--name two_sum`）
- `--workspace <路径>` — 工作区根路径（默认为当前目录）

脚本执行步骤：
1. 解析 slug（若传入题号，则通过题目列表 API 查找对应 slug）
2. 从 LeetCode 中国 GraphQL API 获取题目数据（含 `codeSnippets` 代码骨架）
3. 创建 `leetcode/{零填充题号}_{蛇形名}/` 目录及全部文件
4. 将 LeetCode 代码骨架写入 `main.cpp/rs`，添加头注释（题目名 + URL + 必要 include）

### 第三步：验证与清理

脚本完成后：
1. 阅读 `statement.md` — 检查题目描述是否渲染正确。LeetCode 内容为 HTML，脚本做了轻量 HTML→markdown 转换，可能需要少量手动清理。
2. **确保题面为中文**：脚本优先使用力扣官方中文翻译（`translatedTitle` / `translatedContent`）。若题目没有官方中文翻译（此时 statement.md 仍是英文），必须手动将题名、描述、示例、提示完整翻译成中文后再交付。
3. 两个 `main.*` 文件均为骨架——可直接开始编码。

### 第四步：刷新 rust-analyzer 项目描述

新增了 `main.rs` 后需重新生成 `rust-project.json`，否则 rust-analyzer 无法识别新题目目录：

```bash
python3 scripts/gen_rust_project.py
```

### 降级方案

若脚本失败（网络问题、API 限流），降级为：
1. 用 `web_fetch` 访问 `https://leetcode.cn/problems/<slug>/` 获取题目内容和代码骨架
2. 按上述目录约定手动创建目录和文件
3. 代码文件只放 LeetCode 提供的类/函数签名 + 头注释，不加 `main()` 和 I/O

## 示例

```
用户："拉一道 LeetCode 题，第 1 题"
→ 运行：python3 .codebuddy/skills/leetcode-fetcher/scripts/fetch_problem.py 1
→ 创建：leetcode/0001_two_sum/

用户："拉取 leetCode 的 longest-substring-without-repeating-characters"
→ 运行：python3 .codebuddy/skills/leetcode-fetcher/scripts/fetch_problem.py longest-substring-without-repeating-characters
→ 创建：leetcode/0003_longest_substring_without_repeating_characters/

用户："拉 LeetCode 的 LRU 缓存"
→ 运行：python3 .codebuddy/skills/leetcode-fetcher/scripts/fetch_problem.py lru-cache
→ 创建：leetcode/0146_lru_cache/
```
