# -*- coding: utf-8 -*-
"""
Gerenciador de Histórico - Sistema DIRENS
"""

import json
import os
import logging
from datetime import datetime
import threading
from typing import List, Dict, Any, Optional

class HistoryManager:
    """Gerenciador do histórico de alterações dos professores"""
    
    def __init__(self):
        """Inicializa o gerenciador de histórico"""
        self.data_dir = "data"
        self.history_dir = os.path.join(self.data_dir, "history")
        self.history_index_file = os.path.join(self.history_dir, "history_index.json")
        self.lock = threading.Lock()
        
        self.ensure_history_directory()
        self.initialize_history_index()
    
    def ensure_history_directory(self):
        """Garante que o diretório de histórico existe"""
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
    
    def initialize_history_index(self):
        """Inicializa o arquivo de índice do histórico"""
        if not os.path.exists(self.history_index_file):
            initial_index = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "teachers": {}
            }
            self.save_json(self.history_index_file, initial_index)
    
    def save_json(self, filepath: str, data: Dict[str, Any]) -> None:
        """Salva dados em JSON com lock"""
        try:
            with self.lock:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logging.error(f"Erro ao salvar JSON {filepath}: {e}")
            raise
    
    def load_json(self, filepath: str) -> Dict[str, Any]:
        """Carrega dados de JSON com lock"""
        try:
            if not os.path.exists(filepath):
                return {}
            
            with self.lock:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar JSON {filepath}: {e}")
            return {}
    
    def get_teacher_history_file(self, siape: str, school: str) -> str:
        """Retorna o caminho do arquivo de histórico de um professor"""
        school_safe = school.replace(" ", "_").replace("/", "_").lower()
        filename = f"history_{school_safe}_{siape}.json"
        return os.path.join(self.history_dir, filename)
    
    def add_history_entry(self, entry: Dict[str, Any]) -> bool:
        """Adiciona uma entrada no histórico"""
        try:
            siape = entry.get('siape')
            school = entry.get('escola')
            
            if not siape or not school:
                logging.error("SIAPE e escola são obrigatórios para o histórico")
                return False
            
            # Adiciona timestamp se não existir
            if 'timestamp' not in entry:
                entry['timestamp'] = datetime.now().isoformat()
            
            # Arquivo de histórico do professor
            history_file = self.get_teacher_history_file(siape, school)
            
            # Carrega histórico existente
            if os.path.exists(history_file):
                history_data = self.load_json(history_file)
            else:
                history_data = {
                    "siape": siape,
                    "escola": school,
                    "created_at": datetime.now().isoformat(),
                    "entries": []
                }
            
            # Adiciona nova entrada
            history_data["entries"].append(entry)
            history_data["last_updated"] = datetime.now().isoformat()
            
            # Salva arquivo de histórico
            self.save_json(history_file, history_data)
            
            # Atualiza índice
            self.update_history_index(siape, school, history_file)
            
            logging.info(f"Entrada de histórico adicionada: {siape} - {entry.get('action', 'N/A')}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao adicionar entrada no histórico: {e}")
            return False
    
    def update_history_index(self, siape: str, school: str, history_file: str) -> None:
        """Atualiza o índice de histórico"""
        try:
            index_data = self.load_json(self.history_index_file)
            
            if "teachers" not in index_data:
                index_data["teachers"] = {}
            
            # Chave única para o professor
            teacher_key = f"{school}_{siape}"
            
            index_data["teachers"][teacher_key] = {
                "siape": siape,
                "escola": school,
                "history_file": history_file,
                "last_updated": datetime.now().isoformat()
            }
            
            index_data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            self.save_json(self.history_index_file, index_data)
            
        except Exception as e:
            logging.error(f"Erro ao atualizar índice do histórico: {e}")
    
    def get_teacher_history(self, siape: str, school: str) -> List[Dict[str, Any]]:
        """Retorna o histórico de um professor"""
        try:
            history_file = self.get_teacher_history_file(siape, school)
            
            if not os.path.exists(history_file):
                logging.info(f"Nenhum histórico encontrado para: {siape} - {school}")
                return []
            
            history_data = self.load_json(history_file)
            entries = history_data.get("entries", [])
            
            # Ordena por timestamp (mais recente primeiro)
            entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return entries
            
        except Exception as e:
            logging.error(f"Erro ao buscar histórico do professor: {e}")
            return []
    
    def get_recent_history(self, school: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Retorna histórico recente de todos os professores ou de uma escola"""
        try:
            all_entries = []
            index_data = self.load_json(self.history_index_file)
            teachers = index_data.get("teachers", {})
            
            for teacher_key, teacher_info in teachers.items():
                # Filtra por escola se especificada
                if school and teacher_info.get("escola") != school:
                    continue
                
                history_file = teacher_info.get("history_file")
                if history_file and os.path.exists(history_file):
                    history_data = self.load_json(history_file)
                    entries = history_data.get("entries", [])
                    
                    # Adiciona informações do professor a cada entrada
                    for entry in entries:
                        entry_with_info = entry.copy()
                        entry_with_info["teacher_siape"] = teacher_info.get("siape")
                        entry_with_info["teacher_escola"] = teacher_info.get("escola")
                        all_entries.append(entry_with_info)
            
            # Ordena por timestamp (mais recente primeiro)
            all_entries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Limita resultado
            return all_entries[:limit]
            
        except Exception as e:
            logging.error(f"Erro ao buscar histórico recente: {e}")
            return []
    
    def get_history_by_action(self, action: str, school: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna histórico filtrado por tipo de ação"""
        try:
            recent_history = self.get_recent_history(school, limit=1000)
            return [entry for entry in recent_history if entry.get('action') == action]
            
        except Exception as e:
            logging.error(f"Erro ao buscar histórico por ação: {e}")
            return []
    
    def get_history_by_user(self, user: str, school: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna histórico filtrado por usuário"""
        try:
            recent_history = self.get_recent_history(school, limit=1000)
            return [entry for entry in recent_history if entry.get('user') == user]
            
        except Exception as e:
            logging.error(f"Erro ao buscar histórico por usuário: {e}")
            return []
    
    def get_history_by_date_range(self, start_date: str, end_date: str, school: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna histórico em um período específico"""
        try:
            recent_history = self.get_recent_history(school, limit=1000)
            filtered_entries = []
            
            for entry in recent_history:
                entry_date = entry.get('timestamp', '')
                if start_date <= entry_date <= end_date:
                    filtered_entries.append(entry)
            
            return filtered_entries
            
        except Exception as e:
            logging.error(f"Erro ao buscar histórico por período: {e}")
            return []
    
    def delete_teacher_history(self, siape: str, school: str) -> bool:
        """Remove todo o histórico de um professor"""
        try:
            history_file = self.get_teacher_history_file(siape, school)
            
            # Remove arquivo de histórico
            if os.path.exists(history_file):
                os.remove(history_file)
                logging.info(f"Arquivo de histórico removido: {history_file}")
            
            # Remove do índice
            index_data = self.load_json(self.history_index_file)
            teachers = index_data.get("teachers", {})
            teacher_key = f"{school}_{siape}"
            
            if teacher_key in teachers:
                del teachers[teacher_key]
                index_data["metadata"]["last_updated"] = datetime.now().isoformat()
                self.save_json(self.history_index_file, index_data)
                logging.info(f"Professor removido do índice de histórico: {siape} - {school}")
            
            return True
            
        except Exception as e:
            logging.error(f"Erro ao remover histórico do professor: {e}")
            return False
    
    def get_history_statistics(self, school: Optional[str] = None) -> Dict[str, Any]:
        """Retorna estatísticas do histórico"""
        try:
            recent_history = self.get_recent_history(school, limit=10000)
            
            if not recent_history:
                return {
                    "total_entries": 0,
                    "actions_count": {},
                    "users_count": {},
                    "first_entry": None,
                    "last_entry": None
                }
            
            # Conta ações
            actions_count = {}
            users_count = {}
            
            for entry in recent_history:
                action = entry.get('action', 'Unknown')
                user = entry.get('user', 'Unknown')
                
                actions_count[action] = actions_count.get(action, 0) + 1
                users_count[user] = users_count.get(user, 0) + 1
            
            # Primeira e última entrada
            sorted_entries = sorted(recent_history, key=lambda x: x.get('timestamp', ''))
            first_entry = sorted_entries[0].get('timestamp') if sorted_entries else None
            last_entry = sorted_entries[-1].get('timestamp') if sorted_entries else None
            
            return {
                "total_entries": len(recent_history),
                "actions_count": actions_count,
                "users_count": users_count,
                "first_entry": first_entry,
                "last_entry": last_entry,
                "school": school
            }
            
        except Exception as e:
            logging.error(f"Erro ao gerar estatísticas do histórico: {e}")
            return {}
    
    def cleanup_old_history(self, days_to_keep: int = 365) -> int:
        """Remove entradas de histórico antigas"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_to_keep)
            cutoff_iso = cutoff_date.isoformat()
            
            cleaned_count = 0
            index_data = self.load_json(self.history_index_file)
            teachers = index_data.get("teachers", {})
            
            for teacher_key, teacher_info in teachers.items():
                history_file = teacher_info.get("history_file")
                
                if not history_file or not os.path.exists(history_file):
                    continue
                
                history_data = self.load_json(history_file)
                entries = history_data.get("entries", [])
                
                # Filtra entradas recentes
                recent_entries = [
                    entry for entry in entries
                    if entry.get('timestamp', '') >= cutoff_iso
                ]
                
                # Se removeu alguma entrada
                if len(recent_entries) < len(entries):
                    history_data["entries"] = recent_entries
                    history_data["last_cleanup"] = datetime.now().isoformat()
                    
                    self.save_json(history_file, history_data)
                    cleaned_count += len(entries) - len(recent_entries)
            
            logging.info(f"Limpeza de histórico concluída: {cleaned_count} entradas removidas")
            return cleaned_count
            
        except Exception as e:
            logging.error(f"Erro na limpeza do histórico: {e}")
            return 0
    
    def export_history(self, siape: str, school: str, format: str = 'json') -> Optional[str]:
        """Exporta histórico de um professor"""
        try:
            history = self.get_teacher_history(siape, school)
            
            if not history:
                return None
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if format.lower() == 'json':
                filename = f"history_{school.replace(' ', '_')}_{siape}_{timestamp}.json"
                filepath = os.path.join("exports", filename)
                
                # Garante que o diretório existe
                os.makedirs("exports", exist_ok=True)
                
                export_data = {
                    "siape": siape,
                    "escola": school,
                    "exported_at": datetime.now().isoformat(),
                    "total_entries": len(history),
                    "history": history
                }
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
                
                return filepath
            
            elif format.lower() == 'csv':
                import csv
                
                filename = f"history_{school.replace(' ', '_')}_{siape}_{timestamp}.csv"
                filepath = os.path.join("exports", filename)
                
                # Garante que o diretório existe
                os.makedirs("exports", exist_ok=True)
                
                with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    fieldnames = ['timestamp', 'action', 'user', 'field', 'old_value', 'new_value', 'notes']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for entry in history:
                        writer.writerow({
                            'timestamp': entry.get('timestamp', ''),
                            'action': entry.get('action', ''),
                            'user': entry.get('user', ''),
                            'field': entry.get('field', ''),
                            'old_value': entry.get('old_value', ''),
                            'new_value': entry.get('new_value', ''),
                            'notes': entry.get('notes', '')
                        })
                
                return filepath
            
            return None
            
        except Exception as e:
            logging.error(f"Erro ao exportar histórico: {e}")
            return None
    
    def validate_history_integrity(self) -> Dict[str, Any]:
        """Valida a integridade dos arquivos de histórico"""
        try:
            issues = []
            fixed_issues = []
            
            # Verifica índice principal
            if not os.path.exists(self.history_index_file):
                issues.append("Arquivo de índice de histórico não encontrado")
                self.initialize_history_index()
                fixed_issues.append("Arquivo de índice recriado")
            
            # Verifica cada arquivo de histórico referenciado no índice
            index_data = self.load_json(self.history_index_file)
            teachers = index_data.get("teachers", {})
            
            for teacher_key, teacher_info in teachers.items():
                history_file = teacher_info.get("history_file")
                
                if not history_file:
                    issues.append(f"Arquivo de histórico não especificado para {teacher_key}")
                    continue
                
                if not os.path.exists(history_file):
                    issues.append(f"Arquivo de histórico não encontrado: {history_file}")
                    continue
                
                try:
                    history_data = self.load_json(history_file)
                    
                    if "entries" not in history_data:
                        issues.append(f"Estrutura inválida no arquivo: {history_file}")
                    
                    entries = history_data.get("entries", [])
                    for i, entry in enumerate(entries):
                        required_fields = ['timestamp', 'action']
                        for field in required_fields:
                            if field not in entry:
                                issues.append(f"Campo {field} ausente na entrada {i} de {history_file}")
                
                except Exception as e:
                    issues.append(f"Erro ao ler arquivo {history_file}: {e}")
            
            return {
                'valid': len(issues) == 0,
                'issues': issues,
                'fixed_issues': fixed_issues,
                'total_teachers_with_history': len(teachers)
            }
            
        except Exception as e:
            logging.error(f"Erro na validação da integridade do histórico: {e}")
            return {
                'valid': False,
                'issues': [f"Erro na validação: {e}"],
                'fixed_issues': [],
                'total_teachers_with_history': 0
            }
