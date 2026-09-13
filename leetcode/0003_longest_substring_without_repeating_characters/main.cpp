// 3. 无重复字符的最长子串
// https://leetcode.cn/problems/longest-substring-without-repeating-characters/
#include <bits/stdc++.h>
using namespace std;

/* 滑动窗口（计数集合版）
 * 用 unordered_set 判断字符是否在窗口内，重复时逐位右移左端并删除字符。
 * 同为 O(n)（左右指针各走一遍），写法更通用，常数略大。
 */
class Solution {
  public:
    int lengthOfLongestSubstring(string s) {
        unordered_set<char> window;
        int                 ans = 0, left = 0;
        for (int right = 0; right < (int)s.size(); ++right) {
            while (window.count(s[right]))
                window.erase(s[left++]);
            window.insert(s[right]);
            ans = max(ans, right - left + 1);
        }
        return ans;
    }
};

// 解法二：
// 滑动窗口：哈希表记录每个字符最后出现位置，
// 右指针扩张时若字符已在窗口内，左端直接跳到上次出现位置的下一位。
// 时间 O(n)，空间 O(128)
// class Solution {
//   public:
//     int lengthOfLongestSubstring(string s) {
//         int last[128]; // 每个字符最后出现的下标，-1 表示未出现
//         fill(begin(last), end(last), -1);
//         int ans = 0, left = 0;
//         for (int right = 0; right < (int)s.size(); ++right) {
//             unsigned char c = s[right];
//             if (last[c] >= left)
//                 left = last[c] + 1; // 重复，收缩左端
//             last[c] = right;
//             ans     = max(ans, right - left + 1);
//         }
//         return ans;
//     }
// };
