import matplotlib.pyplot as plt
import io
from game import Game

def create_results_log(game: Game, output_file: str, include_plot=True):
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Results Log</title>
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
        <h1 style="text-align: center; font-family: Arial, sans-serif">House of Silent Agents Results Log</h1>
        <div style="text-align: center; margin: 20px 0;">
            {svg_image}
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
    if include_plot:
        svg_data = plot_positions(game, show=False, return_svg_data=True)
        html_template = html_template.replace("{svg_image}", svg_data)
    else:
        html_template = html_template.replace("{svg_image}", "")
    
    def add_message(combined_log, agent_num, message_dic):
        """
        agent_num = 0 or 1
        """
        content_with_br = message_dic["content"].replace("\n", "<br>")
        combined_log.append(
            f'<div class="agent-log agent-{agent_num}">'
            f'<span class="agent-label">{message_dic["role"]}:</span> {content_with_br}'
            '</div>'
        )
        return combined_log 

    combined_log = []
    add_message(combined_log, 0, game.agent0.message_record[0])
    add_message(combined_log, 1, game.agent1.message_record[0])

    min_rounds = int(max(len(game.agent0.message_record), len(game.agent1.message_record))/2)
    print('min_rounds = ', min_rounds)
    for r in range(min_rounds):
        user_index = 2*r + 1
        assistant_index = 2*r + 2
        combined_log = add_message(combined_log, 0, game.agent0.message_record[user_index])
        combined_log = add_message(combined_log, 0, game.agent0.message_record[assistant_index])
        combined_log = add_message(combined_log, 1, game.agent1.message_record[user_index])
        combined_log = add_message(combined_log, 1, game.agent1.message_record[assistant_index])

    html_template = html_template.replace("{log_entries}", "\n".join(combined_log))
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Results log saved to {output_file}")

def plot_positions(game: Game, show=True, return_svg_data=False):
    plt.figure()
    plt.plot(game.agent0.position_record)
    plt.plot(game.agent1.position_record)
    plt.ylim(0, game.room.circumference-1)
    num_steps = max(len(game.agent0.position_record), len(game.agent1.position_record))
    plt.xlim(0, num_steps-1)
    plt.legend(['Agent 0', 'Agent 1'])
    ax = plt.gca()
    ax.spines[['right', 'top']].set_visible(False)
    ax.set_yticks(range(game.room.circumference))
    ax.set_xticks(range(num_steps))
    plt.xlabel('Round')
    plt.ylabel('Agent position')
    return_data = None
    if return_svg_data:        
        buffer = io.StringIO()
        plt.savefig(buffer, format='svg')
        return_data = buffer.getvalue()
        buffer.close()
    if show:
        plt.show()
    return return_data
