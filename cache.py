import sys


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = None
        self.tail = None
        self.free_space = capacity

    def get(self, key):
        if key in self.cache:
            # move the accessed key to the front of the linked list
            node = self.cache[key]
            self._remove_node(node)
            self._add_node(node)
            return node.value
        else:
            return -1

    def put(self, key, value):
        # add the new key-value pair to the cache and the front of the linked list
        self.calculate_free_space()
        data_size = sys.getsizeof(value)
        print(f'data_size:{data_size}')
        print(f'self.cache:{self.cache}')
        while self.free_space < data_size:
            # remove the least recently used key from the cache and the end of the linked list
            del self.cache[self.tail.key]
            self._remove_node(self.tail)
            self.calculate_free_space()
        if key in self.cache:
            print('entrou aqui?')
            # update the value and move the key to the front of the linked list
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._add_node(node)
        else:
            print('entrou aqui????')
            node = Node(key, value)
            self.cache[key] = node
            self._add_node(node)
        self.calculate_free_space()

    def _remove_node(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

    def _add_node(self, node):
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node
        if not self.tail:
            self.tail = node

    def calculate_free_space(self):
        space = 0
        for value in self.cache.values():
            space += sys.getsizeof(value)
        self.free_space = self.capacity - space

    def get_free_space(self):
        return self.free_space

    def is_in_cache(self, key):
        if key in self.cache:
            return True
        else:
            return False


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None
