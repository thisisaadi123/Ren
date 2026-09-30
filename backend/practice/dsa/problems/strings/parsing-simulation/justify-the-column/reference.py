class Solution:
    def justify(self, words, width):
        out, i, n = [], 0, len(words)
        while i < n:
            j, size = i + 1, len(words[i])
            while j < n and size + 1 + len(words[j]) <= width:
                size += 1 + len(words[j])
                j += 1
            line, gaps = words[i:j], j - i - 1
            if j == n or gaps == 0:
                s = " ".join(line)
                out.append(s + " " * (width - len(s)))
            else:
                q, r = divmod(width - (size - gaps), gaps)
                parts = [w + " " * (q + (1 if k < r else 0)) for k, w in enumerate(line[:-1])]
                out.append("".join(parts) + line[-1])
            i = j
        return out
