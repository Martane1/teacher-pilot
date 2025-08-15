# -*- coding: utf-8 -*-
"""
Configurações do Sistema DIRENS
"""

import os
import json
import logging
from recursos.utils import get_brazilian_datetime, format_brazilian_datetime
from typing import Dict, Any

class Config:
    """Classe de configuração do sistema"""
    
    def __init__(self):
        """Inicializa as configurações"""
        self.config_file = "data/config.json"
        self.default_config = self.get_default_config()
        self.config = self.load_config()
        
        # Cria arquivo de config se não existir
        if not os.path.exists(self.config_file):
            self.save_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Retorna configurações padrão"""
        return {
            "system": {
                "name": "Sistema DIRENS",
                "version": "1.0.0",
                "description": "Sistema de Controle de Professores DIRENS",
                "author": "Sistema DIRENS",
                "created_at": get_brazilian_datetime().isoformat()
            },
            "database": {
                "auto_backup": True,
                "backup_interval_hours": 24,
                "max_backups": 30,
                "data_validation": True
            },
            "ui": {
                "theme": "default",
                "language": "pt_BR",
                "date_format": "DD-MM-AAAA",
                "window_size": "1200x800",
                "window_maximized": True,
                "show_splash": True
            },
            "export": {
                "default_format": "csv",
                "include_deleted": False,
                "csv_encoding": "utf-8-sig",
                "pdf_page_size": "A4"
            },
            "security": {
                "session_timeout_minutes": 480,  # 8 horas
                "password_min_length": 6,
                "require_password_change": False,
                "lock_after_failed_attempts": 3
            },
            "logging": {
                "level": "INFO",
                "max_file_size_mb": 10,
                "backup_count": 5,
                "log_to_file": True,
                "log_to_console": True
            },
            "validation": {
                "strict_cpf_validation": True,
                "strict_siape_validation": True,
                "strict_date_validation": True,
                "allow_future_dates": False,
                "min_age_years": 18,
                "max_age_years": 80
            },
            "features": {
                "enable_statistics": True,
                "enable_exports": True,
                "enable_history": True,
                "enable_backups": True,
                "enable_advanced_search": True
            }
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                
                # Merge com configurações padrão
                config = self.default_config.copy()
                self._deep_merge(config, saved_config)
                return config
            else:
                return self.default_config.copy()
                
        except Exception as e:
            logging.error(f"Erro ao carregar configurações: {e}")
            return self.default_config.copy()
    
    def save_config(self) -> bool:
        """Salva configurações no arquivo"""
        try:
            # Garante que o diretório existe
            config_dir = os.path.dirname(self.config_file)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            # Atualiza timestamp
            self.config["system"]["last_updated"] = get_brazilian_datetime().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False, default=str)
            
            logging.info("Configurações salvas com sucesso")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao salvar configurações: {e}")
            return False
    
    def _deep_merge(self, target: Dict, source: Dict) -> None:
        """Faz merge profundo de dicionários"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def get(self, section: str, key: str = None, default: Any = None) -> Any:
        """Obtém valor de configuração"""
        try:
            if key is None:
                return self.config.get(section, default)
            
            section_config = self.config.get(section, {})
            return section_config.get(key, default)
            
        except Exception as e:
            logging.error(f"Erro ao obter configuração {section}.{key}: {e}")
            return default
    
    def set(self, section: str, key: str, value: Any) -> bool:
        """Define valor de configuração"""
        try:
            if section not in self.config:
                self.config[section] = {}
            
            self.config[section][key] = value
            return self.save_config()
            
        except Exception as e:
            logging.error(f"Erro ao definir configuração {section}.{key}: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reseta configurações para padrão"""
        try:
            self.config = self.default_config.copy()
            return self.save_config()
        except Exception as e:
            logging.error(f"Erro ao resetar configurações: {e}")
            return False
    
    def validate_config(self) -> Dict[str, Any]:
        """Valida configurações atuais"""
        issues = []
        warnings = []
        
        try:
            # Valida seções obrigatórias
            required_sections = ["system", "database", "ui", "export", "security"]
            for section in required_sections:
                if section not in self.config:
                    issues.append(f"Seção obrigatória ausente: {section}")
            
            # Valida valores específicos
            if self.get("security", "password_min_length", 6) < 4:
                warnings.append("Tamanho mínimo da senha muito baixo")
            
            if self.get("database", "max_backups", 30) < 5:
                warnings.append("Número mínimo de backups muito baixo")
            
            session_timeout = self.get("security", "session_timeout_minutes", 480)
            if session_timeout < 30:
                warnings.append("Timeout de sessão muito baixo")
            elif session_timeout > 1440:  # 24 horas
                warnings.append("Timeout de sessão muito alto")
            
            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "warnings": warnings
            }
            
        except Exception as e:
            logging.error(f"Erro na validação de configurações: {e}")
            return {
                "valid": False,
                "issues": [f"Erro na validação: {e}"],
                "warnings": []
            }
    
    def export_config(self, filepath: str) -> bool:
        """Exporta configurações para arquivo"""
        try:
            export_data = {
                "exported_at": get_brazilian_datetime().isoformat(),
                "system_info": {
                    "name": self.get("system", "name"),
                    "version": self.get("system", "version")
                },
                "config": self.config
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            logging.info(f"Configurações exportadas para: {filepath}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao exportar configurações: {e}")
            return False
    
    def import_config(self, filepath: str) -> bool:
        """Importa configurações de arquivo"""
        try:
            if not os.path.exists(filepath):
                logging.error(f"Arquivo de configuração não encontrado: {filepath}")
                return False
            
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # Valida estrutura
            if "config" not in import_data:
                logging.error("Estrutura de configuração inválida")
                return False
            
            # Faz backup da configuração atual
            backup_file = f"{self.config_file}.backup_{get_brazilian_datetime().strftime('%Y%m%d_%H%M%S')}"
            if os.path.exists(self.config_file):
                import shutil
                shutil.copy2(self.config_file, backup_file)
            
            # Importa nova configuração
            imported_config = import_data["config"]
            self.config = self.default_config.copy()
            self._deep_merge(self.config, imported_config)
            
            # Valida configuração importada
            validation = self.validate_config()
            if not validation["valid"]:
                logging.error("Configuração importada é inválida")
                return False
            
            return self.save_config()
            
        except Exception as e:
            logging.error(f"Erro ao importar configurações: {e}")
            return False
    
    def get_database_config(self) -> Dict[str, Any]:
        """Retorna configurações de banco de dados"""
        return self.config.get("database", {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Retorna configurações de interface"""
        return self.config.get("ui", {})
    
    def get_security_config(self) -> Dict[str, Any]:
        """Retorna configurações de segurança"""
        return self.config.get("security", {})
    
    def get_export_config(self) -> Dict[str, Any]:
        """Retorna configurações de exportação"""
        return self.config.get("export", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Retorna configurações de logging"""
        return self.config.get("logging", {})
    
    def get_validation_config(self) -> Dict[str, Any]:
        """Retorna configurações de validação"""
        return self.config.get("validation", {})
    
    def get_features_config(self) -> Dict[str, Any]:
        """Retorna configurações de funcionalidades"""
        return self.config.get("features", {})
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Verifica se uma funcionalidade está habilitada"""
        return self.get("features", feature_name, True)
    
    def toggle_feature(self, feature_name: str) -> bool:
        """Alterna uma funcionalidade"""
        current_value = self.is_feature_enabled(feature_name)
        return self.set("features", feature_name, not current_value)
