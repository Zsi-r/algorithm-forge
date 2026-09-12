// 5. 最长回文子串
// https://leetcode.cn/problems/longest-palindromic-substring/
#include <bits/stdc++.h>
using namespace std;

// 思路：动态规划，dp[i][j] = dp[i - 1][j - 1] && (s[i]==s[j])
class Solution {
  public:
    string longestPalindrome(string s) {
        int n = s.size();

        vector<vector<int>> dp(n, vector<int>(n));
        string              res;
        int                 res_length = 0;

        for (int length = 0; length < n; length++) {
            for (int i = 0; i + length < n; i++) {
                int j = i + length;
                if (j == i) {
                    dp[i][j] = true;
                } else if (j == i + 1) {
                    dp[i][j] = (s[i] == s[j]);
                } else {
                    dp[i][j] = dp[i + 1][j - 1] && (s[i] == s[j]);
                }
                if (length + 1 > res_length && dp[i][j]) {
                    res        = s.substr(i, length + 1);
                    res_length = length + 1;
                }
            }
        }

        return res;
    }
};