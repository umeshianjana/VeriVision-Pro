# ⚡ VeriVision Pro: AI-Assisted Hardware Verification & RTL Visualizer Suite

> **Empowering Hardware Engineers & Startup Founders with Automated RTL Logic Visualization and Static Linting**

VeriVision Pro is an interactive, browser-based EDA tool designed to bridge the gap between HDL design and hardware verification. It transforms complex Verilog logic into intuitive visual block diagrams, performs real-time static logic checks, and leverages AI suggestions to streamline chip design debugging.

---

## 🎯 The Problem
Hardware engineering and FPGA design have traditionally suffered from high entry barriers:
- Complex syntax debugging without instant visual feedback.
- Expensive commercial EDA tools inaccessible to indie developers and early-stage hardware startups.
- Time-consuming identification of unmapped signals and blocking assignment bugs.

## 💡 The Solution & Key Features
- **🖼️ Automated RTL Logic Visualization**: Parses Verilog AST structures dynamically to draw circuit schematics via Graphviz.
- **🔍 Static Hardware Linter**: Catches unused signals, un-driven wires, and clock-edge blocking assignment warnings instantly.
- **💡 AI Auto-Fix Assistant**: Provides clean, corrected Verilog code previews ready for production.
- **📊 Hardware Symbol Hierarchy**: Generates real-time AST summaries and signal metrics (Inputs, Outputs, Wires, Registers).
- **📥 One-Click Export**: Allows exporting designs directly as `.v` files for simulation tools like ModelSim and Vivado.

---

## 🛠️ Tech Stack & Architecture
- **Frontend & App Framework**: Streamlit (Python)
- **RTL Parser Engine**: Regular Expression Syntax Pattern Engine
- **Schematic Renderer**: Graphviz Engine
- **Static Analysis Module**: Python-based AST Verification Logic

---

## 💼 Business Model & Sustainability Strategy
VeriVision Pro is structured as a scalable B2B SaaS startup tool:

1. **Freemium Tier (Open Source)**:
   - Free for students, researchers, and open-source FPGA developers.
2. **Pro Designer Tier ($19/month)**:
   - Deep LLM-driven AI synthesis explanations, full testbench generation, and SystemVerilog support.
3. **Enterprise & Startup Suite ($149/month per team)**:
   - On-premise CI/CD linting integration, GitHub Actions plugin, and proprietary IP block protection.

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.9+
- Graphviz installed on system path

### Installation & Running Locally
```bash
# Clone repository
git clone https://github.com/umeshianjana/VeriVision-Pro.gitcd VeriVision-Pro

# Install dependencies
pip install streamlit graphviz

# Run application
streamlit run app.py
