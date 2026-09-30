class Solution:
    # Mistake: assumes every length is a single digit.
    def unpack(self, bundle):
        out, i = [], 0
        while i < len(bundle):
            size = int(bundle[i])
            out.append(bundle[i + 2:i + 2 + size])
            i += 2 + size
        return out
