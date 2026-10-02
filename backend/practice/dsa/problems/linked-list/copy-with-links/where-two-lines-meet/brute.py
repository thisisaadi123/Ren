class Solution:
    def meetPoint(self, headA, headB):
        seen = set()
        node = headA
        while node:
            seen.add(id(node))
            node = node.next
        node = headB
        while node:
            if id(node) in seen:
                return node
            node = node.next
        return None
