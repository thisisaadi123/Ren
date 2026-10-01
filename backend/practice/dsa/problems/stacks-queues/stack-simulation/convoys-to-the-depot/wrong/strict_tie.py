class Solution:
    # Mistake: a truck that catches up exactly at the depot is counted as its own convoy.
    def convoys(self, depot, position, speed):
        trucks = sorted(zip(position, speed), reverse=True)
        count = 0
        lead_dist, lead_speed = 0, 1
        for p, s in trucks:
            dist = depot - p
            if dist * lead_speed >= lead_dist * s:
                count += 1
                lead_dist, lead_speed = dist, s
        return count
