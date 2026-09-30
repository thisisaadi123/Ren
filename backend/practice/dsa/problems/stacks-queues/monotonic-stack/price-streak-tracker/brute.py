class PriceStreak:
    def __init__(self):
        self.days = []

    def record(self, price):
        self.days.append(price)
        count = 0
        for p in reversed(self.days):
            if p > price:
                break
            count += 1
        return count
