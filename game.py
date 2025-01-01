from agents.agent import Agent
from rooms.room import Room


class Game:
    def __init__(self, room: Room, agent0: Agent, agent1: Agent):
        """
        Args:
          room: Room class
          agent0: chatbot model provided by ollama
          agent1: chatbot model provided by ollama
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

    def play_round(self, turn_number: int):
        """
        Executes a round of the game allowing each agent to make their next choice.
        """
        previous_turn_number = turn_number - 1
        choice0 = self.agent0.play_turn(
            other_agent_position=self.agent1.position,
            other_agent_choice=self.agent1.choice_record[previous_turn_number],
        )
        choice1 = self.agent1.play_turn(
            other_agent_position=self.agent0.position,
            other_agent_choice=self.agent0.choice_record[previous_turn_number]
        )
        return (choice0, choice1)

    def print_message_record(self):
        for message in self.message_record:
            role = message["role"].capitalize()
            content = message["content"]
            print(f"{role}: {content}\n")

    def run_game(self, num_turns):
        """
        Initiates and runs the game for a specified number of turns.
        """
        initial_choices = self.initiate_game()
        print(initial_choices)

        for i in range(num_turns):
            choices = self.play_round(i)
            print(choices)

        print(self.agent0.position_record)
        print(self.agent1.position_record)
        self.agent0.print_message_record()
