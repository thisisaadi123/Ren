class Solution:
    def convoys(self, depot, position, speed):
        trucks = sorted(zip(position, speed), reverse=True)
        count = 0
        lead_dist, lead_speed = 0, 1  # arrival time of the convoy ahead, as a fraction
        for p, s in trucks:
            dist = depot - p
            if dist * lead_speed > lead_dist * s:
                count += 1
                lead_dist, lead_speed = dist, s
        return count
