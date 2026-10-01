import re


class Solution:
    def expand(self, pattern):
        inner = re.compile(r"(\d+)\[([a-z]*)\]")
        while "[" in pattern:
            pattern = inner.sub(lambda m: m.group(2) * int(m.group(1)), pattern)
        return pattern
