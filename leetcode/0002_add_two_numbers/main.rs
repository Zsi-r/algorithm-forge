// 2. 两数相加
// https://leetcode.cn/problems/add-two-numbers/
// Definition for singly-linked list.
#[derive(PartialEq, Eq, Clone, Debug)]
pub struct ListNode {
    pub val: i32,
    pub next: Option<Box<ListNode>>,
}

impl ListNode {
    #[inline]
    fn new(val: i32) -> Self {
        ListNode { next: None, val }
    }
}
impl Solution {
    pub fn add_two_numbers(
        l1: Option<Box<ListNode>>,
        l2: Option<Box<ListNode>>,
    ) -> Option<Box<ListNode>> {
        // 哑结点简化头插逻辑，模拟竖式加法，逐位相加并处理进位
        let mut dummy = ListNode::new(0);
        // cur 指向结果链表的尾结点，用可变引用不断后移
        let mut cur = &mut dummy;
        let mut carry = 0;

        // 三个可迭代源：p1、p2 为两个输入链表的"游标"，carry 充当第三位输入
        let mut p1 = l1;
        let mut p2 = l2;

        // 只要任一链表还有节点，或还有进位未处理，就继续循环
        while p1.is_some() || p2.is_some() || carry != 0 {
            let mut sum = carry;

            // take() 把 Option 里的值"拿走"，原变量变为 None，避免所有权冲突
            if let Some(node) = p1.take() {
                sum += node.val;
                p1 = node.next; // 游标后移（node 的 next 所有权转移给 p1）
            }
            if let Some(node) = p2.take() {
                sum += node.val;
                p2 = node.next;
            }

            carry = sum / 10;
            cur.next = Some(Box::new(ListNode::new(sum % 10)));
            // as_deref_mut: Option<Box<T>> -> Option<&mut T>，把 cur 移到新节点上
            cur = cur.next.as_deref_mut().unwrap();
        }

        dummy.next
    }
}
