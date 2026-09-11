// 45. 跳跃游戏 II
// https://leetcode.cn/problems/jump-game-ii/
#include <bits/stdc++.h>
using namespace std;
// 贪心（隐式 BFS 分层）：end 为当前步数能到达的边界，farthest 为下一步最远可达
// 越过 end 时步数 +1，边界扩张到 farthest
// 时间 O(n)，空间 O(1)
class Solution {
  public:
    int jump(vector<int> &nums) {
        int steps    = 0;
        int end      = 0; // 当前这一步覆盖的右边界
        int farthest = 0; // 从当前层再跳一步的最远位置
        // 注意！！遍历到 n-1 就停：因为到达最后一个位置时不需要再起跳
        for (int i = 0; i < (int)nums.size() - 1; ++i) {
            farthest = max(farthest, i + nums[i]);
            if (i == end) {     // 走完当前层的全部选择
                ++steps;        // 起跳一次
                end = farthest; // 进入下一层
                if (end >= (int)nums.size() - 1) {
                    break; // 已能覆盖终点
                }
            }
        }
        return steps;
    }
};
