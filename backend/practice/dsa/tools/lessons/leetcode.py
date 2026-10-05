"""LeetCode problems to practise after each pattern lesson, listed at the end of the lesson.

Each entry is (number, slug, title, difficulty, premium). lesson() adds the pattern's list
to its JSON and fails if a lesson has none. The details were taken from LeetCode itself;
run this file to check them again (it needs the network):

    python3 backend/practice/dsa/tools/lessons/leetcode.py
"""

LEETCODE = {
    "frequency-counting": [
        (242, "valid-anagram", "Valid Anagram", "easy", False),
        (383, "ransom-note", "Ransom Note", "easy", False),
        (387, "first-unique-character-in-a-string", "First Unique Character in a String", "easy", False),
        (389, "find-the-difference", "Find the Difference", "easy", False),
        (1512, "number-of-good-pairs", "Number of Good Pairs", "easy", False),
        (1189, "maximum-number-of-balloons", "Maximum Number of Balloons", "easy", False),
        (1207, "unique-number-of-occurrences", "Unique Number of Occurrences", "easy", False),
        (1002, "find-common-characters", "Find Common Characters", "easy", False),
        (451, "sort-characters-by-frequency", "Sort Characters By Frequency", "medium", False),
        (347, "top-k-frequent-elements", "Top K Frequent Elements", "medium", False),
        (1347, "minimum-number-of-steps-to-make-two-strings-anagram", "Minimum Number of Steps to Make Two Strings Anagram", "medium", False),
        (1657, "determine-if-two-strings-are-close", "Determine if Two Strings Are Close", "medium", False),
    ],
    "complement-lookup": [
        (1, "two-sum", "Two Sum", "easy", False),
        (219, "contains-duplicate-ii", "Contains Duplicate II", "easy", False),
        (2006, "count-number-of-pairs-with-absolute-difference-k", "Count Number of Pairs With Absolute Difference K", "easy", False),
        (532, "k-diff-pairs-in-an-array", "K-diff Pairs in an Array", "medium", False),
        (1679, "max-number-of-k-sum-pairs", "Max Number of K-Sum Pairs", "medium", False),
        (1010, "pairs-of-songs-with-total-durations-divisible-by-60", "Pairs of Songs With Total Durations Divisible by 60", "medium", False),
        (1497, "check-if-array-pairs-are-divisible-by-k", "Check If Array Pairs Are Divisible by k", "medium", False),
        (1711, "count-good-meals", "Count Good Meals", "medium", False),
        (454, "4sum-ii", "4Sum II", "medium", False),
        (167, "two-sum-ii-input-array-is-sorted", "Two Sum II - Input Array Is Sorted", "medium", False),
    ],
    "group-by-key": [
        (1128, "number-of-equivalent-domino-pairs", "Number of Equivalent Domino Pairs", "easy", False),
        (49, "group-anagrams", "Group Anagrams", "medium", False),
        (1282, "group-the-people-given-the-group-size-they-belong-to", "Group the People Given the Group Size They Belong To", "medium", False),
        (890, "find-and-replace-pattern", "Find and Replace Pattern", "medium", False),
        (609, "find-duplicate-file-in-system", "Find Duplicate File in System", "medium", False),
        (2352, "equal-row-and-column-pairs", "Equal Row and Column Pairs", "medium", False),
        (2001, "number-of-pairs-of-interchangeable-rectangles", "Number of Pairs of Interchangeable Rectangles", "medium", False),
        (1814, "count-nice-pairs-in-an-array", "Count Nice Pairs in an Array", "medium", False),
        (2342, "max-sum-of-a-pair-with-equal-sum-of-digits", "Max Sum of a Pair With Equal Sum of Digits", "medium", False),
        (2364, "count-number-of-bad-pairs", "Count Number of Bad Pairs", "medium", False),
        (249, "group-shifted-strings", "Group Shifted Strings", "medium", True),
    ],
    "prefix-sums": [
        (1480, "running-sum-of-1d-array", "Running Sum of 1d Array", "easy", False),
        (1732, "find-the-highest-altitude", "Find the Highest Altitude", "easy", False),
        (303, "range-sum-query-immutable", "Range Sum Query - Immutable", "easy", False),
        (724, "find-pivot-index", "Find Pivot Index", "easy", False),
        (1991, "find-the-middle-index-in-array", "Find the Middle Index in Array", "easy", False),
        (560, "subarray-sum-equals-k", "Subarray Sum Equals K", "medium", False),
        (525, "contiguous-array", "Contiguous Array", "medium", False),
        (523, "continuous-subarray-sum", "Continuous Subarray Sum", "medium", False),
        (974, "subarray-sums-divisible-by-k", "Subarray Sums Divisible by K", "medium", False),
        (930, "binary-subarrays-with-sum", "Binary Subarrays With Sum", "medium", False),
        (1248, "count-number-of-nice-subarrays", "Count Number of Nice Subarrays", "medium", False),
        (304, "range-sum-query-2d-immutable", "Range Sum Query 2D - Immutable", "medium", False),
        (1352, "product-of-the-last-k-numbers", "Product of the Last K Numbers", "medium", False),
    ],
    "difference-arrays": [
        (1854, "maximum-population-year", "Maximum Population Year", "easy", False),
        (1094, "car-pooling", "Car Pooling", "medium", False),
        (1109, "corporate-flight-bookings", "Corporate Flight Bookings", "medium", False),
        (2381, "shifting-letters-ii", "Shifting Letters II", "medium", False),
        (3355, "zero-array-transformation-i", "Zero Array Transformation I", "medium", False),
        (731, "my-calendar-ii", "My Calendar II", "medium", False),
        (1943, "describe-the-painting", "Describe the Painting", "medium", False),
        (2536, "increment-submatrices-by-one", "Increment Submatrices by One", "medium", False),
        (370, "range-addition", "Range Addition", "medium", True),
        (2251, "number-of-flowers-in-full-bloom", "Number of Flowers in Full Bloom", "hard", False),
        (2132, "stamping-the-grid", "Stamping the Grid", "hard", False),
    ],
    "index-marking": [
        (448, "find-all-numbers-disappeared-in-an-array", "Find All Numbers Disappeared in an Array", "easy", False),
        (645, "set-mismatch", "Set Mismatch", "easy", False),
        (442, "find-all-duplicates-in-an-array", "Find All Duplicates in an Array", "medium", False),
        (287, "find-the-duplicate-number", "Find the Duplicate Number", "medium", False),
        (41, "first-missing-positive", "First Missing Positive", "hard", False),
    ],
    "matrix-traversal": [
        (1572, "matrix-diagonal-sum", "Matrix Diagonal Sum", "easy", False),
        (867, "transpose-matrix", "Transpose Matrix", "easy", False),
        (832, "flipping-an-image", "Flipping an Image", "easy", False),
        (566, "reshape-the-matrix", "Reshape the Matrix", "easy", False),
        (766, "toeplitz-matrix", "Toeplitz Matrix", "easy", False),
        (1380, "lucky-numbers-in-a-matrix", "Lucky Numbers in a Matrix", "easy", False),
        (1886, "determine-whether-matrix-can-be-obtained-by-rotation", "Determine Whether Matrix Can Be Obtained By Rotation", "easy", False),
        (54, "spiral-matrix", "Spiral Matrix", "medium", False),
        (59, "spiral-matrix-ii", "Spiral Matrix II", "medium", False),
        (48, "rotate-image", "Rotate Image", "medium", False),
        (498, "diagonal-traverse", "Diagonal Traverse", "medium", False),
        (1329, "sort-the-matrix-diagonally", "Sort the Matrix Diagonally", "medium", False),
        (885, "spiral-matrix-iii", "Spiral Matrix III", "medium", False),
        (1914, "cyclically-rotating-a-grid", "Cyclically Rotating a Grid", "medium", False),
    ],
    "sort-then-scan": [
        (455, "assign-cookies", "Assign Cookies", "easy", False),
        (561, "array-partition", "Array Partition", "easy", False),
        (976, "largest-perimeter-triangle", "Largest Perimeter Triangle", "easy", False),
        (1200, "minimum-absolute-difference", "Minimum Absolute Difference", "easy", False),
        (1365, "how-many-numbers-are-smaller-than-the-current-number", "How Many Numbers Are Smaller Than the Current Number", "easy", False),
        (1331, "rank-transform-of-an-array", "Rank Transform of an Array", "easy", False),
        (350, "intersection-of-two-arrays-ii", "Intersection of Two Arrays II", "easy", False),
        (881, "boats-to-save-people", "Boats to Save People", "medium", False),
        (1877, "minimize-maximum-pair-sum-in-array", "Minimize Maximum Pair Sum in Array", "medium", False),
        (274, "h-index", "H-Index", "medium", False),
        (1798, "maximum-number-of-consecutive-values-you-can-make", "Maximum Number of Consecutive Values You Can Make", "medium", False),
        (330, "patching-array", "Patching Array", "hard", False),
    ],
    "prefix-suffix-products": [
        (121, "best-time-to-buy-and-sell-stock", "Best Time to Buy and Sell Stock", "easy", False),
        (2574, "left-and-right-sum-differences", "Left and Right Sum Differences", "easy", False),
        (1422, "maximum-score-after-splitting-a-string", "Maximum Score After Splitting a String", "easy", False),
        (238, "product-of-array-except-self", "Product of Array Except Self", "medium", False),
        (845, "longest-mountain-in-array", "Longest Mountain in Array", "medium", False),
        (915, "partition-array-into-disjoint-intervals", "Partition Array into Disjoint Intervals", "medium", False),
        (2100, "find-good-days-to-rob-the-bank", "Find Good Days to Rob the Bank", "medium", False),
        (42, "trapping-rain-water", "Trapping Rain Water", "hard", False),
        (135, "candy", "Candy", "hard", False),
        (1671, "minimum-number-of-removals-to-make-mountain-array", "Minimum Number of Removals to Make Mountain Array", "hard", False),
        (768, "max-chunks-to-make-sorted-ii", "Max Chunks To Make Sorted II", "hard", False),
    ],
    "cyclic-sort": [
        (268, "missing-number", "Missing Number", "easy", False),
        (448, "find-all-numbers-disappeared-in-an-array", "Find All Numbers Disappeared in an Array", "easy", False),
        (645, "set-mismatch", "Set Mismatch", "easy", False),
        (442, "find-all-duplicates-in-an-array", "Find All Duplicates in an Array", "medium", False),
        (287, "find-the-duplicate-number", "Find the Duplicate Number", "medium", False),
        (41, "first-missing-positive", "First Missing Positive", "hard", False),
        (765, "couples-holding-hands", "Couples Holding Hands", "hard", False),
    ],
    "majority-vote": [
        (169, "majority-element", "Majority Element", "easy", False),
        (1287, "element-appearing-more-than-25-in-sorted-array", "Element Appearing More Than 25% In Sorted Array", "easy", False),
        (1150, "check-if-a-number-is-majority-element-in-a-sorted-array", "Check If a Number Is Majority Element in a Sorted Array", "easy", True),
        (229, "majority-element-ii", "Majority Element II", "medium", False),
        (2780, "minimum-index-of-a-valid-split", "Minimum Index of a Valid Split", "medium", False),
        (1157, "online-majority-element-in-subarray", "Online Majority Element In Subarray", "hard", False),
    ],
    "consecutive-runs": [
        (228, "summary-ranges", "Summary Ranges", "easy", False),
        (2229, "check-if-an-array-is-consecutive", "Check if an Array Is Consecutive", "easy", True),
        (163, "missing-ranges", "Missing Ranges", "easy", True),
        (128, "longest-consecutive-sequence", "Longest Consecutive Sequence", "medium", False),
        (2501, "longest-square-streak-in-an-array", "Longest Square Streak in an Array", "medium", False),
        (846, "hand-of-straights", "Hand of Straights", "medium", False),
        (1296, "divide-array-in-sets-of-k-consecutive-numbers", "Divide Array in Sets of K Consecutive Numbers", "medium", False),
    ],
    "rotate-reverse": [
        (344, "reverse-string", "Reverse String", "easy", False),
        (541, "reverse-string-ii", "Reverse String II", "easy", False),
        (557, "reverse-words-in-a-string-iii", "Reverse Words in a String III", "easy", False),
        (2000, "reverse-prefix-of-word", "Reverse Prefix of Word", "easy", False),
        (796, "rotate-string", "Rotate String", "easy", False),
        (1752, "check-if-array-is-sorted-and-rotated", "Check if Array Is Sorted and Rotated", "easy", False),
        (189, "rotate-array", "Rotate Array", "medium", False),
        (151, "reverse-words-in-a-string", "Reverse Words in a String", "medium", False),
        (186, "reverse-words-in-a-string-ii", "Reverse Words in a String II", "medium", True),
    ],
    "next-permutation": [
        (31, "next-permutation", "Next Permutation", "medium", False),
        (1053, "previous-permutation-with-one-swap", "Previous Permutation With One Swap", "medium", False),
        (556, "next-greater-element-iii", "Next Greater Element III", "medium", False),
        (47, "permutations-ii", "Permutations II", "medium", False),
        (1850, "minimum-adjacent-swaps-to-reach-the-kth-smallest-number", "Minimum Adjacent Swaps to Reach the Kth Smallest Number", "medium", False),
        (60, "permutation-sequence", "Permutation Sequence", "hard", False),
        (1842, "next-palindrome-using-same-digits", "Next Palindrome Using Same Digits", "hard", True),
    ],
    "matrix-in-place": [
        (661, "image-smoother", "Image Smoother", "easy", False),
        (73, "set-matrix-zeroes", "Set Matrix Zeroes", "medium", False),
        (289, "game-of-life", "Game of Life", "medium", False),
        (48, "rotate-image", "Rotate Image", "medium", False),
        (723, "candy-crush", "Candy Crush", "medium", True),
    ],
    "comparison-sorts": [
        (88, "merge-sorted-array", "Merge Sorted Array", "easy", False),
        (977, "squares-of-a-sorted-array", "Squares of a Sorted Array", "easy", False),
        (905, "sort-array-by-parity", "Sort Array By Parity", "easy", False),
        (912, "sort-an-array", "Sort an Array", "medium", False),
        (75, "sort-colors", "Sort Colors", "medium", False),
        (148, "sort-list", "Sort List", "medium", False),
        (147, "insertion-sort-list", "Insertion Sort List", "medium", False),
        (2161, "partition-array-according-to-given-pivot", "Partition Array According to Given Pivot", "medium", False),
        (23, "merge-k-sorted-lists", "Merge k Sorted Lists", "hard", False),
    ],
    "custom-order": [
        (2418, "sort-the-people", "Sort the People", "easy", False),
        (1356, "sort-integers-by-the-number-of-1-bits", "Sort Integers by The Number of 1 Bits", "easy", False),
        (1122, "relative-sort-array", "Relative Sort Array", "easy", False),
        (1636, "sort-array-by-increasing-frequency", "Sort Array by Increasing Frequency", "easy", False),
        (791, "custom-sort-string", "Custom Sort String", "medium", False),
        (165, "compare-version-numbers", "Compare Version Numbers", "medium", False),
        (937, "reorder-data-in-log-files", "Reorder Data in Log Files", "medium", False),
        (2545, "sort-the-students-by-their-kth-score", "Sort the Students by Their Kth Score", "medium", False),
        (1366, "rank-teams-by-votes", "Rank Teams by Votes", "medium", False),
        (1029, "two-city-scheduling", "Two City Scheduling", "medium", False),
        (179, "largest-number", "Largest Number", "medium", False),
        (406, "queue-reconstruction-by-height", "Queue Reconstruction by Height", "medium", False),
        (354, "russian-doll-envelopes", "Russian Doll Envelopes", "hard", False),
    ],
    "counting-bucket": [
        (1051, "height-checker", "Height Checker", "easy", False),
        (2037, "minimum-number-of-moves-to-seat-everyone", "Minimum Number of Moves to Seat Everyone", "easy", False),
        (1122, "relative-sort-array", "Relative Sort Array", "easy", False),
        (75, "sort-colors", "Sort Colors", "medium", False),
        (274, "h-index", "H-Index", "medium", False),
        (347, "top-k-frequent-elements", "Top K Frequent Elements", "medium", False),
        (451, "sort-characters-by-frequency", "Sort Characters By Frequency", "medium", False),
        (164, "maximum-gap", "Maximum Gap", "medium", False),
        (220, "contains-duplicate-iii", "Contains Duplicate III", "hard", False),
    ],
    "quickselect": [
        (2099, "find-subsequence-of-length-k-with-the-largest-sum", "Find Subsequence of Length K With the Largest Sum", "easy", False),
        (1985, "find-the-kth-largest-integer-in-the-array", "Find the Kth Largest Integer in the Array", "medium", False),
        (215, "kth-largest-element-in-an-array", "Kth Largest Element in an Array", "medium", False),
        (973, "k-closest-points-to-origin", "K Closest Points to Origin", "medium", False),
        (347, "top-k-frequent-elements", "Top K Frequent Elements", "medium", False),
        (462, "minimum-moves-to-equal-array-elements-ii", "Minimum Moves to Equal Array Elements II", "medium", False),
        (1471, "the-k-strongest-values-in-an-array", "The k Strongest Values in an Array", "medium", False),
        (324, "wiggle-sort-ii", "Wiggle Sort II", "medium", False),
        (296, "best-meeting-point", "Best Meeting Point", "hard", True),
    ],
    "merge-count": [
        (775, "global-and-local-inversions", "Global and Local Inversions", "medium", False),
        (315, "count-of-smaller-numbers-after-self", "Count of Smaller Numbers After Self", "hard", False),
        (493, "reverse-pairs", "Reverse Pairs", "hard", False),
        (327, "count-of-range-sum", "Count of Range Sum", "hard", False),
        (2426, "number-of-pairs-satisfying-inequality", "Number of Pairs Satisfying Inequality", "hard", False),
        (1649, "create-sorted-array-through-instructions", "Create Sorted Array through Instructions", "hard", False),
        (2179, "count-good-triplets-in-an-array", "Count Good Triplets in an Array", "hard", False),
    ],
    "opposite-ends": [
        (344, "reverse-string", "Reverse String", "easy", False),
        (125, "valid-palindrome", "Valid Palindrome", "easy", False),
        (977, "squares-of-a-sorted-array", "Squares of a Sorted Array", "easy", False),
        (917, "reverse-only-letters", "Reverse Only Letters", "easy", False),
        (345, "reverse-vowels-of-a-string", "Reverse Vowels of a String", "easy", False),
        (2824, "count-pairs-whose-sum-is-less-than-target", "Count Pairs Whose Sum is Less than Target", "easy", False),
        (167, "two-sum-ii-input-array-is-sorted", "Two Sum II - Input Array Is Sorted", "medium", False),
        (11, "container-with-most-water", "Container With Most Water", "medium", False),
        (881, "boats-to-save-people", "Boats to Save People", "medium", False),
        (1679, "max-number-of-k-sum-pairs", "Max Number of K-Sum Pairs", "medium", False),
        (2563, "count-the-number-of-fair-pairs", "Count the Number of Fair Pairs", "medium", False),
        (1750, "minimum-length-of-string-after-deleting-similar-ends", "Minimum Length of String After Deleting Similar Ends", "medium", False),
        (42, "trapping-rain-water", "Trapping Rain Water", "hard", False),
        (1099, "two-sum-less-than-k", "Two Sum Less Than K", "easy", True),
        (2422, "merge-operations-to-turn-array-into-a-palindrome", "Merge Operations to Turn Array Into a Palindrome", "medium", True),
    ],
    "read-write-pointers": [
        (26, "remove-duplicates-from-sorted-array", "Remove Duplicates from Sorted Array", "easy", False),
        (27, "remove-element", "Remove Element", "easy", False),
        (283, "move-zeroes", "Move Zeroes", "easy", False),
        (1089, "duplicate-zeros", "Duplicate Zeros", "easy", False),
        (2460, "apply-operations-to-an-array", "Apply Operations to an Array", "easy", False),
        (80, "remove-duplicates-from-sorted-array-ii", "Remove Duplicates from Sorted Array II", "medium", False),
        (443, "string-compression", "String Compression", "medium", False),
        (151, "reverse-words-in-a-string", "Reverse Words in a String", "medium", False),
    ],
    "k-sum": [
        (15, "3sum", "3Sum", "medium", False),
        (16, "3sum-closest", "3Sum Closest", "medium", False),
        (18, "4sum", "4Sum", "medium", False),
        (611, "valid-triangle-number", "Valid Triangle Number", "medium", False),
        (923, "3sum-with-multiplicity", "3Sum With Multiplicity", "medium", False),
        (1577, "number-of-ways-where-square-of-number-is-equal-to-product-of-two-numbers", "Number of Ways Where Square of Number Is Equal to Product of Two Numbers", "medium", False),
        (259, "3sum-smaller", "3Sum Smaller", "medium", True),
    ],
    "partition": [
        (905, "sort-array-by-parity", "Sort Array By Parity", "easy", False),
        (922, "sort-array-by-parity-ii", "Sort Array By Parity II", "easy", False),
        (75, "sort-colors", "Sort Colors", "medium", False),
        (2161, "partition-array-according-to-given-pivot", "Partition Array According to Given Pivot", "medium", False),
        (2149, "rearrange-array-elements-by-sign", "Rearrange Array Elements by Sign", "medium", False),
        (215, "kth-largest-element-in-an-array", "Kth Largest Element in an Array", "medium", False),
        (324, "wiggle-sort-ii", "Wiggle Sort II", "medium", False),
    ],
    "merge-sorted": [
        (88, "merge-sorted-array", "Merge Sorted Array", "easy", False),
        (21, "merge-two-sorted-lists", "Merge Two Sorted Lists", "easy", False),
        (1768, "merge-strings-alternately", "Merge Strings Alternately", "easy", False),
        (349, "intersection-of-two-arrays", "Intersection of Two Arrays", "easy", False),
        (350, "intersection-of-two-arrays-ii", "Intersection of Two Arrays II", "easy", False),
        (2540, "minimum-common-value", "Minimum Common Value", "easy", False),
        (2570, "merge-two-2d-arrays-by-summing-values", "Merge Two 2D Arrays by Summing Values", "easy", False),
        (986, "interval-list-intersections", "Interval List Intersections", "medium", False),
        (1213, "intersection-of-three-sorted-arrays", "Intersection of Three Sorted Arrays", "easy", True),
        (1570, "dot-product-of-two-sparse-vectors", "Dot Product of Two Sparse Vectors", "medium", True),
    ],
    "subsequence-check": [
        (392, "is-subsequence", "Is Subsequence", "easy", False),
        (925, "long-pressed-name", "Long Pressed Name", "easy", False),
        (2486, "append-characters-to-string-to-make-subsequence", "Append Characters to String to Make Subsequence", "medium", False),
        (524, "longest-word-in-dictionary-through-deleting", "Longest Word in Dictionary through Deleting", "medium", False),
        (792, "number-of-matching-subsequences", "Number of Matching Subsequences", "medium", False),
        (2825, "make-string-a-subsequence-using-cyclic-increments", "Make String a Subsequence Using Cyclic Increments", "medium", False),
        (1023, "camelcase-matching", "Camelcase Matching", "medium", False),
        (1898, "maximum-number-of-removable-characters", "Maximum Number of Removable Characters", "medium", False),
        (522, "longest-uncommon-subsequence-ii", "Longest Uncommon Subsequence II", "medium", False),
        (1055, "shortest-way-to-form-string", "Shortest Way to Form String", "medium", True),
    ],
    "expand-center": [
        (5, "longest-palindromic-substring", "Longest Palindromic Substring", "medium", False),
        (647, "palindromic-substrings", "Palindromic Substrings", "medium", False),
        (2472, "maximum-number-of-non-overlapping-palindrome-substrings", "Maximum Number of Non-overlapping Palindrome Substrings", "hard", False),
        (1745, "palindrome-partitioning-iv", "Palindrome Partitioning IV", "hard", False),
        (1960, "maximum-product-of-the-length-of-two-palindromic-substrings", "Maximum Product of the Length of Two Palindromic Substrings", "hard", False),
    ],
    "rolling-hash": [
        (28, "find-the-index-of-the-first-occurrence-in-a-string", "Find the Index of the First Occurrence in a String", "easy", False),
        (187, "repeated-dna-sequences", "Repeated DNA Sequences", "medium", False),
        (718, "maximum-length-of-repeated-subarray", "Maximum Length of Repeated Subarray", "medium", False),
        (1044, "longest-duplicate-substring", "Longest Duplicate Substring", "hard", False),
        (1316, "distinct-echo-substrings", "Distinct Echo Substrings", "hard", False),
        (1923, "longest-common-subpath", "Longest Common Subpath", "hard", False),
        (2156, "find-substring-with-given-hash-value", "Find Substring With Given Hash Value", "hard", False),
        (1062, "longest-repeating-substring", "Longest Repeating Substring", "medium", True),
        (1698, "number-of-distinct-substrings-in-a-string", "Number of Distinct Substrings in a String", "medium", True),
    ],
    "pattern-matching": [
        (28, "find-the-index-of-the-first-occurrence-in-a-string", "Find the Index of the First Occurrence in a String", "easy", False),
        (459, "repeated-substring-pattern", "Repeated Substring Pattern", "easy", False),
        (796, "rotate-string", "Rotate String", "easy", False),
        (1408, "string-matching-in-an-array", "String Matching in an Array", "easy", False),
        (686, "repeated-string-match", "Repeated String Match", "medium", False),
        (214, "shortest-palindrome", "Shortest Palindrome", "hard", False),
        (1392, "longest-happy-prefix", "Longest Happy Prefix", "hard", False),
        (2223, "sum-of-scores-of-built-strings", "Sum of Scores of Built Strings", "hard", False),
        (3008, "find-beautiful-indices-in-the-given-array-ii", "Find Beautiful Indices in the Given Array II", "hard", False),
        (3031, "minimum-time-to-revert-word-to-initial-state-ii", "Minimum Time to Revert Word to Initial State II", "hard", False),
    ],
    "parsing-simulation": [
        (1556, "thousand-separator", "Thousand Separator", "easy", False),
        (1592, "rearrange-spaces-between-words", "Rearrange Spaces Between Words", "easy", False),
        (2042, "check-if-numbers-are-ascending-in-a-sentence", "Check if Numbers Are Ascending in a Sentence", "easy", False),
        (6, "zigzag-conversion", "Zigzag Conversion", "medium", False),
        (8, "string-to-integer-atoi", "String to Integer (atoi)", "medium", False),
        (165, "compare-version-numbers", "Compare Version Numbers", "medium", False),
        (468, "validate-ip-address", "Validate IP Address", "medium", False),
        (722, "remove-comments", "Remove Comments", "medium", False),
        (68, "text-justification", "Text Justification", "hard", False),
        (65, "valid-number", "Valid Number", "hard", False),
        (591, "tag-validator", "Tag Validator", "hard", False),
        (271, "encode-and-decode-strings", "Encode and Decode Strings", "medium", True),
    ],
    "string-signature": [
        (242, "valid-anagram", "Valid Anagram", "easy", False),
        (1347, "minimum-number-of-steps-to-make-two-strings-anagram", "Minimum Number of Steps to Make Two Strings Anagram", "medium", False),
        (2186, "minimum-number-of-steps-to-make-two-strings-anagram-ii", "Minimum Number of Steps to Make Two Strings Anagram II", "medium", False),
        (1657, "determine-if-two-strings-are-close", "Determine if Two Strings Are Close", "medium", False),
        (49, "group-anagrams", "Group Anagrams", "medium", False),
        (1177, "can-make-palindrome-from-substring", "Can Make Palindrome from Substring", "medium", False),
        (1915, "number-of-wonderful-substrings", "Number of Wonderful Substrings", "medium", False),
        (1542, "find-longest-awesome-substring", "Find Longest Awesome Substring", "hard", False),
        (266, "palindrome-permutation", "Palindrome Permutation", "easy", True),
    ],
    "char-mapping": [
        (205, "isomorphic-strings", "Isomorphic Strings", "easy", False),
        (290, "word-pattern", "Word Pattern", "easy", False),
        (2325, "decode-the-message", "Decode the Message", "easy", False),
        (890, "find-and-replace-pattern", "Find and Replace Pattern", "medium", False),
        (291, "word-pattern-ii", "Word Pattern II", "medium", True),
        (1153, "string-transforms-into-another-string", "String Transforms Into Another String", "hard", True),
    ],
    "palindrome-checks": [
        (125, "valid-palindrome", "Valid Palindrome", "easy", False),
        (9, "palindrome-number", "Palindrome Number", "easy", False),
        (2108, "find-first-palindromic-string-in-the-array", "Find First Palindromic String in the Array", "easy", False),
        (2697, "lexicographically-smallest-palindrome", "Lexicographically Smallest Palindrome", "easy", False),
        (1332, "remove-palindromic-subsequences", "Remove Palindromic Subsequences", "easy", False),
        (680, "valid-palindrome-ii", "Valid Palindrome II", "easy", False),
        (1328, "break-a-palindrome", "Break a Palindrome", "medium", False),
        (1616, "split-two-strings-to-make-palindrome", "Split Two Strings to Make Palindrome", "medium", False),
        (2330, "valid-palindrome-iv", "Valid Palindrome IV", "medium", True),
    ],
}


