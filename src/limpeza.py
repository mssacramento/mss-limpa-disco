#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Módulo de limpeza do sistema
Contém todas as classes responsáveis pela limpeza de disco
"""

import os
import shutil
import winshell
import psutil
from pathlib import Path
from typing import List, Tuple, Dict, Optional
from abc import ABC, abstractmethod

from utils import formatar_tamanho, obter_pasta_usuario, obter_pasta_temp


class LimpezaBase(ABC):
    """Classe base abstrata para todas as limpezas"""

    def __init__(self):
        self.nome = self.__class__.__name__
        self.espaco_liberado = 0
        self.arquivos_removidos = 0
        self.mensagens = []

    @abstractmethod
    def executar(self) -> bool:
        """Método abstrato que executa a limpeza"""
        pass

    def get_resultado(self) -> str:
        """Retorna o resultado formatado da limpeza"""
        if self.espaco_liberado > 0:
            return f"✅ {self.nome}: {formatar_tamanho(self.espaco_liberado)} ({self.arquivos_removidos} arquivos)"
        return f"ℹ️ {self.nome}: nenhum arquivo encontrado"

    def _get_folder_size(self, pasta: str) -> int:
        """Calcula tamanho total de uma pasta"""
        total = 0
        try:
            for root, dirs, files in os.walk(pasta):
                for file in files:
                    try:
                        filepath = os.path.join(root, file)
                        total += os.path.getsize(filepath)
                    except:
                        continue
        except:
            pass
        return total


class LimpezaLixeira(LimpezaBase):
    """Classe responsável por limpar a lixeira"""

    def __init__(self):
        super().__init__()
        self.nome = "Lixeira"

    def executar(self) -> bool:
        try:
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.mensagens.append("✅ Lixeira limpa com sucesso")
            return True
        except Exception as e:
            self.mensagens.append(f"❌ Lixeira: erro - {str(e)}")
            return False


class LimpezaTemporarios(LimpezaBase):
    """Classe responsável por limpar arquivos temporários"""

    def __init__(self):
        super().__init__()
        self.nome = "Arquivos Temporários"

    def executar(self) -> bool:
        try:
            temp_pastas = [
                obter_pasta_temp(),
                os.path.join(obter_pasta_usuario(), "AppData", "Local", "Temp")
            ]

            for pasta in temp_pastas:
                if os.path.exists(pasta):
                    for root, dirs, files in os.walk(pasta, topdown=False):
                        for arquivo in files:
                            caminho = os.path.join(root, arquivo)
                            try:
                                if os.path.isfile(caminho):
                                    self.espaco_liberado += os.path.getsize(caminho)
                                    os.remove(caminho)
                                    self.arquivos_removidos += 1
                            except:
                                continue

                        for diretorio in dirs:
                            try:
                                caminho_pasta = os.path.join(root, diretorio)
                                os.rmdir(caminho_pasta)
                            except:
                                continue

            return True
        except Exception as e:
            self.mensagens.append(f"❌ Temporários: erro - {str(e)}")
            return False


class LimpezaCacheNavegadores(LimpezaBase):
    """Classe responsável por limpar cache dos navegadores"""

    def __init__(self):
        super().__init__()
        self.nome = "Cache Navegadores"

    def executar(self) -> bool:
        try:
            usuario = obter_pasta_usuario()

            caches = [
                ("Chrome", os.path.join(usuario, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Cache")),
                ("Chrome Code", os.path.join(usuario, "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Code Cache")),
                ("Edge", os.path.join(usuario, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Cache")),
                ("Edge Code", os.path.join(usuario, "AppData", "Local", "Microsoft", "Edge", "User Data", "Default", "Code Cache")),
            ]

            for nome, cache in caches:
                if os.path.exists(cache):
                    tamanho = self._get_folder_size(cache)
                    if tamanho > 0:
                        try:
                            shutil.rmtree(cache)
                            self.espaco_liberado += tamanho
                            self.arquivos_removidos += 1
                        except:
                            continue

            # Firefox
            firefox_profiles = os.path.join(usuario, "AppData", "Local", "Mozilla", "Firefox", "Profiles")
            if os.path.exists(firefox_profiles):
                for perfil in os.listdir(firefox_profiles):
                    cache_firefox = os.path.join(firefox_profiles, perfil, "cache2")
                    if os.path.exists(cache_firefox):
                        tamanho = self._get_folder_size(cache_firefox)
                        if tamanho > 0:
                            try:
                                shutil.rmtree(cache_firefox)
                                self.espaco_liberado += tamanho
                                self.arquivos_removidos += 1
                            except:
                                continue

            return True
        except Exception as e:
            self.mensagens.append(f"ℹ️ Navegadores: erro ao verificar")
            return False


class LimpezaThumbnails(LimpezaBase):
    """Classe responsável por limpar cache de miniaturas"""

    def __init__(self):
        super().__init__()
        self.nome = "Miniaturas"

    def executar(self) -> bool:
        try:
            pasta_thumb = os.path.join(obter_pasta_usuario(),
                                      "AppData", "Local", "Microsoft", "Windows", "Explorer")

            if os.path.exists(pasta_thumb):
                for arquivo in os.listdir(pasta_thumb):
                    if "thumbcache" in arquivo.lower():
                        caminho = os.path.join(pasta_thumb, arquivo)
                        if os.path.isfile(caminho):
                            try:
                                self.espaco_liberado += os.path.getsize(caminho)
                                os.remove(caminho)
                                self.arquivos_removidos += 1
                            except:
                                continue

            return True
        except Exception as e:
            self.mensagens.append(f"ℹ️ Miniaturas: erro ao limpar")
            return False


class GerenciadorLimpeza:
    """Gerencia todas as operações de limpeza"""

    def __init__(self):
        self.total_limpo = 0
        self.resultados = []
        self.limpezas = [
            LimpezaLixeira(),
            LimpezaTemporarios(),
            LimpezaCacheNavegadores(),
            LimpezaThumbnails(),
        ]

    def executar_todas(self) -> Tuple[List[str], int]:
        """
        Executa todas as limpezas configuradas

        Returns:
            Tupla com (lista de resultados, total liberado)
        """
        self.total_limpo = 0
        self.resultados = []

        for limpeza in self.limpezas:
            limpeza.executar()
            self.resultados.append(limpeza.get_resultado())
            self.total_limpo += limpeza.espaco_liberado

        return self.resultados, self.total_limpo

    def get_disk_usage(self) -> Optional[Dict]:
        """Retorna informações de uso do disco"""
        try:
            disk = psutil.disk_usage('C:')
            return {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
        except:
            return None
