# -*- coding: utf-8 -*-
"""
Formulário de Disciplina do Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

class DisciplineFormWindow:
    """Janela do formulário de disciplina"""
    
    def __init__(self, parent, discipline_manager, discipline_data=None, callback=None, current_user='admin'):
        """Inicializa o formulário"""
        self.parent = parent
        self.discipline_manager = discipline_manager
        self.discipline_data = discipline_data
        self.callback = callback
        self.current_user = current_user
        
        # Determina se é edição ou novo
        self.is_edit = discipline_data is not None
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Editar Disciplina" if self.is_edit else "Nova Disciplina")
        self.window.geometry("600x400")
        self.window.resizable(True, True)
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
        
        # Preenche dados se for edição
        if self.is_edit:
            self.populate_fields()
        
        # Modal
        self.window.after(100, self.make_modal)
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 600
        height = 400
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def make_modal(self):
        """Torna a janela modal"""
        try:
            self.window.grab_set()
            self.window.focus_set()
            self.window.lift()
        except Exception as e:
            logging.warning(f"Não foi possível tornar janela modal: {e}")
    
    def create_widgets(self):
        """Cria os widgets do formulário"""
        # Frame principal com padding
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Editar Disciplina" if self.is_edit else "Nova Disciplina"
        ttk.Label(
            main_frame,
            text=title_text,
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Frame do formulário
        form_frame = ttk.LabelFrame(main_frame, text="Dados da Disciplina", padding="15")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        form_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Código da disciplina
        ttk.Label(form_frame, text="Código:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.codigo_var = tk.StringVar()
        codigo_entry = ttk.Entry(form_frame, textvariable=self.codigo_var, width=15)
        codigo_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        codigo_entry.focus_set()
        
        # Dica para código
        ttk.Label(
            form_frame, 
            text="(3-10 caracteres: letras, números, hífen, underscore)",
            font=('Arial', 8), 
            foreground='gray'
        ).grid(row=row, column=2, sticky=tk.W, padx=5)
        
        # Se for edição, torna código readonly
        if self.is_edit:
            codigo_entry.config(state='readonly')
        
        row += 1
        
        # Nome da disciplina
        ttk.Label(form_frame, text="Nome da Disciplina:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.nome_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nome_var, width=50).grid(
            row=row, column=1, columnspan=2, sticky="we", pady=5
        )
        
        row += 1
        
        # Requisito específico
        ttk.Label(form_frame, text="Requisito Específico:*").grid(row=row, column=0, sticky=tk.NW, pady=5)
        
        # Frame para requisito específico com scrollbar
        requisito_frame = ttk.Frame(form_frame)
        requisito_frame.grid(row=row, column=1, columnspan=2, sticky="we", pady=5)
        requisito_frame.grid_columnconfigure(0, weight=1)
        
        self.requisito_especifico_text = tk.Text(requisito_frame, height=6, width=50, wrap=tk.WORD)
        requisito_scroll = ttk.Scrollbar(requisito_frame, orient=tk.VERTICAL, command=self.requisito_especifico_text.yview)
        
        self.requisito_especifico_text.configure(yscrollcommand=requisito_scroll.set)
        
        self.requisito_especifico_text.grid(row=0, column=0, sticky="we")
        requisito_scroll.grid(row=0, column=1, sticky="ns")
        
        # Configurar expansão das colunas
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Botões
        self.create_buttons(main_frame)
        
        # Status
        self.status_message_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_message_var, foreground="red").pack(pady=10)
    
    def create_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        # Botão salvar
        save_text = "Atualizar" if self.is_edit else "Salvar"
        ttk.Button(
            button_frame,
            text=save_text,
            command=self.save_discipline,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Botão cancelar
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Botão limpar (apenas para novo)
        if not self.is_edit:
            ttk.Button(
                button_frame,
                text="Limpar",
                command=self.clear_form,
                width=15
            ).pack(side=tk.LEFT, padx=5)
    
    def populate_fields(self):
        """Preenche os campos com dados da disciplina"""
        if not self.discipline_data:
            return
        
        self.codigo_var.set(self.discipline_data.get('codigo', ''))
        self.nome_var.set(self.discipline_data.get('nome', ''))
        
        # Requisito específico
        requisito_especifico = self.discipline_data.get('requisito_especifico', '')
        self.requisito_especifico_text.delete(1.0, tk.END)
        self.requisito_especifico_text.insert(1.0, requisito_especifico)
    
    def clear_form(self):
        """Limpa todos os campos do formulário"""
        self.codigo_var.set('')
        self.nome_var.set('')
        self.requisito_especifico_text.delete(1.0, tk.END)
        
        self.status_message_var.set('')
    
    def validate_form(self):
        """Valida os dados do formulário"""
        discipline_data = self.get_form_data()
        return self.discipline_manager.validate_discipline_data(discipline_data)
    
    def get_form_data(self):
        """Obtém dados do formulário"""
        return {
            'codigo': self.codigo_var.get().strip().upper(),
            'nome': self.nome_var.get().strip(),
            'requisito_especifico': self.requisito_especifico_text.get(1.0, tk.END).strip(),
            'active': True,  # Sempre ativa por padrão
            'created_by': self.current_user,
            'updated_by': self.current_user
        }
    
    def save_discipline(self):
        """Salva a disciplina"""
        try:
            self.status_message_var.set("")
            
            # Valida formulário
            errors = self.validate_form()
            if errors:
                error_msg = "Erros encontrados:\n" + "\n".join(f"• {error}" for error in errors)
                self.status_message_var.set("Formulário inválido")
                messagebox.showerror("Erro de Validação", error_msg)
                return
            
            # Obtém dados
            discipline_data = self.get_form_data()
            
            # Salva
            if self.is_edit:
                codigo = self.discipline_data.get('codigo') if self.discipline_data else discipline_data.get('codigo')
                success = self.discipline_manager.update_discipline(codigo, discipline_data)
                operation = "atualizada"
            else:
                success = self.discipline_manager.add_discipline(discipline_data)
                operation = "criada"
            
            if success:
                messagebox.showinfo("Sucesso", f"Disciplina {operation} com sucesso!")
                
                # Chama callback se fornecido
                if self.callback:
                    self.callback()
                
                # Fecha janela
                self.window.destroy()
            else:
                self.status_message_var.set("Erro ao salvar")
                messagebox.showerror("Erro", f"Erro ao salvar disciplina")
                
        except ValueError as e:
            self.status_message_var.set("Erro de validação")
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            self.status_message_var.set("Erro inesperado")
            logging.error(f"Erro ao salvar disciplina: {e}")
            messagebox.showerror("Erro", f"Erro inesperado:\n{e}")