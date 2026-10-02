class Solution:
    def spacedStrings(self, n, ones):
        out, cur = [], []

        def go(left, last):
            room = n - len(cur)
            if left == 0:
                out.append("".join(cur) + "0" * room)
                return
            need = 2 * left - 1 + (1 if last == "1" else 0)
            if room < need:
                return
            cur.append("0")
            go(left, "0")
            cur.pop()
            if last != "1":
                cur.append("1")
                go(left - 1, "1")
                cur.pop()

        go(ones, "")
        return out
