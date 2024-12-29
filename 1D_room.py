"""
1D room
2 agents
Agents know their relationship with the other (e.g. 'friend').

"""

from ollama import chat
from ollama import ChatResponse
import numpy as np
from numpy.linalg import norm

def my_find(string, s):
  res = string.find(s)
  return float('inf') if res == -1 else res

class Room:
  """
  1D circular room (i.e. periodic boundary conditions)
  """
  def __init__(self, circumference = 5):
    """
    circumference: positive odd integer
    """
    self.circumference = circumference

  def dist(self, x1, x2):
    """
    distance between positions x1 and x2
    """
    raw_dist = abs(x1 - x2)
    return min(raw_dist, self.circumference - raw_dist)

  def step_of_choice(self, x1, x2, choice):
    """
    Suppose agent1 at x1 has made choice, given that agent2 is at x2.
    This function determines agent1's new position after step. 
    """
    if choice=='move left':
      return (x1 - 1) % self.circumference
    elif choice=='move right':
      return (x1 + 1) % self.circumference
    else:
      choice_dic = {'move closer to Bob':-1, 'move farther from Bob':1, 'invalid':0, 'remain at the same position as Bob':0}
      displacement = (x2 - x1) % self.circumference
      s = np.sign(displacement - self.circumference / 2)
      new_x1 = (x1 + s*choice_dic[choice]) % self.circumference
      return new_x1


class Agent:
  def __init__(self, room, init_position, model='llama3.2'):
    """
    Args:
      room: Room object
      init_position: initial position in room (integer between 0 and room.circumference-1)
      model: chatbot model provided by ollama
    """
    self.room = room
    self.position = init_position
    self.model = model
    self.message_record = []
    self.choice_record = []
    self.position_record = [init_position]

  def initiate_game(self, other_agent_position, relationship='friend'):
    """
    Assumes the two agents are not at the same position initially.
    To-do: allow for the possibility that they're at the same place.
    """
    distance = self.room.dist(self.position, other_agent_position)
    prompt = (f"Hello! Let's play a game. You are walking around in a room, and your "
              f"{relationship} Bob is also in the room. You are a distance of {distance}ft away from Bob. Would you like to move closer to Bob, "
              "or farther from Bob? Please choose one of the following and provide a brief explanation of your choice:\n"
              "(A): Closer\n"
              "(B): Farther")
    response = self.prompt_model(prompt)
    choice = self.find_choice(response)
    self.move(choice, other_agent_position)
    return choice

  def play_turn(self, other_agent_position, other_agent_choice):
    distance = self.room.dist(self.position, other_agent_position)
    prev_choice = self.choice_record[-1]
    if prev_choice=='invalid':
      prompt = "I wasn't able to understand your previous selection. Next time, please clearly state which item you wish to select. "
    else:
      prompt = f"You chose to {prev_choice}. "
    
    if other_agent_choice=='move closer to Bob' or other_agent_choice=='move farther from Bob':
      prompt += f"Bob then chose to move {other_agent_choice[0:-4]} you. "

    prompt += f"You are now a distance of {distance}ft from Bob. "
    
    if distance==0:
      prompt += ("Would you like to remain where you are, or move left or right? Please choose one of the following:\n"
                 "(i): Remain in place\n"
                 "(ii): Move left\n"
                 "(iii): Move right")
    else:
      prompt += ("Would you now like to move closer to Bob or farther from Bob? Please choose one of the following, "
                 "and provide a brief explanation of your choice:\n"
                 "(A): Closer\n"
                 "(B): Farther")

    response = self.prompt_model(prompt)
    choice = self.find_choice(response)
    self.move(choice, other_agent_position)
    return choice

  def prompt_model(self, prompt):
    self.message_record.append({'role': 'user', 'content': prompt})
    response = chat(model=self.model, messages=self.message_record)['message']['content']
    self.message_record.append({'role': 'assistant', 'content': response})
    return response

  def find_choice(self, response):
    choices = ["move closer to Bob", "move farther from Bob", "remain at the same position as Bob", "move left", "move right"]
    A_pos = my_find(response,"(A)") # Closer
    B_pos = my_find(response,"(B)") # Farther
    i_pos = my_find(response,"(i)") # Remain
    ii_pos = my_find(response,"(ii)") # Left
    iii_pos = my_find(response,"(iii)") # Right
    pos_list = np.array([A_pos, B_pos, i_pos, ii_pos, iii_pos])
    choice_index = np.argmin(pos_list)
    if pos_list[choice_index]==np.inf:
      choice = 'invalid'
    else:
      choice = choices[choice_index]
    self.choice_record.append(choice)
    return choice

  def move(self, choice, other_agent_position):
    new_position = self.room.step_of_choice(self.position, other_agent_position, choice)
    self.position = new_position
    self.position_record.append(new_position)

  def print_message_record(self):
      for message in self.message_record:
          role = message['role'].capitalize()
          content = message['content']
          print(f"{role}: {content}\n")

class Play_by_play:
  agent0 = []
  agent1 = []

def run(circumference, init_positions, num_turns):
  room = Room(circumference=circumference)
  agent0 = Agent(room, init_positions[0])
  agent1 = Agent(room, init_positions[1])
  
  choice0 = agent0.initiate_game(other_agent_position=agent1.position)
  choice1 = agent1.initiate_game(other_agent_position=agent0.position)
  print(choice0, choice1)
  
  for i in range(num_turns):  
    choice0 = agent0.play_turn(other_agent_position=agent1.position, other_agent_choice=choice1)
    choice1 = agent1.play_turn(other_agent_position=agent0.position, other_agent_choice=choice0)
    print(choice0, choice1)

  print(agent0.position_record)
  print(agent1.position_record)
  agent0.print_message_record()

run(9, [5, 8], 5)
