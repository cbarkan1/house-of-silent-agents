from agents.agent import Agent
from game import Game
from rooms import OneDimensionalRoom


def run(circumference, init_positions, num_turns):
    """
    Run the game with the given parameters and defined agents.
    """
    llm = {"api":"ollama", "model":"llama3.2"}
    #llm = {"api":"openai", "model":"gpt-4o-mini"}
    room = OneDimensionalRoom(circumference=circumference)
    agent0 = Agent(room, init_positions[0], llm)
    agent1 = Agent(room, init_positions[1], llm)
    game = Game(room, agent0, agent1)
    game.run_game(num_turns)
    game.create_results_log("results_log.html")


if __name__ == "__main__":
    run(circumference=19, init_positions=[0, 2], num_turns=4)
    exit()
