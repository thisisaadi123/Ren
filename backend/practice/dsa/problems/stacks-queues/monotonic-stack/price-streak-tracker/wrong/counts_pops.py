class PriceStreak:
    # Mistake: adds 1 per popped entry instead of the popped entry's whole streak.
    def __init__(self):
        self.st = []

    def record(self, price):
        streak = 1
        while self.st and self.st[-1] <= price:
            self.st.pop()
            streak += 1
        self.st.append(price)
        return streak
