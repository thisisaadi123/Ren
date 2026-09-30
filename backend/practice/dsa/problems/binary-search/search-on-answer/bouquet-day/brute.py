class Solution:
    def earliestBouquetDay(self, bloom, bouquets, size):
        for day in sorted(set(bloom)):
            made = run = 0
            for b in bloom:
                run = run + 1 if b <= day else 0
                if run == size:
                    made += 1
                    run = 0
            if made >= bouquets:
                return day
        return -1
