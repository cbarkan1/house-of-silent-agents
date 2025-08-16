from importlib import import_module
import re


class Agent:
    def __init__(self, room, init_position, llm, goal_prompt = ""):
        """
        Args:
          room: Room object
          init_position: initial position in room (integer between 0 and room.circumference-1)
          llm: dictionary of form {"api":"<api_name>", "model":"model_name"}
        """
        self.room = room
        self.position = init_position
        self.message_record = []
        self.choice_record = []
        self.position_record = [init_position]
        create_generate = import_module(f"agents.generate_with_api_funcs.{llm['api']}_generate").create_generate
        self.generate = create_generate(llm["model"])
        self.goal_prompt = goal_prompt
        self.choice_dic = {"(A)": "left", "(B)": "right", "(C)": "remain"}

    def initiate_game(self, other_agent_position, relationship="friend"):
        """
        Assumes the two agents are not at the same position initially.
        To-do: allow for the possibility that they're at the same place.
        """
        system_prompt = (
            f"You are an AI agent walking around in a ring-shaped room. The circumference of the room is {self.room.circumference} meters, "
            f"and you can occupy any position $x \\in [0,{self.room.circumference})$ along the ring. Note that, because the room is "
            f"shaped as a ring, position $x=0$ and $x={self.room.circumference}$ are equivalent. Your {relationship} Bob is also in "
            f"the room. Although you and Bob cannot speak to each other, you can observe each other's movements, which gives you "
            f"and Bob the chance to interact! "
        )
        system_prompt += self.goal_prompt
        self.message_record.append({"role": "system","content": system_prompt})
        
        distance = self.room.dist(self.position, other_agent_position)

        prompt = (
            f"You are at position $x={self.position}$ and Bob is at position $x={other_agent_position}$, "
            f"so you are a distance of {distance} meters away from Bob. You can take a 1 meter step in either "
            f" direction, so your options are:\n"
            f"(A): Move left to position $x={(self.position-1)%self.room.circumference}$.\n"
            f"(B): Move right to position $x={(self.position+1)%self.room.circumference}$.\n"
            f"(C): Remain in place.\n\n"
            f"Please consider how you would like to move, provide a brief explanation of your thought process, "
            f"and conclude your response with either \"(A)\", \"(B)\", or \"(C)\"."
        )
        response = self.prompt_model(prompt)
        choice = self.choice_and_move(response)
        return choice

    def play_turn(self, other_agent_position_record):
        prev_choice = self.choice_record[-1]
        if prev_choice == "invalid":
            prompt = (
                "I wasn't able to understand your previous selection, so you have remained in place at position "
                f"{self.position}. Next time, please conclude your response with either \"(A)\", \"(B)\", or \"(C)\"."
            )
        else:
            prompt = (
                f"You chose {prev_choice}, to move {self.choice_dic[prev_choice]} from position $x={self.position_record[-2]}$ "
                f"to position $x={self.position_record[-1]}$. "
            )

        prompt += f"Bob then chose to move from position $x={other_agent_position_record[-2]}$ to $x={other_agent_position_record[-1]}$. "

        distance = self.room.dist(self.position, other_agent_position_record[-1])
        prompt += f"You are now a distance of {distance} meters from Bob. "

        prompt += (
            "How would you like to move next? Your options are:\n"
            f"(A): Move left to position $x={(self.position-1)%self.room.circumference}$.\n"
            f"(B): Move right to position $x={(self.position+1)%self.room.circumference}$.\n"
            f"(C): Remain in place.\n\n"
            f"Please consider how you would like to move, provide a brief explanation of your thought process, "
            f"and conclude your response with either \"(A)\", \"(B)\", or \"(C)\"."
        )

        response = self.prompt_model(prompt)
        choice = self.choice_and_move(response)
        return choice

    def choice_and_move(self, response):
        keys_to_match = r"\(A\)|\(B\)|\(C\)"
        matches = re.findall(keys_to_match, response)
        if len(matches)==0:
            choice = "invalid"
        else:
            choice = matches[-1]
            if choice=="(A)":
                self.position = (self.position-1)%self.room.circumference
            elif choice=="(B)":
                self.position = (self.position+1)%self.room.circumference
        self.choice_record.append(choice)
        self.position_record.append(self.position)
        return choice

    def print_message_record(self):
        for message in self.message_record:
            role = message["role"].capitalize()
            content = message["content"]
            print(f"{role}: {content}\n")

    def prompt_model(self, prompt):
        self.message_record.append({"role": "user", "content": prompt})
        response = self.generate(self.message_record)
        self.message_record.append({"role": "assistant", "content": response})
        return response
