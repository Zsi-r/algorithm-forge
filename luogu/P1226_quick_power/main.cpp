// P1226 【模板】快速幂||取余运算
// https://www.luogu.com.cn/problem/P1226
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll qpow(ll b, ll p, ll k) {
    ll r = 1 % k;
    for (b %= k; p; p >>= 1, b = b * b % k)
        if (p & 1) r = r * b % k;
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll b, p, k;
    cin >> b >> p >> k;
    cout << b << "^" << p << " mod " << k << "=" << qpow(b, p, k) << "\n";
    return 0;
}
