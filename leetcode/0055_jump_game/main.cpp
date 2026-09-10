// 55. 跳跃游戏
// https://leetcode.cn/problems/jump-game/
#include <bits/stdc++.h>
using namespace std;
// 贪心：维护从起点出发能到达的最远下标 farthest
// 若遍历到 i 时 farthest < i，说明 i 不可达；farthest 能覆盖末尾则成功
// 时间 O(n)，空间 O(1)
class Solution {
  public:
    bool canJump(vector<int> &nums) {
        int farthest = 0;
        for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
            if (i > farthest) {
                return false;
            }
            farthest = max(farthest, i + nums[i]);
        }
        return true;
    }
};
