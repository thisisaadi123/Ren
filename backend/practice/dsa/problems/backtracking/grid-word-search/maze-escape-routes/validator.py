def validate(maze):
    assert isinstance(maze, list) and 1 <= len(maze) <= 5, "1 <= rows <= 5"
    n = len(maze[0])
    assert 1 <= n <= 5 and all(isinstance(r, list) and len(r) == n for r in maze), "1 <= columns <= 5"
    assert all(v in (0, 1) and type(v) is int for r in maze for v in r), "cells are 0 or 1"
    assert maze[0][0] == 0 and maze[-1][-1] == 0, "the corners are open"
