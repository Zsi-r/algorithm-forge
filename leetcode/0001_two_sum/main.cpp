// 1. 两数之和
// https://leetcode.cn/problems/two-sum/
#include <bits/stdc++.h>
using namespace std;
// 哈希表一次遍历：边查"target - nums[i] 是否出现过"边插入
// 时间 O(n)，空间 O(n)
class Solution {
  public:
    vector<int> twoSum(vector<int> &nums, int target) {
        unordered_map<int, int> position; // 值 -> 下标
        for (auto i = 0; i < nums.size(); ++i) {
            auto it = position.find(target - nums[i]);
            if (it != position.end()) {
                return {it->second, i};
            }
            position[nums[i]] = i;
        }
        return {};
    }
};
