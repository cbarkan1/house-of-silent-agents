from ollama import chat
from agents.response_parser import ModelResponseParser


class Agent:
    def __init__(
        self, room, init_position, model="llama3.2", move_parser=ModelResponseParser()
    ):
        """
        Args:
          room: Room object
          init_position: initial position in room (integer between 0 and room.circumference-1)
          model: chatbot model provided by ollama
        """
        self.room = room
        self.position = init_position
        self.model = model
        self.move_parser = move_parser
        self.message_record = []
        self.choice_record = []
        self.position_record = [init_position]

    def initiate_game(self, other_agent_position, relationship="friend"):
        """
        Assumes the two agents are not at the same position initially.
        To-do: allow for the possibility that they're at the same place.
        """
        distance = self.room.dist(self.position, other_agent_position)
        prompt = (
            f"Hello! You are an AI agent walking around in a room, and your "
            f"{relationship} Bob is also in the room. You are a distance of {distance}ft away from Bob. Would you like to move closer to Bob, "
            "or farther from Bob? Please choose one of the following and provide a brief explanation of your choice:\n"
            "(A): Closer\n"
            "(B): Farther"
        )
        response = self.prompt_model(prompt)
        choice = self.find_choice(response)
        self.choice_record.append(choice)
        self.move(choice, other_agent_position)
        return choice

    def play_turn(self, other_agent_position, other_agent_choice):
        distance = self.room.dist(self.position, other_agent_position)
        prev_choice = self.choice_record[-1]
        if prev_choice == "invalid":
            prompt = "I wasn't able to understand your previous selection. Next time, please clearly state which item you wish to select. "
        else:
            prompt = f"You chose to {prev_choice}. "

        if (
            other_agent_choice == "move closer to Bob"
            or other_agent_choice == "move farther from Bob"
        ):
            prompt += f"Bob then chose to {other_agent_choice[0:-4]} you. "

        prompt += f"You are now a distance of {distance}ft from Bob. "

        if distance == 0:
            prompt += (
                "Would you like to remain where you are, or move left or right? Please choose one of the following:\n"
                "(i): Remain in place\n"
                "(ii): Move left\n"
                "(iii): Move right"
            )
        else:
            prompt += (
                "Would you now like to move closer to Bob or farther from Bob? Please choose one of the following, "
                "and provide a brief explanation of your choice:\n"
                "(A): Closer\n"
                "(B): Farther"
            )

        response = self.prompt_model(prompt)
        choice = self.find_choice(response)
        self.move(choice, other_agent_position)
        return choice

    def find_choice(self, response):
        choice = self.move_parser.parse_response_for_move_choice(response)
        self.choice_record.append(choice)
        return choice

    def move(self, choice, other_agent_position):
        new_position = self.room.step_of_choice(
            self.position, other_agent_position, choice
        )
        self.position = new_position
        self.position_record.append(new_position)

    def print_message_record(self):
        for message in self.message_record:
            role = message["role"].capitalize()
            content = message["content"]
            print(f"{role}: {content}\n")

    def prompt_model(self, prompt):
        self.message_record.append({"role": "user", "content": prompt})
        response = chat(model=self.model, messages=self.message_record)["message"][
            "content"
        ]
        self.message_record.append({"role": "assistant", "content": response})
        return response
