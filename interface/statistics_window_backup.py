# -*- coding: utf-8 -*-
"""
Janela de Estatísticas - Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from recursos.constants import CARGAS_HORARIAS, CARREIRAS, POS_GRADUACAO

class StatisticsWindow:
    """Janela para visualização de estatísticas"""
    
    def __init__(self, parent, teacher_manager, school):
        """Inicializa a janela de estatísticas"""
        self.parent = parent
        self.teacher_manager = teacher_manager
        self.school = school
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title(f"Estatísticas - {school}")
        self.window.geometry("1000x700")
        self.window.resizable(True, True)
        
        # Modal
        self.window.grab_set()
        self.window.focus_set()
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
        
        # Carrega dados
        self.load_statistics()
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 1000
        height = 700
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(
            header_frame,
            text=f"Estatísticas - {self.school}",
            font=("Arial", 16, "bold")
        ).pack(side=tk.LEFT)
        
        ttk.Button(
            header_frame,
            text="Atualizar",
            command=self.load_statistics
        ).pack(side=tk.RIGHT)
        
        ttk.Button(
            header_frame,
            text="Exportar Relatório",
            command=self.export_report
        ).pack(side=tk.RIGHT, padx=(0, 10))
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Aba de resumo
        self.create_summary_tab()
        
        # Aba de gráficos
        self.create_charts_tab()
        
        # Aba de detalhes
        self.create_details_tab()
        
        # Botão fechar
        ttk.Button(
            main_frame,
            text="Fechar",
            command=self.window.destroy
        ).pack(pady=10)
    
    def create_summary_tab(self):
        """Cria aba de resumo"""
        summary_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(summary_frame, text="Resumo Geral")
        
        # Frame para cards de estatísticas
        cards_frame = ttk.Frame(summary_frame)
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Cards de estatísticas principais
        self.create_stat_card(cards_frame, "Total de Professores", "total_professores", 0, 0)
        self.create_stat_card(cards_frame, "Professores Ativos", "professores_ativos", 0, 1)
        self.create_stat_card(cards_frame, "40H Dedicação Exclusiva", "professores_40h_de", 0, 2)
        self.create_stat_card(cards_frame, "Com Doutorado", "professores_doutorado", 1, 0)
        self.create_stat_card(cards_frame, "Com Mestrado", "professores_mestrado", 1, 1)
        self.create_stat_card(cards_frame, "Carreira EBTT", "professores_ebtt", 1, 2)
        
        # Tabela de distribuição
        table_frame = ttk.LabelFrame(summary_frame, text="Distribuição por Categoria", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para tabela
        columns = ("Categoria", "Quantidade", "Percentual")
        self.summary_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.summary_tree.heading(col, text=col)
            self.summary_tree.column(col, width=150, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scrollbar.set)
        
        self.summary_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_stat_card(self, parent, title, var_name, row, col):
        """Cria um card de estatística"""
        card_frame = ttk.LabelFrame(parent, text=title, padding="10")
        card_frame.grid(row=row, column=col, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Variável para o valor
        var = tk.StringVar()
        setattr(self, f"{var_name}_var", var)
        
        # Label com valor grande
        value_label = ttk.Label(
            card_frame,
            textvariable=var,
            font=("Arial", 20, "bold"),
            anchor=tk.CENTER
        )
        value_label.pack()
        
        # Configura grid
        parent.grid_columnconfigure(col, weight=1)
    
    def create_charts_tab(self):
        """Cria aba de gráficos"""
        charts_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(charts_frame, text="Gráficos")
        
        # Frame para os gráficos
        self.charts_container = ttk.Frame(charts_frame)
        self.charts_container.pack(fill=tk.BOTH, expand=True)
    
    def create_details_tab(self):
        """Cria aba de detalhes"""
        details_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(details_frame, text="Detalhes")
        
        # Frame para filtros
        filter_frame = ttk.LabelFrame(details_frame, text="Filtros", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Filtros
        ttk.Label(filter_frame, text="Pós-graduação:").pack(side=tk.LEFT, padx=(0, 5))
        self.detail_pos_var = tk.StringVar()
        ttk.Combobox(
            filter_frame,
            textvariable=self.detail_pos_var,
            values=["Todos"] + POS_GRADUACAO,
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(filter_frame, text="Carreira:").pack(side=tk.LEFT, padx=(0, 5))
        self.detail_carreira_var = tk.StringVar()
        ttk.Combobox(
            filter_frame,
            textvariable=self.detail_carreira_var,
            values=["Todos"] + CARREIRAS,
            state="readonly",
            width=15
        ).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Button(
            filter_frame,
            text="Aplicar Filtros",
            command=self.apply_detail_filters
        ).pack(side=tk.LEFT, padx=20)
        
        # Lista detalhada
        list_frame = ttk.Frame(details_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("SIAPE", "Nome", "Carreira", "Carga Horária", "Pós-graduação", "Status")
        self.details_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        column_widths = {
            "SIAPE": 100,
            "Nome": 250,
            "Carreira": 100,
            "Carga Horária": 120,
            "Pós-graduação": 130,
            "Status": 100
        }
        
        for col in columns:
            self.details_tree.heading(col, text=col)
            self.details_tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.details_tree.yview)
        h_scroll = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.details_tree.xview)
        
        self.details_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.details_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Definir valores padrão dos filtros
        self.detail_pos_var.set("Todos")
        self.detail_carreira_var.set("Todos")
    
    def load_statistics(self):
        """Carrega as estatísticas"""
        try:
            # Carrega dados dos professores
            professores_todos = self.teacher_manager.get_teachers_by_school(self.school)
            
            # Filtra aposentados do cômputo (mas mantém no registro)
            professores = [p for p in professores_todos if p.get('status', 'Ativo') != 'Aposentado']
            
            if not professores:
                messagebox.showinfo("Informação", "Nenhum professor ativo encontrado para esta escola")
                return
            
            # Calcula estatísticas
            self.calculate_statistics(professores)
            
            # Atualiza gráficos
            self.update_charts(professores)
            
            # Atualiza lista de detalhes
            self.update_details_list(professores)
            
        except Exception as e:
            logging.error(f"Erro ao carregar estatísticas: {e}")
            messagebox.showerror("Erro", f"Erro ao carregar estatísticas:\n{e}")
    
    def calculate_statistics(self, professores):
        """Calcula as estatísticas principais"""
        total = len(professores)
        
        # Contadores
        ativos = len([p for p in professores if p.get('status', 'Ativo') == 'Ativo'])
        prof_40h_de = len([p for p in professores if p.get('carga_horaria') == '40H_DE'])
        doutorado = len([p for p in professores if p.get('pos_graduacao') == 'DOUTORADO'])
        mestrado = len([p for p in professores if p.get('pos_graduacao') == 'MESTRADO'])
        ebtt = len([p for p in professores if p.get('carreira') == 'EBTT'])
        
        # Atualiza cards
        self.total_professores_var.set(str(total))
        self.professores_ativos_var.set(str(ativos))
        self.professores_40h_de_var.set(str(prof_40h_de))
        self.professores_doutorado_var.set(str(doutorado))
        self.professores_mestrado_var.set(str(mestrado))
        self.professores_ebtt_var.set(str(ebtt))
        
        # Atualiza tabela de distribuição
        self.update_summary_table(professores, total)
    
    def update_summary_table(self, professores, total):
        """Atualiza a tabela de resumo"""
        # Limpa tabela
        for item in self.summary_tree.get_children():
            self.summary_tree.delete(item)
        
        if total == 0:
            return
        
        # Distribuição por pós-graduação
        pos_counter = Counter([p.get('pos_graduacao', 'Não informado') for p in professores])
        self.summary_tree.insert('', tk.END, values=("PÓS-GRADUAÇÃO", "", ""))
        
        for pos, count in sorted(pos_counter.items()):
            percent = (count / total) * 100
            self.summary_tree.insert('', tk.END, values=(
                f"  {pos}", str(count), f"{percent:.1f}%"
            ))
        
        # Distribuição por carga horária
        carga_counter = Counter([p.get('carga_horaria', 'Não informado') for p in professores])
        self.summary_tree.insert('', tk.END, values=("", "", ""))
        self.summary_tree.insert('', tk.END, values=("CARGA HORÁRIA", "", ""))
        
        for carga, count in sorted(carga_counter.items()):
            percent = (count / total) * 100
            self.summary_tree.insert('', tk.END, values=(
                f"  {carga}", str(count), f"{percent:.1f}%"
            ))
        
        # Distribuição por carreira
        carreira_counter = Counter([p.get('carreira', 'Não informado') for p in professores])
        self.summary_tree.insert('', tk.END, values=("", "", ""))
        self.summary_tree.insert('', tk.END, values=("CARREIRA", "", ""))
        
        for carreira, count in sorted(carreira_counter.items()):
            percent = (count / total) * 100
            self.summary_tree.insert('', tk.END, values=(
                f"  {carreira}", str(count), f"{percent:.1f}%"
            ))
    
    def update_charts(self, professores):
        """Atualiza os gráficos"""
        # Limpa container de gráficos
        for widget in self.charts_container.winfo_children():
            widget.destroy()
        
        if not professores:
            ttk.Label(
                self.charts_container,
                text="Nenhum dado disponível para gráficos",
                font=("Arial", 12)
            ).pack(expand=True)
            return
        
        try:
            # Cria figura com subplots
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
            fig.suptitle(f'Estatísticas - {self.school}', fontsize=16, fontweight='bold')
            
            # Gráfico 1: Distribuição por pós-graduação
            pos_data = Counter([p.get('pos_graduacao', 'Não informado') for p in professores])
            if pos_data:
                labels1, values1 = zip(*pos_data.most_common())
                ax1.pie(values1, labels=labels1, autopct='%1.1f%%', startangle=90)
                ax1.set_title('Pós-graduação')
            
            # Gráfico 2: Distribuição por carga horária
            carga_data = Counter([p.get('carga_horaria', 'Não informado') for p in professores])
            if carga_data:
                labels2, values2 = zip(*carga_data.most_common())
                ax2.bar(labels2, values2, color=['#ff9999', '#66b3ff', '#99ff99'])
                ax2.set_title('Carga Horária')
                ax2.tick_params(axis='x', rotation=45)
            
            # Gráfico 3: Distribuição por carreira
            carreira_data = Counter([p.get('carreira', 'Não informado') for p in professores])
            if carreira_data:
                labels3, values3 = zip(*carreira_data.most_common())
                ax3.pie(values3, labels=labels3, autopct='%1.1f%%', startangle=90)
                ax3.set_title('Carreira')
            
            # Gráfico 4: Status dos professores
            status_data = Counter([p.get('status', 'Ativo') for p in professores])
            if status_data:
                labels4, values4 = zip(*status_data.most_common())
                colors = ['#90EE90' if l == 'Ativo' else '#FFB6C1' for l in labels4]
                ax4.bar(labels4, values4, color=colors)
                ax4.set_title('Status')
                ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            # Integra com Tkinter
            canvas = FigureCanvasTkAgg(fig, self.charts_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ImportError:
            # Fallback se matplotlib não estiver disponível
            ttk.Label(
                self.charts_container,
                text="Matplotlib não disponível.\nInstale com: pip install matplotlib",
                font=("Arial", 12),
                justify=tk.CENTER
            ).pack(expand=True)
        except Exception as e:
            logging.error(f"Erro ao criar gráficos: {e}")
            ttk.Label(
                self.charts_container,
                text=f"Erro ao gerar gráficos:\n{str(e)}",
                font=("Arial", 12),
                justify=tk.CENTER
            ).pack(expand=True)
    
    def update_details_list(self, professores):
        """Atualiza a lista de detalhes"""
        # Limpa lista
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        
        # Adiciona professores
        for professor in sorted(professores, key=lambda x: x.get('nome', '')):
            self.details_tree.insert('', tk.END, values=(
                professor.get('siape', ''),
                professor.get('nome', ''),
                professor.get('carreira', ''),
                professor.get('carga_horaria', ''),
                professor.get('pos_graduacao', ''),
                professor.get('status', 'Ativo')
            ))
    
    def apply_detail_filters(self):
        """Aplica filtros na lista de detalhes"""
        try:
            professores = self.teacher_manager.get_teachers_by_school(self.school)
            
            # Aplica filtros
            pos_filter = self.detail_pos_var.get()
            carreira_filter = self.detail_carreira_var.get()
            
            if pos_filter and pos_filter != "Todos":
                professores = [p for p in professores if p.get('pos_graduacao') == pos_filter]
            
            if carreira_filter and carreira_filter != "Todos":
                professores = [p for p in professores if p.get('carreira') == carreira_filter]
            
            # Atualiza lista
            self.update_details_list(professores)
            
        except Exception as e:
            logging.error(f"Erro ao aplicar filtros: {e}")
            messagebox.showerror("Erro", f"Erro ao aplicar filtros:\n{e}")
    
    def export_report(self):
        """Exporta relatório estatístico"""
        try:
            from tkinter import filedialog
            from datetime import datetime
            
            # Seleciona arquivo
            filename = filedialog.asksaveasfilename(
                title="Exportar Relatório de Estatísticas",
                defaultextension=".txt",
                filetypes=[
                    ("Arquivos de texto", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("Todos os arquivos", "*.*")
                ],
                initialname=f"estatisticas_{self.school}_{datetime.now().strftime('%Y%m%d')}.txt"
            )
            
            if not filename:
                return
            
            # Carrega dados
            professores = self.teacher_manager.get_teachers_by_school(self.school)
            
            # Gera relatório
            report_content = self.generate_report_content(professores)
            
            # Salva arquivo
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{filename}")
            
        except Exception as e:
            logging.error(f"Erro ao exportar relatório: {e}")
            messagebox.showerror("Erro", f"Erro ao exportar relatório:\n{e}")
    
    def generate_report_content(self, professores):
        """Gera conteúdo do relatório"""
        from datetime import datetime
        
        content = f"""RELATÓRIO DE ESTATÍSTICAS - SISTEMA DIRENS
