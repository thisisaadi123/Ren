class Solution:
    def unpack(self, bundle):
        out, i, n = [], 0, len(bundle)
        while i < n:
            j = i
            while bundle[j] != "#":
                j += 1
            size = int(bundle[i:j])
            out.append(bundle[j + 1:j + 1 + size])
            i = j + 1 + size
        return out
