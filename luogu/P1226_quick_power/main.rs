// P1226 【模板】快速幂||取余运算
// https://www.luogu.com.cn/problem/P1226
use std::io::{self, Read, Write};

fn qpow(mut b: i64, mut p: i64, k: i64) -> i64 {
    let mut r = 1 % k;
    b %= k;
    while p > 0 {
        if p & 1 == 1 {
            r = r * b % k;
        }
        b = b * b % k;
        p >>= 1;
    }
    r
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut it = input.split_ascii_whitespace();
    let b: i64 = it.next().unwrap().parse().unwrap();
    let p: i64 = it.next().unwrap().parse().unwrap();
    let k: i64 = it.next().unwrap().parse().unwrap();

    let mut out = io::BufWriter::new(io::stdout().lock());
    writeln!(out, "{}^{} mod {}={}", b, p, k, qpow(b, p, k)).unwrap();
}
