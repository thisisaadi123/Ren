class Solution:
    # Mistake: starts from the truck farthest from the depot.
    def convoys(self, depot, position, speed):
        trucks = sorted(zip(position, speed))
        count = 0
        lead_dist, lead_speed = 0, 1
        for p, s in trucks:
            dist = depot - p
            if dist * lead_speed > lead_dist * s:
                count += 1
                lead_dist, lead_speed = dist, s
        return count
