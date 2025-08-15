# -*- coding: utf-8 -*-
"""
Janela de Visualização de Escolas - Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

from recursos.constants import ESCOLAS

class SchoolsWindow:
    """Janela para visualização de todas as escolas"""
    
    def __init__(self, parent):
        """Inicializa a janela de escolas"""
        self.parent = parent
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Todas as Escolas - Sistema DIRENS")
        self.window.geometry("1000x600")
        self.window.resizable(True, True)
        
        # Modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 1000
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
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(
            header_frame,
            text="Escolas da DIRENS",
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            header_frame,
            text=f"Total: {len(ESCOLAS)} escolas",
            font=("Arial", 12),
            foreground="blue"
        ).pack(side=tk.RIGHT)
        
        # Frame para a tabela
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview para listar as escolas
        columns = ("Sigla", "Nome Completo", "Código", "Cidade", "Estado", "Telefone")
        self.schools_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        column_widths = {
            "Sigla": 80,
            "Nome Completo": 350,
            "Código": 100,
            "Cidade": 150,
            "Estado": 60,
            "Telefone": 150
        }
        
        for col in columns:
            self.schools_tree.heading(col, text=col)
            self.schools_tree.column(col, width=column_widths.get(col, 100), anchor=tk.CENTER if col in ["Sigla", "Código", "Estado"] else tk.W)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.schools_tree.yview)
        h_scroll = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.schools_tree.xview)
        
        self.schools_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.schools_tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Carregar dados das escolas
        self.load_schools_data()
        
        # Frame de detalhes
        details_frame = ttk.LabelFrame(main_frame, text="Detalhes da Escola Selecionada", padding="15")
        details_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.details_text = tk.Text(details_frame, height=6, width=80, wrap=tk.WORD, state=tk.DISABLED)
        details_scroll = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scroll.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleção
        self.schools_tree.bind('<<TreeviewSelect>>', self.on_school_select)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="Atualizar",
            command=self.load_schools_data,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Exportar Lista",
            command=self.export_schools,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)
    
    def load_schools_data(self):
        """Carrega dados das escolas na tabela"""
        # Limpa tabela
        for item in self.schools_tree.get_children():
            self.schools_tree.delete(item)
        
        # Adiciona escolas
        for sigla, dados in ESCOLAS.items():
            self.schools_tree.insert('', tk.END, values=(
                sigla,
                dados.get('nome_completo', ''),
                dados.get('codigo', ''),
                dados.get('cidade', ''),
                dados.get('estado', ''),
                dados.get('telefone', '')
            ))
    
    def on_school_select(self, event):
        """Evento quando uma escola é selecionada"""
        selection = self.schools_tree.selection()
        if not selection:
            return
        
        # Obtém dados da escola selecionada
        item = self.schools_tree.item(selection[0])
        sigla = item['values'][0]
        
        if sigla in ESCOLAS:
            dados = ESCOLAS[sigla]
            
            # Monta texto de detalhes
            details_text = f"""ESCOLA: {sigla} - {dados.get('nome_completo', '')}

CÓDIGO: {dados.get('codigo', '')}

ENDEREÇO:
{dados.get('endereco', '')}
{dados.get('cidade', '')}, {dados.get('estado', '')}

CONTATO:
Telefone: {dados.get('telefone', '')}

INFORMAÇÕES GERAIS:
• Esta é uma instituição de ensino subordinada à DIRENS
• Possui sistema próprio de controle de professores
• Dados atualizados automaticamente pelo sistema"""
            
            # Atualiza área de detalhes
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            self.details_text.insert(1.0, details_text)
            self.details_text.config(state=tk.DISABLED)
    
    def export_schools(self):
        """Exporta lista de escolas"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            
            # Seleciona arquivo
            filename = filedialog.asksaveasfilename(
                title="Exportar Lista de Escolas",
                defaultextension=".txt",
                filetypes=[
                    ("Arquivos de texto", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("Todos os arquivos", "*.*")
                ],
                # inicialmente vazio, será preenchido pelo usuário
            )
            
            if not filename:
                return
            
            # Gera conteúdo do relatório
            content = f"""LISTA DE ESCOLAS - SISTEMA DIRENS
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

{'='*80}

Total de Escolas: {len(ESCOLAS)}

"""
            
            for i, (sigla, dados) in enumerate(ESCOLAS.items(), 1):
                content += f"""{i:02d}. {sigla} - {dados.get('nome_completo', '')}
     Código: {dados.get('codigo', '')}
     Endereço: {dados.get('endereco', '')}
     Cidade: {dados.get('cidade', '')}, {dados.get('estado', '')}
     Telefone: {dados.get('telefone', '')}

"""
            
            content += f"""{'='*80}
Relatório gerado pelo Sistema DIRENS v1.0
Total de registros: {len(ESCOLAS)}
"""
            
            # Salva arquivo
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            messagebox.showinfo("Sucesso", f"Lista exportada para:\n{filename}")
            
        except Exception as e:
            logging.error(f"Erro ao exportar escolas: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar lista:\n{e}")