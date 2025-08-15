# -*- coding: utf-8 -*-
"""
Tela de Login do Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import logging

from core.auth import AuthManager
from recursos.constants import ESCOLAS

class LoginWindow:
    """Janela de login do sistema"""
    
    def __init__(self, parent, sistema):
        """Inicializa a janela de login"""
        self.parent = parent
        self.sistema = sistema
        self.auth_manager = AuthManager()
        
        # Cria a janela de login
        self.window = tk.Toplevel(parent)
        self.window.title("Sistema DIRENS - Login")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        
        # Centraliza a janela
        self.center_window()
        
        # Configura o fechamento da janela
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Cria a interface
        self.create_widgets()
        
        # Configuração modal depois da criação da interface
        self.window.after(100, self.make_modal)
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.window.update_idletasks()
        width = 400
        height = 500
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configurar grid
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text="Sistema DIRENS",
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Subtítulo
        subtitle_label = ttk.Label(
            main_frame,
            text="Controle de Professores",
            font=("Arial", 12)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(main_frame, text="Acesso ao Sistema", padding="15")
        form_frame.grid(row=2, column=0, sticky='ew', pady=(0, 20))
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Escola
        ttk.Label(form_frame, text="Escola:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        self.escola_var = tk.StringVar()
        escola_combo = ttk.Combobox(
            form_frame,
            textvariable=self.escola_var,
            values=list(ESCOLAS.keys()),
            state="readonly",
            width=30
        )
        escola_combo.grid(row=0, column=1, sticky='ew', pady=(0, 10))
        
        # Usuário
        ttk.Label(form_frame, text="Usuário:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        self.usuario_var = tk.StringVar()
        usuario_entry = ttk.Entry(form_frame, textvariable=self.usuario_var, width=30)
        usuario_entry.grid(row=1, column=1, sticky='ew', pady=(0, 10))
        
        # Senha
        ttk.Label(form_frame, text="Senha:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        self.senha_var = tk.StringVar()
        senha_entry = ttk.Entry(form_frame, textvariable=self.senha_var, show="*", width=30)
        senha_entry.grid(row=2, column=1, sticky='ew', pady=(0, 10))
        
        # Bind Enter key
        senha_entry.bind('<Return>', lambda e: self.login())
        usuario_entry.bind('<Return>', lambda e: senha_entry.focus())
        escola_combo.bind('<Return>', lambda e: usuario_entry.focus())
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=20)
        
        login_btn = ttk.Button(
            button_frame,
            text="Entrar",
            command=self.login,
            width=15
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(
            button_frame,
            text="Redefinir Senha",
            command=self.reset_password,
            width=15
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="red")
        status_label.grid(row=4, column=0, pady=10)
        
        # Informações do sistema
        info_frame = ttk.LabelFrame(main_frame, text="Informações", padding="10")
        info_frame.grid(row=5, column=0, sticky='ew', pady=(20, 0))
        
        info_text = tk.Text(info_frame, height=4, width=40, wrap=tk.WORD)
        info_text.grid(row=0, column=0)
        
        info_content = """Sistema de Controle de Professores DIRENS
Versão 1.0 - Desktop Application

