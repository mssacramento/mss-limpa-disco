#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MSS Limpeza de Disco
Ponto de entrada principal do programa
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app import LimpaDiscoApp

def main():
    """Função principal que inicia o programa"""
    try:
        app = LimpaDiscoApp()
        app.run()
    except KeyboardInterrupt:
        print("\n⚠️ Programa interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
