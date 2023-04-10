from sd.cache.Node import Node


class DoublyLinkedList:
    def __init__(self):
        self.dummy_head = Node(None, None)
        self.tail = self.dummy_head
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def insert(self, node: Node):
        self.tail.next = node
        node.prev = self.tail
        self.size += 1

    def remove(self, node: Node = None) -> Node:
        if self.size == 0:
            return None

        if not node:
            node = self.dummy_head.next

        node.prev.next = node.next

        if node.next:
            node.next.prev = node.prev

        # update tail if node is tail
        if node == self.tail:
            self.tail = self.tail.prev

        self.size -= 1
        return node
