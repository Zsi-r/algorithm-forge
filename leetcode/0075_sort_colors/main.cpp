// 75. 颜色分类
// https://leetcode.cn/problems/sort-colors/
#include <bits/stdc++.h>
using namespace std;
// 荷兰国旗三指针：[0,p0) 全 0、(p2,n) 全 2、[p0,cur) 全 1，
// cur 遇 0 与 p0 交换（p0 处换来的必是 1，可直接前进）、
// 遇 2 与 p2 交换（换来的值未知，需原地复查）、遇 1 前进。
// 时间 O(n)（一遍扫描），空间 O(1)
class Solution {
  public:
    void sortColors(vector<int> &nums) {
        int p0 = 0, cur = 0, p2 = (int)nums.size() - 1;
        while (cur <= p2) {
            if (nums[cur] == 0) {
                swap(nums[cur++], nums[p0++]);
            } else if (nums[cur] == 2) {
                swap(nums[cur], nums[p2--]); // 换来的值未检查，cur 不动
            } else {
                ++cur;
            }
        }
    }
};

/* 解法二：两遍计数排序
 * 第一遍统计 0/1/2 的个数，第二遍按个数直接覆写数组。
 * 时间 O(n)，空间 O(1)，简单直观，但需要两遍扫描（不满足题目"一遍"进阶要求）。
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int c0 = 0, c1 = 0;
        for (int v : nums) {
            if (v == 0) ++c0;
            else if (v == 1) ++c1;
        }
        fill(nums.begin(), nums.begin() + c0, 0);
        fill(nums.begin() + c0, nums.begin() + c0 + c1, 1);
        fill(nums.begin() + c0 + c1, nums.end(), 2);
    }
};
*/
