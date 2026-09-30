class Solution:
    # Compares letter by letter from every start: O(n * m).
    def findAll(self, text, tag):
        out = []
        for i in range(len(text) - len(tag) + 1):
            j = 0
            while j < len(tag) and text[i + j] == tag[j]:
                j += 1
            if j == len(tag):
                out.append(i)
        return out
