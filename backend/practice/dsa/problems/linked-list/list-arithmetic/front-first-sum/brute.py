class Solution:
    def addFrontFirst(self, a, b):
        def num(node):
            s = ""
            while node:
                s += str(node.val)
                node = node.next
            return int(s)

        out = None
        for ch in reversed(str(num(a) + num(b))):
            out = ListNode(int(ch), out)
        return out
