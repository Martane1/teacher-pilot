# -*- coding: utf-8 -*-
"""
Janela de Gerenciamento de Backups - Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
import logging

from core.backup_manager import BackupManager

class BackupWindow:
    """Janela para gerenciamento de backups"""
    
    def __init__(self, parent, callback=None):
        """Inicializa a janela de backups"""
        self.parent = parent
        self.callback = callback
        self.backup_manager = BackupManager()
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Gerenciamento de Backups")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
        
        # Carrega dados
        self.load_backups()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 800
        height = 600
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título e controles
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame,
            text="Gerenciamento de Backups",
            font=("Arial", 14, "bold")
        ).pack(side=tk.LEFT)
        
        # Botões de ação
        button_header_frame = ttk.Frame(header_frame)
        button_header_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            button_header_frame,
            text="Criar Backup",
            command=self.create_backup
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            button_header_frame,
            text="Atualizar",
            command=self.load_backups
        ).pack(side=tk.LEFT, padx=2)
        
        # Frame da lista
        list_frame = ttk.LabelFrame(main_frame, text="Backups Disponíveis", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview
        columns = ("Nome", "Data/Hora", "Tamanho", "Tipo", "Status")
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=12)
        
        # Configurar colunas
        column_widths = {
            "Nome": 200,
            "Data/Hora": 140,
            "Tamanho": 100,
            "Tipo": 100,
            "Status": 100
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
        
        # Frame de informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Backup", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=4, wrap=tk.WORD)
        info_scroll = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scroll.set)
        
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de seleção
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        
        # Frame de ações
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X)
        
        # Botões de ação
        ttk.Button(
            action_frame,
            text="Restaurar",
            command=self.restore_backup
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Excluir",
            command=self.delete_backup
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame,
            text="Exportar",
            command=self.export_backup
        ).pack(side=tk.LEFT, padx=5)
        
        # Configurações de backup automático
        ttk.Separator(action_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        self.auto_backup_var = tk.BooleanVar()
        ttk.Checkbutton(
            action_frame,
            text="Backup automático",
            variable=self.auto_backup_var,
            command=self.toggle_auto_backup
        ).pack(side=tk.LEFT, padx=10)
        
        # Botão fechar
        ttk.Button(
            action_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        # Carrega configuração de backup automático
        self.auto_backup_var.set(self.backup_manager.is_auto_backup_enabled())
    
    def load_backups(self):
        """Carrega a lista de backups"""
        try:
            # Limpa a lista
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Carrega backups
            backups = self.backup_manager.list_backups()
            
            if not backups:
                self.tree.insert('', tk.END, values=(
                    "Nenhum backup encontrado", "", "", "", ""
                ))
                return
            
            # Ordena por data (mais recente primeiro)
            backups.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Adiciona à lista
            for backup in backups:
                timestamp = backup.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        formatted_date = dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        formatted_date = timestamp
                else:
                    formatted_date = ''
                
                # Calcula tamanho do arquivo
                filepath = backup.get('filepath', '')
                size_str = ''
                if filepath and os.path.exists(filepath):
                    size_bytes = os.path.getsize(filepath)
                    size_str = self.format_file_size(size_bytes)
                
                self.tree.insert('', tk.END, values=(
                    backup.get('name', ''),
                    formatted_date,
                    size_str,
                    backup.get('type', 'Manual'),
                    backup.get('status', 'OK')
                ))
                
        except Exception as e:
            logging.error(f"Erro ao carregar backups: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar backups:\n{e}")
    
    def format_file_size(self, size_bytes):
        """Formata tamanho do arquivo"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        
        return f"{s} {size_names[i]}"
    
    def on_selection_change(self, event):
        """Callback para mudança de seleção"""
        selection = self.tree.selection()
        if not selection:
            self.info_text.delete(1.0, tk.END)
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        if not values or len(values) < 5:
            self.info_text.delete(1.0, tk.END)
            return
        
        # Busca informações detalhadas do backup
        backup_name = values[0]
        backups = self.backup_manager.list_backups()
        
        backup_info = None
        for backup in backups:
            if backup.get('name') == backup_name:
                backup_info = backup
                break
        
        if not backup_info:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, "Informações não disponíveis")
            return
        
        # Monta informações
        info = f"Nome: {backup_info.get('name', 'N/A')}\n"
        info += f"Data/Hora: {values[1]}\n"
        info += f"Tamanho: {values[2]}\n"
        info += f"Tipo: {backup_info.get('type', 'Manual')}\n"
        info += f"Descrição: {backup_info.get('description', 'Sem descrição')}\n"
        info += f"Arquivo: {backup_info.get('filepath', 'N/A')}"
        
        # Atualiza text widget
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def create_backup(self):
        """Cria um novo backup"""
        try:
            # Janela de confirmação com opções
            dialog = BackupCreateDialog(self.window)
            self.window.wait_window(dialog.window)
            
            if dialog.result:
                description = dialog.result.get('description', '')
                include_history = dialog.result.get('include_history', True)
                
                # Cria o backup
                backup_info = self.backup_manager.create_backup(
                    description=description,
                    include_history=include_history
                )
                
                if backup_info:
                    messagebox.showinfo("Sucesso", "Backup criado com sucesso!")
                    self.load_backups()
                else:
                    messagebox.showerror("Erro", "Erro ao criar backup")
                    
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
            messagebox.showerror("Erro", f"Erro ao criar backup:\n{e}")
    
    def restore_backup(self):
        """Restaura um backup selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um backup para restaurar")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        if not values:
            return
        
        backup_name = values[0]
        
        # Confirma restauração
        response = messagebox.askyesno(
            "Confirmar Restauração",
            f"Deseja restaurar o backup '{backup_name}'?\n\n"
            "ATENÇÃO: Esta ação irá substituir todos os dados atuais!\n"
            "Recomenda-se criar um backup antes de prosseguir."
        )
        
        if not response:
            return
        
        try:
            # Cria backup de segurança antes da restauração
            self.backup_manager.create_backup(
                description="Backup automático antes da restauração",
                backup_type="pre_restore"
            )
            
            # Restaura o backup
            success = self.backup_manager.restore_backup(backup_name)
            
            if success:
                messagebox.showinfo(
                    "Sucesso",
                    "Backup restaurado com sucesso!\n\n"
                    "O sistema será atualizado automaticamente."
                )
                
                # Chama callback se definido
                if self.callback:
                    self.callback()
                    
                self.window.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao restaurar backup")
                
        except Exception as e:
            logging.error(f"Erro ao restaurar backup: {e}")
            messagebox.showerror("Erro", f"Erro ao restaurar backup:\n{e}")
    
    def delete_backup(self):
        """Exclui um backup selecionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um backup para excluir")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        if not values:
            return
        
        backup_name = values[0]
        
        # Confirma exclusão
        response = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja excluir o backup '{backup_name}'?\n\n"
            "Esta ação não pode ser desfeita."
        )
        
        if not response:
            return
        
        try:
            success = self.backup_manager.delete_backup(backup_name)
            
            if success:
                messagebox.showinfo("Sucesso", "Backup excluído com sucesso!")
                self.load_backups()
            else:
                messagebox.showerror("Erro", "Erro ao excluir backup")
                
        except Exception as e:
            logging.error(f"Erro ao excluir backup: {e}")
            messagebox.showerror("Erro", f"Erro ao excluir backup:\n{e}")
    
    def export_backup(self):
        """Exporta um backup para local específico"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um backup para exportar")
            return
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        if not values:
            return
        
        backup_name = values[0]
        
        try:
            from tkinter import filedialog
            
            # Seleciona destino
            filename = filedialog.asksaveasfilename(
                title="Exportar Backup",
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip"), ("Todos os arquivos", "*.*")],
                initialname=f"{backup_name}.zip"
            )
            
            if not filename:
                return
            
            success = self.backup_manager.export_backup(backup_name, filename)
            
            if success:
                messagebox.showinfo("Sucesso", f"Backup exportado para:\n{filename}")
            else:
                messagebox.showerror("Erro", "Erro ao exportar backup")
                
        except Exception as e:
            logging.error(f"Erro ao exportar backup: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar backup:\n{e}")
    
    def toggle_auto_backup(self):
        """Alterna backup automático"""
        enabled = self.auto_backup_var.get()
        
        try:
            self.backup_manager.set_auto_backup(enabled)
            
            status = "ativado" if enabled else "desativado"
            messagebox.showinfo("Backup Automático", f"Backup automático {status}")
            
        except Exception as e:
            logging.error(f"Erro ao configurar backup automático: {e}")
            messagebox.showerror("Erro", f"Erro ao configurar backup automático:\n{e}")


class BackupCreateDialog:
    """Diálogo para criação de backup"""
    
    def __init__(self, parent):
        """Inicializa o diálogo"""
        self.parent = parent
        self.result = None
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Criar Backup")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        
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
        
        width = 400
        height = 300
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets do diálogo"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            main_frame,
            text="Criar Novo Backup",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 20))
        
        # Descrição
        ttk.Label(main_frame, text="Descrição:").pack(anchor=tk.W, pady=(0, 5))
        self.description_var = tk.StringVar()
        self.description_var.set(f"Backup manual - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        desc_entry = ttk.Entry(main_frame, textvariable=self.description_var, width=40)
        desc_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Opções
        options_frame = ttk.LabelFrame(main_frame, text="Opções", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.include_history_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            options_frame,
            text="Incluir histórico de alterações",
            variable=self.include_history_var
        ).pack(anchor=tk.W)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Criar",
            command=self.create_backup
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=self.cancel
        ).pack(side=tk.LEFT, padx=5)
        
        # Foco inicial
        desc_entry.focus()
        desc_entry.select_range(0, tk.END)
    
    def create_backup(self):
        """Confirma criação do backup"""
        self.result = {
            'description': self.description_var.get().strip(),
            'include_history': self.include_history_var.get()
        }
        self.window.destroy()
    
    def cancel(self):
        """Cancela criação"""
        self.result = None
        self.window.destroy()
