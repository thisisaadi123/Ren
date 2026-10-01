class Solution:
    # Mistake: treats any name made of dots (like "...") as a step up.
    def tidyPath(self, path):
        stack = []
        for part in path.split("/"):
            if part and set(part) == {"."} and part != ".":
                if stack:
                    stack.pop()
            elif part and part != ".":
                stack.append(part)
        return "/" + "/".join(stack)
