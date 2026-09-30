class Solution:
    # Mistake: correct, but splits each range with a linear scan: O(n^2) on a sorted sequence.
    def couldBePreorder(self, keys):
        todo = [(0, len(keys))]
        while todo:
            a, b = todo.pop()
            if b - a <= 1:
                continue
            root = keys[a]
            m = a + 1
            while m < b and keys[m] < root:
                m += 1
            for j in range(m, b):
                if keys[j] < root:
                    return False
            todo.append((a + 1, m))
            todo.append((m, b))
        return True
