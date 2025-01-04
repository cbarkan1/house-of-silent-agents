def generate_html_log(self, output_file="chat_log.html"):
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
        <h1>Multi-Agent Simulation Log</h1>
        <div class="container">
            {log_entries}
        </div>
    </body>
    </html>
    """
    
    combined_log = []
    min_rounds = int(max(len(self.agent0.message_record), len(self.agent1.message_record))/2)
    print('min_rounds = ', min_rounds)
    for r in range(min_rounds):
        # agent0
        user_index = 2*r
        assistant_index = 2*r + 1

        combined_log.append(
            f'<div class="agent-log agent-0">'
            f'<span class="agent-label">agent_0 - user:</span> {self.agent0.message_record[user_index]["content"]}</div>'
        )
        combined_log.append(
            f'<div class="agent-log agent-0">'
            f'<span class="agent-label">agent_0 - assistant:</span> {self.agent0.message_record[assistant_index]["content"]}</div>'
        )

        # agent1
        combined_log.append(
            f'<div class="agent-log agent-1">'
            f'<span class="agent-label">agent_1 - user:</span> {self.agent1.message_record[user_index]["content"]}</div>'
        )
        combined_log.append(
            f'<div class="agent-log agent-1">'
            f'<span class="agent-label">agent_1 - assistant:</span> {self.agent1.message_record[assistant_index]["content"]}</div>'
        )


    # Generate final HTML by inserting the combined log entries
    final_html = html_template.replace("{log_entries}", "\n".join(combined_log))

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"HTML log saved to {output_file}")