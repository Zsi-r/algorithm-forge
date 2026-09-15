// 31. 下一个排列
// https://leetcode.cn/problems/next-permutation/
#include <bits/stdc++.h>
using namespace std;
// 经典三步：从右找第一个下降点 i（后缀为降序），
// 再从右找第一个大于 nums[i] 的 j 并交换，最后把 i 之后（仍降序）的后缀反转成升序。
// 无下降点说明整个数组降序，直接反转为最小排列。
// 时间 O(n)，空间 O(1)
class Solution {
public:
    void nextPermutation(vector<int>& nums) {
        int n = nums.size(), i = n - 2;
        while (i >= 0 && nums[i] >= nums[i + 1]) --i; // 第一个下降点
        if (i >= 0) {
            int j = n - 1;
            while (nums[j] <= nums[i]) --j; // 从右往左第一个大于 nums[i] 的数
            swap(nums[i], nums[j]);
        }
        reverse(nums.begin() + i + 1, nums.end()); // 后缀反转成最小
    }
};
