# -*- coding: utf-8 -*-
"""
Constantes do Sistema DIRENS
"""

# Escolas subordinadas à DIRENS
ESCOLAS = {
    "IFPE - Campus Recife": {
        "codigo": "PE01",
        "endereco": "Av. Prof. Luís Freire, 500 - Cidade Universitária",
        "cidade": "Recife",
        "estado": "PE",
        "telefone": "(81) 2125-1600"
    },
    "IFPE - Campus Olinda": {
        "codigo": "PE02", 
        "endereco": "Rua Márcio Canuto, 210 - Nossa Senhora do Amparo",
        "cidade": "Olinda",
        "estado": "PE",
        "telefone": "(81) 3412-5000"
    },
    "IFPE - Campus Jaboatão": {
        "codigo": "PE03",
        "endereco": "BR-104, Km 56 - Sucupira",
        "cidade": "Jaboatão dos Guararapes", 
        "estado": "PE",
        "telefone": "(81) 3186-5000"
    },
    "IFPE - Campus Vitória": {
        "codigo": "PE04",
        "endereco": "Rua Sebastião Cavalcanti, 158 - Vitória de Santo Antão",
        "cidade": "Vitória de Santo Antão",
        "estado": "PE", 
        "telefone": "(81) 3523-8100"
    },
    "IFPE - Campus Palmares": {
        "codigo": "PE05",
        "endereco": "BR-101 Sul, Km 83 - Engenho Noruega",
        "cidade": "Palmares",
        "estado": "PE",
        "telefone": "(81) 3661-9500"
    },
    "IFPE - Campus Garanhuns": {
        "codigo": "PE06",
        "endereco": "Av. Rui Barbosa, s/n - Vila Kennedy", 
        "cidade": "Garanhuns",
        "estado": "PE",
        "telefone": "(87) 3761-4304"
    },
    "IFPE - Campus Caruaru": {
        "codigo": "PE07",
        "endereco": "Rodovia BR-104, Km 59,2 - Fazenda Riachão",
        "cidade": "Caruaru",
        "estado": "PE",
        "telefone": "(81) 3706-8700"
    },
    "IFPE - Campus Pesqueira": {
        "codigo": "PE08",
        "endereco": "Rodovia BR-232, Km 214 - Prado",
        "cidade": "Pesqueira", 
        "estado": "PE",
        "telefone": "(87) 3835-1929"
    },
    "IFPE - Campus Cabo": {
        "codigo": "PE09",
        "endereco": "Av. Beira Rio, s/n - Vila Velha",
        "cidade": "Cabo de Santo Agostinho",
        "estado": "PE",
        "telefone": "(81) 3518-8900"
    },
    "IFPE - Campus Barreiros": {
        "codigo": "PE10",
        "endereco": "Fazenda Sapé, s/n - Zona Rural",
        "cidade": "Barreiros",
        "estado": "PE", 
        "telefone": "(81) 3675-1400"
    },
    "IFPE - Campus Belo Jardim": {
        "codigo": "PE11",
        "endereco": "Av. Sebastião Rodrigues da Costa, s/n - São Pedro",
        "cidade": "Belo Jardim",
        "estado": "PE",
        "telefone": "(81) 3726-4900"
    },
    "IFPE - Campus Afogados da Ingazeira": {
        "codigo": "PE12",
        "endereco": "Rodovia PE-366, s/n - DNER",
        "cidade": "Afogados da Ingazeira",
        "estado": "PE",
        "telefone": "(87) 3838-2100"
    },
    "IFPE - Campus Abreu e Lima": {
        "codigo": "PE13",
        "endereco": "Rua Venâncio João da Costa, s/n - Fosfato",
        "cidade": "Abreu e Lima", 
        "estado": "PE",
        "telefone": "(81) 3362-7777"
    },
    "IFPE - Campus Ipojuca": {
        "codigo": "PE14",
        "endereco": "Rodovia PE-060, s/n - Ipojuca",
        "cidade": "Ipojuca",
        "estado": "PE",
        "telefone": "(81) 3511-4100"
    },
    "IFPE - Campus Igarassu": {
        "codigo": "PE15",
        "endereco": "Rodovia PE-015, Km 12 - Cruz de Rebouças",
        "cidade": "Igarassu",
        "estado": "PE",
        "telefone": "(81) 3543-3600"
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

# Estados brasileiros
ESTADOS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
    "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]

# Estados com nomes completos
ESTADOS_COMPLETOS = {
    "AC": "Acre",
    "AL": "Alagoas", 
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso", 
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima", 
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}

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
