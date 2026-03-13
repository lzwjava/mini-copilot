# mini-copilot

An interactive terminal REPL for chatting with GitHub Copilot, built with Python.

## Features

- Multi-turn conversations with GitHub Copilot in your terminal
- GitHub OAuth device flow authentication
- Automatic Copilot token refresh during session
- GPT-4o model

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Authenticate with GitHub:
   ```bash
   python scripts/login.py
   ```
   This runs the GitHub device authorization flow and saves your token to `public/config.json`.

3. Start the REPL:
   ```bash
   python src/mini_copilot.py
   ```

## Usage

```
> What is a closure in Python?

GitHub Copilot: A closure is ...

> Can you give me an example?

GitHub Copilot: Sure! Here's an example ...
```

Type `.exit` or press `Ctrl+C` to quit.

## Project Structure

```
scripts/
└── login.py            # CLI login utility

src/
└── mini_copilot.py     # Interactive REPL

public/
└── config.json         # Generated token store (gitignored)

requirements.txt        # Python dependencies
```
