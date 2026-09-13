// 56. 合并区间
// https://leetcode.cn/problems/merge-intervals/
#include <bits/stdc++.h>
using namespace std;
// 思路：根据每个数组的第一个元素对intervals进行排序
// 排序 + 顺序合并：按左端点排序后依次扫描，
// 当前区间左端 <= 结果末区间的右端则可以合并（右端取 max），否则新起一段。
// 时间 O(n·log n)，空间 O(log n)（排序栈，不计输出）
class Solution {
  public:
    vector<vector<int>> merge(vector<vector<int>> &intervals) {
        sort(intervals.begin(), intervals.end());
        vector<vector<int>> res;
        res.reserve(intervals.size());

        for (auto &one_interval : intervals) {
            if (!res.empty() && one_interval[0] <= res.back()[1]) { // can merge
                res.back()[1] = max(res.back()[1], one_interval[1]);
            } else {
                res.push_back(std::move(one_interval));
            }
        }
        return res;
    }
};
