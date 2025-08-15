# -*- coding: utf-8 -*-
"""
Constantes do Sistema DIRENS
"""

# Escolas subordinadas à DIRENS
ESCOLAS = {
    "DIRENS": {
        "codigo": "DIRENS01",
        "nome_completo": "Diretoria de Ensino da Aeronáutica",
        "endereco": "Av. Marechal Fontenelle, 1000 - Campo dos Afonsos",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "telefone": "(21) 2441-5000"
    },
    "AFA": {
        "codigo": "AFA01",
        "nome_completo": "Academia da Força Aérea",
        "endereco": "Rodovia Marechal do Ar Márcio de Souza e Mello, s/n",
        "cidade": "Pirassununga",
        "estado": "SP",
        "telefone": "(19) 3565-1234"
    },
    "CBNB": {
        "codigo": "CBNB01",
        "nome_completo": "Colégio Brigadeiro Newton Braga",
        "endereco": "Av. Mal. Fontenelle, 1000 - Sulacap",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "telefone": "(21) 3441-9000"
    },
    "CIAAR": {
        "codigo": "CIAAR01",
        "nome_completo": "Centro de Instrução e Adaptação da Aeronáutica",
        "endereco": "Av. Marechal Fontenelle, 1000 - Campo dos Afonsos",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "telefone": "(21) 2441-7000"
    },
    "CTRB": {
        "codigo": "CTRB01",
        "nome_completo": "Colégio Tenente Rêgo Barros",
        "endereco": "Av. Júlio César, 9001 - Val-de-Cans",
        "cidade": "Belém",
        "estado": "PA",
        "telefone": "(91) 3210-4000"
    },
    "ECE": {
        "codigo": "ECE01",
        "nome_completo": "Escola Caminho das Estrelas",
        "endereco": "Rua Santos Dumont, 149 - Centro",
        "cidade": "São José dos Campos",
        "estado": "SP",
        "telefone": "(12) 3947-5000"
    },
    "EEAR": {
        "codigo": "EEAR01",
        "nome_completo": "Escola de Especialista de Aeronáutica",
        "endereco": "Av. Marechal do Ar Márcio de Souza e Mello, 321",
        "cidade": "Guaratinguetá",
        "estado": "SP",
        "telefone": "(12) 3125-9000"
    },
    "EPCAR": {
        "codigo": "EPCAR01",
        "nome_completo": "Escola Preparatória de Cadetes do Ar",
        "endereco": "Rod. MG-179, Km 3 - Aeroporto",
        "cidade": "Barbacena",
        "estado": "MG",
        "telefone": "(32) 3339-4000"
    },
    "EAOAR": {
        "codigo": "EAOAR01",
        "nome_completo": "Escola de Aperfeiçoamento de Oficiais da Aeronáutica",
        "endereco": "Av. Marechal Fontenelle, 1000 - Campo dos Afonsos",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "telefone": "(21) 2441-8000"
    },
    "ECEMAR": {
        "codigo": "ECEMAR01",
        "nome_completo": "Escola de Comando Estado Maior da Aeronáutica",
        "endereco": "Av. Marechal Fontenelle, 1000 - Campo dos Afonsos",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "telefone": "(21) 2441-9000"
    },
    "UNIFA": {
        "codigo": "UNIFA01",
        "nome_completo": "Universidade da Força Aérea",
        "endereco": "Estrada de Jacarepaguá, 9007 - Jacarepaguá",
        "cidade": "Rio de Janeiro",
        "estado": "RJ",
        "telefone": "(21) 2136-7000"
    }
}

# Cargas horárias disponíveis
CARGAS_HORARIAS = [
    "20H",
    "40H", 
    "40H_DE"  # Dedicação Exclusiva
]

# Carreiras docentes
CARREIRAS = [
    "MS",    # Magistério Superior
    "EBTT"   # Ensino Básico, Técnico e Tecnológico
]

# Níveis de pós-graduação
POS_GRADUACAO = [
    "GRADUAÇÃO",
    "ESPECIALIZAÇÃO", 
    "MESTRADO",
    "DOUTORADO"
]

# DDDs do Brasil
DDDS_BRASIL = [
    "11", "12", "13", "14", "15", "16", "17", "18", "19",
    "21", "22", "24", "27", "28",
    "31", "32", "33", "34", "35", "37", "38",
    "41", "42", "43", "44", "45", "46", "47", "48", "49",
    "51", "53", "54", "55",
    "61", "62", "63", "64", "65", "66", "67", "68", "69",
    "71", "73", "74", "75", "77", "79",
    "81", "82", "83", "84", "85", "86", "87", "88", "89",
    "91", "92", "93", "94", "95", "96", "97", "98", "99"
]

