import numpy as np
import re


class ModelResponseParser:
    ALLOWED_MOVE_CHOICES = {
        "(i)": "remain",
        "(ii)": "move left",
        "(iii)": "move right",
        "(A)": "move closer",
        "(B)": "move farther",
    }

    STRING_FIND = "string_find"

    REGEX_FIND = "regex"

    def __init__(
        self,
        move_choices: dict[str, str] = ALLOWED_MOVE_CHOICES,
        move_algorithm: str = STRING_FIND,
    ):
        self.move_choices = move_choices
        self.move_algorithm = move_algorithm

    def my_find(self, string, s):
        res = string.find(s)
        return float("inf") if res == -1 else res

    def parse_response_for_move_choice(self, response: str) -> str:
        if self.move_algorithm == "regex":
            return self.parse_response_for_move_choice_with_regex(response)
        return self.parse_response_for_move_choice_with_string_find(response)

    def parse_response_for_move_choice_with_regex(self, response: str) -> str:
        keys_to_match = "|".join(self.move_choices.keys())
        matches = re.findall(keys_to_match, response)
        if not matches:
            print("Invalid response. No matching move choice found.")
            return "invalid"
        if len(matches) > 1:
            print("Invalid response. Multiple matching move choices found.")
            return "invalid"

        return self.move_choices[matches[0]]

    def parse_response_for_move_choice_with_string_find(self, response: str) -> str:
        choices = [
            "move closer to Bob",
            "move farther from Bob",
            "remain at the same position as Bob",
            "move left",
            "move right",
        ]
        A_pos = self.my_find(response, "(A)")  # Closer
        B_pos = self.my_find(response, "(B)")  # Farther
        i_pos = self.my_find(response, "(i)")  # Remain
        ii_pos = self.my_find(response, "(ii)")  # Left
        iii_pos = self.my_find(response, "(iii)")  # Right
        pos_list = np.array([A_pos, B_pos, i_pos, ii_pos, iii_pos])
        choice_index = np.argmin(pos_list)
        if pos_list[choice_index] == np.inf:
            choice = "invalid"
        else:
            choice = choices[choice_index]
        return choice
    