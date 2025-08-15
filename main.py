#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Controle de Professores DIRENS
Aplicação Desktop com Python + Tkinter
Versão: 1.0
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import logging
from datetime import datetime

# Adicionar o diretório atual ao path para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interface.login import LoginWindow
from recursos.config import Config
from dados.data_manager import DataManager

class SistemaDIRENS:
    """Classe principal do sistema DIRENS"""
    
    def __init__(self):
        """Inicializa o sistema"""
        self.setup_logging()
        self.setup_directories()
        self.data_manager = DataManager()
        self.current_user = None
        self.current_school = None
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_filename = os.path.join(log_dir, f"direns_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        logging.info("Sistema DIRENS iniciado")
    
    def setup_directories(self):
        """Cria os diretórios necessários"""
        directories = [
            "data",
            "backups", 
            "exports",
            "logs"
        ]
        
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Diretório criado: {directory}")
    
    def run(self):
        """Executa o sistema"""
        try:
            # Cria a janela principal (invisível inicialmente)
            root = tk.Tk()
            root.withdraw()  # Esconde a janela principal
            
            # Configura o estilo da aplicação
            root.title("Sistema DIRENS - Controle de Professores")
            root.geometry("1200x800")
            root.resizable(True, True)
            
            # Define ícone da aplicação (se existir)
            try:
                root.iconbitmap("recursos/icon.ico")
            except:
                pass  # Ignora se não encontrar o ícone
            
            # Mostra a tela de login
            login_window = LoginWindow(root, self)
            
            # Inicia o loop principal
            root.mainloop()
            
        except Exception as e:
            logging.error(f"Erro fatal no sistema: {e}")
            messagebox.showerror("Erro Fatal", f"Erro ao iniciar o sistema:\n{e}")
    
    def on_login_success(self, user_data):
        """Callback executado após login bem-sucedido"""
        self.current_user = user_data['username']
        self.current_school = user_data['school']
        
        logging.info(f"Login realizado: {self.current_user} - Escola: {self.current_school}")
        
        # Importa e abre a janela principal
        from interface.main_window import MainWindow
        
        # Cria a janela principal
        root = tk.Tk()
        app = MainWindow(root, self)
        
        # Centraliza a janela
        self.center_window(root, 1200, 800)
        
        # Inicia o loop da janela principal
        root.mainloop()
    
    def center_window(self, window, width, height):
        """Centraliza uma janela na tela"""
        # Obtém as dimensões da tela
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calcula a posição
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        # Define a geometria
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def logout(self):
        """Realiza o logout do sistema"""
        logging.info(f"Logout realizado: {self.current_user}")
        self.current_user = None
        self.current_school = None

def main():
    """Função principal"""
    try:
        sistema = SistemaDIRENS()
        sistema.run()
    except KeyboardInterrupt:
        logging.info("Sistema encerrado pelo usuário")
    except Exception as e:
        logging.error(f"Erro não tratado: {e}")
        print(f"Erro fatal: {e}")

if __name__ == "__main__":
    main()
