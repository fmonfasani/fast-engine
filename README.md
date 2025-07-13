# fast-engine

Fast-Engine is a lightweight command line utility for quickly creating new project skeletons. It ships with a collection of example templates so you can start new services with sensible defaults in seconds.

## Installation

Install the package in editable mode:

```bash
pip install -e .
```

After installation, set the `FAST_ENGINE_HOME` environment variable to the directory where you want Fast-Engine to store generated projects and templates:

```bash
export FAST_ENGINE_HOME="$HOME/.fast-engine"
```

## Usage

To create a new project skeleton, run the init command:

```bash
fast-engine init my-service
```

The command will prompt you to choose from the example templates bundled with the repository and then create `my-service` under `FAST_ENGINE_HOME`.
