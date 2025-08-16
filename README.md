# House of Silent Agents

An experiment where two LLM agents walk silently in a room, interacting only by observing each other's movements. The experiment demonstrates that LLMs can strategize about social influence, choosing strategies to influence the other agent's movements to achieve their goal.

**Links:**
- [More detailed report](https://docs.google.com/document/d/13vxh-wfnLAqKVTQgwLt7E273XeQWsb6Uo6DuGHUc4hs/edit?usp=sharing)
- [Example simulation transcript](https://cbarkan1.github.io/HOSA_log.html)

## Installation and Setup

Dependencies: Python 3.9+, matplotlib, openai, python-dotenv

### Quick Start with uv
1. Clone the repository
2. Install dependencies: `uv sync`
3. Set up your OpenAI API key in a `.env` file: `OPENAI_API_KEY=your_key_here`
4. Run the experiment: `uv run main.py`

## Experiment Results

The experiment generates an HTML log file in the `logs/` directory showing:
- Agent movements after each turn
- Complete transcript of both agents' chain of thought