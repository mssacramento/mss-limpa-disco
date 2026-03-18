#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Módulo de utilitários
Funções auxiliares para todo o projeto
"""

import os
import tempfile
from pathlib import Path
from typing import Union

def formatar_tamanho(tamanho_bytes: Union[int, float]) -> str:
    """
    Converte bytes para formato legível (KB, MB, GB, TB)

    Args:
        tamanho_bytes: Tamanho em bytes

    Returns:
        String formatada (ex: "1.5 MB")
    """
    if tamanho_bytes == 0:
        return "0 B"

    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamanho_bytes < 1024.0:
            return f"{tamanho_bytes:.2f} {unidade}"
        tamanho_bytes /= 1024.0

    return f"{tamanho_bytes:.2f} PB"

def obter_pasta_usuario() -> str:
    """Retorna o caminho da pasta do usuário"""
    return str(Path.home())

def obter_pasta_temp() -> str:
    """Retorna a pasta temporária do usuário"""
    return tempfile.gettempdir()

def garantir_execucao_admin() -> bool:
    """
    Verifica se o programa está rodando como administrador

    Returns:
        True se for admin, False caso contrário
    """
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
