class Solution:
    def justify(self, words, width):
        lines, cur = [], []
        for w in words:
            if cur and len(" ".join(cur + [w])) > width:
                lines.append(cur)
                cur = []
            cur.append(w)
        lines.append(cur)
        out = []
        for idx, line in enumerate(lines):
            if idx == len(lines) - 1 or len(line) == 1:
                s = " ".join(line)
                out.append(s + " " * (width - len(s)))
                continue
            gaps = [1] * (len(line) - 1)
            while sum(gaps) + sum(len(w) for w in line) < width:
                gaps[gaps.index(min(gaps))] += 1
            s = line[0]
            for g, w in zip(gaps, line[1:]):
                s += " " * g + w
            out.append(s)
        return out
