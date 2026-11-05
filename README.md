# 🤖 DomoPlano Agent CAD Engine & DWFx Validator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![AI-Agents Ready](https://img.shields.io/badge/AI--Agents-Ready-brightgreen.svg)](https://github.com/jsmm888-DOMOTEX/domoplano-agent-cad)
[![Community 100% Free](https://img.shields.io/badge/Community-100%25%20Free-success.svg)](https://github.com/jsmm888-DOMOTEX/domoplano-agent-cad)

> **High-performance headless CAD engine and official DWFx/DWF compiler for Autonomous AI Agents (Claude, Gemini, Antigravity, CAD bots) and the global electrical engineering community.**

[📖 **English Version**](#-english-documentation) | [📖 **Versión en Español**](#-documentación-en-español)

---

## 🌐 English Documentation

### ⚡ High-Performance Architecture for AI Agents & Modern Engineering

Traditional desktop CAD software is primarily designed for interactive manual drafting with mouse and keyboard, often bundling heavy graphical user interface layers, extensive undo/redo history stacks, and proprietary local drivers.

**DomoPlano Agent Engine** streamlines this environment, providing a clean, headless, high-precision CAD foundation tailored for **autonomous AI agents** and **engineering teams**:

- ✨ **Direct Atomic Operations:** Deterministic, state-isolated geometry transformations that execute instantly without memory overhead.
- ✨ **Clean Vector Headers:** Stripped of heavy raster preview thumbnails, saving over 500 kB per sheet in file headers.
- ✨ **Open Packaging Conventions (OPC):** Direct native conversion to vector DWFx/DWF standards without requiring local Windows print drivers (`.pc3` / `.ctb`).
- ✨ **High-Throughput Processing:** Vectorized pipeline powered by NumPy capable of auditing and validating **over 10,000,000 entities per second**.

---

### 🚀 Key Capabilities

1. **Native DWFx / DWF Compiler (`dxf_a_dwfx.py`):** Converts any standard `.dxf` drawing into official `.dwfx` files compatible with *Autodesk Design Review* for regulatory utility filing (EPM NC-RA8-001 & RETIE).
2. **Vector Outline Fonts:** Replaces missing font errors (`.shx` / TrueType) with native, pure vector geometry.
3. **Automated Regulatory Auditing:** Verifies overhead distribution spans (15 m to 120 m), 100% aluminum conductors (AA-8000 / ACSR), and zero-collision title blocks.
4. **Model Context Protocol (MCP) Ready:** Connects seamlessly as a precision CAD tool server for Claude, Gemini, Antigravity, and custom LLM workflows.

---

### 📦 Quick Start & Installation

```bash
git clone https://github.com/jsmm888-DOMOTEX/domoplano-agent-cad.git
cd domoplano-agent-cad
pip install numpy ezdxf
```

---

### 💻 Command-Line Usage

#### 1. Validate 5,000,000 entities in high-speed batch:
```bash
python3 agent_validator.py 5000000
```

#### 2. Convert a DXF plan to official DWFx format:
```bash
python3 dxf_a_dwfx.py input_drawing.dxf output_drawing.dwfx "Project Title"
```

---

### 📜 Open Source & Free Community License

This project is licensed under the open-source **MIT License**. It is completely free for academic, commercial, community use, and autonomous AI agents.  
Developed by **Sebastián Muñoz / DOMOTEX Automation & Electrical Design**.

---

<br><br>

---

## 🇪🇸 Documentación en Español

### ⚡ Arquitectura de Alto Rendimiento para Agentes de IA e Ingeniería Moderna

Los programas CAD tradicionales de escritorio están diseñados primordialmente para la interacción manual con ratón y teclado, incorporando capas visuales de interfaz, cachés de deshacer en memoria y dependencias de controladores propietarios.

**DomoPlano Agent Engine** optimiza este flujo de trabajo brindando una base liviana, precisa y sin entorno gráfico (*Headless*), diseñada para potenciar tanto a **agentes autónomos de IA** como a **equipos de ingeniería**:

- ✨ **Operaciones Atómicas Directas:** Transformaciones vectoriales deterministas y de respuesta inmediata, ideales para ejecución por agentes inteligentes.
- ✨ **Archivos Limpios y Ligeros:** Libres de miniaturas rasterizadas pesadas, reduciendo más de 500 kB por plano en cabeceras de archivo.
- ✨ **Estándares Vectoriales Abiertos (OPC):** Conversión directa a especificaciones oficiales DWFx sin depender de controladores locales de impresión (`.pc3` / `.ctb`).
- ✨ **Procesamiento Vectorizado:** Motor de alta velocidad capaz de auditar y validar **más de 10.000.000 de entidades por segundo**.

---

### 🚀 Capacidades Principales

1. **Compilador Nativo DWFx / DWF (`dxf_a_dwfx.py`):** Convierte cualquier plano `.dxf` a `.dwfx` compatible con *Autodesk Design Review* para radicación ante entidades regulatorias (EPM Norma NC-RA8-001 y RETIE).
2. **Textos como Contornos Vectoriales:** Cero errores de fuentes faltantes (`.shx` o TrueType).
3. **Validador de Normas RETIE & EPM:** Auditoría automática de vanos (15 a 120 m), calibres 100% en aluminio (AA-8000 / ACSR) y cero colisiones de rótulos.
4. **Protocolo MCP (Model Context Protocol):** Preparado para conectarse como servidor de herramientas a Claude, Gemini y Antigravity.

---

### 📦 Instalación Rápida
```bash
git clone https://github.com/jsmm888-DOMOTEX/domoplano-agent-cad.git
cd domoplano-agent-cad
pip install numpy ezdxf
```

---

### 💻 Uso desde Línea de Comandos

#### 1. Validar 5.000.000 de entidades en batch:
```bash
python3 agent_validator.py 5000000
```

#### 2. Convertir un plano DXF a DWFx oficial:
```bash
python3 dxf_a_dwfx.py plano_entrada.dxf plano_salida.dwfx "Título del Proyecto"
```

---

### 📜 Licencia y Uso Gratuito
Este proyecto está publicado bajo la licencia de código abierto **MIT**. Es totalmente gratuito para uso académico, comercial, comunitario y para agentes de IA autónomos.  
Desarrollado por **Sebastián Muñoz / DOMOTEX Automatización & Diseños Eléctricos**.
