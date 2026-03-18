#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Módulo da interface gráfica
Contém a classe principal do aplicativo
"""

import customtkinter as ctk
from tkinter import messagebox
import threading
import os
from typing import Optional

from limpeza import GerenciadorLimpeza
from utils import formatar_tamanho, garantir_execucao_admin


class LimpaDiscoApp:
    """Classe principal da interface gráfica"""

    # Constantes de configuração
    TITULO = "🐍 MSSacramento"
    GEOMETRIA = "900x750"
    FONTE_TITULO = ("Consolas", 32, "bold")
    FONTE_SUBTITULO = ("Consolas", 20, "bold")
    FONTE_NORMAL = ("Consolas", 14)
    FONTE_LOG = ("Consolas", 12)

    # Cores
    COR_SUCESSO = "#4CAF50"
    COR_ERRO = "#f44336"
    COR_AVISO = "#FFA500"
    COR_TEXTO_SECUNDARIO = "gray"

    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("MSS - Limpeza de Disco")
        self.root.geometry(self.GEOMETRIA)

        self._configurar_icone()

        self.gerenciador = GerenciadorLimpeza()
        self.criar_interface()

        # Verificar admin ao iniciar
        self._verificar_admin()

    def _configurar_icone(self):
        """Configura o ícone da janela"""
        try:
            # Caminho correto: sobe um nível (src/) e vai para pasta img/
            caminho_icone = os.path.join(
                os.path.dirname(__file__),  # src/
                '..',                        # sobe um nível
                'img',                       # pasta img
                'icone.ico'                   # arquivo
            )
            caminho_icone = os.path.abspath(caminho_icone)

            if os.path.exists(caminho_icone):
                self.root.iconbitmap(caminho_icone)
        except:
            pass  # Ignora se não encontrar o ícone

    def _verificar_admin(self):
        """Verifica e avisa se não estiver como administrador"""
        if not garantir_execucao_admin():
            self._mostrar_aviso_admin()

    def _mostrar_aviso_admin(self):
        """Mostra aviso sobre permissões de administrador"""
        aviso = ctk.CTkLabel(
            self.root,
            text="⚠️ Execute como Administrador para melhores resultados!",
            font=self.FONTE_NORMAL,
            text_color=self.COR_AVISO
        )
        aviso.pack(pady=5)

    def criar_interface(self):
        """Cria todos os elementos da interface"""
        self._criar_titulo()
        self._criar_frame_disco()
        self._criar_frame_principal()
        self._criar_rodape()

    def _criar_titulo(self):
        """Cria o título principal"""
        titulo = ctk.CTkLabel(
            self.root,
            text=self.TITULO,
            font=self.FONTE_TITULO
        )
        titulo.pack(pady=30)

    def _criar_frame_disco(self):
        """Cria o frame com informações do disco"""
        self.disk_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.disk_frame.pack(pady=20, padx=40, fill="x")
        self.atualizar_info_disco()

    def _criar_frame_principal(self):
        """Cria o frame principal com scroll"""
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=10)
        self.main_frame.pack(pady=20, padx=40, fill="both", expand=True)

        self._criar_opcoes_limpeza()
        self._criar_area_log()
        self._criar_botoes()

    def _criar_opcoes_limpeza(self):
        """Cria a lista de itens que serão limpos"""
        self.frame_opcoes = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.frame_opcoes.pack(pady=15, padx=20, fill="x")

        ctk.CTkLabel(
            self.frame_opcoes,
            text="📋 O QUE SERÁ LIMPO:",
            font=self.FONTE_SUBTITULO
        ).pack(pady=20)

        itens = [
            ("🗑️ Lixeira", "Arquivos deletados aguardando remoção permanente"),
            ("📁 Arquivos Temporários", "Cache de programas e sistema operacional"),
            ("🌐 Cache dos Navegadores", "Chrome, Edge, Firefox e outros"),
            ("🖼️ Cache de Miniaturas", "Pré-visualizações de imagens e vídeos"),
        ]

        for item, desc in itens:
            self._criar_item_lista(item, desc)

    def _criar_item_lista(self, item: str, desc: str):
        """Cria um item na lista de limpeza"""
        item_frame = ctk.CTkFrame(self.frame_opcoes, corner_radius=8)
        item_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(
            item_frame,
            text=item,
            font=self.FONTE_NORMAL,
            width=220,
            anchor="w"
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            item_frame,
            text=desc,
            font=self.FONTE_LOG,
            text_color=self.COR_TEXTO_SECUNDARIO
        ).pack(side="left", padx=10)

    def _criar_area_log(self):
        """Cria a área de log para exibir o progresso"""
        ctk.CTkLabel(
            self.main_frame,
            text="📊 PROGRESSO DA LIMPEZA:",
            font=self.FONTE_SUBTITULO
        ).pack(pady=(25, 10))

        self.log_area = ctk.CTkTextbox(
            self.main_frame,
            width=800,
            height=220,
            font=self.FONTE_LOG,
            corner_radius=8
        )
        self.log_area.pack(pady=10, padx=20)

    def _criar_botoes(self):
        """Cria os botões de ação"""
        self.frame_botoes = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        self.frame_botoes.pack(pady=25)

        self.btn_limpar = ctk.CTkButton(
            self.frame_botoes,
            text="🚀 INICIAR LIMPEZA COMPLETA",
            command=self.iniciar_limpeza,
            width=300,
            height=55,
            font=self.FONTE_NORMAL,
            fg_color=self.COR_SUCESSO,
            hover_color="#45a049",
            corner_radius=8
        )
        self.btn_limpar.pack(side="left", padx=15)

        btn_sair = ctk.CTkButton(
            self.frame_botoes,
            text="❌ SAIR",
            command=self.root.quit,
            width=150,
            height=55,
            font=self.FONTE_NORMAL,
            fg_color=self.COR_ERRO,
            hover_color="#da190b",
            corner_radius=8
        )
        btn_sair.pack(side="left", padx=15)

    def _criar_rodape(self):
        """Cria o texto informativo no rodapé"""
        info_text = ctk.CTkLabel(
            self.root,
            text="⚠️ Limpeza 100% segura - Remove apenas arquivos temporários e desnecessários",
            font=self.FONTE_LOG,
            text_color=self.COR_AVISO
        )
        info_text.pack(pady=10)

    def atualizar_info_disco(self):
        """Atualiza as informações do disco na interface"""
        disk_info = self.gerenciador.get_disk_usage()
        if not disk_info:
            return

        # Limpa o frame
        for widget in self.disk_frame.winfo_children():
            widget.destroy()

        self._criar_info_disco(disk_info)

    def _criar_info_disco(self, disk_info: dict):
        """Cria os elementos de informação do disco"""
        ctk.CTkLabel(
            self.disk_frame,
            text="💾 INFORMAÇÕES DO DISCO",
            font=self.FONTE_SUBTITULO
        ).pack(pady=10)

        info_text = (f"Disco C:  {formatar_tamanho(disk_info['used'])} usado  |  "
                    f"{formatar_tamanho(disk_info['free'])} livre  |  "
                    f"Total: {formatar_tamanho(disk_info['total'])}")

        ctk.CTkLabel(
            self.disk_frame,
            text=info_text,
            font=self.FONTE_NORMAL
        ).pack(pady=8)

        progress = ctk.CTkProgressBar(self.disk_frame, width=600, height=20, corner_radius=5)
        progress.pack(pady=10)
        progress.set(disk_info['percent'] / 100)

        ctk.CTkLabel(
            self.disk_frame,
            text=f"{disk_info['percent']:.1f}% do disco está ocupado",
            font=self.FONTE_LOG
        ).pack(pady=5)

    def log(self, mensagem: str):
        """Adiciona uma mensagem à área de log"""
        self.log_area.insert("end", mensagem + "\n")
        self.log_area.see("end")
        self.root.update()

    def iniciar_limpeza(self):
        """Inicia o processo de limpeza"""
        if not self._confirmar_limpeza():
            return

        self._preparar_interface_limpeza()

        # Executa em thread separada
        thread = threading.Thread(target=self._executar_limpeza)
        thread.daemon = True
        thread.start()

    def _confirmar_limpeza(self) -> bool:
        """Mostra diálogo de confirmação"""
        return messagebox.askyesno(
            "🔔 CONFIRMAR LIMPEZA",
            "🧹 DESEJA REALMENTE INICIAR A LIMPEZA?\n\n"
            "Isso irá:\n"
            "✅ Esvaziar a lixeira\n"
            "✅ Remover arquivos temporários\n"
            "✅ Limpar cache dos navegadores\n"
            "✅ Limpar cache de miniaturas\n\n"
            "⚠️ Esta ação NÃO pode ser desfeita!",
            icon='warning'
        )

    def _preparar_interface_limpeza(self):
        """Prepara a interface para iniciar a limpeza"""
        self.btn_limpar.configure(state="disabled", text="🔄 LIMPANDO...")
        self.log_area.delete("1.0", "end")

        self.log("="*70)
        self.log("🚀 INICIANDO LIMPEZA DO SISTEMA")
        self.log("="*70)
        self.log("")

    def _executar_limpeza(self):
        """Executa o processo de limpeza (em thread separada)"""
        try:
            # Executa todas as limpezas
            resultados, total = self.gerenciador.executar_todas()

            # Mostra resultados
            self._mostrar_resultados(resultados, total)

            # Atualiza interface
            self.root.after(0, self._finalizar_limpeza, total)

        except Exception as e:
            self.log(f"❌ Erro durante a limpeza: {str(e)}")
            self.root.after(0, self._reativar_botao)

    def _mostrar_resultados(self, resultados: list, total: int):
        """Mostra os resultados da limpeza no log"""
        self.log("")
        self.log("✅ " + "="*70)
        self.log("📊 RESUMO DA LIMPEZA")
        self.log("✅ " + "="*70)

        for resultado in resultados:
            self.log(resultado)

        self.log("✅ " + "="*70)
        self.log(f"💾 TOTAL LIBERADO: {formatar_tamanho(total)}")
        self.log("✅ " + "="*70)
        self.log("")
        self.log("✨ LIMPEZA CONCLUÍDA COM SUCESSO!")

    def _finalizar_limpeza(self, total: int):
        """Finaliza o processo de limpeza e atualiza interface"""
        self.atualizar_info_disco()
        self._reativar_botao()

        disk_info = self.gerenciador.get_disk_usage()
        messagebox.showinfo(
            "✅ LIMPEZA CONCLUÍDA",
            f"Limpeza finalizada com sucesso!\n\n"
            f"💾 Total liberado: {formatar_tamanho(total)}\n"
            f"📊 Espaço livre agora: {formatar_tamanho(disk_info['free'])}"
        )

    def _reativar_botao(self):
        """Reativa o botão de limpeza"""
        self.btn_limpar.configure(
            state="normal",
            text="🚀 INICIAR LIMPEZA COMPLETA"
        )

    def run(self):
        """Inicia o loop principal da aplicação"""
        self.root.mainloop()
