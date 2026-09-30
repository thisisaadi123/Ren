class Solution:
    # Mistake: divides the spaces evenly and forgets the remainder, so some lines come up short.
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
                q = (width - (size - gaps)) // gaps
                out.append((" " * q).join(line))
            i = j
        return out
