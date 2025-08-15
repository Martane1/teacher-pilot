# -*- coding: utf-8 -*-
"""
Janela Principal do Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from datetime import datetime

from interface.teacher_form import TeacherFormWindow
from interface.history_window import HistoryWindow
from interface.backup_window import BackupWindow
from interface.statistics_window import StatisticsWindow
from core.teacher_manager import TeacherManager
from core.export_manager import ExportManager
from recursos.constants import CARGAS_HORARIAS, CARREIRAS, POS_GRADUACAO

class MainWindow:
    """Janela principal do sistema"""
    
    def __init__(self, root, sistema):
        """Inicializa a janela principal"""
        self.root = root
        self.sistema = sistema
        self.teacher_manager = TeacherManager()
        self.export_manager = ExportManager()
        
        # Configurações da janela
        self.root.title(f"Sistema DIRENS - {sistema.current_school}")
        self.root.geometry("1200x800")
        # Maximiza a janela de forma compatível com diferentes sistemas
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                # Linux/Unix - tenta atributo zoomed
                self.root.attributes('-zoomed', True)
            except:
                # Fallback - apenas maximiza o tamanho da janela
                self.root.geometry("1400x900")
        
        # Variáveis de filtro
        self.filter_pos = tk.StringVar()
        self.filter_carga = tk.StringVar()
        self.filter_carreira = tk.StringVar()
        self.search_var = tk.StringVar()
        
        # Bind para busca em tempo real
        self.search_var.trace('w', self.on_search_change)
        
        # Cria a interface
        self.create_widgets()
        
        # Carrega dados iniciais
        self.refresh_data()
        
        # Configura fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Menu principal
        self.create_menu()
        
        # Toolbar
        self.create_toolbar()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Frame de filtros
        self.create_filters_frame(main_frame)
        
        # Frame da lista
        self.create_list_frame(main_frame)
        
        # Status bar
        self.create_status_bar()
    
    def create_menu(self):
        """Cria o menu principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Novo Professor", command=self.new_teacher, accelerator="Ctrl+N")
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Exportar CSV", command=self.export_csv)
        arquivo_menu.add_command(label="Exportar PDF", command=self.export_pdf)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.on_close, accelerator="Ctrl+Q")
        
        # Menu Editar
        editar_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=editar_menu)
        editar_menu.add_command(label="Editar Professor", command=self.edit_teacher, accelerator="F2")
        editar_menu.add_command(label="Excluir Professor", command=self.delete_teacher, accelerator="Del")
        editar_menu.add_separator()
        editar_menu.add_command(label="Histórico", command=self.show_history, accelerator="F3")
        
        # Menu Ferramentas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=tools_menu)
        tools_menu.add_command(label="Estatísticas", command=self.show_statistics)
        tools_menu.add_command(label="Backups", command=self.show_backups)
        tools_menu.add_command(label="Atualizar", command=self.refresh_data, accelerator="F5")
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
        
        # Atalhos do teclado
        self.root.bind('<Control-n>', lambda e: self.new_teacher())
        self.root.bind('<Control-q>', lambda e: self.on_close())
        self.root.bind('<F2>', lambda e: self.edit_teacher())
        self.root.bind('<Delete>', lambda e: self.delete_teacher())
        self.root.bind('<F3>', lambda e: self.show_history())
        self.root.bind('<F5>', lambda e: self.refresh_data())
    
    def create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        # Botões principais
        ttk.Button(
            toolbar,
            text="Novo Professor",
            command=self.new_teacher
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(
            toolbar,
            text="Editar",
            command=self.edit_teacher
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Excluir",
            command=self.delete_teacher
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(
            toolbar,
            text="Histórico",
            command=self.show_history
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Estatísticas",
            command=self.show_statistics
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(
            toolbar,
            text="Exportar CSV",
            command=self.export_csv
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="Exportar PDF",
            command=self.export_pdf
        ).pack(side=tk.LEFT, padx=2)
        
        # Informações do usuário (direita)
        user_frame = ttk.Frame(toolbar)
        user_frame.pack(side=tk.RIGHT)
        
        ttk.Label(
            user_frame,
            text=f"Usuário: {self.sistema.current_user} | Escola: {self.sistema.current_school}"
        ).pack(side=tk.RIGHT, padx=10)
        
        ttk.Button(
            user_frame,
            text="Logout",
            command=self.logout
        ).pack(side=tk.RIGHT)
    
    def create_filters_frame(self, parent):
        """Cria o frame de filtros"""
        filters_frame = ttk.LabelFrame(parent, text="Filtros e Busca", padding="10")
        filters_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Primeira linha - filtros
        filter_row1 = ttk.Frame(filters_frame)
        filter_row1.pack(fill=tk.X, pady=(0, 10))
        
        # Pós-graduação
        ttk.Label(filter_row1, text="Pós-graduação:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Combobox(
            filter_row1,
            textvariable=self.filter_pos,
            values=["Todos"] + POS_GRADUACAO,
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # Carga horária
        ttk.Label(filter_row1, text="Carga Horária:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Combobox(
            filter_row1,
            textvariable=self.filter_carga,
            values=["Todos"] + CARGAS_HORARIAS,
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # Carreira
        ttk.Label(filter_row1, text="Carreira:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Combobox(
            filter_row1,
            textvariable=self.filter_carreira,
            values=["Todos"] + CARREIRAS,
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        # Botão limpar filtros
        ttk.Button(
            filter_row1,
            text="Limpar Filtros",
            command=self.clear_filters
        ).pack(side=tk.LEFT, padx=20)
        
        # Segunda linha - busca
        search_row = ttk.Frame(filters_frame)
        search_row.pack(fill=tk.X)
        
        ttk.Label(search_row, text="Buscar (Nome/SIAPE):").pack(side=tk.LEFT, padx=(0, 10))
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT)
        
        # Contador de registros
        self.count_var = tk.StringVar()
        ttk.Label(search_row, textvariable=self.count_var).pack(side=tk.RIGHT, padx=10)
        
        # Configurar eventos de filtro
        self.filter_pos.trace('w', self.apply_filters)
        self.filter_carga.trace('w', self.apply_filters)
        self.filter_carreira.trace('w', self.apply_filters)
        
        # Definir valores padrão
        self.filter_pos.set("Todos")
        self.filter_carga.set("Todos")
        self.filter_carreira.set("Todos")
    
    def create_list_frame(self, parent):
        """Cria o frame da lista de professores"""
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview com scrollbars
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Colunas da lista
        columns = (
            "SIAPE", "Nome", "Data Nascimento", "Carga Horária",
            "Carreira", "Pós-graduação", "Data Ingresso", "Status"
        )
        
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        
        # Configurar colunas
        column_widths = {
            "SIAPE": 100,
            "Nome": 250,
            "Data Nascimento": 120,
            "Carga Horária": 100,
            "Carreira": 100,
            "Pós-graduação": 130,
            "Data Ingresso": 120,
            "Status": 100
        }
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            self.tree.column(col, width=column_widths.get(col, 100), minwidth=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Eventos
        self.tree.bind('<Double-1>', lambda e: self.edit_teacher())
        self.tree.bind('<Return>', lambda e: self.edit_teacher())
    
    def create_status_bar(self):
        """Cria a barra de status"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Data/hora atual
        self.datetime_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.datetime_var).pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Atualizar data/hora
        self.update_datetime()
    
    def update_datetime(self):
        """Atualiza data e hora na barra de status"""
        now = datetime.now()
        self.datetime_var.set(now.strftime("%d/%m/%Y %H:%M:%S"))
        self.root.after(1000, self.update_datetime)
    
    def refresh_data(self):
        """Atualiza a lista de professores"""
        try:
            self.status_var.set("Carregando dados...")
            
            # Limpa a lista
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Carrega professores da escola atual
            professores = self.teacher_manager.get_teachers_by_school(self.sistema.current_school)
            
            # Aplica filtros
            professores_filtrados = self.apply_current_filters(professores)
            
            # Adiciona à lista
            for professor in professores_filtrados:
                self.tree.insert('', tk.END, values=(
                    professor.get('siape', ''),
                    professor.get('nome', ''),
                    professor.get('data_nascimento', ''),
                    professor.get('carga_horaria', ''),
                    professor.get('carreira', ''),
                    professor.get('pos_graduacao', ''),
                    professor.get('data_ingresso', ''),
                    professor.get('status', 'Ativo')
                ))
            
            # Atualiza contador
            total = len(professores)
            filtrados = len(professores_filtrados)
            self.count_var.set(f"{filtrados} de {total} professores")
            
            self.status_var.set("Dados carregados")
            
        except Exception as e:
            logging.error(f"Erro ao carregar dados: {e}")
            self.status_var.set("Erro ao carregar dados")
            messagebox.showerror("Erro", f"Erro ao carregar dados:\n{e}")
    
    def apply_current_filters(self, professores):
        """Aplica os filtros atuais aos professores"""
        filtrados = professores.copy()
        
        # Filtro por pós-graduação
        if self.filter_pos.get() and self.filter_pos.get() != "Todos":
            filtrados = [p for p in filtrados if p.get('pos_graduacao') == self.filter_pos.get()]
        
        # Filtro por carga horária
        if self.filter_carga.get() and self.filter_carga.get() != "Todos":
            filtrados = [p for p in filtrados if p.get('carga_horaria') == self.filter_carga.get()]
        
        # Filtro por carreira
        if self.filter_carreira.get() and self.filter_carreira.get() != "Todos":
            filtrados = [p for p in filtrados if p.get('carreira') == self.filter_carreira.get()]
        
        # Filtro por busca
        search_term = self.search_var.get().strip().lower()
        if search_term:
            filtrados = [
                p for p in filtrados
                if search_term in p.get('nome', '').lower() or 
                   search_term in p.get('siape', '')
            ]
        
        return filtrados
    
    def apply_filters(self, *args):
        """Aplica filtros quando alterados"""
        self.refresh_data()
    
    def on_search_change(self, *args):
        """Callback para mudança na busca"""
        # Aplica busca com delay para evitar muitas chamadas
        if hasattr(self, '_search_timer'):
            self.root.after_cancel(self._search_timer)
        
        self._search_timer = self.root.after(300, self.refresh_data)
    
    def clear_filters(self):
        """Limpa todos os filtros"""
        self.filter_pos.set("Todos")
        self.filter_carga.set("Todos")
        self.filter_carreira.set("Todos")
        self.search_var.set("")
    
    def sort_column(self, column):
        """Ordena por coluna"""
        # Implementação básica de ordenação
        items = [(self.tree.item(item)['values'], item) for item in self.tree.get_children()]
        
        col_index = list(self.tree['columns']).index(column)
        
        # Ordena numericamente se for SIAPE, caso contrário alfabeticamente
        if column == "SIAPE":
            items.sort(key=lambda x: int(x[0][col_index]) if x[0][col_index].isdigit() else 0)
        else:
            items.sort(key=lambda x: str(x[0][col_index]).lower())
        
        # Reordena os itens
        for index, (values, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def get_selected_teacher(self):
        """Retorna o professor selecionado"""
        selection = self.tree.selection()
        if not selection:
            return None
        
        item = selection[0]
        values = self.tree.item(item)['values']
        
        if not values:
            return None
        
        return {
            'siape': values[0],
            'nome': values[1],
            'data_nascimento': values[2],
            'carga_horaria': values[3],
            'carreira': values[4],
            'pos_graduacao': values[5],
            'data_ingresso': values[6],
            'status': values[7] if len(values) > 7 else 'Ativo'
        }
    
    def new_teacher(self):
        """Abre formulário para novo professor"""
        TeacherFormWindow(self.root, self.teacher_manager, self.sistema.current_school, callback=self.refresh_data)
    
    def edit_teacher(self):
        """Edita o professor selecionado"""
        selected = self.get_selected_teacher()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um professor para editar")
            return
        
        # Carrega dados completos do professor
        professor_completo = self.teacher_manager.get_teacher_by_siape(
            selected['siape'], self.sistema.current_school
        )
        
        if professor_completo:
            TeacherFormWindow(
                self.root, 
                self.teacher_manager, 
                self.sistema.current_school,
                teacher_data=professor_completo,
                callback=self.refresh_data
            )
    
    def delete_teacher(self):
        """Exclui o professor selecionado"""
        selected = self.get_selected_teacher()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um professor para excluir")
            return
        
        # Confirma exclusão
        response = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o professor:\n{selected['nome']} (SIAPE: {selected['siape']})?\n\nEsta ação não pode ser desfeita."
        )
        
        if response:
            try:
                success = self.teacher_manager.delete_teacher(
                    selected['siape'], 
                    self.sistema.current_school,
                    self.sistema.current_user
                )
                
                if success:
                    messagebox.showinfo("Sucesso", "Professor excluído com sucesso")
                    self.refresh_data()
                else:
                    messagebox.showerror("Erro", "Erro ao excluir professor")
                    
            except Exception as e:
                logging.error(f"Erro ao excluir professor: {e}")
                messagebox.showerror("Erro", f"Erro ao excluir professor:\n{e}")
    
    def show_history(self):
        """Mostra histórico do professor selecionado"""
        selected = self.get_selected_teacher()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um professor para ver o histórico")
            return
        
        HistoryWindow(self.root, selected['siape'], self.sistema.current_school)
    
    def show_statistics(self):
        """Mostra janela de estatísticas"""
        StatisticsWindow(self.root, self.teacher_manager, self.sistema.current_school)
    
    def show_backups(self):
        """Mostra janela de backups"""
        BackupWindow(self.root, callback=self.refresh_data)
    
    def export_csv(self):
        """Exporta para CSV"""
        try:
            self.status_var.set("Exportando CSV...")
            
            professores = self.teacher_manager.get_teachers_by_school(self.sistema.current_school)
            filepath = self.export_manager.export_csv(professores, self.sistema.current_school)
            
            self.status_var.set("CSV exportado com sucesso")
            messagebox.showinfo("Sucesso", f"Dados exportados para:\n{filepath}")
            
        except Exception as e:
            logging.error(f"Erro ao exportar CSV: {e}")
            self.status_var.set("Erro na exportação")
            messagebox.showerror("Erro", f"Erro ao exportar CSV:\n{e}")
    
    def export_pdf(self):
        """Exporta para PDF"""
        try:
            self.status_var.set("Exportando PDF...")
            
            professores = self.teacher_manager.get_teachers_by_school(self.sistema.current_school)
            filepath = self.export_manager.export_pdf(professores, self.sistema.current_school)
            
            self.status_var.set("PDF exportado com sucesso")
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filepath}")
            
        except Exception as e:
            logging.error(f"Erro ao exportar PDF: {e}")
            self.status_var.set("Erro na exportação")
            messagebox.showerror("Erro", f"Erro ao exportar PDF:\n{e}")
    
    def show_about(self):
        """Mostra informações sobre o sistema"""
        about_text = """Sistema DIRENS - Controle de Professores
Versão 1.0

Aplicação Desktop desenvolvida em Python + Tkinter
para gerenciamento de professores das escolas
subordinadas à DIRENS.

Funcionalidades:
• Cadastro completo de professores
• Controle de acesso por escola
• Histórico de alterações
• Exportações (CSV/PDF)
• Backups automáticos
• Estatísticas e relatórios

Desenvolvido em 2024"""
        
        messagebox.showinfo("Sobre o Sistema", about_text)
    
    def logout(self):
        """Realiza logout do sistema"""
        response = messagebox.askyesno("Logout", "Deseja realmente sair do sistema?")
        if response:
            self.root.destroy()
            self.sistema.logout()
            
            # Reinicia o sistema
            from interface.login import LoginWindow
            new_root = tk.Tk()
            new_root.withdraw()
            LoginWindow(new_root, self.sistema)
            new_root.mainloop()
    
    def on_close(self):
        """Fecha a aplicação"""
        response = messagebox.askyesno("Sair", "Deseja realmente fechar o sistema?")
        if response:
            logging.info("Sistema encerrado pelo usuário")
            self.root.quit()
