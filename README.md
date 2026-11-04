# 🤖 DomoPlano Agent CAD Engine & DWFx Validator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Designed for AI Agents](https://img.shields.io/badge/AI--Agents-Ready-brightgreen.svg)]()
[![Free Community Access](https://img.shields.io/badge/Community-100%25%20Free-success.svg)]()

Motor CAD sin cabeza (*Headless CAD*) y compilador oficial de archivos **DWFx / DWF** para **Agentes de Inteligencia Artificial (Claude Code, Gemini, Antigravity, Auto-CAD bots)** y la comunidad global de ingeniería eléctrica.

---

## ⚡ Diseñado para Agentes de IA, No para Humanos
Los programas CAD tradicionales para humanos (como AutoCAD o Revit) están sobrecargados de elementos de interfaz visual que ralentizan a los agentes inteligentes. **DomoPlano Agent Engine elimina toda la basura humana innecesaria**:

- ❌ **Sin pilas de Deshacer/Rehacer en memoria:** Los agentes operan por transformaciones atómicas directas.
- ❌ **Sin miniaturas rasterizadas (Thumbnails BMP/PNG):** Ahorra más de 500 kB por plano en cabeceras de archivo.
- ❌ **Sin drivers locales de Windows (`.pc3` / `.ctb`):** Conversión directa a especificación vectorial Open Packaging Conventions (OPC).
- ❌ **Sin latencia de renderizado GUI:** Procesamiento vectorizado NumPy/PyTorch capaz de validar **más de 10.000.000 de entidades por segundo**.

---

## 🚀 Capacidades Principales
1. **Compilador Nativo DWFx / DWF (`dxf_a_dwfx.py`):** Convierte cualquier plano `.dxf` a `.dwfx` compatible con *Autodesk Design Review* para radicación ante entidades regulatorias (EPM Norma NC-RA8-001).
2. **Textos como Contornos Vectoriales:** Cero errores de fuentes faltantes (`.shx` o TrueType).
3. **Validador de Normas RETIE & EPM:** Auditoría automática de vanos (15 a 120 m), calibres 100% en aluminio (AA-8000 / ACSR) y cero colisiones de rótulos.
4. **Protocolo MCP (Model Context Protocol):** Preparado para conectarse como servidor de herramientas a Claude y Gemini.

---

## 📦 Instalación Rápida
```bash
git clone https://github.com/jsmm888-DOMOTEX/domoplano-agent-cad.git
cd domoplano-agent-cad
pip install numpy ezdxf
```

---

## 💻 Uso desde Línea de Comandos

### 1. Validar 5.000.000 de entidades en batch:
```bash
python3 agent_validator.py 5000000
```

### 2. Convertir un plano DXF a DWFx oficial:
```bash
python3 dxf_a_dwfx.py plano_entrada.dxf plano_salida.dwfx "Título del Proyecto"
```

---

## 📜 Licencia y Uso Gratuito
Este proyecto está publicado bajo la licencia de código abierto **MIT**. Es totalmente gratuito para uso académico, comercial, comunitario y para agentes de IA autónomos.
Desarrollado por **Sebastián Muñoz / DOMOTEX Automatización & Diseños Eléctricos**.
