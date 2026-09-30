class Solution:
    # Mistake: appends the second train after the first.
    def mergeLines(self, first, second):
        if not first:
            return second
        node = first
        while node.next:
            node = node.next
        node.next = second
        return first
