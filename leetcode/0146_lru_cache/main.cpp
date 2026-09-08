// 146. LRU Cache
// https://leetcode.cn/problems/lru-cache/

#include <bits/stdc++.h>

using namespace std;

struct Node {
    int   key, value;
    Node *next;

    Node *prev;

    Node(int k, int v) : key(k), value(v), next(nullptr), prev(nullptr) {}
};

class LRUCache {
  public:
    LRUCache(int capacity) : capacity_(capacity) {
        // 哨兵头尾节点，简化边界处理
        head_       = new Node(-1, -1);
        tail_       = new Node(-1, -1);
        head_->next = tail_;
        tail_->prev = head_;
    }

    ~LRUCache() {
        auto *node = head_;
        while (node != nullptr) {
            auto *next = node->next;
            delete node;
            node = next;
        }
    }

    int get(int key) {
        auto it = map_.find(key);
        if (it == map_.end())
            return -1;
        auto *node = it->second; // 复用迭代器，避免二次哈希查找
        // 命中后移到头部（最近使用）
        detach(node);
        addToHead(node);
        return node->value;
    }

    void put(int key, int value) {
        // key 已存在：更新 value 并移到头部
        auto it = map_.find(key);
        if (it != map_.end()) {
            auto *node  = it->second; // 复用迭代器，避免二次哈希查找
            node->value = value;
            detach(node);
            addToHead(node);
            return;
        }

        // 容量满：驱逐尾部节点（最久未使用）
        if (static_cast<int>(map_.size()) == capacity_) {
            auto *last = tail_->prev;
            evict(last);
        }

        // 新建节点，插入头部并登记到 map_
        auto *node = new Node(key, value);
        addToHead(node);
        map_[key] = node;
    }

  private:
    // 仅断链，不删节点、不擦 map（用于移动到头部）
    void detach(Node *node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
        node->prev       = nullptr;
        node->next       = nullptr;
    }

    // 断链 + 擦 map + delete（用于驱逐尾部）
    void evict(Node *node) {
        detach(node);
        map_.erase(node->key);
        delete node;
    }

    // 将节点插入哨兵头之后
    void addToHead(Node *node) {
        node->next        = head_->next;
        node->prev        = head_;
        head_->next->prev = node;
        head_->next       = node;
    }

    int                        capacity_;
    unordered_map<int, Node *> map_;
    Node                      *head_;
    Node                      *tail_;
};

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache* obj = new LRUCache(capacity);
 * int param_1 = obj->get(key);
 * obj->put(key,value);
 */
