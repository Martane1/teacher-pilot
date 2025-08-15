# -*- coding: utf-8 -*-
"""
Janela de Configuração da Ordem das Colunas - Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import logging

class ColumnOrderWindow:
    """Janela para configurar ordem das colunas"""
    
    def __init__(self, parent, current_columns, school, callback=None):
        """Inicializa a janela de configuração de colunas"""
        self.parent = parent
        self.current_columns = current_columns
        self.school = school
        self.callback = callback
        self.config_file = "data/column_order.json"
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Configurar Ordem das Colunas")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        # Modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Centraliza
        self.center_window()
        
        # Carrega ordem salva ou usa ordem atual
        self.column_order = self.load_column_order()
        
        # Cria a interface
        self.create_widgets()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 500
        height = 600
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = f"Configurar Ordem das Colunas - {self.school}"
        ttk.Label(
            main_frame,
            text=title_text,
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Instruções
        instructions = ttk.Label(
            main_frame,
            text="Arraste as colunas para cima e para baixo para reordenar.\nA primeira coluna será a mais à esquerda.",
            justify=tk.CENTER,
            foreground="blue"
        )
        instructions.pack(pady=(0, 20))
        
        # Frame para lista de colunas
        list_frame = ttk.LabelFrame(main_frame, text="Ordem das Colunas", padding="15")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Listbox para as colunas
        self.columns_listbox = tk.Listbox(
            list_frame,
            height=12,
            font=("Arial", 11),
            selectmode=tk.SINGLE
        )
        self.columns_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar para listbox
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.columns_listbox.yview)
        self.columns_listbox.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Popula listbox com colunas
        self.populate_listbox()
        
        # Frame para botões de movimento
        move_frame = ttk.Frame(main_frame)
        move_frame.pack(pady=(0, 20))
        
        ttk.Button(
            move_frame,
            text="⬆ Mover para Cima",
            command=self.move_up,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            move_frame,
            text="⬇ Mover para Baixo", 
            command=self.move_down,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Separador
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Frame para botões de ação
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)
        
        ttk.Button(
            action_frame,
            text="Restaurar Padrão",
            command=self.restore_default,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Aplicar",
            command=self.apply_order,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Cancelar",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, foreground="green").pack(pady=10)
    
    def populate_listbox(self):
        """Popula listbox com colunas na ordem atual"""
        self.columns_listbox.delete(0, tk.END)
        
        for column in self.column_order:
            self.columns_listbox.insert(tk.END, column)
    
    def move_up(self):
        """Move coluna selecionada para cima"""
        try:
            selection = self.columns_listbox.curselection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione uma coluna para mover")
                return
            
            index = selection[0]
            if index == 0:
                messagebox.showinfo("Informação", "A coluna já está no topo")
                return
            
            # Troca posições na lista
            self.column_order[index], self.column_order[index-1] = \
                self.column_order[index-1], self.column_order[index]
            
            # Atualiza listbox
            self.populate_listbox()
            
            # Mantém seleção
            self.columns_listbox.selection_set(index-1)
            
        except Exception as e:
            logging.error(f"Erro ao mover coluna para cima: {e}")
            messagebox.showerror("Erro", "Erro ao mover coluna")
    
    def move_down(self):
        """Move coluna selecionada para baixo"""
        try:
            selection = self.columns_listbox.curselection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione uma coluna para mover")
                return
            
            index = selection[0]
            if index == len(self.column_order) - 1:
                messagebox.showinfo("Informação", "A coluna já está no final")
                return
            
            # Troca posições na lista
            self.column_order[index], self.column_order[index+1] = \
                self.column_order[index+1], self.column_order[index]
            
            # Atualiza listbox
            self.populate_listbox()
            
            # Mantém seleção
            self.columns_listbox.selection_set(index+1)
            
        except Exception as e:
            logging.error(f"Erro ao mover coluna para baixo: {e}")
            messagebox.showerror("Erro", "Erro ao mover coluna")
    
    def restore_default(self):
        """Restaura ordem padrão das colunas"""
        try:
            result = messagebox.askyesno(
                "Confirmar",
                "Restaurar ordem padrão das colunas?"
            )
            
            if result:
                # Usa ordem original das colunas
                self.column_order = list(self.current_columns)
                self.populate_listbox()
                self.status_var.set("Ordem padrão restaurada")
                
        except Exception as e:
            logging.error(f"Erro ao restaurar padrão: {e}")
            messagebox.showerror("Erro", "Erro ao restaurar ordem padrão")
    
    def apply_order(self):
        """Aplica nova ordem das colunas"""
        try:
            # Salva configuração
            self.save_column_order()
            
            # Chama callback para atualizar interface principal
            if self.callback:
                self.callback(self.column_order)
            
            self.status_var.set("Ordem aplicada com sucesso!")
            
            # Fecha janela após 1 segundo
            self.window.after(1000, self.window.destroy)
            
        except Exception as e:
            logging.error(f"Erro ao aplicar ordem: {e}")
            messagebox.showerror("Erro", "Erro ao aplicar nova ordem")
    
    def load_column_order(self):
        """Carrega ordem salva das colunas"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                school_config = config.get(self.school, {})
                saved_order = school_config.get('column_order', [])
                
                # Valida se todas as colunas estão presentes
                if all(col in saved_order for col in self.current_columns):
                    return saved_order
            
            # Se não há configuração salva ou está inválida, usa ordem atual
            return list(self.current_columns)
            
        except Exception as e:
            logging.error(f"Erro ao carregar ordem das colunas: {e}")
            return list(self.current_columns)
    
    def save_column_order(self):
        """Salva ordem atual das colunas"""
        try:
            # Carrega configuração existente
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # Atualiza configuração para esta escola
            if self.school not in config:
                config[self.school] = {}
            
            config[self.school]['column_order'] = self.column_order
            from datetime import datetime
            config[self.school]['last_updated'] = datetime.now().isoformat()
            
            # Garante que diretório existe
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Salva configuração
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Ordem das colunas salva para {self.school}")
            
        except Exception as e:
            logging.error(f"Erro ao salvar ordem das colunas: {e}")
            raise e
    
    @staticmethod
    def get_saved_column_order(school, default_columns):
        """Método estático para obter ordem salva das colunas"""
        try:
            config_file = "data/column_order.json"
            
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                school_config = config.get(school, {})
                saved_order = school_config.get('column_order', [])
                
                # Valida se todas as colunas estão presentes
                if all(col in saved_order for col in default_columns):
                    return saved_order
            
            # Se não há configuração ou está inválida, retorna ordem padrão
            return list(default_columns)
            
        except Exception as e:
            logging.error(f"Erro ao obter ordem salva das colunas: {e}")
            return list(default_columns)