// 竞赛 C++ 模板（综合版）
// 编译：g++ -O2 -std=c++17 -o main main.cpp
// 用法：按需保留所需模块，删除不需要的部分
#include <bits/stdc++.h>
using namespace std;

// ==================== 类型别名 ====================
using ll = long long;
using ull = unsigned long long;
using ld = long double;
using pii = pair<int, int>;
using pll = pair<ll, ll>;
using vi = vector<int>;
using vll = vector<ll>;
using vpii = vector<pii>;

// ==================== 宏 ====================
#define rep(i, a, b)  for (int i = (a); i < (b); ++i)
#define per(i, a, b)  for (int i = (b) - 1; i >= (a); --i)
#define all(x)        (x).begin(), (x).end()
#define sz(x)         ((int)(x).size())
#define pb            push_back
#define eb            emplace_back
#define mp            make_pair
#define fi            first
#define se            second

// ==================== 常量 ====================
constexpr int  INF  = 1e9 + 7;
constexpr ll   LINF = 1e18 + 7;
constexpr int  MOD  = 1e9 + 7;
constexpr double EPS = 1e-9;

// ==================== 数学 ====================

template<class T> T gcd(T a, T b) { return b ? gcd(b, a % b) : a; }
template<class T> T lcm(T a, T b) { return a / gcd(a, b) * b; }

// 快速幂
ll qpow(ll b, ll p, ll mod = MOD) {
    ll r = 1 % mod;
    for (b %= mod; p; p >>= 1, b = b * b % mod)
        if (p & 1) r = r * b % mod;
    return r;
}

// 扩展欧几里得：求 ax + by = gcd(a,b)，返回 gcd，x/y 为一组解
ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (!b) { x = 1; y = 0; return a; }
    ll d = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return d;
}

// 模逆元（mod 互质）
ll inv(ll a, ll mod = MOD) {
    ll x, y; exgcd(a, mod, x, y);
    return (x % mod + mod) % mod;
}

// 组合计数（预处理阶乘 + 逆元）
const int N = 2e5 + 10;
ll fact[N], invfact[N];
void init_c(int n, ll mod = MOD) {
    fact[0] = 1;
    rep(i, 1, n + 1) fact[i] = fact[i - 1] * i % mod;
    invfact[n] = qpow(fact[n], mod - 2, mod);
    per(i, 0, n) invfact[i] = invfact[i + 1] * (i + 1) % mod;
}
ll C(int n, int k, ll mod = MOD) {
    if (k < 0 || k > n) return 0;
    return fact[n] * invfact[k] % mod * invfact[n - k] % mod;
}

// 线性筛（欧拉筛）
vi primes;
bool is_comp[N];
void sieve(int n) {
    rep(i, 2, n + 1) {
        if (!is_comp[i]) primes.pb(i);
        for (int p : primes) {
            if (i * p > n) break;
            is_comp[i * p] = true;
            if (i % p == 0) break;
        }
    }
}

// ==================== 数据结构 ====================

// 并查集（路径压缩 + 按秩合并）
struct DSU {
    vi p, r;
    DSU(int n) : p(n + 1), r(n + 1) { iota(all(p), 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (r[a] < r[b]) swap(a, b);
        p[b] = a;
        if (r[a] == r[b]) ++r[a];
        return true;
    }
};

// 树状数组（单点更新 + 前缀查询）
struct BIT {
    vll t; int n;
    BIT(int n) : t(n + 1), n(n) {}
    void add(int i, ll v) { for (; i <= n; i += i & -i) t[i] += v; }
    ll   sum(int i) { ll s = 0; for (; i > 0; i -= i & -i) s += t[i]; return s; }
    ll   sum(int l, int r) { return sum(r) - sum(l - 1); }
};

// 线段树（区间更新 + 区间查询，懒标记）
struct SegTree {
    int n; vll tag, sum;
    SegTree(int n) : n(n), tag(n << 2), sum(n << 2) {}
    void push_down(int o, int len) {
        if (tag[o]) {
            tag[o*2] += tag[o]; tag[o*2+1] += tag[o];
            sum[o*2] += tag[o] * (len - len/2);
            sum[o*2+1] += tag[o] * (len/2);
            tag[o] = 0;
        }
    }
    void _add(int o, int l, int r, int ql, int qr, ll v) {
        if (ql <= l && r <= qr) { sum[o] += v * (r-l+1); tag[o] += v; return; }
        push_down(o, r-l+1);
        int m = (l+r) >> 1;
        if (ql <= m) _add(o*2, l, m, ql, qr, v);
        if (qr >  m) _add(o*2+1, m+1, r, ql, qr, v);
        sum[o] = sum[o*2] + sum[o*2+1];
    }
    ll _qry(int o, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return sum[o];
        push_down(o, r-l+1);
        int m = (l+r) >> 1; ll s = 0;
        if (ql <= m) s += _qry(o*2, l, m, ql, qr);
        if (qr >  m) s += _qry(o*2+1, m+1, r, ql, qr);
        return s;
    }
    void add(int l, int r, ll v) { _add(1, 1, n, l, r, v); }
    ll  qry(int l, int r) { return _qry(1, 1, n, l, r); }
};

// ST 表（区间最值，O(1) 查询，不可修改）
struct SparseTable {
    int n; vector<vll> st;
    SparseTable(const vll &a) : n(sz(a)), st(__lg(n) + 1, vll(n)) {
        st[0] = a;
        rep(j, 1, sz(st)) rep(i, 0, n - (1 << j) + 1)
            st[j][i] = min(st[j-1][i], st[j-1][i + (1 << (j-1))]);
    }
    ll qry(int l, int r) {  // [l, r] 0-indexed
        int k = __lg(r - l + 1);
        return min(st[k][l], st[k][r - (1 << k) + 1]);
    }
};

// ==================== 图论 ====================

// Dijkstra（优先队列优化）
vll dijkstra(int s, const vector<vpii> &g, int n) {
    vll d(n + 1, LINF); d[s] = 0;
    priority_queue<pll, vector<pll>, greater<>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top(); pq.pop();
        if (du > d[u]) continue;
        for (auto [v, w] : g[u])
            if (d[v] > du + w) { d[v] = du + w; pq.push({d[v], v}); }
    }
    return d;
}

