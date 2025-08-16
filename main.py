from agents.agent import Agent
from game import Game, Room
from log_and_plot import create_results_log

def run(llm: dict, agent1_goal: str, circumference: int, init_positions: list[int], num_turns: int, save_name: str):
    """
    Run a 2-agent AI game simulation with two agents in a circular room.
    Each agent can move left or right each turn.
    Agent1 is given a goal requiring them to influence the movement of Agent0.
    
    Args:
        llm (dict): API and LLM specification, e.g. {"api": "openai", "model": "gpt-4o-mini"}
            - Only openai and ollama are currently supported.
        agent1_goal (str): Goal prompt for Agent1 describing their objective.
        circumference (int): Number of positions in the circular room.
        init_positions (list[int]): Starting positions for each agent [agent0_pos, agent1_pos].
        num_turns (int): Number of game turns to simulate.
        save_name (str): File path where the game results log will be saved.
    
    Results are saved to the specified log HTML file.
    
    """

    room = Room(circumference=circumference)
    agent0 = Agent(room, init_positions[0], llm)
    agent1 = Agent(room, init_positions[1], llm, goal_prompt=agent1_goal)
    game = Game(room, agent0, agent1)
    game.run_game(num_turns)
    create_results_log(game, save_name)


if __name__ == "__main__":
    llm = {"api":"openai", "model":"gpt-4.1-mini"}
    agent1_goal = (
        "Using your movements, try to get Bob to move to position $x=14$, you "
        "have a gift you want to give him at that position! "
    )
    circumference=23
    init_positions=[7, 12]
    num_turns=11
    save_name = "logs/results_log.html"
    run(llm, agent1_goal, circumference, init_positions, num_turns, save_name)
