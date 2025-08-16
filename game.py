from agents.agent import Agent


class Room:
    """
    Room shaped as a 1-dimensional ring
    """
    def __init__(self, circumference):
        self.circumference = circumference

    def dist(self, x1, x2):
        """
        distance between positions x1 and x2
        """
        raw_dist = abs(x1 - x2)
        return min(raw_dist, self.circumference - raw_dist)


class Game:
    def __init__(self, room: Room, agent0: Agent, agent1: Agent):
        """
        Args:
          room: Room class
          agent0: Agent class
          agent1: Agent class
        """
        self.room = room
        self.agent0 = agent0
        self.agent1 = agent1

    def initiate_game(self):
        """
        Initializes the game by prompting the agents about the environment and requests their first choices.
        NB: Assumes the two agents are not at the same position initially.
        """
        choice0 = self.agent0.initiate_game(
            other_agent_position=self.agent1.position
        )
        choice1 = self.agent1.initiate_game(
            other_agent_position=self.agent0.position
        )
        return (choice0, choice1)

    def play_round(self):
        """
        Executes a round of the game allowing each agent to make their next choice.
        """
        choice0 = self.agent0.play_turn(other_agent_position_record=self.agent1.position_record)
        choice1 = self.agent1.play_turn(other_agent_position_record=self.agent0.position_record)
        return (choice0, choice1)

    def run_game(self, num_turns):
        """
        Initiates and runs the game for a specified number of turns.
        """
        print("Running game...")
        initial_choices = self.initiate_game()
        print(f"(agent0 choice, agent1_choice) = {initial_choices}")

        for i in range(num_turns):
            choices = self.play_round()
            print(f"(agent0 choice, agent1_choice) = {choices}")
