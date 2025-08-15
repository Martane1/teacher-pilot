"""
Módulo de Recursos do Sistema DIRENS
Contém configurações, constantes e utilitários
"""

__version__ = "1.0.0"
__author__ = "Sistema DIRENS"

from .constants import ESCOLAS, CARGAS_HORARIAS, CARREIRAS, POS_GRADUACAO, ESTADOS
from .config import Config
from .utils import format_cpf, format_siape, format_phone, validate_date_format

__all__ = [
    'ESCOLAS',
    'CARGAS_HORARIAS', 
    'CARREIRAS',
    'POS_GRADUACAO',
    'ESTADOS',
    'Config',
    'format_cpf',
    'format_siape', 
    'format_phone',
    'validate_date_format'
]
