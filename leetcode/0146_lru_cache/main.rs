// 146. LRU Cache
// https://leetcode.cn/problems/lru-cache/

use std::collections::HashMap;
use std::ptr;

/// 双向链表节点
struct Node {
    key: i32,
    value: i32,
    prev: *mut Node,
    next: *mut Node,
}

impl Node {
    /// 在堆上分配一个孤立节点
    fn new(key: i32, value: i32) -> *mut Node {
        Box::into_raw(Box::new(Node {
            key,
            value,
            prev: ptr::null_mut(),
            next: ptr::null_mut(),
        }))
    }
}

struct LRUCache {
    capacity: usize,
    map: HashMap<i32, *mut Node>,
    head: *mut Node, // 哨兵头，越靠近头部表示越「最近使用」
    tail: *mut Node, // 哨兵尾，越靠近尾部表示越「久未使用」
}

impl LRUCache {
    fn new(capacity: i32) -> Self {
        // 哨兵头尾节点，简化链表边界处理
        let head = Node::new(-1, -1);
        let tail = Node::new(-1, -1);
        unsafe {
            (*head).next = tail;
            (*tail).prev = head;
        }
        Self {
            capacity: capacity as usize,
            map: HashMap::new(),
            head,
            tail,
        }
    }

    fn get(&self, key: i32) -> i32 {
        match self.map.get(&key) {
            Some(&node) => unsafe {
                // 命中后移到头部（最近使用）
                self.detach(node);
                self.add_to_head(node);
                (*node).value
            },
            None => -1,
        }
    }

    fn put(&mut self, key: i32, value: i32) {
        // key 已存在：更新 value 并移到头部
        if let Some(&node) = self.map.get(&key) {
            unsafe {
                (*node).value = value;
                self.detach(node);
                self.add_to_head(node);
            }
            return;
        }

        // 容量已满：驱逐尾部节点（最久未使用）
        if self.map.len() == self.capacity {
            unsafe {
                let last = (*self.tail).prev;
                self.evict(last);
            }
        }

        // 新建节点，插入头部并登记到 map
        let node = Node::new(key, value);
        unsafe {
            self.add_to_head(node);
        }
        self.map.insert(key, node);
    }

    /// 仅断链，不删节点、不擦 map（用于移动到头部）
    unsafe fn detach(&self, node: *mut Node) {
        (*(*node).prev).next = (*node).next;
        (*(*node).next).prev = (*node).prev;
        (*node).prev = ptr::null_mut();
        (*node).next = ptr::null_mut();
    }

    /// 断链 + 擦 map + 释放节点（用于驱逐尾部）
    unsafe fn evict(&mut self, node: *mut Node) {
        self.detach(node);
        self.map.remove(&(*node).key);
        drop(Box::from_raw(node));
    }

    /// 将节点插入哨兵头之后
    unsafe fn add_to_head(&self, node: *mut Node) {
        (*node).next = (*self.head).next;
        (*node).prev = self.head;
        (*(*self.head).next).prev = node;
        (*self.head).next = node;
    }
}

impl Drop for LRUCache {
    fn drop(&mut self) {
        // 沿链表释放所有节点（含哨兵），避免内存泄漏
        unsafe {
            let mut cur = self.head;
            while !cur.is_null() {
                let next = (*cur).next;
                drop(Box::from_raw(cur));
                cur = next;
            }
        }
    }
}

// Your LRUCache object will be instantiated and called as such:
// let obj = LRUCache::new(capacity);
// let ret_1: i32 = obj.get(key);
// obj.put(key, value);
