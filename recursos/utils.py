# -*- coding: utf-8 -*-
"""
Utilitários do Sistema DIRENS
"""

import re
import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
import tkinter as tk
from tkinter import messagebox

def format_cpf(cpf: str) -> str:
    """Formata CPF no padrão XXX.XXX.XXX-XX"""
    if not cpf:
        return ""
    
    # Remove caracteres não numéricos
    cpf_clean = re.sub(r'\D', '', str(cpf))
    
    # Adiciona formatação se tem 11 dígitos
    if len(cpf_clean) == 11:
        return f"{cpf_clean[:3]}.{cpf_clean[3:6]}.{cpf_clean[6:9]}-{cpf_clean[9:]}"
    
    return cpf_clean

def format_siape(siape: str) -> str:
    """Formata SIAPE removendo caracteres não numéricos"""
    if not siape:
        return ""
    
    # Remove caracteres não numéricos
    siape_clean = re.sub(r'\D', '', str(siape))
    
    # Retorna apenas se tem 7 dígitos
    if len(siape_clean) == 7:
        return siape_clean
    
    return siape_clean

def format_phone(phone: str) -> str:
    """Formata telefone no padrão (XX) XXXX-XXXX ou (XX) XXXXX-XXXX"""
    if not phone:
        return ""
    
    # Remove caracteres não numéricos  
    phone_clean = re.sub(r'\D', '', str(phone))
    
    # Formata conforme número de dígitos
    if len(phone_clean) == 10:
        return f"({phone_clean[:2]}) {phone_clean[2:6]}-{phone_clean[6:]}"
    elif len(phone_clean) == 11:
        return f"({phone_clean[:2]}) {phone_clean[2:7]}-{phone_clean[7:]}"
    
    return phone_clean

def format_cep(cep: str) -> str:
    """Formata CEP no padrão XXXXX-XXX"""
    if not cep:
        return ""
    
    # Remove caracteres não numéricos
    cep_clean = re.sub(r'\D', '', str(cep))
    
    # Adiciona formatação se tem 8 dígitos
    if len(cep_clean) == 8:
        return f"{cep_clean[:5]}-{cep_clean[5:]}"
    
    return cep_clean

def validate_date_format(date_str: str, format_str: str = "%d-%m-%Y") -> bool:
    """Valida formato de data"""
    if not date_str:
        return False
    
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False

def convert_date_format(date_str: str, input_format: str = "%d-%m-%Y", 
                       output_format: str = "%Y-%m-%d") -> Optional[str]:
    """Converte data entre formatos"""
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return None

def calculate_age(birth_date: str, reference_date: Optional[str] = None) -> Optional[int]:
    """Calcula idade a partir da data de nascimento"""
    try:
        birth = datetime.strptime(birth_date, "%d-%m-%Y")
        
        if reference_date:
            ref = datetime.strptime(reference_date, "%d-%m-%Y")
        else:
            ref = datetime.now()
        
        age = ref.year - birth.year
        
        # Ajusta se ainda não fez aniversário no ano
        if ref.month < birth.month or (ref.month == birth.month and ref.day < birth.day):
            age -= 1
        
        return age
        
    except ValueError:
        return None

def sanitize_filename(filename: str) -> str:
    """Remove caracteres inválidos de nome de arquivo"""
    # Caracteres não permitidos em nomes de arquivo
    invalid_chars = r'[<>:"/\\|?*]'
    
    # Remove caracteres inválidos
    clean_filename = re.sub(invalid_chars, '_', filename)
    
    # Remove pontos no final
    clean_filename = clean_filename.rstrip('.')
    
    # Limita tamanho
    if len(clean_filename) > 200:
        clean_filename = clean_filename[:200]
    
    return clean_filename

def format_file_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo em formato legível"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

def get_system_info() -> Dict[str, Any]:
    """Retorna informações do sistema"""
    import platform
    
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation()
    }

def center_window(window: tk.Tk, width: int, height: int) -> None:
    """Centraliza janela na tela"""
    # Obtém dimensões da tela
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calcula posição central
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Define geometria
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_error(title: str, message: str, parent: Optional[tk.Tk] = None) -> None:
    """Mostra diálogo de erro"""
    messagebox.showerror(title, message, parent=parent)

def show_warning(title: str, message: str, parent: Optional[tk.Tk] = None) -> None:
    """Mostra diálogo de aviso"""
    messagebox.showwarning(title, message, parent=parent)

def show_info(title: str, message: str, parent: Optional[tk.Tk] = None) -> None:
    """Mostra diálogo de informação"""
    messagebox.showinfo(title, message, parent=parent)

def confirm_dialog(title: str, message: str, parent: Optional[tk.Tk] = None) -> bool:
    """Mostra diálogo de confirmação"""
    return messagebox.askyesno(title, message, parent=parent)

