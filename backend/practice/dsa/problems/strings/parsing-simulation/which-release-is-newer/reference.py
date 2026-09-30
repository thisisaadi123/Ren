class Solution:
    def compareReleases(self, a, b):
        i = j = 0
        n, m = len(a), len(b)
        while i < n or j < m:
            si = i
            while i < n and a[i] != ".":
                i += 1
            sj = j
            while j < m and b[j] != ".":
                j += 1
            ra, rb = a[si:i].lstrip("0"), b[sj:j].lstrip("0")
            i += 1
            j += 1
            if len(ra) != len(rb):
                return 1 if len(ra) > len(rb) else -1
            if ra != rb:
                return 1 if ra > rb else -1
        return 0
