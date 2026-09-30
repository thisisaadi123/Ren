class Solution:
    def compress(self, text):
        out = []
        i = 0
        while i < len(text):
            j = i
            while j < len(text) and text[j] == text[i]:
                j += 1
            out.append(text[i])
            if j - i > 1:
                out.append(str(j - i))
            i = j
        return "".join(out)
