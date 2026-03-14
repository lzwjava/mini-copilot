# Mini Copilot

A small utility using Playwright to handle GitHub device authorization.

## Overview

This project automates the [GitHub Device Login](https://github.com/login/device) flow. It uses Playwright to:
1. Navigate to the device login page.
2. Enter a provided user code.
3. Handle the authorization button clicks.
4. Capture screenshots for debugging.

## Setup

```bash
npm install
```

## Usage

Check `github_auth.js` for the automation logic. It uses a persistent browser context to maintain session state.

```bash
node github_auth.js
```

## Features

- **Automated Login**: Handles the device code entry and authorization.
- **Persistent Context**: Uses the OpenClaw browser profile.
- **Debugging**: Generates screenshots (`github-debug-*.png`) for each step.
