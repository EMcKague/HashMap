# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        self._buckets = []
        for i in range(self.capacity):
            self._buckets.append(LinkedList())
        self.size = 0
        
    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """
        # hash the key to determine the bucket 
        location = self.create_hash(key)

        # search bucket for given key and return value if found
        if self._buckets[location].contains(key):
            return self._buckets[location].contains(key).value
        else:
            return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        # check if downsizing 
        if self.capacity > capacity:
            # change capcity
            self.capacity = capacity
            # rehash
            self.rehash()
            print("capcity:", self.capacity)

        else:
            # change capcity
            amt_to_add = capacity - self.capacity
            self.capacity = capacity
            # increase bucket size
            for i in range(amt_to_add):
                self._buckets.append(LinkedList())
            # rehash
            self.rehash()
            print("capcity:", self.capacity)


    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """ 
        # creates an index by running key through the hash function
        index = self.create_hash(key)

        # checks if given key already exists at given index and updates value if it does
        if self._buckets[index].contains(key):
            self._buckets[index].contains(key).value = value
            return True
        
        # adds the value to given index's linked list
        else:
            self._buckets[index].add_front(key, value)
            self.size += 1
            return True

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """
        # hash the key to find the bucket
        location = self.create_hash(key)

        # remove key at given location 
        self._buckets[location].remove(key)

        self.size -= 1

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """
        location = self.create_hash(key)
        if self._buckets[location].contains(key):
            return True
        else:
            return False
        
    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        i = 0
        for bucket in self._buckets:
            # print(bucket)
            if bucket.head == None:
                i += 1
        return i

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        # figure out the number of links
        
        total = 0
        for bucket in self._buckets:
            i = 0
            if bucket.head:
                pointer = bucket.head
                while pointer.next:
                    i += 1
                    pointer = pointer.next
                i += 1
            total += i

        # print("total:", total)
        return total / self.capacity

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

    def rehash(self):
        for bucket in self._buckets:
            if bucket.head:
                pointer = bucket.head
                while pointer.next:
                    self.put(pointer.key, pointer.value)
                    temp = pointer.next
                    bucket.remove(pointer.key)
                    pointer = temp
                self.put(pointer.key, pointer.value)
                bucket.remove(pointer.key)
        return

    def create_hash(self, key):
        """
        Hashes a given key

        Returns:
            An index for the given key
        """
        index = self._hash_function(key)
        index = index % self.capacity
    
        return index

    def sorted_tup(self):
        descending_values = []
        for bucket in self._buckets:
            # checks if bucket is empty
            if bucket.head:
                cur = bucket.head
                while cur.next:
                    descending_values.append((cur.key, cur.value))
                    cur = cur.next
                descending_values.append((cur.key, cur.value))
        # print("unsorted", descending_values)
        # print("sorted", sorted(descending_values))
        return sorted(descending_values, key=lambda x: float(x[1]), reverse=True)

# if __name__ == "__main__":

    # print("EMPTY BUCKETS - EXAMPLE ONE")
    # m = HashMap(100, hash_function_1)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.size, m.capacity)
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(100, 0, 100)
    # print(99, 1, 100)
    # print(98, 2, 100)
    # print(98, 2, 100)
    # print(97, 3, 100)
    # print("-----------")
    # print("EMPTY BUCKETS - EXAMPLE TWO")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(49, 1, 50)
    # print(39, 31, 50)
    # print(36, 61, 50)
    # print(33, 91, 50)
    # print(30, 121, 50)
    # print("-----------")

    # print("PUT - EXAMPLE ONE")
    # m = HashMap(50, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(39, 0.5, 25, 50)
    # print(37, 1.0, 50, 50)
    # print(35, 1.5, 75, 50)
    # print(32, 2.0, 100, 50)
    # print(30, 2.5, 125, 50)
    # print(30, 3.0, 150, 50)
    # print("-----------")
    # print("PUT - EXAMPLE TWO")
    # m = HashMap(40, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(36, 0.1, 4, 40)
    # print(33, 0.175, 7, 40)
    # print(30, 0.25, 10, 40)
    # print(27, 0.35, 14, 40)
    # print(25, 0.425, 17, 40)
    # print("-----------")

    # print("TABLE_LOAD - EXAMPLE ONE")
    # m = HashMap(100, hash_function_1)
    # print(m.table_load())
    # m.put('key1', 10)
    # print(m.table_load())
    # m.put('key2', 20)
    # print(m.table_load())
    # m.put('key1', 30)
    # print(m.table_load())
    # print('CORRECT OUTPUT')
    # print(0.0)
    # print(0.01)
    # print(0.02)
    # print(0.02)
    # print("-----------")
    # print("TABLE_LOAD - EXAMPLE TWO")
    # m = HashMap(50, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #             print(m.table_load(), m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(0.02, 1, 50)
    # print(0.22, 11, 50)
    # print(0.42, 21, 50)
    # print(0.62, 31, 50)
    # print(0.82, 41, 50)
    # print("-----------")

    # print("CLEAR - EXAMPLE ONE")
    # m = HashMap(100, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(0, 100)
    # print(2, 100)
    # print(0, 100)
    # print("-----------")
    # print("CLEAR - EXAMPLE TWO")
    # m = HashMap(50, hash_function_1)
    # print(m.size, m.capacity)
    # m.put('key1', 10)
    # print(m.size, m.capacity)
    # m.put('key2', 20)
    # print(m.size, m.capacity)
    # m.resize_table(100)
    # print(m.size, m.capacity)
    # m.clear()
    # print(m.size, m.capacity)
    # print('CORRECT OUTPUT')
    # print(0, 50)
    # print(1, 50)
    # print(2, 50)
    # print(2, 100)
    # print(0, 100)
    # print("-----------")

    # print("CONTAINS KEY - EXAMPLE ONE")
    # m = HashMap(50, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    # print('CORRECT OUTPUT')
    # print("False")
    # print("True")
    # print("False") 
    # print("True")
    # print("True")   
    # print("False")
    # print("-----------")
    # print("CONTAINS KEY - EXAMPLE TWO")
    # m = HashMap(75, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.size, m.capacity)
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result = result and m.contains_key(str(key))
    #     # all NOT inserted keys must be absent
    #     result = result and not m.contains_key(str(key + 1))
    # print(result)
    # print('CORRECT OUTPUT')
    # print(50, 75)
    # print("True")
    # print("-----------")

    # print("GET - EXAMPLE ONE")
    # m = HashMap(30, hash_function_1)  
    # print(m.get('key'))   
    # m.put('key1', 10)   
    # print(m.get('key1'))
    # print('CORRECT OUTPUT')
    # print("None")
    # print(10)
    # print("-----------")
    # print("GET - EXAMPLE TWO")
    # m = HashMap(150, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.size, m.capacity)
    # for i in range(200, 300, 21): 
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10) 
    # print('CORRECT OUTPUT')
    # print(15, 150)
    # print(200, 2000,"True")
    # print(201, "None", "False")
    # print(221, 2210, 'True')
    # print(222, 'None', 'False')
    # print(242, 2420, 'True')                   
    # print(243, 'None', 'False')
    # print(263, 2630, 'True')
    # print(264, 'None', 'False')
    # print(284, 2840, 'True')
    # print(285, 'None', 'False')
    # print("-----------")
