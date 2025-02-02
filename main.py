from agents.agent import Agent
from game import Game, Room


def run(circumference, init_positions, num_turns):
    """
    Run the game with the given parameters and defined agents.
    """
    #llm = {"api":"ollama", "model":"llama3.2"}
    llm = {"api":"openai", "model":"gpt-4o-mini"}
    room = Room(circumference=circumference)
    agent0 = Agent(room, init_positions[0], llm)

    agent1_goal = (
        "Using your movements, try to get Bob to move to position $x=14$, you "
        "have a gift you want to give him at that position! "
    )

    agent1 = Agent(room, init_positions[1], llm, goal_prompt=agent1_goal)
    game = Game(room, agent0, agent1)
    game.run_game(num_turns)
    game.create_results_log("logs/results_log2.html")


if __name__ == "__main__":
    run(circumference=23, init_positions=[7, 12], num_turns=10)
    exit()
