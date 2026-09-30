class Solution:
    # Mistake: correct, but re-reads every branch from scratch: O(n^2) on a long chain.
    def richestOrderlyBranch(self, root):
        best = -float("inf")
        todo = [root]
        while todo:
            top = todo.pop()
            seq, stack, node = [], [], top
            while stack or node:
                while node:
                    stack.append(node)
                    node = node.left
                node = stack.pop()
                seq.append(node.val)
                node = node.right
            if all(a < b for a, b in zip(seq, seq[1:])):
                best = max(best, sum(seq))
            for c in (top.left, top.right):
                if c:
                    todo.append(c)
        return best
