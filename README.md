# Project Overview

Welcome to the House of Silent Agents.

## Environment setup and installation

The dependencies for this project are being managed using Poetry. Poetry is being run in non-package mode to avoid Poetry attempting to install the project as a package. This can be modified using the `package-mode` option in the `pyproject.toml` file.

To install the dependencies, run the following command:

```bash
poetry install
```

Documentation about poetry can be found [here](https://python-poetry.org/docs/).

## Running the project

To run the project, run the following command:

```bash
poetry run python -m house_of_silent_agents
```
