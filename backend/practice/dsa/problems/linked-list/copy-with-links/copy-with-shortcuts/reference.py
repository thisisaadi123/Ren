class Solution:
    def copyList(self, head):
        copy = {None: None}
        node = head
        while node:
            copy[node] = RandomNode(node.val)
            node = node.next
        node = head
        while node:
            copy[node].next = copy[node.next]
            copy[node].random = copy[node.random]
            node = node.next
        return copy[head]
