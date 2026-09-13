// 11. 盛最多水的容器
// https://leetcode.cn/problems/container-with-most-water/
#include <bits/stdc++.h>
using namespace std;

// 思路：经典双指针问题
// 相向双指针：容量 = min(短板) × 宽度，从最宽出发，
// 每次移动较短的一侧，试试盛水面积能不能更大
// 时间 O(n)，空间 O(1)
class Solution {
  public:
    int maxArea(vector<int> &height) {
        int left  = 0;
        int right = height.size() - 1;

        int res = 0;

        while (left < right) {
            res = max(res, min(height[left], height[right]) * (right - left));
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        return res;
    }
};