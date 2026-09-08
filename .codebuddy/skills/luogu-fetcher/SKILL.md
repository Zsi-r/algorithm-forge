---
name: luogu-fetcher
description: 通过题目 ID 从洛谷拉取题目，并创建包含 statement.md 及 C++/Rust 两语言模板的解题目录。当用户想要拉取洛谷题目、开一道新的洛谷题目、或搭建洛谷题目目录骨架时，应使用此 skill。
---

# 洛格拉取器

## 概述

从洛谷拉取一道题目，在 `luogu/` 下按项目命名规范创建可直接开始编码的目录：`{题目ID}_{小写蛇形英文名}/`。每个题目目录包含 `statement.md`、`main.cpp`、`main.rs` 三个文件。

## 何时使用

当用户想要以下操作时触发此 skill：
- 拉取 / 抓取 / 导入一道洛谷题目
- 开一道新的洛谷题
- 创建洛谷题目目录骨架

典型用户用语："拉一道洛谷题"、"拉取 P1226"、"开一道洛谷题"、"fetch luogu P1001"。

## 目录约定

```
luogu/P1226_quick_power/
├── statement.md   # 题面：来源链接、背景、描述、输入输出格式、样例
├── main.cpp       # 从 templates/cpp/template.cpp 复制
└── main.rs        # 从 templates/rust/template.rs 复制
```

- 目录名：`{题目ID}_{小写蛇形英文名}`，如 `P1226_quick_power`、`B2001_hello_world`
- 洛谷题目标题为中文，需提供一个简短的英文蛇形名（如"快速幂"→ `quick_power`）
- 两语言文件均独立可运行、零外部依赖

## 工作流程

### 第一步：确定题目与英文名

确定以下两项：
1. **题目 ID** — 如 `P1226`、`B2001`、`P1001`
2. **英文蛇形名** — 将中文标题翻译为简短的英文 snake_case 名称（如"快速幂||取余运算"→ `quick_power`，"A+B Problem"→ `a_plus_b`）。该名称将作为目录名的一部分。

### 第二步：运行拉取脚本

```bash
python3 .codebuddy/skills/luogu-fetcher/scripts/fetch_problem.py <题目ID> <英文名>
```

可选参数：
- `--workspace <路径>` — 工作区根路径（默认为当前目录）

脚本执行步骤：
1. 从洛谷 content-only API 获取题目数据（`https://www.luogu.com.cn/problem/<题目ID>?_contentOnly=true`）
2. 创建 `luogu/{题目ID}_{蛇形名}/` 目录及全部文件
3. 从 `templates/` 复制两语言模板并添加题目头注释

### 第三步：验证与清理

脚本完成后：
1. 阅读 `statement.md` — 检查题目描述。洛谷 API 返回的是 markdown 格式内容，可能含 KaTeX 数学公式（`$...$`），通常可直接保留。
2. 两个 `main.*` 文件均为模板——可直接开始编码。

### 第四步：刷新 rust-analyzer 项目描述

新增了 `main.rs` 后需重新生成 `rust-project.json`，否则 rust-analyzer 无法识别新题目目录：

```bash
python3 scripts/gen_rust_project.py
```

### 降级方案

若脚本失败（网络问题、API 错误），降级为：
1. 用 `web_fetch` 访问 `https://www.luogu.com.cn/problem/<题目ID>` 获取题目内容
2. 按上述目录约定手动创建目录和文件
3. 从 `templates/cpp/template.cpp`、`templates/rust/template.rs` 复制模板

## 示例

```
用户："拉一道洛谷题 P1226"
→ 翻译标题"【模板】快速幂||取余运算"→ quick_power
→ 运行：python3 .codebuddy/skills/luogu-fetcher/scripts/fetch_problem.py P1226 quick_power
→ 创建：luogu/P1226_quick_power/

用户："开洛谷 B2001"
→ 翻译标题"A+B Problem"→ a_plus_b
→ 运行：python3 .codebuddy/skills/luogu-fetcher/scripts/fetch_problem.py B2001 a_plus_b
→ 创建：luogu/B2001_a_plus_b/
```
