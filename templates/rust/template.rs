#![allow(dead_code, non_snake_case, non_camel_case_types)]
// 竞赛 Rust 模板（综合版）：零外部依赖，一次性读入 + 游标取数。
// 编译：rustc -O main.rs -o main
// 按需保留所需模块，删除不需要的部分。
use std::io::{self, Read, Write};

// ==================== 数学 ====================

fn gcd(mut a: i64, mut b: i64) -> i64 { while b != 0 { let t = a % b; a = b; b = t; } a }
fn lcm(a: i64, b: i64) -> i64 { a / gcd(a, b) * b }

fn qpow(mut b: i64, mut p: i64, m: i64) -> i64 {
    let mut r = 1 % m;
    b %= m;
    while p > 0 {
        if p & 1 == 1 { r = r * b % m; }
        b = b * b % m;
        p >>= 1;
    }
    r
}

// 扩展欧几里得：返回 (g, x, y)，a*x + b*y = g
fn exgcd(a: i64, b: i64) -> (i64, i64, i64) {
    if b == 0 { return (a, 1, 0); }
    let (g, x, y) = exgcd(b, a % b);
    (g, y, x - (a / b) * y)
}

fn mod_inv(a: i64, m: i64) -> i64 {
    let (_, x, _) = exgcd(a, m);
    ((x % m) + m) % m
}

// ==================== 数据结构 ====================

// 并查集（路径压缩 + 按秩合并）
struct DSU { p: Vec<usize>, r: Vec<u32> }
impl DSU {
    fn new(n: usize) -> Self { Self { p: (0..=n).collect(), r: vec![0; n + 1] } }
    fn find(&mut self, x: usize) -> usize {
        if self.p[x] != x { self.p[x] = self.find(self.p[x]); }
        self.p[x]
    }
    fn unite(&mut self, a: usize, b: usize) -> bool {
        let (a, b) = (self.find(a), self.find(b));
        if a == b { return false; }
        if self.r[a] < self.r[b] { self.p[a] = b; } else {
            self.p[b] = a;
            if self.r[a] == self.r[b] { self.r[a] += 1; }
        }
        true
    }
}

// 树状数组（单点更新 + 前缀查询），1-indexed
struct BIT { n: usize, t: Vec<i64> }
impl BIT {
    fn new(n: usize) -> Self { Self { n, t: vec![0; n + 1] } }
    fn add(&mut self, mut i: usize, v: i64) {
        while i <= self.n { self.t[i] += v; i += i & (!i + 1); }
    }
    fn sum(&self, mut i: usize) -> i64 {
        let mut s = 0; while i > 0 { s += self.t[i]; i -= i & (!i + 1); } s
    }
    fn range_sum(&self, l: usize, r: usize) -> i64 { self.sum(r) - self.sum(l - 1) }
}

// ==================== 字符串 ====================

// KMP 失败函数
fn kmp_fail(s: &[u8]) -> Vec<usize> {
    let n = s.len(); let mut f = vec![0; n];
    let mut j = 0;
    for i in 1..n {
        while j > 0 && s[i] != s[j] { j = f[j - 1]; }
        if s[i] == s[j] { j += 1; }
        f[i] = j;
    }
    f
}

// ==================== 其他 ====================

// 坐标压缩（返回 1-indexed）
fn compress(mut a: Vec<i64>) -> Vec<i64> {
    let mut b = a.clone(); b.sort(); b.dedup();
    for x in a.iter_mut() { *x = b.binary_search(x).unwrap() as i64 + 1; }
    a
}

// ==================== 主函数 ====================

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut it = input.split_ascii_whitespace();

    // 示例读入
    // let n: usize = it.next().unwrap().parse().unwrap();
    // let a: Vec<i64> = (0..n).map(|_| it.next().unwrap().parse::<i64>().unwrap()).collect();

    let mut out = io::BufWriter::new(io::stdout().lock());
    // writeln!(out, "{}", ans).unwrap();
}
