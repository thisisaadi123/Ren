class Solution:
    # Mistake: performs the k mod n beats one by one, walking to the end each time: O(n^2).
    def shiftLine(self, head, k):
        if head is None:
            return None
        n, node = 0, head
        while node:
            n += 1
            node = node.next
        for _ in range(k % n):
            prev, last = None, head
            while last.next:
                prev, last = last, last.next
            if prev is None:
                break
            prev.next = None
            last.next = head
            head = last
        return head
