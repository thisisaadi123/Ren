class PriceStreak:
    # Mistake: walks back over every earlier day on each call: O(n) per call.
    def __init__(self):
        self.days = []

    def record(self, price):
        self.days.append(price)
        i = len(self.days) - 1
        while i >= 0 and self.days[i] <= price:
            i -= 1
        return len(self.days) - 1 - i
