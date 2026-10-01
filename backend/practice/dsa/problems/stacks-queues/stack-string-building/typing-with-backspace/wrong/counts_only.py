class Solution:
    # Mistake: compares how long the final texts are, not what they say.
    def sameText(self, a, b):
        def size(keys):
            n = 0
            for c in keys:
                n = max(0, n - 1) if c == "#" else n + 1
            return n

        return size(a) == size(b)
