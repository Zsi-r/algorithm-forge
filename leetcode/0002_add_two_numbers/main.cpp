// 2. 两数相加
// https://leetcode.cn/problems/add-two-numbers/
#include <bits/stdc++.h>
using namespace std;

// Definition for singly-linked list.
struct ListNode {
    int       val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

// 思路：模拟竖式加法（one-pass）。
// 时间 O(max(m,n))，空间 O(1)（不计结果）。
class Solution {
  public:
    ListNode *addTwoNumbers(ListNode *l1, ListNode *l2) {
        ListNode *dummy = new ListNode();
        ListNode *tail  = dummy;
        int       carry = 0;
        while (l1 || l2) {
            if (l1) {
                carry += l1->val;
                l1 = l1->next;
            }
            if (l2) {
                carry += l2->val;
                l2 = l2->next;
            }
            tail->next = new ListNode(carry % 10);
            carry /= 10;
            tail = tail->next;
        }
        if (carry > 0) {
            tail->next = new ListNode(carry);
        }
        return dummy->next;
    }
};

/*
解法二：递归
递归相加剩余部分，返回进位，当前节点值为 (l1->val + l2->val + carry) % 10。
时间 O(max(m,n))，空间 O(max(m,n))（递归栈）
class Solution {
    // 返回新链表头节点
    ListNode* add(ListNode* l1, ListNode* l2, int carry) {
        if (!l1 && !l2 && !carry) return nullptr;
        int sum = carry;
        if (l1) { sum += l1->val; l1 = l1->next; }
        if (l2) { sum += l2->val; l2 = l2->next; }
        ListNode* node = new ListNode(sum % 10);
        node->next = add(l1, l2, sum / 10);
        return node;
    }

public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        return add(l1, l2, 0);
    }
};
*/
