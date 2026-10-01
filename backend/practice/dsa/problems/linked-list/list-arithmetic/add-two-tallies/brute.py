class Solution:
    def addTallies(self, a, b):
        def num(node):
            digits = []
            while node:
                digits.append(str(node.val))
                node = node.next
            return int("".join(reversed(digits)))

        s = str(num(a) + num(b))
        out = None
        for ch in s:
            out = ListNode(int(ch), out)
        return out
