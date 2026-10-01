class Solution:
    # Mistake: keeps "." as a folder name.
    def tidyPath(self, path):
        stack = []
        for part in path.split("/"):
            if part == "..":
                if stack:
                    stack.pop()
            elif part:
                stack.append(part)
        return "/" + "/".join(stack)
