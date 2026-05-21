# Midra

[简体中文](README_zh.md) | [English](README.md)

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-lightgrey.svg)](LICENSE)

**Midra 是一个面向可编辑、可控音乐生成的 agentic prompt-to-code MIDI 编曲框架。**

它将自然语言提示词转换为结构化音乐代码，再渲染为可透明检查、可修改、可复用的 MIDI 文件——不同于黑盒式端到端 AI 音频生成。

**Prompt it. Code it. MIDI it.**

## 为什么是 Midra

多数音乐生成系统直接从提示词生成音频，效果强但中间过程不透明。

Midra 提供的是 code-first 编曲范式：

- 将自然语言提示词编译为可检查的结构化音乐代码；
- 将每个阶段保存为 checkpoint JSON；
- 输出可编辑 MIDI，便于后续精修与复用。

这让 Midra 非常适合用于 **agent 编曲实验**、**人机协同编辑**、**可复现实验流程**。

## 核心模式

### 1) LLM 音符模式（`--note-mode llm`）

逐轨由模型生成音符事件，提示词对齐能力更强、变化更丰富。

### 2) 规则音符模式（`--note-mode rule`）

逐轨由规则生成器产生音符事件，结果更稳定、可重复性更好。

## 差异化能力

- **Prompt-to-code 优先**：先生成结构化符号音乐，而不是直接黑盒音频。
- **Checkpoint 原生**：每个阶段可持久化、可恢复。
- **产物可编辑**：MIDI 与 JSON 均可检查、修改、复用。
- **Agent 编排**：规划与渲染在显式阶段中执行，便于观测。

## 架构速览

- `music_agent/agents/`：意图/歌曲/编配/音符规划
- `music_agent/prompts/`：集中式提示词模板
- `music_agent/generators/`：鼓/贝斯/和弦/主旋律规则生成器
- `music_agent/core/`：Schema、MIDI IR 组装、渲染、校验
- `music_agent/utils/`：音频转换工具（`fluidsynth` / `ffmpeg`）
- `outputs/projects/`：按项目存放中间产物与最终输出

## 快速开始

### 1）安装依赖

```bash
sudo apt install ffmpeg
sudo apt install fluidsynth fluid-soundfont-gm
pip install -r requirements.txt
pip install -e .
```

### 2）配置环境变量

```bash
cp .env.example .env
```

按 [`.env.example`](.env.example:1) 默认项配置：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `OPENAI_MODEL`

可选项：

- `MAX_MUSIC_DURATION_SECONDS`

### 3）Docker 启动（前后端一体）

#### 必要配置

1. 在 [`backend/config.yaml`](backend/config.yaml) 中配置后端运行参数。
2. 通过 shell 环境变量（或 Docker Compose 读取的 `.env`）提供 OpenAI 凭证：

```bash
export OPENAI_API_KEY="your_key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-5.5"
```

3. 确保挂载目录存在：

```bash
mkdir -p backend/data outputs
```

#### 一键启动

```bash
docker compose up --build -d
```

#### 访问地址

- 前端：`http://localhost:5173`
- 后端 API：`http://localhost:8000`

#### 停止

```bash
docker compose down
```

### 4）运行（CLI）

```bash
midra "generate a 30 seconds cyberpunk boss battle bgm with drums bass chords and lead" --project-name demo --project-id test001
```

### 5）断点续运行（CLI）

```bash
midra "generate a 30 seconds cyberpunk boss battle bgm with drums bass chords and lead" --project-name demo --project-id test001 --resume
```

## 输出目录

生成产物位于：

```text
outputs/projects/demo_test001/
```

目录中包含各阶段 checkpoint JSON 与最终渲染结果。

## 路线图

- 增强长时段结构与动机一致性
- 增强可控参数与提示词约束
- 增强轨道级诊断与可观测性
- 增加更多导出/渲染选项与工作流集成

## Star This Project

如果你认同 **agentic、可编辑的 prompt-to-MIDI 生成范式**，欢迎给 Midra 一个 Star。

这将帮助项目吸引贡献者并加速可控音乐智能体研究。

## 开源协议

参见 [`LICENSE`](LICENSE)。
