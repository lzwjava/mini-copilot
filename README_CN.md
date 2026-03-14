# mini-copilot (中文说明)

这是一个基于 Python 的交互式终端 REPL，用于在终端中与 GitHub Copilot 进行对话。

## 功能特性

- **多轮对话**：在终端中与 GitHub Copilot 进行持续对话。
- **GitHub OAuth 认证**：通过 GitHub 设备授权流程进行认证。
- **自动刷新**：在会话期间自动刷新 Copilot 令牌。
- **使用 GPT-4o 模型**。

## 安装步骤

```bash
git clone https://github.com/lzwjava/mini-copilot
cd mini-copilot
pip install -e .
```

## 使用说明

1. **GitHub 认证（仅需一次）**：
   ```bash
   mini-copilot-login
   ```
   这将启动 GitHub 设备授权流程，并将您的令牌保存到 `~/.config/mini-copilot/config.json`。

2. **启动 REPL**：
   ```bash
   mini-copilot
   ```

```
> 什么是 Python 中的闭包？

GitHub Copilot: 闭包是……

> 能给我个例子吗？

GitHub Copilot: 没问题！这是一个例子……
```

输入 `.exit` 或按下 `Ctrl+C` 即可退出。

## 项目结构

```
mini_copilot/
├── main.py       # 交互式 REPL
└── login.py      # CLI 登录工具

pyproject.toml    # 项目元数据和入口点
```