Para primeiro acesso, use:
Usuário: admin | Senha: direns2024"""
        
        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED)
        
        # Foco inicial - após um delay para garantir que a janela esteja pronta
        self.window.after(200, lambda: escola_combo.focus_set())
    
    def make_modal(self):
        """Torna a janela modal após estar completamente criada"""
        try:
            self.window.grab_set()
            self.window.focus_set()
            self.window.lift()
        except Exception as e:
            logging.warning(f"Não foi possível tornar janela modal: {e}")
    
    def login(self):
        """Realiza o login"""
        escola = self.escola_var.get()
        usuario = self.usuario_var.get().strip()
        senha = self.senha_var.get()
        
        # Validações básicas
        if not escola:
            self.status_var.set("Selecione uma escola")
            return
        
        if not usuario:
            self.status_var.set("Digite o usuário")
            return
        
        if not senha:
            self.status_var.set("Digite a senha")
            return
        
        # Limpa status
        self.status_var.set("")
        
        try:
            # Tenta autenticar
            auth_result = self.auth_manager.authenticate(escola, usuario, senha)
            
            if auth_result['success']:
                logging.info(f"Login bem-sucedido: {usuario} - {escola}")
                
                # Fecha a janela de login
                self.window.destroy()
                self.parent.destroy()
                
                # Chama callback de sucesso
                user_data = {
                    'username': usuario,
                    'school': escola,
                    'level': auth_result['level']
                }
                self.sistema.on_login_success(user_data)
                
            else:
                self.status_var.set(auth_result['message'])
                logging.warning(f"Falha no login: {usuario} - {escola}")
                
        except Exception as e:
            self.status_var.set("Erro interno do sistema")
            logging.error(f"Erro no login: {e}")
    
    def reset_password(self):
        """Abre janela de redefinição de senha"""
        ResetPasswordWindow(self.window, self.auth_manager)
    
    def on_close(self):
        """Fecha a aplicação"""
        self.parent.quit()


class ResetPasswordWindow:
    """Janela para redefinição de senha"""
    
    def __init__(self, parent, auth_manager):
        """Inicializa a janela de redefinição"""
        self.parent = parent
        self.auth_manager = auth_manager
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Redefinir Senha")
        self.window.geometry("350x300")
        self.window.resizable(False, False)
        
        # Centraliza
        self.center_window()
        
        # Modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Cria interface
        self.create_widgets()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 350
        height = 300
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Redefinir Senha",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Escola
        ttk.Label(main_frame, text="Escola:").pack(anchor=tk.W, pady=(0, 5))
        self.escola_var = tk.StringVar()
        ttk.Combobox(
            main_frame,
            textvariable=self.escola_var,
            values=list(ESCOLAS.keys()),
            state="readonly"
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Usuário
        ttk.Label(main_frame, text="Usuário:").pack(anchor=tk.W, pady=(0, 5))
        self.usuario_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.usuario_var).pack(fill=tk.X, pady=(0, 10))
        
        # Senha atual (apenas para usuário comum)
        ttk.Label(main_frame, text="Senha Atual:").pack(anchor=tk.W, pady=(0, 5))
        self.senha_atual_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.senha_atual_var, show="*").pack(fill=tk.X, pady=(0, 10))
        
        # Nova senha
        ttk.Label(main_frame, text="Nova Senha:").pack(anchor=tk.W, pady=(0, 5))
        self.nova_senha_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nova_senha_var, show="*").pack(fill=tk.X, pady=(0, 10))
        
        # Checkbox admin
        self.is_admin_var = tk.BooleanVar()
        ttk.Checkbutton(
            main_frame,
            text="Sou administrador (pode alterar qualquer senha)",
            variable=self.is_admin_var
        ).pack(pady=10)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Alterar",
            command=self.reset_password
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.window.destroy
        ).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, foreground="red").pack(pady=10)
    
    def reset_password(self):
        """Realiza a redefinição de senha"""
        escola = self.escola_var.get()
        usuario = self.usuario_var.get().strip()
        senha_atual = self.senha_atual_var.get()
        nova_senha = self.nova_senha_var.get()
        is_admin = self.is_admin_var.get()
        
        # Validações
        if not escola or not usuario or not nova_senha:
            self.status_var.set("Preencha todos os campos obrigatórios")
            return
        
        if len(nova_senha) < 6:
            self.status_var.set("Nova senha deve ter pelo menos 6 caracteres")
            return
        
        if not is_admin and not senha_atual:
            self.status_var.set("Digite a senha atual")
            return
        
        try:
            result = self.auth_manager.reset_password(
                escola, usuario, senha_atual, nova_senha, is_admin
            )
            
            if result['success']:
                messagebox.showinfo("Sucesso", result['message'])
                self.window.destroy()
            else:
                self.status_var.set(result['message'])
                
        except Exception as e:
            self.status_var.set("Erro interno do sistema")
            logging.error(f"Erro ao redefinir senha: {e}")
