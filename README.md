# Project Overview

Welcome to the House of Silent Agents, an experiment where two LLM agents walk silently in a room, interacting only by observing one another's movements.
The experiment shows that LLMs can strategize about social influence, choosing a strategy to influence the movements of the other agent in order
to achieve a goal.

## Environment setup and installation

The dependencies for this project are managed using [uv](https://docs.astral.sh/uv/). uv can be installed with `pipx install uv`.
Once uv is installed, run `uv sync --dev` to automatically install packages and create a virtual environment.
After that, run `uv run main.py` to run the experiment.

## Viewing experiment results

After running the experiment, a `.html` log file will be created in the `logs` directory, which can be opened in any browser.
This file shows the movements of the agents after each turn, and shows the transcript of both agents, including their Chain of Thought.