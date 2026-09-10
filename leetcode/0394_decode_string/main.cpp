// 394. Decode String
// https://leetcode.cn/problems/decode-string/
#include <bits/stdc++.h>
using namespace std;
// 单栈解法：遇 '[' 压入（倍数, 当前前缀），遇 ']' 弹出并拼接展开
// 时间 O(n + 输出长度)，空间 O(输出长度)
class Solution {
  public:
    string decodeString(string s) {
        string                   cur; //
        int                      num = 0;
        stack<pair<int, string>> st;

        for (char c : s) {
            if (isdigit(c)) {
                num = num * 10 + (c - '0');
            } else if (c == '[') {
                st.emplace(num, move(cur));
                num = 0;
                cur.clear();
            } else if (c == ']') {
                auto [k, prev] = st.top();
                st.pop();
                prev.reserve(prev.size() + cur.size() * k);
                for (int i = 0; i < k; ++i) {
                    prev += cur;
                }
                cur = move(prev);
            } else {
                cur += c;
            }
        }
        return cur;
    }
};
