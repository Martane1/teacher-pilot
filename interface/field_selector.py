# -*- coding: utf-8 -*-
"""
Seletor de Campos para Exportação - Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox

class FieldSelectorWindow:
    """Janela para seleção de campos para exportação"""
    
    def __init__(self, parent, callback=None):
        """Inicializa o seletor de campos"""
        self.parent = parent
        self.callback = callback
        self.selected_fields = []
        
        # Campos disponíveis
        self.available_fields = {
            'siape': 'SIAPE',
            'nome': 'Nome',
            'data_nascimento': 'Data de Nascimento',
            'sexo': 'Sexo',
            'carga_horaria': 'Carga Horária',
            'carreira': 'Carreira',
            'data_ingresso': 'Data de Ingresso',
            'status': 'Status',
            'area_atuacao': 'Área de Atuação',
            'pos_graduacao': 'Pós-graduação',
            'graduacao': 'Graduação',
            'instituicao_graduacao': 'Instituição Graduação',
            'curso_pos': 'Curso Pós-graduação',
            'instituicao_pos': 'Instituição Pós',
            'email': 'Email',
            'telefone': 'Telefone'
        }
        
        # Variáveis dos checkboxes
        self.field_vars = {}
        for field_key in self.available_fields.keys():
            self.field_vars[field_key] = tk.BooleanVar(value=True)  # Todos selecionados por padrão
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Selecionar Campos para Exportação")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
        
        # Modal
        self.window.after(100, self.make_modal)
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 400
        height = 500
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def make_modal(self):
        """Torna a janela modal"""
        try:
            self.window.grab_set()
            self.window.focus_set()
            self.window.lift()
        except Exception:
            pass
    
    def create_widgets(self):
        """Cria os widgets da janela"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Selecione os campos para incluir no PDF:",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 15))
        
        # Frame dos checkboxes com scrollbar
        canvas = tk.Canvas(main_frame, height=300)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Checkboxes para cada campo
        for field_key, field_label in self.available_fields.items():
            checkbox_frame = ttk.Frame(scrollable_frame)
            checkbox_frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Checkbutton(
                checkbox_frame,
                text=field_label,
                variable=self.field_vars[field_key]
            ).pack(anchor=tk.W)
        
        # Botões de controle
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(15, 10))
        
        ttk.Button(
            control_frame,
            text="Selecionar Todos",
            command=self.select_all,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            control_frame,
            text="Limpar Todos",
            command=self.clear_all,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Botões principais
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Gerar PDF",
            command=self.confirm_selection,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def select_all(self):
        """Seleciona todos os campos"""
        for var in self.field_vars.values():
            var.set(True)
    
    def clear_all(self):
        """Limpa todos os campos"""
        for var in self.field_vars.values():
            var.set(False)
    
    def confirm_selection(self):
        """Confirma a seleção e chama o callback"""
        # Coleta campos selecionados
        selected = []
        for field_key, var in self.field_vars.items():
            if var.get():
                selected.append({
                    'key': field_key,
                    'label': self.available_fields[field_key]
                })
        
        if not selected:
            messagebox.showwarning("Aviso", "Selecione pelo menos um campo para exportar.")
            return
        
        self.selected_fields = selected
        
        # Chama callback se definido
        if self.callback:
            self.callback(self.selected_fields)
        
        # Fecha janela
        self.window.destroy()