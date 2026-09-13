// 15. 三数之和
// https://leetcode.cn/problems/3sum/
#include <bits/stdc++.h>
using namespace std;
// 排序 + 双指针：固定最小数 i，左右指针夹逼另两数，
// 三处去重（i 枚举、左指针、右指针）保证不输出重复三元组。
// 时间 O(n²)，空间 O(log n)（排序栈，不计输出）
class Solution {
  public:
    vector<vector<int>> threeSum(vector<int> &nums) {
        sort(nums.begin(), nums.end()); // 先排序
        int                 n = nums.size();
        vector<vector<int>> ans;
        for (int i = 0; i < n - 2 && nums[i] <= 0; ++i) { // 只考虑最小数小于等于零，early stop
            if (i > 0 && nums[i] == nums[i - 1]) {        // 去重，相同的最小值，已经上一轮 for 讨论过了
                continue;
            }
            int left = i + 1, right = n - 1; // 对 i 右侧的剩余数组，两端往中间
            while (left < right) {
                uint64_t sum = (uint64_t)nums[i] + nums[left] + nums[right];
                if (sum < 0) {
                    ++left;
                } else if (sum > 0) {
                    --right;
                } else {
                    ans.push_back({nums[i], nums[left], nums[right]});
                    while (left < right && nums[left] == nums[left + 1]) {
                        ++left; // 左端去重
                    }
                    while (left < right && nums[right] == nums[right - 1]) {
                        --right; // 右端去重
                    }
                    ++left;
                    --right;
                }
            }
        }
        return ans;
    }
};
