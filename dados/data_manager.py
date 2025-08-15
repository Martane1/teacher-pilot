# -*- coding: utf-8 -*-
"""
Gerenciador de Dados - Sistema DIRENS
"""

import json
import os
import logging
from datetime import datetime
import threading
from filelock import FileLock

class DataManager:
    """Gerenciador de persistência de dados"""
    
    def __init__(self):
        """Inicializa o gerenciador de dados"""
        self.data_dir = "data"
        self.teachers_file = os.path.join(self.data_dir, "teachers.json")
        self.schools_file = os.path.join(self.data_dir, "schools.json")
        self.lock = threading.Lock()
        
        self.ensure_data_directory()
        self.initialize_data_files()
    
    def ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def initialize_data_files(self):
        """Inicializa arquivos de dados se não existirem"""
        # Arquivo de professores
        if not os.path.exists(self.teachers_file):
            initial_data = {
                "teachers": {},
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            self.save_json(self.teachers_file, initial_data)
        
        # Arquivo de escolas
        if not os.path.exists(self.schools_file):
            from recursos.constants import ESCOLAS
            schools_data = {
                "schools": ESCOLAS,
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            self.save_json(self.schools_file, schools_data)
    
    def save_json(self, filepath, data):
        """Salva dados em JSON com lock"""
        try:
            # Usa FileLock para evitar conflitos
            lock_file = filepath + ".lock"
            
            with FileLock(lock_file, timeout=10):
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
                    
        except Exception as e:
            if "FileLock" in str(type(e)):
                # Fallback sem FileLock se não estiver disponível
                with self.lock:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            else:
                logging.error(f"Erro ao salvar JSON {filepath}: {e}")
                raise
    
    def load_json(self, filepath):
        """Carrega dados de JSON com lock"""
        try:
            if not os.path.exists(filepath):
                return {}
            
            # Usa FileLock para evitar conflitos
            lock_file = filepath + ".lock"
            
            with FileLock(lock_file, timeout=10):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
                    
        except Exception as e:
            if "FileLock" in str(type(e)):
                # Fallback sem FileLock se não estiver disponível
                with self.lock:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        return json.load(f)
            else:
                logging.error(f"Erro ao carregar JSON {filepath}: {e}")
                return {}
    
    def save_teacher(self, teacher_data):
        """Salva dados de um professor"""
        try:
            # Carrega dados atuais
            data = self.load_json(self.teachers_file)
            
            if "teachers" not in data:
                data["teachers"] = {}
            
            school = teacher_data.get('escola', '')
            siape = teacher_data.get('siape', '')
            
            if not school or not siape:
                logging.error("Escola e SIAPE são obrigatórios")
                return False
            
            # Cria estrutura da escola se não existir
            if school not in data["teachers"]:
                data["teachers"][school] = {}
            
            # Salva professor
            data["teachers"][school][siape] = teacher_data
            
            # Atualiza metadados
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Salva arquivo
            self.save_json(self.teachers_file, data)
            
            logging.info(f"Professor salvo: {siape} - {school}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao salvar professor: {e}")
            return False
    
    def get_teacher_by_siape(self, siape, school):
        """Busca professor por SIAPE e escola"""
        try:
            # Ensure SIAPE is string for consistent lookup
            siape = str(siape)
            
            data = self.load_json(self.teachers_file)
            
            teachers = data.get("teachers", {})
            school_teachers = teachers.get(school, {})
            
            return school_teachers.get(siape)
            
        except Exception as e:
            logging.error(f"Erro ao buscar professor: {e}")
            return None
    
    def get_teachers_by_school(self, school):
        """Lista todos os professores de uma escola"""
        try:
            data = self.load_json(self.teachers_file)
            
            teachers = data.get("teachers", {})
            school_teachers = teachers.get(school, {})
            
            # Retorna lista de professores
            return list(school_teachers.values())
            
        except Exception as e:
            logging.error(f"Erro ao listar professores: {e}")
            return []
    
    def update_teacher(self, teacher_data):
        """Atualiza dados de um professor"""
        try:
            school = teacher_data.get('escola', '')
            siape = teacher_data.get('siape', '')
            
            if not school or not siape:
                logging.error("Escola e SIAPE são obrigatórios")
                return False
            
            # Verifica se professor existe
            existing_teacher = self.get_teacher_by_siape(siape, school)
            if not existing_teacher:
                logging.error(f"Professor não encontrado: {siape} - {school}")
                return False
            
            # Atualiza dados (reutiliza save_teacher)
            return self.save_teacher(teacher_data)
            
        except Exception as e:
            logging.error(f"Erro ao atualizar professor: {e}")
            return False
    
    def delete_teacher(self, siape, school):
        """Remove um professor (exclusão física)"""
        try:
            data = self.load_json(self.teachers_file)
            
            teachers = data.get("teachers", {})
            
            if school not in teachers:
                logging.error(f"Escola não encontrada: {school}")
                return False
            
            if siape not in teachers[school]:
                logging.error(f"Professor não encontrado: {siape}")
                return False
            
            # Remove professor
            del teachers[school][siape]
            
            # Atualiza metadados
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Salva arquivo
            self.save_json(self.teachers_file, data)
            
            logging.info(f"Professor removido: {siape} - {school}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao remover professor: {e}")
            return False
    
    def search_teachers(self, school, search_term=None, filters=None):
        """Busca professores com filtros"""
        try:
            teachers = self.get_teachers_by_school(school)
            
            if not teachers:
                return []
            
            # Aplica filtros
            filtered_teachers = teachers
            
            # Filtro por termo de busca
            if search_term:
                search_term = search_term.lower().strip()
                filtered_teachers = [
                    t for t in filtered_teachers
                    if search_term in t.get('nome', '').lower() or
                       search_term in t.get('siape', '')
                ]
            
            # Filtros específicos
            if filters:
                for field, value in filters.items():
                    if value and value != "Todos":
                        filtered_teachers = [
                            t for t in filtered_teachers
                            if t.get(field) == value
                        ]
            
            return filtered_teachers
            
        except Exception as e:
            logging.error(f"Erro na busca de professores: {e}")
            return []
    
    def get_all_teachers(self):
        """Retorna todos os professores de todas as escolas"""
        try:
            data = self.load_json(self.teachers_file)
            teachers = data.get("teachers", {})
            
            all_teachers = []
            for school, school_teachers in teachers.items():
                all_teachers.extend(school_teachers.values())
            
            return all_teachers
            
        except Exception as e:
            logging.error(f"Erro ao listar todos os professores: {e}")
            return []
    
    def get_teachers_count_by_school(self):
        """Retorna contagem de professores por escola"""
        try:
            data = self.load_json(self.teachers_file)
            teachers = data.get("teachers", {})
            
            count_by_school = {}
            for school, school_teachers in teachers.items():
                # Conta apenas professores não excluídos
                active_teachers = [
                    t for t in school_teachers.values()
                    if t.get('status') != 'Excluído'
                ]
                count_by_school[school] = len(active_teachers)
            
            return count_by_school
            
        except Exception as e:
            logging.error(f"Erro ao contar professores: {e}")
            return {}
    
    def backup_data(self, backup_path):
        """Cria backup dos dados"""
        try:
            import shutil
            
            # Cria diretório de backup se não existir
            backup_dir = os.path.dirname(backup_path)
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Copia diretório de dados
            if os.path.exists(self.data_dir):
                shutil.copytree(self.data_dir, backup_path, dirs_exist_ok=True)
                logging.info(f"Backup criado: {backup_path}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
            return False
    
    def restore_data(self, backup_path):
        """Restaura dados de um backup"""
        try:
            import shutil
            
            if not os.path.exists(backup_path):
                logging.error(f"Backup não encontrado: {backup_path}")
                return False
            
            # Remove dados atuais
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            
            # Restaura backup
            shutil.copytree(backup_path, self.data_dir)
            
            logging.info(f"Dados restaurados de: {backup_path}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao restaurar dados: {e}")
            return False
    
    def validate_data_integrity(self):
        """Valida integridade dos dados"""
        try:
            issues = []
            
            # Verifica arquivo de professores
            if not os.path.exists(self.teachers_file):
                issues.append("Arquivo de professores não encontrado")
            else:
                try:
                    data = self.load_json(self.teachers_file)
                    if "teachers" not in data:
                        issues.append("Estrutura de dados inválida")
                except Exception as e:
                    issues.append(f"Erro ao ler arquivo de professores: {e}")
            
            # Verifica arquivo de escolas
            if not os.path.exists(self.schools_file):
                issues.append("Arquivo de escolas não encontrado")
            
            # Verifica consistência dos dados
            all_teachers = self.get_all_teachers()
            for teacher in all_teachers:
                required_fields = ['siape', 'nome', 'escola']
                for field in required_fields:
                    if not teacher.get(field):
                        issues.append(f"Professor sem {field}: {teacher}")
                        break
            
            return {
                'valid': len(issues) == 0,
                'issues': issues
            }
            
        except Exception as e:
            logging.error(f"Erro na validação de integridade: {e}")
            return {
                'valid': False,
                'issues': [f"Erro na validação: {e}"]
            }
    
    def get_data_statistics(self):
        """Retorna estatísticas dos dados"""
        try:
            all_teachers = self.get_all_teachers()
            count_by_school = self.get_teachers_count_by_school()
            
            # Tamanho dos arquivos
            teachers_size = os.path.getsize(self.teachers_file) if os.path.exists(self.teachers_file) else 0
            schools_size = os.path.getsize(self.schools_file) if os.path.exists(self.schools_file) else 0
            
            return {
                'total_teachers': len(all_teachers),
                'teachers_by_school': count_by_school,
                'data_files_size': teachers_size + schools_size,
                'teachers_file_size': teachers_size,
                'schools_file_size': schools_size,
                'last_update': self.get_last_update_time()
            }
            
        except Exception as e:
            logging.error(f"Erro ao gerar estatísticas: {e}")
            return {}
    
    def get_last_update_time(self):
        """Retorna último tempo de atualização"""
        try:
            data = self.load_json(self.teachers_file)
            return data.get("metadata", {}).get("last_updated")
        except Exception:
            return None