Escola: {self.school}
Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

{'='*60}

RESUMO GERAL:
- Total de Professores: {len(professores)}
- Professores Ativos: {len([p for p in professores if p.get('status', 'Ativo') == 'Ativo'])}
- Professores 40H DE: {len([p for p in professores if p.get('carga_horaria') == '40H_DE'])}
- Com Doutorado: {len([p for p in professores if p.get('pos_graduacao') == 'DOUTORADO'])}
- Com Mestrado: {len([p for p in professores if p.get('pos_graduacao') == 'MESTRADO'])}
- Carreira EBTT: {len([p for p in professores if p.get('carreira') == 'EBTT'])}

{'='*60}

DISTRIBUIÇÃO POR PÓS-GRADUAÇÃO:
"""
        
        # Adiciona distribuição por pós-graduação
        pos_counter = Counter([p.get('pos_graduacao', 'Não informado') for p in professores])
        total = len(professores)
        
        for pos, count in sorted(pos_counter.items()):
            percent = (count / total) * 100 if total > 0 else 0
            content += f"- {pos}: {count} ({percent:.1f}%)\n"
        
        content += f"\n{'='*60}\n\nDISTRIBUIÇÃO POR CARGA HORÁRIA:\n"
        
        # Adiciona distribuição por carga horária
        carga_counter = Counter([p.get('carga_horaria', 'Não informado') for p in professores])
        
        for carga, count in sorted(carga_counter.items()):
            percent = (count / total) * 100 if total > 0 else 0
            content += f"- {carga}: {count} ({percent:.1f}%)\n"
        
        content += f"\n{'='*60}\n\nDISTRIBUIÇÃO POR CARREIRA:\n"
        
        # Adiciona distribuição por carreira
        carreira_counter = Counter([p.get('carreira', 'Não informado') for p in professores])
        
        for carreira, count in sorted(carreira_counter.items()):
            percent = (count / total) * 100 if total > 0 else 0
            content += f"- {carreira}: {count} ({percent:.1f}%)\n"
        
        content += f"\n{'='*60}\n\nLISTA COMPLETA DE PROFESSORES:\n"
        
        # Adiciona lista de professores
        for i, professor in enumerate(sorted(professores, key=lambda x: x.get('nome', '')), 1):
            content += f"\n{i:03d}. {professor.get('nome', '')}\n"
            content += f"     SIAPE: {professor.get('siape', '')}\n"
            content += f"     Carreira: {professor.get('carreira', '')}\n"
            content += f"     Carga Horária: {professor.get('carga_horaria', '')}\n"
            content += f"     Pós-graduação: {professor.get('pos_graduacao', '')}\n"
            content += f"     Status: {professor.get('status', 'Ativo')}\n"
        
        content += f"\n{'='*60}\n"
        content += f"Relatório gerado pelo Sistema DIRENS v1.0\n"
        content += f"Total de registros: {len(professores)}\n"
        
        return content
