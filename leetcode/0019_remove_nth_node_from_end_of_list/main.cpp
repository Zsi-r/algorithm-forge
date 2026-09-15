// 19. 删除链表的倒数第 N 个结点
// https://leetcode.cn/problems/remove-nth-node-from-end-of-list/
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

// 思路：哑节点 + 快慢指针（one-pass）。
// 快指针先走 n+1 步，随后快慢同速前进，快指针到 nullptr 时
// 慢指针恰停在倒数第 n+1 个节点处，直接跳过被删节点。
// 时间 O(n)，空间 O(1)。
class Solution {
  public:
    ListNode *removeNthFromEnd(ListNode *head, int n) {
        ListNode  dummy(0, head);
        ListNode *fast = &dummy, *slow = &dummy;
        for (int i = 0; i <= n; ++i)
            fast = fast->next; // 快指针先走 n+1 步
        while (fast) {
            fast = fast->next;
            slow = slow->next;
        }
        ListNode *del = slow->next;
        slow->next    = del->next;
        delete del;
        return dummy.next;
    }
};

/*
解法二：两遍遍历
第一遍统计链表长度 len，第二遍走到第 len-n 个节点执行删除。
时间 O(n)（两遍），空间 O(1)
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode dummy(0, head);
        int len = 0;
        for (ListNode* p = head; p; p = p->next) ++len;
        ListNode* cur = &dummy;
        for (int i = 0; i < len - n; ++i) cur = cur->next;
        ListNode* del = cur->next;
        cur->next     = del->next;
        delete del;
        return dummy.next;
    }
};
*/
