# mini-copilot

An interactive terminal REPL for chatting with GitHub Copilot, built with Python.

## Features

- Multi-turn conversations with GitHub Copilot in your terminal
- GitHub OAuth device flow authentication
- Automatic Copilot token refresh during session
- GPT-4o model

## Installation

```bash
git clone https://github.com/lzwjava/mini-copilot
cd mini-copilot
pip install -e .
```

## Usage

1. Authenticate with GitHub (once):
   ```bash
   mini-copilot-login
   ```
   This runs the GitHub device authorization flow and saves your token to `~/.config/mini-copilot/config.json`.

2. Start the REPL:
   ```bash
   mini-copilot
   ```

```
> What is a closure in Python?

GitHub Copilot: A closure is ...

> Can you give me an example?

GitHub Copilot: Sure! Here's an example ...
```

Type `.exit` or press `Ctrl+C` to quit.

## Project Structure

```
mini_copilot/
├── main.py       # Interactive REPL
└── login.py      # CLI login utility

pyproject.toml    # Package metadata and entry points
```

