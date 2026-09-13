// 1. 两数之和
// https://leetcode.cn/problems/two-sum/
use std::collections::HashMap;

impl Solution {
    // pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
    //     // 哈希表记录 值 -> 下标，一次遍历完成查找
    //     let mut seen: HashMap<i32, usize> = HashMap::new();
    //     for (i, &num) in nums.iter().enumerate() {
    //         // 查找是否存在互补数 target - num
    //         if let Some(&j) = seen.get(&(target - num)) {
    //             return vec![j as i32, i as i32];
    //         }
    //         seen.insert(num, i);
    //     }
    //     vec![]
    // }
    pub fn two_sum(nums: Vec<i32>, target: i32) -> Vec<i32> {
        let mut seen: HashMap<i32, usize> = HashMap::new();
        for (i, &num) in nums.iter().enumerate() {
            if let Some(&j) = seen.get(&(target - num)) {
                return vec![j as i32, i as i32];
            }
            seen.insert(num, i);
        }
        vec![]
    }
}
