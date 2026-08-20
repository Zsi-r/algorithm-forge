#!/usr/bin/env python3
# P1226 【模板】快速幂||取余运算
# https://www.luogu.com.cn/problem/P1226
import sys


def qpow(b: int, p: int, k: int) -> int:
    r = 1 % k
    b %= k
    while p:
        if p & 1:
            r = r * b % k
        b = b * b % k
        p >>= 1
    return r


def main() -> None:
    b, p, k = map(int, sys.stdin.buffer.read().split())
    print(f"{b}^{p} mod {k}={qpow(b, p, k)}")


if __name__ == "__main__":
    main()
