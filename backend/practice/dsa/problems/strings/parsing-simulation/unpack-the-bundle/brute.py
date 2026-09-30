class Solution:
    def unpack(self, bundle):
        if not bundle:
            return []
        head, _, rest = bundle.partition("#")
        k = int(head)
        return [rest[:k]] + self.unpack(rest[k:])
