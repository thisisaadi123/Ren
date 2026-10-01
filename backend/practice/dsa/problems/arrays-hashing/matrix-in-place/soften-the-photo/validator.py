def validate(image):
    assert isinstance(image, list) and 1 <= len(image) <= 200, "1 <= image.length <= 200"
    n = len(image[0])
    assert 1 <= n <= 200, "1 <= image[i].length <= 200"
    assert all(isinstance(r, list) and len(r) == n for r in image), "all rows have the same length"
    assert all(type(v) is int and 0 <= v <= 255 for r in image for v in r), "0 <= image[i][j] <= 255"
