# -*- coding: utf-8 -*-
"""
Gerenciador de Backups - Sistema DIRENS
"""

import os
import json
import shutil
import zipfile
import logging
from datetime import datetime, timedelta
import tempfile

class BackupManager:
    """Gerenciador de backups do sistema"""
    
    def __init__(self):
        """Inicializa o gerenciador de backups"""
        self.backup_dir = "backups"
        self.data_dir = "data"
        self.config_file = os.path.join(self.backup_dir, "backup_config.json")
        self.ensure_backup_directory()
        self.load_config()
    
    def ensure_backup_directory(self):
        """Garante que o diretório de backups existe"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def load_config(self):
        """Carrega configurações de backup"""
        default_config = {
            'auto_backup_enabled': True,
            'auto_backup_interval_hours': 24,
            'max_backups': 30,
            'last_backup': None
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            logging.error(f"Erro ao carregar config de backup: {e}")
            self.config = default_config
    
    def save_config(self):
        """Salva configurações de backup"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Erro ao salvar config de backup: {e}")
    
    def create_backup(self, description="", backup_type="manual", include_history=True):
        """Cria um novo backup"""
        try:
            timestamp = datetime.now()
            timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
            
            backup_name = f"backup_{timestamp_str}"
            backup_filename = f"{backup_name}.zip"
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # Cria arquivo ZIP
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Adiciona todos os arquivos de dados
                if os.path.exists(self.data_dir):
                    for root, dirs, files in os.walk(self.data_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Calcula path relativo
                            arcname = os.path.relpath(file_path, '.')
                            zipf.write(file_path, arcname)
                
                # Adiciona logs se solicitado
                if include_history and os.path.exists("logs"):
                    for root, dirs, files in os.walk("logs"):
                        for file in files:
                            if file.endswith('.log'):
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, '.')
                                zipf.write(file_path, arcname)
            
            # Salva metadados do backup
            backup_info = {
                'name': backup_name,
                'filename': backup_filename,
                'filepath': backup_path,
                'timestamp': timestamp.isoformat(),
                'type': backup_type,
                'description': description or f"Backup {backup_type} - {timestamp.strftime('%d/%m/%Y %H:%M')}",
                'size': os.path.getsize(backup_path),
                'status': 'OK',
                'include_history': include_history
            }
            
            # Salva registro do backup
            self.save_backup_info(backup_info)
            
            # Atualiza config
            self.config['last_backup'] = timestamp.isoformat()
            self.save_config()
            
            # Limpa backups antigos
            self.cleanup_old_backups()
            
            logging.info(f"Backup criado: {backup_filename}")
            return backup_info
            
        except Exception as e:
            logging.error(f"Erro ao criar backup: {e}")
            return None
    
    def list_backups(self):
        """Lista todos os backups disponíveis"""
        try:
            backups = []
            backup_index_file = os.path.join(self.backup_dir, "backup_index.json")
            
            if os.path.exists(backup_index_file):
                with open(backup_index_file, 'r', encoding='utf-8') as f:
                    backup_index = json.load(f)
                    backups = backup_index.get('backups', [])
            
            # Verifica se os arquivos ainda existem
            valid_backups = []
            for backup in backups:
                filepath = backup.get('filepath', '')
                if os.path.exists(filepath):
                    # Atualiza tamanho se necessário
                    backup['size'] = os.path.getsize(filepath)
                    valid_backups.append(backup)
                else:
                    logging.warning(f"Arquivo de backup não encontrado: {filepath}")
            
            return valid_backups
            
        except Exception as e:
            logging.error(f"Erro ao listar backups: {e}")
            return []
    
    def save_backup_info(self, backup_info):
        """Salva informações de um backup no índice"""
        try:
            backup_index_file = os.path.join(self.backup_dir, "backup_index.json")
            
            # Carrega índice atual
            if os.path.exists(backup_index_file):
                with open(backup_index_file, 'r', encoding='utf-8') as f:
                    backup_index = json.load(f)
            else:
                backup_index = {'backups': []}
            
            # Adiciona novo backup
            backup_index['backups'].append(backup_info)
            
            # Salva índice atualizado
            with open(backup_index_file, 'w', encoding='utf-8') as f:
                json.dump(backup_index, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logging.error(f"Erro ao salvar info do backup: {e}")
    
    def restore_backup(self, backup_name):
        """Restaura um backup específico"""
        try:
            # Encontra o backup
            backups = self.list_backups()
            backup_info = None
            
            for backup in backups:
                if backup['name'] == backup_name:
                    backup_info = backup
                    break
            
            if not backup_info:
                logging.error(f"Backup não encontrado: {backup_name}")
                return False
            
            backup_file = backup_info['filepath']
            if not os.path.exists(backup_file):
                logging.error(f"Arquivo de backup não existe: {backup_file}")
                return False
            
            # Cria backup da situação atual antes da restauração
            self.create_backup(
                description="Backup automático antes da restauração",
                backup_type="pre_restore"
            )
            
            # Cria diretório temporário
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extrai backup
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    zipf.extractall(temp_dir)
                
                # Remove dados atuais (backup já foi feito)
                if os.path.exists(self.data_dir):
                    shutil.rmtree(self.data_dir)
                
                # Restaura dados do backup
                backup_data_dir = os.path.join(temp_dir, 'data')
                if os.path.exists(backup_data_dir):
                    shutil.copytree(backup_data_dir, self.data_dir)
                
                # Restaura logs se existirem no backup
                backup_logs_dir = os.path.join(temp_dir, 'logs')
                if os.path.exists(backup_logs_dir) and backup_info.get('include_history', True):
                    if not os.path.exists('logs'):
                        os.makedirs('logs')
                    
                    for file in os.listdir(backup_logs_dir):
                        src = os.path.join(backup_logs_dir, file)
                        dst = os.path.join('logs', file)
                        shutil.copy2(src, dst)
            
            logging.info(f"Backup restaurado: {backup_name}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao restaurar backup: {e}")
            return False
    
    def delete_backup(self, backup_name):
        """Exclui um backup específico"""
        try:
            # Encontra o backup
            backups = self.list_backups()
            backup_to_delete = None
            
            for backup in backups:
                if backup['name'] == backup_name:
                    backup_to_delete = backup
                    break
            
            if not backup_to_delete:
                logging.error(f"Backup não encontrado: {backup_name}")
                return False
            
            # Remove arquivo físico
            backup_file = backup_to_delete['filepath']
            if os.path.exists(backup_file):
                os.remove(backup_file)
            
            # Remove do índice
            backup_index_file = os.path.join(self.backup_dir, "backup_index.json")
            if os.path.exists(backup_index_file):
                with open(backup_index_file, 'r', encoding='utf-8') as f:
                    backup_index = json.load(f)
                
                # Remove backup do índice
                backup_index['backups'] = [
                    b for b in backup_index['backups'] 
                    if b['name'] != backup_name
                ]
                
                # Salva índice atualizado
                with open(backup_index_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_index, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Backup excluído: {backup_name}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao excluir backup: {e}")
            return False
    
    def export_backup(self, backup_name, destination_path):
        """Exporta backup para local específico"""
        try:
            # Encontra o backup
            backups = self.list_backups()
            backup_info = None
            
            for backup in backups:
                if backup['name'] == backup_name:
                    backup_info = backup
                    break
            
            if not backup_info:
                logging.error(f"Backup não encontrado: {backup_name}")
                return False
            
            source_file = backup_info['filepath']
            if not os.path.exists(source_file):
                logging.error(f"Arquivo de backup não existe: {source_file}")
                return False
            
            # Copia arquivo
            shutil.copy2(source_file, destination_path)
            
            logging.info(f"Backup exportado: {backup_name} -> {destination_path}")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao exportar backup: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove backups antigos baseado na configuração"""
        try:
            max_backups = self.config.get('max_backups', 30)
            backups = self.list_backups()
            
            if len(backups) <= max_backups:
                return
            
            # Ordena por data (mais antigo primeiro)
            backups.sort(key=lambda x: x.get('timestamp', ''))
            
            # Remove os mais antigos
            backups_to_remove = backups[:-max_backups]
            
            for backup in backups_to_remove:
                # Não remove backups de restauração
                if backup.get('type') != 'pre_restore':
                    self.delete_backup(backup['name'])
                    logging.info(f"Backup antigo removido: {backup['name']}")
            
        except Exception as e:
            logging.error(f"Erro na limpeza de backups: {e}")
    
    def is_auto_backup_enabled(self):
        """Verifica se backup automático está habilitado"""
        return self.config.get('auto_backup_enabled', True)
    
    def set_auto_backup(self, enabled):
        """Habilita/desabilita backup automático"""
        self.config['auto_backup_enabled'] = enabled
        self.save_config()
        logging.info(f"Backup automático {'habilitado' if enabled else 'desabilitado'}")
    
    def should_create_auto_backup(self):
        """Verifica se deve criar backup automático"""
        if not self.is_auto_backup_enabled():
            return False
        
        last_backup = self.config.get('last_backup')
        if not last_backup:
            return True
        
        try:
            last_backup_time = datetime.fromisoformat(last_backup)
            interval_hours = self.config.get('auto_backup_interval_hours', 24)
            
            time_diff = datetime.now() - last_backup_time
            return time_diff.total_seconds() > (interval_hours * 3600)
            
        except Exception:
            return True
    
    def create_auto_backup_if_needed(self):
        """Cria backup automático se necessário"""
        if self.should_create_auto_backup():
            try:
                self.create_backup(
                    description="Backup automático",
                    backup_type="auto"
                )
                logging.info("Backup automático criado")
                return True
            except Exception as e:
                logging.error(f"Erro no backup automático: {e}")
                return False
        return False
    
    def get_backup_statistics(self):
        """Retorna estatísticas dos backups"""
        try:
            backups = self.list_backups()
            
            if not backups:
                return {
                    'total_backups': 0,
                    'total_size': 0,
                    'oldest_backup': None,
                    'newest_backup': None,
                    'auto_backups': 0,
                    'manual_backups': 0
                }
            
            total_size = sum(backup.get('size', 0) for backup in backups)
            auto_backups = len([b for b in backups if b.get('type') == 'auto'])
            manual_backups = len([b for b in backups if b.get('type') == 'manual'])
            
            # Ordena por data
            sorted_backups = sorted(backups, key=lambda x: x.get('timestamp', ''))
            
            return {
                'total_backups': len(backups),
                'total_size': total_size,
                'oldest_backup': sorted_backups[0].get('timestamp') if sorted_backups else None,
                'newest_backup': sorted_backups[-1].get('timestamp') if sorted_backups else None,
                'auto_backups': auto_backups,
                'manual_backups': manual_backups
            }
            
        except Exception as e:
            logging.error(f"Erro ao gerar estatísticas de backup: {e}")
            return {}
