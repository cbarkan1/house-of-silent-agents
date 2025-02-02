"""
1D room
2 agents
Agents know their relationship with the other (e.g. 'friend').

"""


def my_find(string, s):
    res = string.find(s)
    return float("inf") if res == -1 else res


class Room:
    """
    Base room class
    Holds utility functions that are common to all rooms
    """

    def __init__(self, max_distance):
        """
        Initializer for room class
        """
        self.max_distance = max_distance

    def dist(self, x1, x2):
        """
        distance between positions x1 and x2
        """
        raw_dist = abs(x1 - x2)
        return min(raw_dist, self.max_distance - raw_dist)


class Play_by_play:
    agent0 = []
    agent1 = []
