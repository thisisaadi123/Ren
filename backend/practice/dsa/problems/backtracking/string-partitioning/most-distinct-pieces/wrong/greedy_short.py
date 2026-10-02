class Solution:
    # Mistake: greedily takes the shortest new piece each time.
    def mostPieces(self, s):
        used, i = set(), 0
        while i < len(s):
            j = i + 1
            while j <= len(s) and s[i:j] in used:
                j += 1
            if j > len(s):
                break
            used.add(s[i:j])
            i = j
        return len(used)