# Áreas do conhecimento (CNPQ)
AREAS_CONHECIMENTO = [
    "Ciências Exatas e da Terra",
    "Ciências Biológicas",
    "Engenharias",
    "Ciências da Saúde", 
    "Ciências Agrárias",
    "Ciências Sociais Aplicadas",
    "Ciências Humanas",
    "Linguística, Letras e Artes",
    "Multidisciplinar"
]

# Tipos de vínculo
TIPOS_VINCULO = [
    "Efetivo",
    "Substituto",
    "Temporário",
    "Visitante"
]

# Status do professor
STATUS_PROFESSOR = [
    "Ativo",
    "Afastado",
    "Licença Médica",
    "Licença Maternidade", 
    "Licença Paternidade",
    "Licença Capacitação",
    "Cedido",
    "Aposentado",
    "Exonerado",
    "Falecido"
]

# Regimes de trabalho
REGIMES_TRABALHO = [
    "RDE",  # Regime de Dedicação Exclusiva
    "RT",   # Regime de Tempo Integral 
    "TP"    # Regime de Tempo Parcial
]

# Classes da carreira docente
CLASSES_DOCENTE = {
    "EBTT": ["DI", "DII", "DIII", "DIV", "DV"],
    "MS": ["Adjunto", "Associado", "Titular"]
}

# Níveis por classe EBTT
NIVEIS_EBTT = ["1", "2", "3", "4"]

# Níveis por classe MS
NIVEIS_MS = ["1", "2", "3", "4"]

# Formatos de data aceitos
DATE_FORMATS = [
    "%d-%m-%Y",
    "%d/%m/%Y", 
    "%Y-%m-%d",
    "%d.%m.%Y"
]

# Expressões regulares comuns
REGEX_PATTERNS = {
    "cpf": r"^\d{3}\.\d{3}\.\d{3}-\d{2}$",
    "siape": r"^\d{7}$",
    "telefone": r"^\(\d{2}\)\s\d{4,5}-\d{4}$",
    "cep": r"^\d{5}-\d{3}$",
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
}

# Configurações de interface
UI_CONFIG = {
    "colors": {
        "primary": "#1f4e79",
        "secondary": "#7fa6d3", 
        "success": "#28a745",
        "warning": "#ffc107",
        "danger": "#dc3545",
        "info": "#17a2b8"
    },
    "fonts": {
        "default": ("Segoe UI", 9),
        "header": ("Segoe UI", 12, "bold"),
        "title": ("Segoe UI", 14, "bold")
    }
}

# Mensagens padrão
MESSAGES = {
    "success": {
        "save": "Dados salvos com sucesso!",
        "delete": "Registro excluído com sucesso!",
        "export": "Dados exportados com sucesso!",
        "backup": "Backup criado com sucesso!",
        "restore": "Backup restaurado com sucesso!"
    },
    "error": {
        "save": "Erro ao salvar dados",
        "delete": "Erro ao excluir registro",
        "export": "Erro ao exportar dados", 
        "backup": "Erro ao criar backup",
        "restore": "Erro ao restaurar backup",
        "validation": "Dados inválidos"
    },
    "warning": {
        "unsaved_changes": "Há alterações não salvas. Deseja continuar?",
        "delete_confirm": "Deseja realmente excluir este registro?",
        "overwrite_confirm": "Arquivo já existe. Deseja sobrescrever?"
    },
    "info": {
        "loading": "Carregando dados...",
        "processing": "Processando...",
        "no_data": "Nenhum dado encontrado",
        "empty_list": "Lista vazia"
    }
}

# Constantes do sistema
SYSTEM_CONFIG = {
    "name": "Sistema DIRENS", 
    "version": "1.0.0",
    "author": "Sistema DIRENS",
    "description": "Sistema de Controle de Professores DIRENS",
    "max_file_size_mb": 50,
    "supported_image_formats": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "supported_document_formats": [".pdf", ".doc", ".docx", ".txt"],
    "date_format_display": "%d/%m/%Y",
    "datetime_format_display": "%d/%m/%Y %H:%M:%S",
    "backup_retention_days": 90,
    "session_timeout_minutes": 480
}

# Validações específicas
VALIDATION_RULES = {
    "siape": {
        "length": 7,
        "type": "numeric",
        "required": True
    },
    "cpf": {
        "length": 11,
        "type": "numeric",
        "required": True,
        "validate_digits": True
    },
    "nome": {
        "min_length": 2,
        "max_length": 100, 
        "type": "text",
        "required": True,
        "uppercase": True
    },
    "data_nascimento": {
        "format": "DD-MM-YYYY",
        "min_age": 18,
        "max_age": 80,
        "required": True
    },
    "data_ingresso": {
        "format": "DD-MM-YYYY",
        "not_future": True,
        "required": True
    }
}
