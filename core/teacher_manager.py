# -*- coding: utf-8 -*-
"""
Gerenciador de Professores - Sistema DIRENS
"""

import logging
from datetime import datetime
import json
import os

from dados.data_manager import DataManager
from dados.history_manager import HistoryManager
from core.validators import ValidatorManager

class TeacherManager:
    """Gerenciador de operações com professores"""
    
    def __init__(self):
        """Inicializa o gerenciador"""
        self.data_manager = DataManager()
        self.history_manager = HistoryManager()
        self.validator = ValidatorManager()
    
    def create_teacher(self, teacher_data, user):
        """Cria um novo professor"""
        try:
            # Valida dados
            validation_result = self.validator.validate_teacher_data(teacher_data)
            if not validation_result['valid']:
                logging.error(f"Dados inválidos: {validation_result['errors']}")
                return False
            
            # Verifica se SIAPE já existe
            if self.teacher_exists(teacher_data['siape'], teacher_data['escola']):
                logging.error(f"SIAPE já existe: {teacher_data['siape']}")
                return False
            
            # Adiciona metadados
            teacher_data['data_criacao'] = datetime.now().isoformat()
            teacher_data['data_atualizacao'] = datetime.now().isoformat()
            teacher_data['criado_por'] = user
            
            # Salva no data manager
            success = self.data_manager.save_teacher(teacher_data)
            
            if success:
                # Registra no histórico
                self.history_manager.add_history_entry({
                    'siape': teacher_data['siape'],
                    'escola': teacher_data['escola'],
                    'action': 'CREATE',
                    'user': user,
                    'timestamp': datetime.now().isoformat(),
                    'field': 'professor',
                    'old_value': None,
                    'new_value': 'Novo professor criado',
                    'notes': f"Professor {teacher_data['nome']} criado com SIAPE {teacher_data['siape']}"
                })
                
                logging.info(f"Professor criado: {teacher_data['siape']} - {teacher_data['nome']}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Erro ao criar professor: {e}")
            return False
    
    def update_teacher(self, teacher_data, school, user):
        """Atualiza dados de um professor"""
        try:
            siape = teacher_data['siape']
            
            # Carrega dados atuais
            current_data = self.data_manager.get_teacher_by_siape(siape, school)
            if not current_data:
                logging.error(f"Professor não encontrado: {siape}")
                return False
            
            # Valida novos dados
            validation_result = self.validator.validate_teacher_data(teacher_data)
            if not validation_result['valid']:
                logging.error(f"Dados inválidos: {validation_result['errors']}")
                return False
            
            # Atualiza metadados
            teacher_data['data_atualizacao'] = datetime.now().isoformat()
            teacher_data['atualizado_por'] = user
            
            # Preserva dados de criação
            teacher_data['data_criacao'] = current_data.get('data_criacao')
            teacher_data['criado_por'] = current_data.get('criado_por')
            
            # Identifica alterações
            changes = self.identify_changes(current_data, teacher_data)
            
            # Salva alterações
            success = self.data_manager.update_teacher(teacher_data)
            
            if success:
                # Registra histórico das alterações
                for field, (old_value, new_value) in changes.items():
                    self.history_manager.add_history_entry({
                        'siape': siape,
                        'escola': school,
                        'action': 'UPDATE',
                        'user': user,
                        'timestamp': datetime.now().isoformat(),
                        'field': field,
                        'old_value': str(old_value) if old_value is not None else '',
                        'new_value': str(new_value) if new_value is not None else '',
                        'notes': f"Campo {field} alterado"
                    })
                
                logging.info(f"Professor atualizado: {siape} - {len(changes)} alterações")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Erro ao atualizar professor: {e}")
            return False
    
    def delete_teacher(self, siape, school, user):
        """Exclui um professor"""
        try:
            # Verifica se professor existe
            teacher_data = self.data_manager.get_teacher_by_siape(siape, school)
            if not teacher_data:
                logging.error(f"Professor não encontrado: {siape}")
                return False
            
            # Marca como excluído em vez de deletar fisicamente
            teacher_data['status'] = 'Excluído'
            teacher_data['data_exclusao'] = datetime.now().isoformat()
            teacher_data['excluido_por'] = user
            
            # Atualiza registro
            success = self.data_manager.update_teacher(teacher_data)
            
            if success:
                # Registra no histórico
                self.history_manager.add_history_entry({
                    'siape': siape,
                    'escola': school,
                    'action': 'DELETE',
                    'user': user,
                    'timestamp': datetime.now().isoformat(),
                    'field': 'professor',
                    'old_value': teacher_data['nome'],
                    'new_value': 'EXCLUÍDO',
                    'notes': f"Professor {teacher_data['nome']} excluído"
                })
                
                logging.info(f"Professor excluído: {siape} - {teacher_data['nome']}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Erro ao excluir professor: {e}")
            return False
    
    def get_teacher_by_siape(self, siape, school):
        """Busca professor por SIAPE"""
        try:
            return self.data_manager.get_teacher_by_siape(siape, school)
        except Exception as e:
            logging.error(f"Erro ao buscar professor: {e}")
            return None
    
    def get_teachers_by_school(self, school, include_deleted=False):
        """Lista professores de uma escola"""
        try:
            teachers = self.data_manager.get_teachers_by_school(school)
            
            if not include_deleted:
                # Filtra professores não excluídos
                teachers = [t for t in teachers if t.get('status') != 'Excluído']
            
            return teachers
            
        except Exception as e:
            logging.error(f"Erro ao listar professores: {e}")
            return []
    
    def get_all_teachers(self, include_deleted=False):
        """Lista todos os professores de todas as escolas"""
        try:
            teachers = self.data_manager.get_all_teachers()
            
            if not include_deleted:
                # Filtra professores não excluídos
                teachers = [t for t in teachers if t.get('status') != 'Excluído']
            
            return teachers
            
        except Exception as e:
            logging.error(f"Erro ao listar todos os professores: {e}")
            return []
    
    def search_teachers(self, school, search_term, filters=None):
        """Busca professores com filtros"""
        try:
            teachers = self.get_teachers_by_school(school)
            
            if not teachers:
                return []
            
            # Aplica busca por termo
            if search_term:
                search_term = search_term.lower().strip()
                teachers = [
                    t for t in teachers
                    if search_term in t.get('nome', '').lower() or
                       search_term in t.get('siape', '')
                ]
            
            # Aplica filtros adicionais
            if filters:
                if filters.get('pos_graduacao'):
                    teachers = [t for t in teachers if t.get('pos_graduacao') == filters['pos_graduacao']]
                
                if filters.get('carga_horaria'):
                    teachers = [t for t in teachers if t.get('carga_horaria') == filters['carga_horaria']]
                
                if filters.get('carreira'):
                    teachers = [t for t in teachers if t.get('carreira') == filters['carreira']]
                
                if filters.get('status'):
                    teachers = [t for t in teachers if t.get('status') == filters['status']]
            
            return teachers
            
        except Exception as e:
            logging.error(f"Erro na busca de professores: {e}")
            return []
    
    def teacher_exists(self, siape, school):
        """Verifica se professor já existe"""
        try:
            teacher = self.data_manager.get_teacher_by_siape(siape, school)
            return teacher is not None and teacher.get('status') != 'Excluído'
        except Exception as e:
            logging.error(f"Erro ao verificar existência do professor: {e}")
            return False
    
    def identify_changes(self, old_data, new_data):
        """Identifica alterações entre dados antigos e novos"""
        changes = {}
        
        # Campos que devem ser monitorados
        monitored_fields = [
            'nome', 'data_nascimento', 'sexo', 'estado', 'email', 'telefone',
            'carga_horaria', 'carreira', 'data_ingresso', 'status',
            'area_atuacao', 'pos_graduacao', 'graduacao', 'instituicao_graduacao',
            'curso_pos', 'instituicao_pos'
        ]
        
        for field in monitored_fields:
            old_value = old_data.get(field)
            new_value = new_data.get(field)
            
            # Converte para string para comparação
            old_str = str(old_value) if old_value is not None else ''
            new_str = str(new_value) if new_value is not None else ''
            
            if old_str != new_str:
                changes[field] = (old_value, new_value)
        
        return changes
    
    def get_statistics(self, school):
        """Gera estatísticas dos professores"""
        try:
            teachers = self.get_teachers_by_school(school)
            
            if not teachers:
                return {
                    'total': 0,
                    'ativos': 0,
                    'por_pos_graduacao': {},
                    'por_carga_horaria': {},
                    'por_carreira': {},
                    'por_status': {}
                }
            
            # Contadores
            total = len(teachers)
            ativos = len([t for t in teachers if t.get('status', 'Ativo') == 'Ativo'])
            
            # Distribuição por categoria
            from collections import Counter
            
            pos_graduacao = Counter([t.get('pos_graduacao', 'Não informado') for t in teachers])
            carga_horaria = Counter([t.get('carga_horaria', 'Não informado') for t in teachers])
            carreira = Counter([t.get('carreira', 'Não informado') for t in teachers])
            status = Counter([t.get('status', 'Ativo') for t in teachers])
            
            return {
                'total': total,
                'ativos': ativos,
                'por_pos_graduacao': dict(pos_graduacao),
                'por_carga_horaria': dict(carga_horaria),
                'por_carreira': dict(carreira),
                'por_status': dict(status)
            }
            
        except Exception as e:
            logging.error(f"Erro ao gerar estatísticas: {e}")
            return {}
    
    def validate_teacher_consistency(self, school):
        """Valida consistência dos dados dos professores"""
        try:
            teachers = self.get_teachers_by_school(school, include_deleted=True)
            issues = []
            
            for teacher in teachers:
                teacher_issues = []
                
                # Valida dados obrigatórios
                required_fields = ['siape', 'nome', 'data_nascimento', 'estado', 'email', 'telefone', 'carga_horaria', 'carreira']
                for field in required_fields:
                    if not teacher.get(field):
                        teacher_issues.append(f"Campo obrigatório ausente: {field}")
                
                # Valida SIAPE
                siape = teacher.get('siape', '')
                if not self.validator.validate_siape(siape):
                    teacher_issues.append("SIAPE inválido")
                
                # CPF removido por questões de segurança e privacidade
                
                # Valida datas
                data_nasc = teacher.get('data_nascimento', '')
                if data_nasc and not self.validator.validate_date(data_nasc):
                    teacher_issues.append("Data de nascimento inválida")
                
                data_ing = teacher.get('data_ingresso', '')
                if data_ing and not self.validator.validate_date(data_ing):
                    teacher_issues.append("Data de ingresso inválida")
                
                if teacher_issues:
                    issues.append({
                        'siape': siape,
                        'nome': teacher.get('nome', 'N/A'),
                        'issues': teacher_issues
                    })
            
            return issues
            
        except Exception as e:
            logging.error(f"Erro na validação de consistência: {e}")
            return []
    
    def fix_data_issues(self, school, user):
        """Corrige problemas nos dados automaticamente"""
        try:
            teachers = self.get_teachers_by_school(school, include_deleted=True)
            fixed_count = 0
            
            for teacher in teachers:
                needs_update = False
                
                # Corrige nome em maiúscula
                if teacher.get('nome'):
                    nome_upper = teacher['nome'].upper()
                    if teacher['nome'] != nome_upper:
                        teacher['nome'] = nome_upper
                        needs_update = True
                
                # Corrige status padrão
                if not teacher.get('status'):
                    teacher['status'] = 'Ativo'
                    needs_update = True
                
                # Adiciona metadados se ausentes
                if not teacher.get('data_criacao'):
                    teacher['data_criacao'] = datetime.now().isoformat()
                    needs_update = True
                
                if needs_update:
                    teacher['data_atualizacao'] = datetime.now().isoformat()
                    teacher['corrigido_por'] = user
                    
                    self.data_manager.update_teacher(teacher)
                    fixed_count += 1
            
            logging.info(f"Correção automática concluída: {fixed_count} registros corrigidos")
            return fixed_count
            
        except Exception as e:
            logging.error(f"Erro na correção automática: {e}")
            return 0
