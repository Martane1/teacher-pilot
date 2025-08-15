# -*- coding: utf-8 -*-
"""
Formulário de Professor do Sistema DIRENS
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging

from core.validators import ValidatorManager
from recursos.constants import CARGAS_HORARIAS, CARREIRAS, POS_GRADUACAO, DDDS_BRASIL

class TeacherFormWindow:
    """Janela do formulário de professor"""
    
    def __init__(self, parent, teacher_manager, school, teacher_data=None, callback=None, current_user='admin'):
        """Inicializa o formulário"""
        self.parent = parent
        self.teacher_manager = teacher_manager
        self.school = school
        self.teacher_data = teacher_data
        self.callback = callback
        self.current_user = current_user
        self.validator = ValidatorManager()
        
        # Determina se é edição ou novo
        self.is_edit = teacher_data is not None
        
        # Cria a janela
        self.window = tk.Toplevel(parent)
        self.window.title("Editar Professor" if self.is_edit else "Novo Professor")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # Centraliza
        self.center_window()
        
        # Cria a interface
        self.create_widgets()
        
        # Preenche dados se for edição
        if self.is_edit:
            self.populate_fields()
            
        # Modal - só depois da janela estar completamente criada
        self.window.after(100, self.make_modal)
    
    def center_window(self):
        """Centraliza a janela"""
        self.window.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        width = 600
        height = 700
        
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def make_modal(self):
        """Torna a janela modal após estar completamente carregada"""
        try:
            self.window.grab_set()
            self.window.focus_set()
            self.window.lift()  # Traz para frente
        except Exception as e:
            logging.warning(f"Não foi possível tornar janela modal: {e}")
    
    def create_widgets(self):
        """Cria os widgets do formulário"""
        # Frame principal com scrollbar
        canvas = tk.Canvas(self.window)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
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
        
        # Frame do conteúdo
        main_frame = ttk.Frame(scrollable_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_text = "Editar Professor" if self.is_edit else "Novo Professor"
        ttk.Label(
            main_frame,
            text=title_text,
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 20))
        
        # Dados pessoais
        self.create_personal_section(main_frame)
        
        # Dados profissionais
        self.create_professional_section(main_frame)
        
        # Dados acadêmicos
        self.create_academic_section(main_frame)
        
        # Botões
        self.create_buttons(main_frame)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.status_var, foreground="red").pack(pady=10)
        
        # Configurar rolagem com mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_personal_section(self, parent):
        """Cria seção de dados pessoais"""
        personal_frame = ttk.LabelFrame(parent, text="Dados Pessoais", padding="15")
        personal_frame.pack(fill=tk.X, pady=(0, 15))
        personal_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # SIAPE
        ttk.Label(personal_frame, text="SIAPE:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.siape_var = tk.StringVar()
        siape_entry = ttk.Entry(personal_frame, textvariable=self.siape_var, width=20)
        siape_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        # SIAPE agora pode ser editado conforme solicitado pelo usuário
        # if self.is_edit:
        #     siape_entry.config(state='readonly')
        
        row += 1
        
        # Nome completo
        ttk.Label(personal_frame, text="Nome Completo:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.nome_var = tk.StringVar()
        nome_entry = ttk.Entry(personal_frame, textvariable=self.nome_var, width=50)
        nome_entry.grid(row=row, column=1, sticky="we", pady=5, columnspan=2)
        
        # Bind para converter para maiúscula
        self.nome_var.trace('w', self.on_name_change)
        
        row += 1
        
        # CPF removido por questões de segurança
        
        # Data de nascimento
        ttk.Label(personal_frame, text="Data Nascimento:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.data_nascimento_var = tk.StringVar()
        data_nasc_entry = ttk.Entry(personal_frame, textvariable=self.data_nascimento_var, width=15)
        data_nasc_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(personal_frame, text="(DD-MM-AAAA)", foreground="gray").grid(row=row, column=2, sticky=tk.W, padx=5)
        
        row += 1
        
        # Sexo
        ttk.Label(personal_frame, text="Sexo:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.sexo_var = tk.StringVar()
        sexo_frame = ttk.Frame(personal_frame)
        sexo_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(sexo_frame, text="Masculino", variable=self.sexo_var, value="M").pack(side=tk.LEFT)
        ttk.Radiobutton(sexo_frame, text="Feminino", variable=self.sexo_var, value="F").pack(side=tk.LEFT, padx=10)
        
        row += 1
        
        # Email institucional
        ttk.Label(personal_frame, text="Email Institucional:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        email_frame = ttk.Frame(personal_frame)
        email_frame.grid(row=row, column=1, sticky="we", pady=5, columnspan=2)
        
        self.email_nome_var = tk.StringVar()
        email_entry = ttk.Entry(email_frame, textvariable=self.email_nome_var, width=20)
        email_entry.pack(side=tk.LEFT)
        ttk.Label(email_frame, text="@fab.mil.br", foreground="blue").pack(side=tk.LEFT, padx=5)
        
        row += 1
        
        # Telefone celular
        ttk.Label(personal_frame, text="Telefone Celular:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        celular_frame = ttk.Frame(personal_frame)
        celular_frame.grid(row=row, column=1, sticky="w", pady=5, columnspan=2)
        
        self.ddd_celular_var = tk.StringVar()
        ttk.Combobox(
            celular_frame,
            textvariable=self.ddd_celular_var,
            values=DDDS_BRASIL,
            state="readonly",
            width=8
        ).pack(side=tk.LEFT)
        ttk.Label(celular_frame, text="-9-", foreground="blue").pack(side=tk.LEFT)
        
        self.numero_celular_var = tk.StringVar()
        celular_entry = ttk.Entry(celular_frame, textvariable=self.numero_celular_var, width=15)
        celular_entry.pack(side=tk.LEFT)
        ttk.Label(celular_frame, text="(xxxx-xxxx)", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Bind para formatar número do celular
        self.numero_celular_var.trace('w', self.format_numero_celular)
        
        row += 1
        
        # Telefone fixo
        ttk.Label(personal_frame, text="Telefone Fixo:").grid(row=row, column=0, sticky=tk.W, pady=5)
        fixo_frame = ttk.Frame(personal_frame)
        fixo_frame.grid(row=row, column=1, sticky="w", pady=5, columnspan=2)
        
        self.ddd_fixo_var = tk.StringVar()
        ttk.Combobox(
            fixo_frame,
            textvariable=self.ddd_fixo_var,
            values=DDDS_BRASIL,
            state="readonly",
            width=8
        ).pack(side=tk.LEFT)
        ttk.Label(fixo_frame, text="-", foreground="blue").pack(side=tk.LEFT)
        
        self.numero_fixo_var = tk.StringVar()
        fixo_entry = ttk.Entry(fixo_frame, textvariable=self.numero_fixo_var, width=15)
        fixo_entry.pack(side=tk.LEFT)
        ttk.Label(fixo_frame, text="(xxxx-xxxx)", foreground="gray").pack(side=tk.LEFT, padx=5)
        
        # Bind para formatar número do fixo
        self.numero_fixo_var.trace('w', self.format_numero_fixo)
        
        row += 1
    
    def create_professional_section(self, parent):
        """Cria seção de dados profissionais"""
        prof_frame = ttk.LabelFrame(parent, text="Dados Profissionais", padding="15")
        prof_frame.pack(fill=tk.X, pady=(0, 15))
        prof_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Carga horária
        ttk.Label(prof_frame, text="Carga Horária:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.carga_horaria_var = tk.StringVar()
        ttk.Combobox(
            prof_frame,
            textvariable=self.carga_horaria_var,
            values=CARGAS_HORARIAS,
            state="readonly",
            width=15
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        
        # Carreira
        ttk.Label(prof_frame, text="Carreira:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.carreira_var = tk.StringVar()
        ttk.Combobox(
            prof_frame,
            textvariable=self.carreira_var,
            values=CARREIRAS,
            state="readonly",
            width=15
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        
        # Data de ingresso
        ttk.Label(prof_frame, text="Data Ingresso:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.data_ingresso_var = tk.StringVar()
        data_ing_entry = ttk.Entry(prof_frame, textvariable=self.data_ingresso_var, width=15)
        data_ing_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Label(prof_frame, text="(DD-MM-AAAA)", foreground="gray").grid(row=row, column=2, sticky=tk.W, padx=5)
        
        row += 1
        
        # Status
        ttk.Label(prof_frame, text="Status:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.status_prof_var = tk.StringVar()
        ttk.Combobox(
            prof_frame,
            textvariable=self.status_prof_var,
            values=["Ativo", "Afastado", "Licença", "Aposentado"],
            state="readonly",
            width=15
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        
        # Área de atuação
        ttk.Label(prof_frame, text="Área de Atuação:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.area_atuacao_var = tk.StringVar()
        ttk.Entry(prof_frame, textvariable=self.area_atuacao_var, width=40).grid(row=row, column=1, sticky="we", pady=5)
    
    def create_academic_section(self, parent):
        """Cria seção de dados acadêmicos"""
        acad_frame = ttk.LabelFrame(parent, text="Dados Acadêmicos", padding="15")
        acad_frame.pack(fill=tk.X, pady=(0, 15))
        acad_frame.grid_columnconfigure(1, weight=1)
        
        row = 0
        
        # Pós-graduação
        ttk.Label(acad_frame, text="Pós-graduação:*").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.pos_graduacao_var = tk.StringVar()
        ttk.Combobox(
            acad_frame,
            textvariable=self.pos_graduacao_var,
            values=POS_GRADUACAO,
            state="readonly",
            width=20
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        
        row += 1
        
        # Graduação
        ttk.Label(acad_frame, text="Graduação:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.graduacao_var = tk.StringVar()
        ttk.Entry(acad_frame, textvariable=self.graduacao_var, width=40).grid(row=row, column=1, sticky="we", pady=5)
        
        row += 1
        
        # Instituição de graduação
        ttk.Label(acad_frame, text="Instituição Graduação:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.instituicao_grad_var = tk.StringVar()
        ttk.Entry(acad_frame, textvariable=self.instituicao_grad_var, width=40).grid(row=row, column=1, sticky="we", pady=5)
        
        row += 1
        
        # Especialização/Mestrado/Doutorado
        ttk.Label(acad_frame, text="Curso Pós-graduação:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.curso_pos_var = tk.StringVar()
        ttk.Entry(acad_frame, textvariable=self.curso_pos_var, width=40).grid(row=row, column=1, sticky="we", pady=5)
        
        row += 1
        
        # Instituição pós
        ttk.Label(acad_frame, text="Instituição Pós:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.instituicao_pos_var = tk.StringVar()
        ttk.Entry(acad_frame, textvariable=self.instituicao_pos_var, width=40).grid(row=row, column=1, sticky="we", pady=5)
    
    def create_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=20)
        
        # Botão salvar
        save_text = "Atualizar" if self.is_edit else "Salvar"
        ttk.Button(
            button_frame,
            text=save_text,
            command=self.save_teacher,
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
    
    def on_name_change(self, *args):
        """Converte nome para maiúscula"""
        current = self.nome_var.get()
        if current != current.upper():
            # Salva posição do cursor
            cursor_pos = 0
            try:
                # Tenta obter a posição do cursor (pode falhar em alguns casos)
                widget = self.window.focus_get()
                if widget and hasattr(widget, 'index'):
                    cursor_pos = widget.index(tk.INSERT)
            except:
                pass
            
            # Atualiza valor
            self.nome_var.set(current.upper())
            
            # Restaura posição do cursor
            try:
                widget = self.window.focus_get()
                if widget and hasattr(widget, 'icursor'):
                    widget.icursor(cursor_pos)
            except:
                pass
    
    def populate_fields(self):
        """Preenche os campos com dados do professor"""
        if not self.teacher_data:
            return
        
        # Dados pessoais
        self.siape_var.set(self.teacher_data.get('siape', ''))
        self.nome_var.set(self.teacher_data.get('nome', ''))
        self.data_nascimento_var.set(self.teacher_data.get('data_nascimento', ''))
        self.sexo_var.set(self.teacher_data.get('sexo', ''))
        
        # Email
        email_completo = self.teacher_data.get('email', '')
        if '@fab.mil.br' in email_completo:
            self.email_nome_var.set(email_completo.replace('@fab.mil.br', ''))
        else:
            self.email_nome_var.set(email_completo)
            
        # Telefone celular
        celular = self.teacher_data.get('telefone_celular', '')
        if celular and '-9-' in celular:
            partes = celular.split('-')
            if len(partes) >= 3:
                self.ddd_celular_var.set(partes[0])
                self.numero_celular_var.set('-'.join(partes[2:]))
        
        # Telefone fixo
        fixo = self.teacher_data.get('telefone_fixo', '')
        if fixo and '-' in fixo:
            partes = fixo.split('-', 1)
            if len(partes) == 2:
                self.ddd_fixo_var.set(partes[0])
                self.numero_fixo_var.set(partes[1])
        
        # Dados profissionais
        self.carga_horaria_var.set(self.teacher_data.get('carga_horaria', ''))
        self.carreira_var.set(self.teacher_data.get('carreira', ''))
        self.data_ingresso_var.set(self.teacher_data.get('data_ingresso', ''))
        self.status_prof_var.set(self.teacher_data.get('status', 'Ativo'))
        self.area_atuacao_var.set(self.teacher_data.get('area_atuacao', ''))
        
        # Dados acadêmicos
        self.pos_graduacao_var.set(self.teacher_data.get('pos_graduacao', ''))
        self.graduacao_var.set(self.teacher_data.get('graduacao', ''))
        self.instituicao_grad_var.set(self.teacher_data.get('instituicao_graduacao', ''))
        self.curso_pos_var.set(self.teacher_data.get('curso_pos', ''))
        self.instituicao_pos_var.set(self.teacher_data.get('instituicao_pos', ''))
    
    def clear_form(self):
        """Limpa todos os campos do formulário"""
        # Dados pessoais
        self.siape_var.set('')
        self.nome_var.set('')
        self.data_nascimento_var.set('')
        self.sexo_var.set('')
        self.email_nome_var.set('')
        self.ddd_celular_var.set('')
        self.numero_celular_var.set('')
        self.ddd_fixo_var.set('')
        self.numero_fixo_var.set('')
        
        # Dados profissionais
        self.carga_horaria_var.set('')
        self.carreira_var.set('')
        self.data_ingresso_var.set('')
        self.status_prof_var.set('Ativo')
        self.area_atuacao_var.set('')
        
        # Dados acadêmicos
        self.pos_graduacao_var.set('')
        self.graduacao_var.set('')
        self.instituicao_grad_var.set('')
        self.curso_pos_var.set('')
        self.instituicao_pos_var.set('')
        
        self.status_var.set('')
    
    def validate_form(self):
        """Valida os dados do formulário"""
        errors = []
        
        # Campos obrigatórios
        required_fields = {
            'SIAPE': self.siape_var.get().strip(),
            'Nome': self.nome_var.get().strip(),
            'Data de Nascimento': self.data_nascimento_var.get().strip(),
            'Sexo': self.sexo_var.get(),
            'Email Institucional': self.email_nome_var.get().strip(),
            'DDD Celular': self.ddd_celular_var.get(),
            'Número Celular': self.numero_celular_var.get().strip(),
            'Carga Horária': self.carga_horaria_var.get(),
            'Carreira': self.carreira_var.get(),
            'Data de Ingresso': self.data_ingresso_var.get().strip(),
            'Pós-graduação': self.pos_graduacao_var.get()
        }
        
        for field, value in required_fields.items():
            if not value:
                errors.append(f"{field} é obrigatório")
        
        if errors:
            return errors
        
        # Validações específicas
        siape = self.siape_var.get().strip()
        if not self.validator.validate_siape(siape):
            errors.append("SIAPE deve ter exatamente 7 dígitos numéricos")
        
        data_nasc = self.data_nascimento_var.get().strip()
        if not self.validator.validate_date(data_nasc):
            errors.append("Data de nascimento inválida (use DD-MM-AAAA)")
        
        data_ing = self.data_ingresso_var.get().strip()
        if not self.validator.validate_date(data_ing):
            errors.append("Data de ingresso inválida (use DD-MM-AAAA)")
        
        # Validação do email institucional
        email_nome = self.email_nome_var.get().strip()
        if not self.validator.validate_fab_email(email_nome):
            errors.append("Email institucional deve conter apenas letras, números e pontos")
        
        # Validação do telefone celular
        ddd_celular = self.ddd_celular_var.get()
        numero_celular = self.numero_celular_var.get().strip()
        if not self.validator.validate_numero_telefone(numero_celular):
            errors.append("Número do celular deve estar no formato xxxx-xxxx")
        
        # Validação do telefone fixo (opcional)
        ddd_fixo = self.ddd_fixo_var.get()
        numero_fixo = self.numero_fixo_var.get().strip()
        if ddd_fixo or numero_fixo:  # Se um foi preenchido, ambos devem estar
            if not ddd_fixo:
                errors.append("DDD do telefone fixo é obrigatório")
            if not numero_fixo:
                errors.append("Número do telefone fixo é obrigatório")
            elif not self.validator.validate_numero_telefone(numero_fixo):
                errors.append("Número do fixo deve estar no formato xxxx-xxxx")
        
        # Verifica se SIAPE já existe
        if not self.is_edit:
            # Novo professor - verifica se SIAPE já existe
            if self.teacher_manager.teacher_exists(siape, self.school):
                errors.append("SIAPE já cadastrado nesta escola")
        else:
            # Edição - permite o mesmo SIAPE ou verifica se o novo SIAPE já existe
            original_siape = self.teacher_data.get('siape', '') if self.teacher_data else ''
            if siape != original_siape and self.teacher_manager.teacher_exists(siape, self.school):
                errors.append("SIAPE já cadastrado nesta escola")
        
        return errors
    
    def save_teacher(self):
        """Salva os dados do professor"""
        # Valida formulário
        errors = self.validate_form()
        if errors:
            self.status_var.set(errors[0])
            return
        
        # Prepara dados
        # Monta telefone celular
        telefone_celular = f"{self.ddd_celular_var.get()}-9-{self.numero_celular_var.get()}" if self.ddd_celular_var.get() and self.numero_celular_var.get() else ''
        
        # Monta telefone fixo (opcional)
        telefone_fixo = ''
        if self.ddd_fixo_var.get() and self.numero_fixo_var.get():
            telefone_fixo = f"{self.ddd_fixo_var.get()}-{self.numero_fixo_var.get()}"
            
        teacher_data = {
            'siape': self.siape_var.get().strip(),
            'nome': self.nome_var.get().strip().upper(),
            'data_nascimento': self.data_nascimento_var.get().strip(),
            'sexo': self.sexo_var.get(),
            'email': self.email_nome_var.get().strip() + '@fab.mil.br',
            'telefone_celular': telefone_celular,
            'telefone_fixo': telefone_fixo,
            'carga_horaria': self.carga_horaria_var.get(),
            'carreira': self.carreira_var.get(),
            'data_ingresso': self.data_ingresso_var.get().strip(),
            'status': self.status_prof_var.get() or 'Ativo',
            'area_atuacao': self.area_atuacao_var.get().strip(),
            'pos_graduacao': self.pos_graduacao_var.get(),
            'graduacao': self.graduacao_var.get().strip(),
            'instituicao_graduacao': self.instituicao_grad_var.get().strip(),
            'curso_pos': self.curso_pos_var.get().strip(),
            'instituicao_pos': self.instituicao_pos_var.get().strip(),
            'escola': self.school,
            'data_criacao': datetime.now().isoformat() if not self.is_edit else (self.teacher_data.get('data_criacao') if self.teacher_data else datetime.now().isoformat()),
            'data_atualizacao': datetime.now().isoformat()
        }
        
        try:
            if self.is_edit:
                # Atualizar professor existente
                success = self.teacher_manager.update_teacher(
                    teacher_data, 
                    self.school,
                    self.current_user
                )
            else:
                # Criar novo professor
                success = self.teacher_manager.create_teacher(
                    teacher_data,
                    self.current_user
                )
            
            if success:
                action = "atualizado" if self.is_edit else "criado"
                messagebox.showinfo("Sucesso", f"Professor {action} com sucesso!")
                
                # Chama callback se definido
                if self.callback:
                    self.callback()
                
                # Fecha janela
                self.window.destroy()
            else:
                self.status_var.set("Erro ao salvar dados do professor")
                
        except Exception as e:
            logging.error(f"Erro ao salvar professor: {e}")
            self.status_var.set("Erro interno do sistema")
            messagebox.showerror("Erro", f"Erro ao salvar professor:\n{e}")
    
    def format_numero_celular(self, *args):
        """Formata número do celular automaticamente (xxxx-xxxx)"""
        current = self.numero_celular_var.get()
        # Remove caracteres não numéricos
        digits = ''.join(filter(str.isdigit, current))
        
        # Formata conforme o padrão xxxx-xxxx
        if len(digits) >= 8:
            formatted = f"{digits[:4]}-{digits[4:8]}"
            if current != formatted:
                self.numero_celular_var.set(formatted)
    
    def format_numero_fixo(self, *args):
        """Formata número do fixo automaticamente (xxxx-xxxx)"""
        current = self.numero_fixo_var.get()
        # Remove caracteres não numéricos
        digits = ''.join(filter(str.isdigit, current))
        
        # Formata conforme o padrão xxxx-xxxx
        if len(digits) >= 8:
            formatted = f"{digits[:4]}-{digits[4:8]}"
            if current != formatted:
                self.numero_fixo_var.set(formatted)