// Kruskal 最小生成树
ll kruskal(int n, vector<tuple<int,int,int>> &edges) {
    sort(all(edges), [](auto &a, auto &b) { return get<2>(a) < get<2>(b); });
    DSU dsu(n); ll tot = 0;
    for (auto [u, v, w] : edges)
        if (dsu.unite(u, v)) tot += w;
    return tot;
}

// 拓扑排序（有向图，返回空表示有环）
vi topo_sort(int n, const vector<vi> &g) {
    vi deg(n + 1), res;
    for (int u = 1; u <= n; ++u) for (int v : g[u]) ++deg[v];
    queue<int> q;
    for (int i = 1; i <= n; ++i) if (!deg[i]) q.push(i);
    while (!q.empty()) {
        int u = q.front(); q.pop(); res.pb(u);
        for (int v : g[u]) if (--deg[v] == 0) q.push(v);
    }
    return sz(res) == n ? res : vi{};
}

// ==================== 字符串 ====================

// KMP 失败函数
vi kmp_fail(const string &s) {
    int n = sz(s); vi f(n);
    for (int i = 1, j = 0; i < n; ++i) {
        while (j && s[i] != s[j]) j = f[j-1];
        f[i] = (j += (s[i] == s[j]));
    }
    return f;
}

// 字符串哈希（双哈希）
struct StringHash {
    const ll B1 = 131, B2 = 137, M1 = 1e9+7, M2 = 1e9+9;
    int n; vll h1, h2, p1, p2;
    StringHash(const string &s) : n(sz(s)), h1(n+1), h2(n+1), p1(n+1), p2(n+1) {
        p1[0] = p2[0] = 1;
        rep(i, 0, n) {
            p1[i+1] = p1[i] * B1 % M1;
            p2[i+1] = p2[i] * B2 % M2;
            h1[i+1] = (h1[i] * B1 + s[i]) % M1;
            h2[i+1] = (h2[i] * B2 + s[i]) % M2;
        }
    }
    pll get(int l, int r) {  // [l, r)
        ll a = (h1[r] - h1[l] * p1[r-l] % M1 + M1) % M1;
        ll b = (h2[r] - h2[l] * p2[r-l] % M2 + M2) % M2;
        return {a, b};
    }
};

// Manacher（最长回文子串）
vi manacher(const string &s) {
    string t = "#";
    for (char c : s) { t += c; t += '#'; }
    int n = sz(t); vi p(n);
    for (int i = 0, c = 0, r = 0; i < n; ++i) {
        int mirror = 2 * c - i;
        if (i < r) p[i] = min(r - i, p[mirror]);
        while (i + p[i] + 1 < n && i - p[i] - 1 >= 0 && t[i+p[i]+1] == t[i-p[i]-1]) ++p[i];
        if (i + p[i] > r) { c = i; r = i + p[i]; }
    }
    return p;  // p[i] = 以 t[i] 为中心的回文半径（原串中回文长度 = p[i]）
}

// ==================== 其他 ====================

// 坐标压缩
vi compress(vi a) {
    vi b = a; sort(all(b)); b.erase(unique(all(b)), b.end());
    for (int &x : a) x = lower_bound(all(b), x) - b.begin() + 1;
    return a;
}

// 整数二分模板
template<class T>
T bs_first(T l, T r, function<bool(T)> check) {  // 找第一个满足 check 的
    while (l < r) { T m = l + (r - l) / 2; check(m) ? r = m : l = m + 1; }
    return l;
}

// ==================== 解题区 ====================
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