def url(slug):
    return f"https://leetcode.com/problems/{slug}/"


def entries(pattern):
    assert pattern in LEETCODE, f"{pattern}: add its LeetCode problems to leetcode.py"
    return [{"id": n, "title": t, "url": url(s), "difficulty": d, **({"premium": True} if p else {})} for n, s, t, d, p in LEETCODE[pattern]]


def verify():
    """Ask LeetCode for every listed problem and report anything that no longer matches."""
    import json
    import subprocess
    from concurrent.futures import ThreadPoolExecutor

    query = "query q($s: String!) { question(titleSlug: $s) { questionFrontendId title difficulty isPaidOnly } }"

    def check(item):
        n, slug, title, diff, paid = item
        out = subprocess.run(
            ["curl", "-s", "-m", "20", "https://leetcode.com/graphql", "-H", "Content-Type: application/json",
             "-H", "Referer: https://leetcode.com", "-d", json.dumps({"query": query, "variables": {"s": slug}})],
            capture_output=True, text=True).stdout
        try:
            q = json.loads(out)["data"]["question"]
        except (ValueError, KeyError, TypeError):
            return f"{slug}: no answer from LeetCode"
        if not q:
            return f"{slug}: not found"
        got = (int(q["questionFrontendId"]), q["title"], q["difficulty"].lower(), q["isPaidOnly"])
        return None if got == (n, title, diff, paid) else f"{slug}: listed {(n, title, diff, paid)}, LeetCode says {got}"

    items = sorted({x for xs in LEETCODE.values() for x in xs})
    with ThreadPoolExecutor(6) as pool:
        problems = [p for p in pool.map(check, items) if p]
    print(f"checked {len(items)} LeetCode problems")
    for p in problems:
        print("  " + p)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(verify())
