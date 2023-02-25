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
            if node.lock is False:
                self._remove_node(node)
                self._add_node(node)
                self.get_cache_order()
                return node.content
            else:
                return -1
        else:
            return -1

    def put(self, key, content, value):
        # add the new key-value pair to the cache and the front of the linked list
        self.calculate_free_space()
        while self.free_space < value:
            # remove the least recently used key from the cache and the end of the linked list
            self.cache[self.tail.key].lock = True
            del self.cache[self.tail.key]
            self._remove_node(self.tail)
            self.calculate_free_space()
        if key in self.cache:
            # update the value and move the key to the front of the linked list
            node = self.cache[key]
            if node.lock is False:
                node.value = value
                self._remove_node(node)
                self._add_node(node)
        else:
            node = Node(key, content, value)
            self.cache[key] = node
            self._add_node(node)
        self.calculate_free_space()
        self.get_cache_order()

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
        for item in self.cache.values():
            space += item.value
        self.free_space = self.capacity - space

    def get_free_space(self):
        return self.free_space

    def is_in_cache(self, key):
        if key in self.cache:
            return True
        else:
            return False

    def get_cache_order(self):
        aux_node = self.head
        count = 0
        print('---------------------------------    CACHE    ---------------------------------')
        print(f'--------- Occupied Space: {self.capacity - self.free_space} -------------  Free Space: {self.free_space}  -----------------')
        while count < len(self.cache):
            content_print = aux_node.content[0:20] if aux_node.content.__len__() > 30 else aux_node.content+'...'
            print(f'Nº: {count} | Key: {aux_node.key} | Content: {content_print} | Value: {aux_node.value}')
            aux_node = aux_node.next
            count+=1
        print('-------------------------------------------------------------------------------')
        print('   ')


    def get_cache_list(self):
        aux_node = self.head
        count = 0
        cache_list = ''
        while count < len(self.cache):
            cache_list = cache_list + f'---- Nº: {count}, Key: {aux_node.key} ----'
            aux_node = aux_node.next
            count+=1
        return cache_list


class Node:
    def __init__(self, key, content, value):
        self.key = key
        self.content = content
        self.value = value
        self.lock = False
        self.prev = None
        self.next = None
