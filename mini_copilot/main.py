#!/usr/bin/env python3
import json
import sys
import time
from pathlib import Path

import requests

CONFIG_PATH = Path.home() / ".config" / "mini-copilot" / "config.json"
TOKEN_REFRESH_INTERVAL = 24 * 60  # seconds (~24 minutes)


def load_github_token():
    if not CONFIG_PATH.exists():
        print("No token found. Run `mini-copilot-login` first.", file=sys.stderr)
        sys.exit(1)
    config = json.loads(CONFIG_PATH.read_text())
    if not config.get("github_token"):
        print(
            "Invalid config: missing github_token. Run `mini-copilot-login` first.",
            file=sys.stderr,
        )
        sys.exit(1)
    return config["github_token"]


def get_copilot_token(github_token):
    resp = requests.get(
        "https://api.github.com/copilot_internal/v2/token",
        headers={
            "Authorization": f"Bearer {github_token}",
            "Editor-Version": "vscode/1.85.0",
            "Editor-Plugin-Version": "copilot/1.155.0",
            "User-Agent": "GithubCopilot/1.155.0",
        },
    )
    if not resp.ok:
        raise RuntimeError(
            f"Failed to get Copilot token: {resp.status_code} {resp.reason}"
        )
    return resp.json()["token"]


def chat(messages, copilot_token):
    resp = requests.post(
        "https://api.githubcopilot.com/chat/completions",
        headers={
            "Authorization": f"Bearer {copilot_token}",
            "Content-Type": "application/json",
            "Editor-Version": "vscode/1.85.0",
            "Editor-Plugin-Version": "copilot/1.155.0",
            "User-Agent": "GithubCopilot/1.155.0",
            "Copilot-Integration-Id": "vscode-chat",
        },
        json={"model": "gpt-4o", "messages": messages, "stream": False},
    )
    if not resp.ok:
        raise RuntimeError(
            f"Chat API error: {resp.status_code} {resp.reason}\n{resp.text}"
        )
    return resp.json()["choices"][0]["message"]["content"]


def main():
    github_token = load_github_token()

    print("Connecting to GitHub Copilot...")
    copilot_token = get_copilot_token(github_token)
    token_expiry = time.monotonic() + TOKEN_REFRESH_INTERVAL

    messages = []

    print("GitHub Copilot CLI ready. Type your message or .exit to quit.\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input == ".exit":
            print("Goodbye!")
            break

        try:
            if time.monotonic() >= token_expiry:
                copilot_token = get_copilot_token(github_token)
                token_expiry = time.monotonic() + TOKEN_REFRESH_INTERVAL

            messages.append({"role": "user", "content": user_input})
            reply = chat(messages, copilot_token)
            messages.append({"role": "assistant", "content": reply})

            print(f"\nGitHub Copilot: {reply}\n")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
