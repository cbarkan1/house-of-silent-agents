from agents.agent import Agent
from game import Game
from rooms import OneDimensionalRoom


def run(circumference, init_positions, num_turns):
    """
    Run the game with the given parameters and defined agents.
    """
    room = OneDimensionalRoom(circumference=circumference)
    agent0 = Agent(room, init_positions[0])
    agent1 = Agent(room, init_positions[1])
    game = Game(room, agent0, agent1)
    game.run_game(num_turns)
    game.generate_html(output_file="message_log.html")


if __name__ == "__main__":
    run(circumference=19, init_positions=[5, 10], num_turns=4)
    exit()
