#!/usr/bin/env python3
"""竞赛 Python 模板：一次性读入全部输入，游标取数（读入最快）。
运行：python3 main.py
"""
import sys
from math import comb, gcd, isqrt, lcm  # 常用数学函数，按需使用


def qpow(b: int, p: int, mod: int) -> int:  # 快速幂
    r = 1 % mod
    b %= mod
    while p:
        if p & 1:
            r = r * b % mod
        b = b * b % mod
        p >>= 1
    return r


def main() -> None:
    data = sys.stdin.buffer.read().split()
    pos = 0

    def next_i() -> int:
        nonlocal pos
        v = int(data[pos])
        pos += 1
        return v

    # n = next_i()
    # a = [next_i() for _ in range(n)]

    # 输出：能攒则攒，一次性写出
    # sys.stdout.write("\n".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    sys.setrecursionlimit(1_000_000)  # 递归题必开
    main()
