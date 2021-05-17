# OAST Project 2

[![CI](https://github.com/Adrimi/oast-ddap/actions/workflows/CI.yml/badge.svg)](https://github.com/Adrimi/oast-ddap/actions/workflows/CI.yml)

The project aims to solve DAP and DDAP with use of evolutionary algorithm.

## 0.3 Release Features:

- **fix: Link load calculation fix**
- **fix: Revert do default configuration**
- DDAP algorithm solver
- Adjusted configuration and seed
- Loading and saving XML net files
- Parsing XML Documents to Network object
- DAP algorithm solver
- Network encoder/decoder and algorithm tests

## How to run (on Linux/macOS)

To properly launch the files you need to:

1. Open project directory in CLI
2. Execute following command:

```sh
export PYTHONPATH="${PYTHONPATH}:`pwd`"
```

3. Then you can run the project, with (for e.g.):

```sh
python3 main.py
```

As long as you dont close the CLI you are fine. When you close it, then you need to repeat step 1. and 2. again :)
