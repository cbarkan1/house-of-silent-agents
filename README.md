# Project Overview

Welcome to the House of Silent Agents, an experiment where two LLM agents walk silently in a room, interacting only by observing one another's movements.
The experiment demonstrates that LLMs can strategize about social influence, choosing a strategy to influence the movements of the other agent in order
to achieve a goal.

A more detailed report on the project is available [here](https://docs.google.com/document/d/13vxh-wfnLAqKVTQgwLt7E273XeQWsb6Uo6DuGHUc4hs/edit?usp=sharing).

A transcript of one run of the simulation is available [here](https://cbarkan1.github.io/HOSA_log.html).

## Environment setup and installation

The dependencies for this project are managed using [uv](https://docs.astral.sh/uv/). uv can be installed with `pipx install uv`.
Once uv is installed, run `uv sync --dev` to automatically install packages and create a virtual environment.
After that, run `uv run main.py` to run the experiment.

## Viewing experiment results

After running the experiment, a `.html` log file will be created in the `logs` directory, which can be opened in any browser.
This file shows the movements of the agents after each turn, and shows the transcript of both agents, including their Chain of Thought.