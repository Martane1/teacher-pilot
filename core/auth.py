# -*- coding: utf-8 -*-
"""
Módulo de Autenticação do Sistema DIRENS
"""

import hashlib
import json
import os
import logging
from datetime import datetime

from recursos.constants import ESCOLAS

class AuthManager:
    """Gerenciador de autenticação"""
    
    def __init__(self):
        """Inicializa o gerenciador de autenticação"""
        self.users_file = "data/users.json"
        self.ensure_data_directory()
        self.initialize_default_users()
    
    def ensure_data_directory(self):
        """Garante que o diretório de dados existe"""
        data_dir = os.path.dirname(self.users_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def initialize_default_users(self):
        """Inicializa usuários padrão se não existirem"""
        if not os.path.exists(self.users_file):
            default_users = {}
            
            # Cria usuário admin padrão para cada escola
            for escola in ESCOLAS.keys():
                escola_key = escola.replace(" ", "_").lower()
                default_users[escola_key] = {
                    "admin": {
                        "password": self.hash_password("direns2024"),
                        "level": "admin",
                        "created_at": datetime.now().isoformat(),
                        "last_login": None,
                        "active": True
                    }
                }
            
            self.save_users(default_users)
            logging.info("Usuários padrão criados")
    
    def hash_password(self, password):
        """Cria hash da senha"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def load_users(self):
        """Carrega usuários do arquivo"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Erro ao carregar usuários: {e}")
            return {}
    
    def save_users(self, users):
        """Salva usuários no arquivo"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Erro ao salvar usuários: {e}")
            raise
    
    def get_school_key(self, school):
        """Converte nome da escola para chave"""
        return school.replace(" ", "_").lower()
    
    def authenticate(self, school, username, password):
        """Autentica usuário"""
        try:
            users = self.load_users()
            school_key = self.get_school_key(school)
            
            # Verifica se escola existe
            if school_key not in users:
                return {
                    'success': False,
                    'message': 'Escola não encontrada'
                }
            
            # Verifica se usuário existe
            if username not in users[school_key]:
                return {
                    'success': False,
                    'message': 'Usuário não encontrado'
                }
            
            user_data = users[school_key][username]
            
            # Verifica se usuário está ativo
            if not user_data.get('active', True):
                return {
                    'success': False,
                    'message': 'Usuário desativado'
                }
            
            # Verifica senha
            password_hash = self.hash_password(password)
            if password_hash != user_data.get('password'):
                return {
                    'success': False,
                    'message': 'Senha incorreta'
                }
            
            # Atualiza último login
            user_data['last_login'] = datetime.now().isoformat()
            users[school_key][username] = user_data
            self.save_users(users)
            
            logging.info(f"Login bem-sucedido: {username} - {school}")
            
            return {
                'success': True,
                'message': 'Login realizado com sucesso',
                'level': user_data.get('level', 'user')
            }
            
        except Exception as e:
            logging.error(f"Erro na autenticação: {e}")
            return {
                'success': False,
                'message': 'Erro interno do sistema'
            }
    
    def reset_password(self, school, username, current_password, new_password, is_admin=False):
        """Redefine senha de usuário"""
        try:
            users = self.load_users()
            school_key = self.get_school_key(school)
            
            # Verifica se escola existe
            if school_key not in users:
                return {
                    'success': False,
                    'message': 'Escola não encontrada'
                }
            
            # Verifica se usuário existe
            if username not in users[school_key]:
                return {
                    'success': False,
                    'message': 'Usuário não encontrado'
                }
            
            user_data = users[school_key][username]
            
            # Se não é admin, verifica senha atual
            if not is_admin:
                current_hash = self.hash_password(current_password)
                if current_hash != user_data.get('password'):
                    return {
                        'success': False,
                        'message': 'Senha atual incorreta'
                    }
            else:
                # Verifica se quem está fazendo a alteração é realmente admin
                # Para simplificar, aceitamos a flag is_admin
                # Em uma implementação mais robusta, verificaríamos a sessão atual
                pass
            
            # Valida nova senha
            if len(new_password) < 6:
                return {
                    'success': False,
                    'message': 'Nova senha deve ter pelo menos 6 caracteres'
                }
            
            # Atualiza senha
            user_data['password'] = self.hash_password(new_password)
            user_data['password_changed_at'] = datetime.now().isoformat()
            
            users[school_key][username] = user_data
            self.save_users(users)
            
            logging.info(f"Senha redefinida: {username} - {school}")
            
            return {
                'success': True,
                'message': 'Senha alterada com sucesso'
            }
            
        except Exception as e:
            logging.error(f"Erro ao redefinir senha: {e}")
            return {
                'success': False,
                'message': 'Erro interno do sistema'
            }
    
    def create_user(self, school, username, password, level='user'):
        """Cria novo usuário"""
        try:
            users = self.load_users()
            school_key = self.get_school_key(school)
            
            # Cria escola se não existir
            if school_key not in users:
                users[school_key] = {}
            
            # Verifica se usuário já existe
            if username in users[school_key]:
                return {
                    'success': False,
                    'message': 'Usuário já existe'
                }
            
            # Valida dados
            if len(username.strip()) < 3:
                return {
                    'success': False,
                    'message': 'Nome de usuário deve ter pelo menos 3 caracteres'
                }
            
            if len(password) < 6:
                return {
                    'success': False,
                    'message': 'Senha deve ter pelo menos 6 caracteres'
                }
            
            if level not in ['user', 'admin']:
                return {
                    'success': False,
                    'message': 'Nível deve ser "user" ou "admin"'
                }
            
            # Cria usuário
            users[school_key][username] = {
                'password': self.hash_password(password),
                'level': level,
                'created_at': datetime.now().isoformat(),
                'last_login': None,
                'active': True
            }
            
            self.save_users(users)
            
            logging.info(f"Usuário criado: {username} - {school} - {level}")
            
            return {
                'success': True,
                'message': 'Usuário criado com sucesso'
            }
            
        except Exception as e:
            logging.error(f"Erro ao criar usuário: {e}")
            return {
                'success': False,
                'message': 'Erro interno do sistema'
            }
    
    def list_users(self, school):
        """Lista usuários de uma escola"""
        try:
            users = self.load_users()
            school_key = self.get_school_key(school)
            
            if school_key not in users:
                return []
            
            user_list = []
            for username, data in users[school_key].items():
                user_info = {
                    'username': username,
                    'level': data.get('level', 'user'),
                    'active': data.get('active', True),
                    'created_at': data.get('created_at'),
                    'last_login': data.get('last_login')
                }
                user_list.append(user_info)
            
            return user_list
            
        except Exception as e:
            logging.error(f"Erro ao listar usuários: {e}")
            return []
    
    def deactivate_user(self, school, username):
        """Desativa usuário"""
        try:
            users = self.load_users()
            school_key = self.get_school_key(school)
            
            if school_key not in users or username not in users[school_key]:
                return {
                    'success': False,
                    'message': 'Usuário não encontrado'
                }
            
            # Não permite desativar o último admin
            if users[school_key][username].get('level') == 'admin':
                admins = [u for u, d in users[school_key].items() 
                         if d.get('level') == 'admin' and d.get('active', True)]
                
                if len(admins) <= 1:
                    return {
                        'success': False,
                        'message': 'Não é possível desativar o último administrador'
                    }
            
            users[school_key][username]['active'] = False
            users[school_key][username]['deactivated_at'] = datetime.now().isoformat()
            
            self.save_users(users)
            
            logging.info(f"Usuário desativado: {username} - {school}")
            
            return {
                'success': True,
                'message': 'Usuário desativado com sucesso'
            }
            
        except Exception as e:
            logging.error(f"Erro ao desativar usuário: {e}")
            return {
                'success': False,
                'message': 'Erro interno do sistema'
            }
    
    def activate_user(self, school, username):
        """Ativa usuário"""
        try:
            users = self.load_users()
            school_key = self.get_school_key(school)
            
            if school_key not in users or username not in users[school_key]:
                return {
                    'success': False,
                    'message': 'Usuário não encontrado'
                }
            
            users[school_key][username]['active'] = True
            if 'deactivated_at' in users[school_key][username]:
                del users[school_key][username]['deactivated_at']
            
            self.save_users(users)
            
            logging.info(f"Usuário ativado: {username} - {school}")
            
            return {
                'success': True,
                'message': 'Usuário ativado com sucesso'
            }
            
        except Exception as e:
            logging.error(f"Erro ao ativar usuário: {e}")
            return {
                'success': False,
                'message': 'Erro interno do sistema'
            }
