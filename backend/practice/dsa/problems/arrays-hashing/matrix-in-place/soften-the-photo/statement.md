A photo is a grid `image` of brightness values from `0` to `255`. To soften it, every pixel is replaced by the **average** of itself and its neighbours: the up to 9 pixels in the 3 × 3 block centred on it that fall inside the photo. The average is rounded down.

All pixels are softened at the same moment, using the original values. Return the softened photo.

{{examples}}

**Constraints**
- `1 ≤ image.length, image[i].length ≤ 200`
- All rows have the same length.
- `0 ≤ image[i][j] ≤ 255`
