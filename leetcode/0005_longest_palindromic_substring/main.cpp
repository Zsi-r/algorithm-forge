// 5. 最长回文子串
// https://leetcode.cn/problems/longest-palindromic-substring/
#include <bits/stdc++.h>
using namespace std;

// 思路：动态规划，dp[i][j] = dp[i - 1][j - 1] && (s[i]==s[j])
// 时间 O(n²)，空间 O(n²)
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

/* 解法二：中心扩展（时间 O(n²)，空间 O(1)）
 * 枚举每个回文中心：奇数长度中心为单个字符 i，偶数长度中心为
 * 相邻字符对 (i, i+1)，从中心向两侧扩展直到字符不等。
 * 记录扩展出的最长回文起点与长度。相比 DP 省掉 O(n²) 的状态表。
 *
 * class Solution {
 *   public:
 *     string longestPalindrome(string s) {
 *         int n = s.size(), start = 0, maxLen = 1;
 *         auto expand = [&](int l, int r) {
 *             while (l >= 0 && r < n && s[l] == s[r]) { --l; ++r; }
 *             // 退出循环时回文串实际范围是 [l+1, r-1]，长度为 r-l-1
 *             if (r - l - 1 > maxLen) {
 *                 start  = l + 1;
 *                 maxLen = r - l - 1;
 *             }2
 *         };
 *         for (int i = 0; i < n; ++i) {
 *             expand(i, i);     // 奇数长度中心
 *             expand(i, i + 1); // 偶数长度中心
 *         }
 *         return s.substr(start, maxLen);
 *     }
 * };
 */