def create_directory_if_not_exists(directory: str) -> bool:
    """Cria diretório se não existir"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception as e:
        logging.error(f"Erro ao criar diretório {directory}: {e}")
        return False

def safe_remove_file(filepath: str) -> bool:
    """Remove arquivo de forma segura"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception as e:
        logging.error(f"Erro ao remover arquivo {filepath}: {e}")
        return False

def backup_file(filepath: str, backup_dir: str = "backups") -> Optional[str]:
    """Cria backup de um arquivo"""
    try:
        if not os.path.exists(filepath):
            return None
        
        # Cria diretório de backup
        create_directory_if_not_exists(backup_dir)
        
        # Nome do backup com timestamp
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copia arquivo
        import shutil
        shutil.copy2(filepath, backup_path)
        
        return backup_path
        
    except Exception as e:
        logging.error(f"Erro ao fazer backup de {filepath}: {e}")
        return None

def load_json_file(filepath: str, default: Any = None) -> Any:
    """Carrega arquivo JSON de forma segura"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default or {}
    except Exception as e:
        logging.error(f"Erro ao carregar JSON {filepath}: {e}")
        return default or {}

def save_json_file(filepath: str, data: Any) -> bool:
    """Salva arquivo JSON de forma segura"""
    try:
        # Cria diretório se não existir
        directory = os.path.dirname(filepath)
        if directory:
            create_directory_if_not_exists(directory)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        logging.error(f"Erro ao salvar JSON {filepath}: {e}")
        return False

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> List[str]:
    """Valida campos obrigatórios"""
    missing_fields = []
    
    for field in required_fields:
        value = data.get(field)
        if not value or str(value).strip() == '':
            missing_fields.append(field)
    
    return missing_fields

def clean_string(text: str, remove_accents: bool = False) -> str:
    """Limpa string removendo caracteres especiais"""
    if not text:
        return ""
    
    # Remove espaços extras
    cleaned = re.sub(r'\s+', ' ', str(text).strip())
    
    # Remove acentos se solicitado
    if remove_accents:
        import unicodedata
        normalized = unicodedata.normalize('NFD', cleaned)
        cleaned = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    
    return cleaned

def generate_unique_id() -> str:
    """Gera ID único baseado em timestamp"""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]

def is_valid_email(email: str) -> bool:
    """Valida formato de email"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def mask_sensitive_data(text: str, mask_char: str = '*', 
                       visible_start: int = 2, visible_end: int = 2) -> str:
    """Mascara dados sensíveis"""
    if not text or len(text) <= visible_start + visible_end:
        return mask_char * len(text) if text else ""
    
    start = text[:visible_start]
    end = text[-visible_end:] if visible_end > 0 else ""
    middle = mask_char * (len(text) - visible_start - visible_end)
    
    return f"{start}{middle}{end}"

def get_resource_path(relative_path: str) -> str:
    """Obtém caminho absoluto para recurso (útil para executáveis)"""
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def setup_logging(log_level: str = "INFO", log_file: str = None) -> None:
    """Configura sistema de logging"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    handlers = [logging.StreamHandler()]
    
    if log_file:
        # Cria diretório de logs
        log_dir = os.path.dirname(log_file)
        if log_dir:
            create_directory_if_not_exists(log_dir)
        
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def benchmark_function(func, *args, **kwargs) -> tuple:
    """Mede tempo de execução de uma função"""
    import time
    
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    execution_time = end_time - start_time
    return result, execution_time

def retry_operation(func, max_attempts: int = 3, delay: float = 1.0, 
                   exceptions: tuple = (Exception,)) -> Any:
    """Repete operação em caso de falha"""
    import time
    
    for attempt in range(max_attempts):
        try:
            return func()
        except exceptions as e:
            if attempt == max_attempts - 1:
                raise e
            
            logging.warning(f"Tentativa {attempt + 1} falhou: {e}. Tentando novamente em {delay}s...")
            time.sleep(delay)
            delay *= 2  # Backoff exponencial

def parse_version(version_string: str) -> tuple:
    """Parse string de versão para tupla comparável"""
    try:
        return tuple(map(int, version_string.split('.')))
    except ValueError:
        return (0, 0, 0)

def compare_versions(version1: str, version2: str) -> int:
    """Compara duas versões. Retorna -1, 0 ou 1"""
    v1 = parse_version(version1)
    v2 = parse_version(version2)
    
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0

def get_free_disk_space(path: str = ".") -> int:
    """Retorna espaço livre em disco em bytes"""
    try:
        if os.name == 'nt':  # Windows
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path),
                ctypes.pointer(free_bytes),
                None, None
            )
            return free_bytes.value
        else:  # Unix/Linux
            statvfs = os.statvfs(path)
            return statvfs.f_frsize * statvfs.f_available
    except Exception:
        return 0

def is_directory_writable(directory: str) -> bool:
    """Verifica se diretório é gravável"""
    try:
        test_file = os.path.join(directory, 'test_write_permission.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except Exception:
        return False
