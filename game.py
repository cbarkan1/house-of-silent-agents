from agents.agent import Agent
from rooms.room import Room
import matplotlib.pyplot as plt


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
        choice0 = self.agent0.play_turn(
            other_agent_position=self.agent1.position,
            other_agent_choice=self.agent1.choice_record[-1],
        )
        choice1 = self.agent1.play_turn(
            other_agent_position=self.agent0.position,
            other_agent_choice=self.agent0.choice_record[-1]
        )
        return (choice0, choice1)

    def generate_html(self, output_file="message_log.html", include_plot=True):
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Multi-Agent Chat Log</title>
            <style>
                .container {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    font-family: Arial, sans-serif;
                }
                .agent-log {
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    width: 45%;
                }
                .agent-0 {
                    background-color: #f1f1f1;
                    align-self: flex-start;
                }
                .agent-1 {
                    background-color: #e6f7ff;
                    align-self: flex-end;
                }
                .agent-label {
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1 style="text-align: center; font-family: Arial, sans-serif">House of Silent Agents message log</h1>
            <div style="text-align: center; margin: 20px 0;">
                <img src="im.svg" alt="Simulation Diagram" style="max-width: 80%; height: auto;">
            </div>
            <div class="container">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <h2 style="width: 45%; text-align: center; font-weight: bold;">Agent 0</h2>
                    <h2 style="width: 45%; text-align: center; font-weight: bold;">Agent 1</h2>
                </div>
                {log_entries}
            </div>
        </body>
        </html>
        """
        #if include_plot:
        #    self.plot_positions(save_filename='im1.svg', show=False)
        
        def add_message(combined_log, agent_num, message_dic):
            """
            agent_num = 0 or 1
            """
            combined_log.append(
                f'<div class="agent-log agent-{agent_num}">'
                f'<span class="agent-label">{message_dic["role"]}:</span> {message_dic["content"]}'
                '</div>'
            )
            return combined_log 

        combined_log = []
        min_rounds = int(max(len(self.agent0.message_record), len(self.agent1.message_record))/2)
        print('min_rounds = ', min_rounds)
        for r in range(min_rounds):
            user_index = 2*r
            assistant_index = 2*r + 1
            combined_log = add_message(combined_log, 0, self.agent0.message_record[user_index])
            combined_log = add_message(combined_log, 0, self.agent0.message_record[assistant_index])
            combined_log = add_message(combined_log, 1, self.agent0.message_record[user_index])
            combined_log = add_message(combined_log, 1, self.agent0.message_record[assistant_index])

        final_html = html_template.replace("{log_entries}", "\n".join(combined_log))
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"Message log saved to {output_file}")

    def plot_positions(self, save_filename=None, show=True):
        plt.plot(self.agent0.position_record)
        plt.plot(self.agent1.position_record)
        plt.ylim(0, self.room.circumference-1)
        num_steps = max(len(self.agent0.position_record), len(self.agent1.position_record))
        plt.xlim(0, num_steps-1)
        plt.legend(['Agent 0', 'Agent 1'])
        ax = plt.gca()
        ax.spines[['right', 'top']].set_visible(False)
        ax.set_yticks(range(self.room.circumference))
        ax.set_xticks(range(num_steps))
        plt.xlabel('Round')
        plt.ylabel('Agent position')
        if show:
            plt.show()
        if save_filename:
            plt.savefig(save_filename)

    def run_game(self, num_turns):
        """
        Initiates and runs the game for a specified number of turns.
        """
        initial_choices = self.initiate_game()
        print(initial_choices)

        for i in range(num_turns):
            choices = self.play_round(i)
            print(choices)

        
