// 560. 和为 K 的子数组
// https://leetcode.cn/problems/subarray-sum-equals-k/
#include <bits/stdc++.h>
using namespace std;
// 前缀和 + 哈希：子数组 (i, j] 的和为 k 等价于 prefix[j] - prefix[i] = k
// 子数组 → 前缀和
// 一边扫描一边统计之前出现过多少个 prefix - k
// 时间 O(n)，空间 O(n)
class Solution {
  public:
    int subarraySum(vector<int> &nums, int k) {
        unordered_map<long long, int> cnt; // 前缀和 -> 出现次数
        cnt[0]           = 1;              // 空前缀，处理从下标 0 开始的子数组
        long long prefix = 0;
        int       ans    = 0;
        for (int x : nums) {
            prefix += x;
            auto it = cnt.find(prefix - k);
            if (it != cnt.end()) {
                ans += it->second; // 以当前结尾、和为 k 的子数组个数
            }
            ++cnt[prefix];
        }
        return ans;
    }
};
