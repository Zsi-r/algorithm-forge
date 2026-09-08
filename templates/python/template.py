#!/usr/bin/env python3
"""竞赛 Python 模板（综合版）：一次性读入全部输入，游标取数。
运行：python3 main.py
按需保留所需模块，删除不需要的部分。
"""
import sys
from math import comb, gcd, isqrt, lcm  # 标准库自带

# ==================== 常量 ====================
INF = 10 ** 18
MOD = 10 ** 9 + 7


# ==================== 数学 ====================

def qpow(b: int, p: int, mod: int = MOD) -> int:
    """快速幂"""
    r = 1 % mod
    b %= mod
    while p:
        if p & 1:
            r = r * b % mod
        b = b * b % mod
        p >>= 1
    return r


def exgcd(a: int, b: int) -> tuple[int, int, int]:
    """扩展欧几里得：返回 (g, x, y) 使得 a*x + b*y = g = gcd(a,b)"""
    if b == 0:
        return a, 1, 0
    g, x, y = exgcd(b, a % b)
    return g, y, x - (a // b) * y


def mod_inv(a: int, mod: int = MOD) -> int:
    """模逆元（要求 gcd(a, mod) = 1）"""
    g, x, _ = exgcd(a, mod)
    assert g == 1, "逆元不存在"
    return (x % mod + mod) % mod


# ==================== 数据结构 ====================

class DSU:
    """并查集（路径压缩 + 按秩合并）"""
    def __init__(self, n: int):
        self.p = list(range(n + 1))
        self.r = [0] * (n + 1)

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def unite(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.r[a] < self.r[b]:
            a, b = b, a
        self.p[b] = a
        if self.r[a] == self.r[b]:
            self.r[a] += 1
        return True


class BIT:
    """树状数组（单点更新 + 前缀查询），1-indexed"""
    def __init__(self, n: int):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i: int, v: int) -> None:
        while i <= self.n:
            self.t[i] += v
            i += i & -i

    def sum(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        return self.sum(r) - self.sum(l - 1)


# ==================== 字符串 ====================

def kmp_fail(s: str) -> list[int]:
    """KMP 失败函数"""
    n = len(s)
    f = [0] * n
    j = 0
    for i in range(1, n):
        while j and s[i] != s[j]:
            j = f[j - 1]
        if s[i] == s[j]:
            j += 1
        f[i] = j
    return f


# ==================== 其他 ====================

def compress(a: list[int]) -> list[int]:
    """坐标压缩，返回 1-indexed 压缩后的值"""
    b = sorted(set(a))
    return [bisect_left(b, x) + 1 for x in a]


def bs_first(lo: int, hi: int, check) -> int:
    """整数二分：找第一个满足 check 的值"""
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ==================== 主函数 ====================

def main() -> None:
    data = sys.stdin.buffer.read().split()
    pos = 0

    def ni() -> int:
        nonlocal pos
        v = int(data[pos])
        pos += 1
        return v

    # n = ni()
    # a = [ni() for _ in range(n)]

    # 输出：能攒则攒，一次性写出
    # sys.stdout.write("\n".join(map(str, ans)) + "\n")


if __name__ == "__main__":
    from bisect import bisect_left  # compress 用
    sys.setrecursionlimit(1_000_000)  # 递归题必开
    main()
