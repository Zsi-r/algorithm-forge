# algorithm-forge

Daily algorithms, sharpening the brain.

每日一题，主打算法竞赛（洛谷 / LeetCode 等）

## 目录结构

```text
algorithm-forge/
├── templates/                 # 三语言竞赛模板，开新题直接复制
│   ├── cpp/template.cpp
│   ├── python/template.py
│   └── rust/template.rs
├── luogu/                     # 洛谷：P1226_quick_power
└── leetcode/                  # LeetCode：0001_two_sum
```

## 每题目录约定

```text
luogu/P1226_quick_power/
├── statement.md   # 题面：来源链接、描述、输入输出格式、样例
├── main.cpp       # C++
├── main.py        # Python
└── main.rs        # Rust
```

- 目录名：`题号_小写蛇形题目名`
- 三个语言版本均独立可运行（单文件、零外部依赖）

## 本地运行

```bash
# cpp
g++ -O2 -std=c++17 -o main main.cpp && ./main
# python
python3 main.py
# rust
rustc -O main.rs -o main && ./main
```

## References

- https://yb.tencent.com/s/gRnEbbi3pnFT