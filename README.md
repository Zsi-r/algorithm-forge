# algorithm-forge

Daily algorithms, sharpening the brain.

每日一题，主打算法竞赛（洛谷 / Codeforces / AtCoder / LeetCode），每题用 C++ / Python / Rust 各实现一遍。

## 目录结构

```text
algorithm-forge/
├── templates/                 # 三语言竞赛模板，开新题直接复制
│   ├── cpp/template.cpp
│   ├── python/template.py
│   └── rust/template.rs
├── luogu/                     # 洛谷：P1226_quick_power
├── codeforces/                # Codeforces：CF1900A_cover_in_water
├── atcoder/                   # AtCoder：ABC365A_jump
└── leetcode/                  # LeetCode：0001_two_sum
```

## 每题目录约定

```text
luogu/P1226_quick_power/
├── statement.md   # 题面：来源链接、描述、输入输出格式、样例
├── solution.md    # 思路 / 复杂度 / 坑点，头部带 front-matter 元信息（source、tags…）
├── main.cpp       # C++
├── main.py        # Python
└── main.rs        # Rust
```

- 目录名：`题号_小写蛇形题目名`
- 三个语言版本均独立可运行（单文件、零外部依赖）

## 本地运行

```bash
g++ -O2 -std=c++17 -o main main.cpp && ./main
python3 main.py
rustc -O main.rs -o main && ./main
```

## 已完成

| 日期 | 题目 | 标签 |
| ---- | ---- | ---- |
| 2026-08-21 | [P1226 【模板】快速幂\|\|取余运算](luogu/P1226_quick_power/) | math, quick-pow |
