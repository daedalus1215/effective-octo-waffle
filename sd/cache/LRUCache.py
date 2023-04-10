from sd.cache.DoublyLinkedList import DoublyLinkedList
from sd.cache.Node import Node


class LRUCache:
    def __init__(self, capacity:int):
        self.capacity = capacity
        self.node_map = {}
        self.node_list = DoublyLinkedList()

        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.node_map:
            node = self.node_map[key]
            self.node_list.remove(node)
            self.node_list.insert(node)
            return node.value
        return None

    def put(self, key, value):
        if key in self.node_map:
            node = self.node_map[key]
            node.value = value
            self.node_list.remove(node)
            self.node_list.insert(node)
        else:
            node = Node(key, value)
            self.node_list.insert(node)
            self.node_list.remove(node)

        if len(self.node_map) > self.capacity:
            node = self.node_list.dummy_head.next
            self.node_list.remove(node)
            del self.node_map[node.key]