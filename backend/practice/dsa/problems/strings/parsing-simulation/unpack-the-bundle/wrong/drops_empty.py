class Solution:
    # Mistake: skips empty strings instead of keeping them in the list.
    def unpack(self, bundle):
        out, i, n = [], 0, len(bundle)
        while i < n:
            j = bundle.index("#", i)
            size = int(bundle[i:j])
            if size:
                out.append(bundle[j + 1:j + 1 + size])
            i = j + 1 + size
        return out
