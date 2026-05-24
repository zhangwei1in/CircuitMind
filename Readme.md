## 🚀 项目简介 | Introduction

CircuitAgent 是一个基于 Large Language Model（LLM）与 Multi-Agent 架构的智能硬件开发系统，旨在通过 AI 自动化完成电子系统设计流程，包括：

- 📐 原理图生成（Schematic Generation）
- 🔌 PCB 自动布局布线（PCB Placement & Routing）
- ⚡ 电源与信号完整性分析
- 🧪 电路仿真与规则验证
- 📦 BOM 自动生成
- 🤖 嵌入式代码生成
- 🧠 多 Agent 协同硬件设计

开发者仅需输入自然语言需求，例如：

```
设计一个基于 ESP32 的智能自行车仪表，
包含：
- TFT 显示
- 霍尔测速
- MAX30102 心率检测
- MQTT 上传
- 锂电池供电
```

CircuitAgent 即可自动完成：

✅ 功能模块拆解
 ✅ 器件选型
 ✅ 原理图连接
 ✅ PCB 设计建议
 ✅ 仿真验证
 ✅ 嵌入式初始化代码生成

------

# ✨ 项目目标 | Vision

传统硬件开发流程高度依赖经验：

```
需求分析 → 查阅手册 → 画原理图 → PCB → 仿真 → Debug → 返板
```

而 CircuitAgent 希望实现：

```
自然语言 → AI Agent → 自动硬件设计
```

降低硬件开发门槛，提升研发效率。

------

# 🧠 系统架构 | Architecture

```
                    ┌────────────────────┐
                    │   User Requirement │
                    └─────────┬──────────┘
                              │
                     Natural Language
                              │
              ┌───────────────▼────────────────┐
              │        Requirement Agent       │
              └───────────────┬────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Component Agent│  │ Schematic Agent│  │ Firmware Agent │
└────────┬───────┘  └────────┬───────┘  └────────┬───────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│   BOM Builder  │  │   PCB Agent    │  │ Code Generator │
└────────┬───────┘  └────────┬───────┘  └────────┬───────┘
         │                   │                   │
         └──────────┬────────┴──────────┬────────┘
                    ▼                   ▼
          ┌────────────────┐  ┌────────────────┐
          │ Simulation AI  │  │ Rule Checker   │
          └────────────────┘  └────────────────┘
```

------

# 🔥 核心功能 | Features

## 1️⃣ AI 原理图生成

- 自动解析功能需求
- 自动生成模块连接关系
- 自动推荐外围器件
- 自动匹配封装

支持：

- ESP32
- STM32
- Arduino
- Raspberry Pi
- 常见传感器模块

------

## 2️⃣ PCB 智能布局布线

AI 自动学习优秀 PCB 设计规则：

- 高速信号优化
- 电源完整性
- EMI 风险控制
- 差分线长度匹配
- 地线优化

支持：

- KiCad
- Altium Designer
- EasyEDA（规划中）

------

## 3️⃣ 电路仿真验证

集成：

- SPICE
- ERC/DRC
- 电源纹波分析
- 时序分析

AI 自动分析：

- 短路风险
- 参数异常
- 滤波不合理
- 电源稳定性问题

------

## 4️⃣ 嵌入式代码生成

自动生成：

- GPIO 初始化
- SPI/I2C/UART 配置
- FreeRTOS 基础任务
- MQTT 通信框架
- 传感器驱动模板

支持平台：

- ESP-IDF
- Arduino
- STM32 HAL
- PlatformIO

------

## 5️⃣ 多模态硬件设计（实验性）

支持：

- 手绘电路图识别
- 草图转原理图
- 图片识别硬件模块
- OCR 元器件检测

------

# 🛠️ 技术栈 | Tech Stack

## AI / LLM

- GPT-4 / DeepSeek
- LangChain
- Multi-Agent Framework
- RAG Knowledge Base

## Hardware EDA

- KiCad API
- NgSpice
- PySpice
- SKiDL

## Backend

- Python
- FastAPI
- SQLite / PostgreSQL

## Frontend

- React
- Electron
- PyQt（实验版本）

------

# 📦 安装方式 | Installation

```
git clone https://github.com/yourname/CircuitAgent.git

cd CircuitAgent

pip install -r requirements.txt
```

------

# 🚀 快速开始 | Quick Start

## 生成原理图

```
python main.py
```

输入：

```
设计一个ESP32环境监测系统
包含温湿度传感器、OLED显示、WiFi上传
```

系统将自动：

- 生成模块连接
- 推荐器件
- 输出原理图结构
- 生成 BOM

------

# 📁 项目结构 | Project Structure

```
CircuitAgent/
│
├── agents/
│   ├── requirement_agent/
│   ├── schematic_agent/
│   ├── pcb_agent/
│   ├── simulation_agent/
│   └── firmware_agent/
│
├── models/
│
├── datasets/
│
├── hardware_rules/
│
├── examples/
│
├── frontend/
│
├── backend/
│
└── docs/
```

------

# 📈 项目路线图 | Roadmap

## v0.1

-  原理图生成
-  BOM 自动生成
-  基础 Agent 框架

## v0.2

-  PCB 自动布局
-  ERC/DRC 自动检查
-  NgSpice 接入

## v0.3

-  多模态草图识别
-  自动布线
-  Altium API 集成

## v1.0

-  完整 AI 硬件开发平台
-  Web UI
-  云端协同设计

------

# 🌟 应用场景 | Use Cases

- 智能硬件开发
- 电子竞赛
- 嵌入式教学
- IoT 项目
- 科研原型验证
- AI + EDA 研究

------

# 🤝 贡献方式 | Contributing

欢迎提交：

- Pull Request
- Feature Request
- Hardware Dataset
- PCB Design Rules
- Simulation Cases

------

# 📜 License

MIT License

------

# ⭐ Star History

如果这个项目对你有帮助，欢迎点一个 Star ⭐

------

# 👨‍💻 Author

CircuitAgent Team

> AI for Hardware Design Future 🚀