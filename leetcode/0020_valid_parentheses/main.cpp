// 20. 有效的括号
// https://leetcode.cn/problems/valid-parentheses/
#include <bits/stdc++.h>
using namespace std;
// 思路：栈匹配。
// 左括号入栈；右括号时栈顶必须是对应左括号（栈空或不匹配即无效），
// 匹配则弹出。最后栈必须为空。时间 O(n)，空间 O(n)。
class Solution {
public:
    bool isValid(string s) {
        // 右括号 -> 对应左括号
        unordered_map<char, char> match = {{')', '('}, {']', '['}, {'}', '{'}};
        stack<char> st;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty() || st.top() != match[c]) return false;
                st.pop();
            }
        }
        return st.empty();
    }
};

/*
解法二：不用哈希表，直接分支判断
逻辑等价，省去 map 的构建开销，常数更小
时间 O(n)，空间 O(n)
class Solution {
public:
    bool isValid(string s) {
        stack<char> st;
        for (char c : s) {
            switch (c) {
                case '(': case '[': case '{':
                    st.push(c);
                    break;
                case ')':
                    if (st.empty() || st.top() != '(') return false;
                    st.pop();
                    break;
                case ']':
                    if (st.empty() || st.top() != '[') return false;
                    st.pop();
                    break;
                case '}':
                    if (st.empty() || st.top() != '{') return false;
                    st.pop();
                    break;
            }
        }
        return st.empty();
    }
};
*/
