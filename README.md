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
If you want this variable available in every shell session, append the export
line to your `~/.bashrc` (or equivalent shell rc file) as well.

## Usage

To create a new project skeleton, run the init command:

```bash
fast-engine init my-service
```

The command will prompt you to choose from the example templates bundled with the repository and then create `my-service` under `FAST_ENGINE_HOME`.

### Example walk-through

Running the following command generates a project called `my-service` using the
default `saas-basic` template:

```bash
fast-engine init my-service
```

You will see messages showing the simulated generation steps, followed by a list
of files written into `FAST_ENGINE_HOME/my-service`. Once the process finishes,
enter the new directory and start your service with `python main.py` or via the
provided `docker-compose.yml`.

### Template structure

Templates live in the `templates/` directory. Each template has its own folder
containing a `template.yml` descriptor and any files organised by component. For
example, the bundled `saas-basic` template includes `backend/`, `frontend/` and
`devops/` directories with Jinja2 files:

```
templates/
└── saas-basic/
    ├── backend/
    │   └── app.py.j2
    ├── frontend/
    │   └── index.html.j2
    ├── devops/
    │   └── Dockerfile.j2
    └── template.yml
```

### Adding your own template

To create a custom template, add a new folder under `FAST_ENGINE_HOME/templates`
following the same layout as above and supply a `template.yml` file describing
the template. Fast‑Engine will then recognise the template name when you run
`fast-engine init` with the `--template` option.

