from agents.agent import Agent
from rooms.room import Room


class Game:
    def __init__(self, room: Room, agent_one: Agent, agent_two: Agent):
        """
        Args:
          room: Room class
          agent_one: chatbot model provided by ollama
          agent_two: chatbot model provided by ollama
          choice_record: list of choices made by agents in each round
        """
        self.room = room
        self.agent_one = agent_one
        self.agent_two = agent_two
        self.message_record = []
        self.choice_record = []
        self.position_record = []

    def initiate_game(self):
        """
        Initializes the game by prompting the agents about the environment and requests their first choices.
        NB: Assumes the two agents are not at the same position initially.
        """
        choice0 = self.agent_one.initiate_game(
            other_agent_position=self.agent_two.position
        )
        choice1 = self.agent_two.initiate_game(
            other_agent_position=self.agent_one.position
        )
        initial_choices = (choice0, choice1)
        self.position_record.append((self.agent_one.position, self.agent_two.position))
        return initial_choices

    def play_round(self, turn_number: int):
        """
        Executes a round of the game allowing each agent to make their next choice.
        """
        previous_turn_number = turn_number - 1
        choice0 = self.agent_one.play_turn(
            other_agent_position=self.agent_two.position,
            other_agent_choice=self.choice_record[previous_turn_number][1],
        )
        choice1 = self.agent_two.play_turn(
            other_agent_position=self.agent_one.position,
            other_agent_choice=self.choice_record[previous_turn_number][0],
        )
        round_choices = (choice0, choice1)
        self.choice_record.append(round_choices)
        self.position_record.append((self.agent_one.position, self.agent_two.position))
        return round_choices

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

        print(self.agent_one.position_record)
        print(self.agent_two.position_record)
        self.agent_one.print_message_record()
