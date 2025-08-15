# -*- coding: utf-8 -*-
"""
Janela de Histórico do Professor - Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

from dados.history_manager import HistoryManager

class HistoryWindow:
    """Janela para visualização do histórico de alterações"""
    
    def __init__(self, parent, siape, school):
        """Inicializa a janela de histórico"""
        self.parent = parent
        self.siape = siape
        self.school = school
        self.history_manager = HistoryManager()
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title(f"Histórico - Professor SIAPE: {siape}")
        self.window.geometry("900x600")
        self.window.resizable(True, True)
        
        # Modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
        
        # Carrega dados
        self.load_history()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 900
        height = 600
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            title_frame,
            text=f"Histórico de Alterações - SIAPE: {self.siape}",
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        # Botão atualizar
        ttk.Button(
            title_frame,
            text="Atualizar",
            command=self.load_history
        ).pack(side=tk.RIGHT)
        
        # Frame da lista
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview com scrollbars
        columns = ("Data/Hora", "Ação", "Usuário", "Campo", "Valor Anterior", "Valor Novo")
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        column_widths = {
            "Data/Hora": 140,
            "Ação": 80,
            "Usuário": 120,
            "Campo": 150,
            "Valor Anterior": 200,
            "Valor Novo": 200
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Frame de detalhes
        details_frame = ttk.LabelFrame(main_frame, text="Detalhes da Alteração", padding="10")
        details_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Text widget para detalhes
        self.details_text = tk.Text(details_frame, height=4, wrap=tk.WORD)
        details_scroll = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scroll.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de seleção
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Frame de estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_var = tk.StringVar()
        ttk.Label(stats_frame, textvariable=self.stats_var).pack()
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="Exportar Histórico",
            command=self.export_history
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
    
    def load_history(self):
        """Carrega o histórico do professor"""
        try:
            # Limpa a lista
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Carrega histórico
            history = self.history_manager.get_teacher_history(self.siape, self.school)
            
            if not history:
                # Adiciona mensagem se não há histórico
                self.tree.insert('', tk.END, values=(
                    "Nenhum histórico encontrado", "", "", "", "", ""
                ))
                self.stats_var.set("Nenhuma alteração registrada")
                return
            
            # Ordena por data (mais recente primeiro)
            history.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Adiciona itens à lista
            for entry in history:
                timestamp = entry.get('timestamp', '')
                if timestamp:
                    try:
                        # Converte timestamp para formato legível
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        formatted_date = dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        formatted_date = timestamp
                else:
                    formatted_date = ''
                
                self.tree.insert('', tk.END, values=(
                    formatted_date,
                    entry.get('action', ''),
                    entry.get('user', ''),
                    entry.get('field', ''),
                    entry.get('old_value', ''),
                    entry.get('new_value', '')
                ))
            
            # Atualiza estatísticas
            self.update_statistics(history)
            
        except Exception as e:
            logging.error(f"Erro ao carregar histórico: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar histórico:\n{e}")
    
    def update_statistics(self, history):
        """Atualiza as estatísticas do histórico"""
        if not history:
            self.stats_var.set("Nenhuma alteração registrada")
            return
        
        # Conta ações
        actions = {}
        users = set()
        
        for entry in history:
            action = entry.get('action', 'Desconhecida')
            user = entry.get('user', 'Desconhecido')
            
            actions[action] = actions.get(action, 0) + 1
            users.add(user)
        
        # Primeira e última alteração
        first_change = history[-1].get('timestamp', '')
        last_change = history[0].get('timestamp', '')
        
        try:
            if first_change:
                first_dt = datetime.fromisoformat(first_change.replace('Z', '+00:00'))
                first_formatted = first_dt.strftime('%d/%m/%Y')
            else:
                first_formatted = 'N/A'
                
            if last_change:
                last_dt = datetime.fromisoformat(last_change.replace('Z', '+00:00'))
                last_formatted = last_dt.strftime('%d/%m/%Y')
            else:
                last_formatted = 'N/A'
        except:
            first_formatted = 'N/A'
            last_formatted = 'N/A'
        
        # Monta string de estatísticas
        stats_text = f"Total de alterações: {len(history)} | "
        stats_text += f"Usuários envolvidos: {len(users)} | "
        stats_text += f"Primeira alteração: {first_formatted} | "
        stats_text += f"Última alteração: {last_formatted}"
        
        self.stats_var.set(stats_text)
    
    def on_selection_change(self, event):
        """Callback para mudança de seleção"""
        selection = self.tree.selection()
        if not selection:
            self.details_text.delete(1.0, tk.END)
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        if not values or len(values) < 6:
            self.details_text.delete(1.0, tk.END)
            return
        
        # Monta detalhes
        details = f"Data/Hora: {values[0]}\n"
        details += f"Ação: {values[1]}\n"
        details += f"Usuário: {values[2]}\n"
        details += f"Campo alterado: {values[3]}\n"
        details += f"Valor anterior: {values[4]}\n"
        details += f"Valor novo: {values[5]}"
        
        # Atualiza text widget
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(1.0, details)
    
    def export_history(self):
        """Exporta o histórico para arquivo"""
        try:
            from tkinter import filedialog
            
            # Seleciona arquivo
            filename = filedialog.asksaveasfilename(
                title="Exportar Histórico",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("Todos os arquivos", "*.*")],
                initialname=f"historico_siape_{self.siape}.csv"
            )
            
            if not filename:
                return
            
            # Carrega dados
            history = self.history_manager.get_teacher_history(self.siape, self.school)
            
            if not history:
                messagebox.showwarning("Aviso", "Não há histórico para exportar")
                return
            
            # Exporta para CSV
            import csv
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Cabeçalho
                writer.writerow([
                    "Data/Hora", "Ação", "Usuário", "Campo", 
                    "Valor Anterior", "Valor Novo", "Observações"
                ])
                
                # Dados
                for entry in sorted(history, key=lambda x: x.get('timestamp', '')):
                    timestamp = entry.get('timestamp', '')
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            formatted_date = dt.strftime('%d/%m/%Y %H:%M:%S')
                        except:
                            formatted_date = timestamp
                    else:
                        formatted_date = ''
                    
                    writer.writerow([
                        formatted_date,
                        entry.get('action', ''),
                        entry.get('user', ''),
                        entry.get('field', ''),
                        entry.get('old_value', ''),
                        entry.get('new_value', ''),
                        entry.get('notes', '')
                    ])
            
            messagebox.showinfo("Sucesso", f"Histórico exportado para:\n{filename}")
            
        except Exception as e:
            logging.error(f"Erro ao exportar histórico: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar histórico:\n{e}")
