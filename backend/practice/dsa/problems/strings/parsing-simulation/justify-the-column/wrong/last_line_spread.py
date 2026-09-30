class Solution:
    # Mistake: spreads the spaces on the last line too, instead of left-aligning it.
    def justify(self, words, width):
        out, i, n = [], 0, len(words)
        while i < n:
            j, size = i + 1, len(words[i])
            while j < n and size + 1 + len(words[j]) <= width:
                size += 1 + len(words[j])
                j += 1
            line, gaps = words[i:j], j - i - 1
            if gaps == 0:
                out.append(line[0] + " " * (width - len(line[0])))
            else:
                q, r = divmod(width - (size - gaps), gaps)
                parts = [w + " " * (q + (1 if k < r else 0)) for k, w in enumerate(line[:-1])]
                out.append("".join(parts) + line[-1])
            i = j
        return out
