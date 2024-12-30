"""
1D room
2 agents
Agents know their relationship with the other (e.g. 'friend').

"""

import numpy as np
from rooms.room import Room


def my_find(string, s):
    res = string.find(s)
    return float("inf") if res == -1 else res


class OneDimensionalRoom(Room):
    """
    1D circular room (i.e. periodic boundary conditions)
    """

    def __init__(self, circumference=5):
        """
        circumference: positive odd integer
        """
        Room.__init__(self, max_distance=circumference)
        self.circumference = circumference

    def step_of_choice(self, x1, x2, choice):
        """
        Suppose agent1 at x1 has made choice, given that agent2 is at x2.
        This function determines agent1's new position after step.
        """
        if choice == "move left":
            return (x1 - 1) % self.circumference
        elif choice == "move right":
            return (x1 + 1) % self.circumference
        else:
            choice_dic = {
                "move closer to Bob": -1,
                "move farther from Bob": 1,
                "invalid": 0,
                "remain at the same position as Bob": 0,
            }
            displacement = (x2 - x1) % self.circumference
            s = np.sign(displacement - self.circumference / 2)
            new_x1 = (x1 + s * choice_dic[choice]) % self.circumference
            return new_x1


class Play_by_play:
    agent0 = []
    agent1 = []
