// 竞赛 C++ 模板
// 编译：g++ -O2 -std=c++17 -o main main.cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using ull = unsigned long long;
using ld = long double;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

#define rep(i, a, b) for (int i = (a); i < (b); ++i)
#define per(i, a, b) for (int i = (b) - 1; i >= (a); --i)
#define all(x) (x).begin(), (x).end()
#define sz(x) ((int)(x).size()))

// ---------- 常用工具（按需保留） ----------
ll qpow(ll b, ll p, ll mod) {  // 快速幂
    ll r = 1 % mod;
    for (b %= mod; p; p >>= 1, b = b * b % mod)
        if (p & 1) r = r * b % mod;
    return r;
}

// ---------- 解题区 ----------
void solve() {
    // 读入 + 核心逻辑 + 输出
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T = 1;
    // cin >> T;  // 多组测试数据时取消注释
    while (T--) solve();
    return 0;
}
