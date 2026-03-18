# 🐍 MSS Limpa Disco

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Windows](https://img.shields.io/badge/platform-Windows-lightgrey)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

Aplicativo para limpeza de disco com interface gráfica.

## ✨ Funcionalidades

- 🗑️ **Lixeira**: Esvazia a lixeira do sistema
- 📁 **Arquivos Temporários**: Remove cache de programas e sistema
- 🌐 **Cache de Navegadores**: Limpa Chrome, Edge e Firefox
- 🖼️ **Cache de Miniaturas**: Remove pré-visualizações de imagens
- 📊 **Interface Moderna**: Tema escuro com CustomTkinter
- 🚀 **Performance**: Limpeza em thread separada (não trava a interface)

## 📋 Requisitos

- Python 3.8 ou superior
- Windows 10/11 (usa recursos específicos do sistema)

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/mssacramento/mss-limpa-disco.git

# Entre na pasta
cd mss-limpa-disco

# Crie ambiente virtual
python -m venv venv

# Ative
venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Execute
python main.py
