# -*- coding: utf-8 -*-
"""
Gerenciador de Disciplinas do Sistema DIRENS
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from filelock import FileLock
from recursos.utils import get_brazilian_datetime

class DisciplineManager:
    """Gerenciador de disciplinas"""
    
    def __init__(self):
        """Inicializa o gerenciador"""
        self.data_dir = "dados"
        self.disciplines_file = os.path.join(self.data_dir, "disciplinas.json")
        self.lock_file = f"{self.disciplines_file}.lock"
        
        # Cria diretório se não existir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Cria arquivo de disciplinas se não existir
        if not os.path.exists(self.disciplines_file):
            self.create_initial_disciplines()
    
    def create_initial_disciplines(self):
        """Cria disciplinas iniciais do sistema"""
        initial_data = {
            "disciplinas": {},
            "metadata": {
                "created_at": get_brazilian_datetime().isoformat(),
                "version": "1.0.0",
                "total_disciplines": 0
            }
        }
        
        try:
            with open(self.disciplines_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
            logging.info("Arquivo de disciplinas criado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao criar arquivo de disciplinas: {e}")
    
    def _load_disciplines_data(self) -> Dict[str, Any]:
        """Carrega dados das disciplinas do arquivo"""
        try:
            if not os.path.exists(self.disciplines_file):
                self.create_initial_disciplines()
            
            with FileLock(self.lock_file):
                with open(self.disciplines_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar disciplinas: {e}")
            return {"disciplinas": {}, "metadata": {}}
    
    def _save_disciplines_data(self, data: Dict[str, Any]) -> bool:
        """Salva dados das disciplinas no arquivo"""
        try:
            with FileLock(self.lock_file):
                # Atualiza metadata
                data["metadata"]["last_updated"] = get_brazilian_datetime().isoformat()
                data["metadata"]["total_disciplines"] = len(data.get("disciplinas", {}))
                
                with open(self.disciplines_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            logging.info("Disciplinas salvas com sucesso")
            return True
        except Exception as e:
            logging.error(f"Erro ao salvar disciplinas: {e}")
            return False
    
    def add_discipline(self, discipline_data: Dict[str, Any]) -> bool:
        """Adiciona uma nova disciplina"""
        try:
            data = self._load_disciplines_data()
            
            codigo = discipline_data.get('codigo', '').strip().upper()
            if not codigo:
                raise ValueError("Código da disciplina é obrigatório")
            
            # Verifica se já existe
            if codigo in data["disciplinas"]:
                raise ValueError(f"Disciplina com código {codigo} já existe")
            
            # Adiciona timestamp e metadata
            discipline_data['created_at'] = get_brazilian_datetime().isoformat()
            discipline_data['created_by'] = discipline_data.get('created_by', 'admin')
            discipline_data['active'] = True
            
            # Adiciona a disciplina
            data["disciplinas"][codigo] = discipline_data
            
            return self._save_disciplines_data(data)
            
        except Exception as e:
            logging.error(f"Erro ao adicionar disciplina: {e}")
            raise e
    
    def update_discipline(self, codigo: str, discipline_data: Dict[str, Any]) -> bool:
        """Atualiza uma disciplina existente"""
        try:
            data = self._load_disciplines_data()
            
            codigo = codigo.strip().upper()
            if codigo not in data["disciplinas"]:
                raise ValueError(f"Disciplina {codigo} não encontrada")
            
            # Preserva dados de criação
            old_data = data["disciplinas"][codigo]
            discipline_data['created_at'] = old_data.get('created_at')
            discipline_data['created_by'] = old_data.get('created_by')
            
            # Adiciona dados de atualização
            discipline_data['updated_at'] = get_brazilian_datetime().isoformat()
            discipline_data['updated_by'] = discipline_data.get('updated_by', 'admin')
            
            # Atualiza a disciplina
            data["disciplinas"][codigo] = discipline_data
            
            return self._save_disciplines_data(data)
            
        except Exception as e:
            logging.error(f"Erro ao atualizar disciplina: {e}")
            raise e
    
    def delete_discipline(self, codigo: str) -> bool:
        """Remove uma disciplina"""
        try:
            data = self._load_disciplines_data()
            
            codigo = codigo.strip().upper()
            if codigo not in data["disciplinas"]:
                raise ValueError(f"Disciplina {codigo} não encontrada")
            
            # Remove a disciplina
            del data["disciplinas"][codigo]
            
            return self._save_disciplines_data(data)
            
        except Exception as e:
            logging.error(f"Erro ao remover disciplina: {e}")
            raise e
    
    def get_discipline_by_code(self, codigo: str) -> Optional[Dict[str, Any]]:
        """Retorna uma disciplina pelo código"""
        try:
            data = self._load_disciplines_data()
            codigo = codigo.strip().upper()
            return data["disciplinas"].get(codigo)
        except Exception as e:
            logging.error(f"Erro ao obter disciplina {codigo}: {e}")
            return None
    
    def get_all_disciplines(self) -> List[Dict[str, Any]]:
        """Retorna todas as disciplinas"""
        try:
            data = self._load_disciplines_data()
            disciplines = []
            
            for codigo, discipline in data["disciplinas"].items():
                discipline['codigo'] = codigo
                disciplines.append(discipline)
            
            # Ordena por nome
            return sorted(disciplines, key=lambda x: x.get('nome', ''))
            
        except Exception as e:
            logging.error(f"Erro ao obter disciplinas: {e}")
            return []
    
    def get_active_disciplines(self) -> List[Dict[str, Any]]:
        """Retorna apenas disciplinas ativas"""
        all_disciplines = self.get_all_disciplines()
        return [d for d in all_disciplines if d.get('active', True)]
    
    def get_disciplines_by_area(self, area: str) -> List[Dict[str, Any]]:
        """Retorna disciplinas por área do conhecimento"""
        all_disciplines = self.get_all_disciplines()
        return [d for d in all_disciplines if d.get('area', '') == area]
    
    def get_discipline_codes(self) -> List[str]:
        """Retorna lista de códigos de disciplinas ativas"""
        active_disciplines = self.get_active_disciplines()
        return [d['codigo'] for d in active_disciplines]
    
    def get_discipline_names_with_codes(self) -> List[str]:
        """Retorna lista formatada com código e nome para combobox"""
        active_disciplines = self.get_active_disciplines()
        return [f"{d['codigo']} - {d['nome']}" for d in active_disciplines]
    
    def search_disciplines(self, search_term: str) -> List[Dict[str, Any]]:
        """Busca disciplinas por termo"""
        all_disciplines = self.get_all_disciplines()
        search_term = search_term.lower().strip()
        
        if not search_term:
            return all_disciplines
        
        filtered = []
        for discipline in all_disciplines:
            codigo = discipline.get('codigo', '').lower()
            nome = discipline.get('nome', '').lower()
            area = discipline.get('area', '').lower()
            
            if (search_term in codigo or 
                search_term in nome or 
                search_term in area):
                filtered.append(discipline)
        
        return filtered
    
    def validate_discipline_data(self, discipline_data: Dict[str, Any]) -> List[str]:
        """Valida dados da disciplina"""
        errors = []
        
        # Campos obrigatórios
        required_fields = {
            'codigo': 'Código',
            'nome': 'Nome da Disciplina',
            'requisito_especifico': 'Requisito Específico'
        }
        
        for field, label in required_fields.items():
            value = discipline_data.get(field, '').strip()
            if not value:
                errors.append(f"{label} é obrigatório")
        
        # Validações específicas
        codigo = discipline_data.get('codigo', '').strip()
        if codigo:
            if len(codigo) < 3:
                errors.append("Código deve ter pelo menos 3 caracteres")
            elif len(codigo) > 10:
                errors.append("Código deve ter no máximo 10 caracteres")
            elif not codigo.replace('-', '').replace('_', '').isalnum():
                errors.append("Código deve conter apenas letras, números, hífens e underscores")
        
        nome = discipline_data.get('nome', '').strip()
        if nome:
            if len(nome) < 3:
                errors.append("Nome deve ter pelo menos 3 caracteres")
            elif len(nome) > 100:
                errors.append("Nome deve ter no máximo 100 caracteres")
        
        requisito_especifico = discipline_data.get('requisito_especifico', '').strip()
        if requisito_especifico:
            if len(requisito_especifico) > 200:
                errors.append("Requisito específico deve ter no máximo 200 caracteres")
        
        return errors
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas das disciplinas"""
        try:
            all_disciplines = self.get_all_disciplines()
            active_disciplines = self.get_active_disciplines()
            
            # Contadores por requisito específico
            requisitos_count = {}
            
            for discipline in active_disciplines:
                requisito = discipline.get('requisito_especifico', 'Não informado')
                if requisito:
                    # Agrupa requisitos similares para evitar muitas categorias únicas
                    requisito_short = requisito[:50] + '...' if len(requisito) > 50 else requisito
                    requisitos_count[requisito_short] = requisitos_count.get(requisito_short, 0) + 1
            
            return {
                'total_disciplines': len(all_disciplines),
                'active_disciplines': len(active_disciplines),
                'inactive_disciplines': len(all_disciplines) - len(active_disciplines),
                'requisitos_distribution': requisitos_count
            }
            
        except Exception as e:
            logging.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def export_disciplines(self, filepath: str) -> bool:
        """Exporta disciplinas para arquivo JSON"""
        try:
            data = self._load_disciplines_data()
            export_data = {
                "exported_at": get_brazilian_datetime().isoformat(),
                "system": "Sistema DIRENS - Disciplinas",
                "total_records": len(data.get("disciplinas", {})),
                "data": data
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Disciplinas exportadas para: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao exportar disciplinas: {e}")
            return False
    
    def backup_disciplines(self, backup_dir: str = "backups") -> Optional[str]:
        """Cria backup das disciplinas"""
        try:
            from recursos.utils import backup_file
            return backup_file(self.disciplines_file, backup_dir)
        except Exception as e:
            logging.error(f"Erro ao fazer backup das disciplinas: {e}")
            return None