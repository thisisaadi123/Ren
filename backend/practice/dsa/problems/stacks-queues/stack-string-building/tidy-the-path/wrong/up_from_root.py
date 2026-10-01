class Solution:
    # Mistake: going up from the root crashes instead of staying at the root.
    def tidyPath(self, path):
        stack = []
        for part in path.split("/"):
            if part == "..":
                stack.pop()
            elif part and part != ".":
                stack.append(part)
        return "/" + "/".join(stack)
