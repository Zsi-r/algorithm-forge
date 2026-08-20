#![allow(dead_code)]
// 竞赛 Rust 模板：零外部依赖，一次性读入 + 游标取数。
// 编译：rustc -O main.rs -o main
use std::io::{self, Read, Write};

// ---------- 常用工具（按需保留） ----------
fn qpow(mut b: i64, mut p: i64, m: i64) -> i64 {  // 快速幂
    let mut r = 1 % m;
    b %= m;
    while p > 0 {
        if p & 1 == 1 {
            r = r * b % m;
        }
        b = b * b % m;
        p >>= 1;
    }
    r
}

fn main() {
    // ---------- 读入 ----------
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut it = input.split_ascii_whitespace();

    // 示例：读入 n 与长度为 n 的数组
    // let n: usize = it.next().unwrap().parse().unwrap();
    // let a: Vec<i64> = (0..n).map(|_| it.next().unwrap().parse::<i64>().unwrap()).collect();

    // ---------- 输出 ----------
    let mut out = io::BufWriter::new(io::stdout().lock());
    // writeln!(out, "{}", ans).unwrap();
}
