# -*- coding: utf-8 -*-
"""
Módulo de Validadores - Sistema DIRENS
"""

import re
from datetime import datetime
import logging

from recursos.constants import CARGAS_HORARIAS, CARREIRAS, POS_GRADUACAO

class ValidatorManager:
    """Gerenciador de validações"""
    
    def __init__(self):
        """Inicializa o validador"""
        self.cpf_pattern = re.compile(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$')
        self.siape_pattern = re.compile(r'^\d{7}$')
        self.date_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')
    
    def validate_siape(self, siape):
        """Valida SIAPE (7 dígitos)"""
        if not siape:
            return False
        
        # Remove espaços e caracteres não numéricos
        siape_clean = re.sub(r'\D', '', str(siape))
        
        # Deve ter exatamente 7 dígitos
        return len(siape_clean) == 7 and siape_clean.isdigit()
    
    def validate_cpf(self, cpf):
        """Valida CPF brasileiro"""
        if not cpf:
            return False
        
        # Remove pontos, hífens e espaços
        cpf_clean = re.sub(r'[^\d]', '', str(cpf))
        
        # Deve ter 11 dígitos
        if len(cpf_clean) != 11:
            return False
        
        # Verifica se não são todos dígitos iguais
        if cpf_clean == cpf_clean[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        sum1 = sum(int(cpf_clean[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (sum1 % 11)
        if digit1 > 9:
            digit1 = 0
        
        # Calcula segundo dígito verificador
        sum2 = sum(int(cpf_clean[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (sum2 % 11)
        if digit2 > 9:
            digit2 = 0
        
        # Verifica se os dígitos conferem
        return cpf_clean[-2:] == f"{digit1}{digit2}"
    
    def validate_date(self, date_str):
        """Valida data no formato DD-MM-AAAA"""
        if not date_str:
            return False
        
        # Verifica formato
        if not self.date_pattern.match(str(date_str)):
            return False
        
        try:
            # Tenta converter para data válida
            day, month, year = map(int, date_str.split('-'))
            datetime(year, month, day)
            
            # Verifica se a data não é muito antiga ou futura
            current_year = datetime.now().year
            if year < 1900 or year > current_year + 1:
                return False
            
            return True
            
        except ValueError:
            return False
    
    def validate_email(self, email):
        """Valida formato de email"""
        if not email:
            return True  # Email é opcional
        
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        return email_pattern.match(email.strip()) is not None
    
    def validate_phone(self, phone):
        """Valida telefone brasileiro"""
        if not phone:
            return True  # Telefone é opcional
        
        # Remove caracteres não numéricos
        phone_clean = re.sub(r'\D', '', str(phone))
        
        # Aceita formatos: 10 dígitos (fixo) ou 11 dígitos (celular)
        return len(phone_clean) in [10, 11]
    
    def validate_required_fields(self, data):
        """Valida campos obrigatórios"""
        required_fields = [
            'siape', 'nome', 'data_nascimento', 'sexo',
            'carga_horaria', 'carreira', 'data_ingresso', 'pos_graduacao'
        ]
        
        missing_fields = []
        
        for field in required_fields:
            value = data.get(field)
            if not value or str(value).strip() == '':
                missing_fields.append(field)
        
        return missing_fields
    
    def validate_restricted_values(self, data):
        """Valida valores restritos (listas fechadas)"""
        errors = []
        
        # Valida carga horária
        carga = data.get('carga_horaria')
        if carga and carga not in CARGAS_HORARIAS:
            errors.append(f"Carga horária inválida: {carga}")
        
        # Valida carreira
        carreira = data.get('carreira')
        if carreira and carreira not in CARREIRAS:
            errors.append(f"Carreira inválida: {carreira}")
        
        # Valida pós-graduação
        pos = data.get('pos_graduacao')
        if pos and pos not in POS_GRADUACAO:
            errors.append(f"Pós-graduação inválida: {pos}")
        
        # Valida sexo
        sexo = data.get('sexo')
        if sexo and sexo not in ['M', 'F']:
            errors.append(f"Sexo deve ser 'M' ou 'F'")
        
        return errors
    
    def validate_business_rules(self, data):
        """Valida regras de negócio específicas"""
        errors = []
        
        # Valida idade mínima (18 anos)
        data_nasc = data.get('data_nascimento')
        if data_nasc and self.validate_date(data_nasc):
            try:
                day, month, year = map(int, data_nasc.split('-'))
                birth_date = datetime(year, month, day)
                age = (datetime.now() - birth_date).days / 365.25
                
                if age < 18:
                    errors.append("Professor deve ter pelo menos 18 anos")
                elif age > 80:
                    errors.append("Verifique a data de nascimento (idade muito alta)")
                    
            except Exception:
                pass
        
        # Valida data de ingresso não pode ser futura
        data_ing = data.get('data_ingresso')
        if data_ing and self.validate_date(data_ing):
            try:
                day, month, year = map(int, data_ing.split('-'))
                ingresso_date = datetime(year, month, day)
                
                if ingresso_date > datetime.now():
                    errors.append("Data de ingresso não pode ser futura")
                    
                # Data de ingresso deve ser posterior ao nascimento + 18 anos
                if data_nasc and self.validate_date(data_nasc):
                    day_nasc, month_nasc, year_nasc = map(int, data_nasc.split('-'))
                    birth_date = datetime(year_nasc, month_nasc, day_nasc)
                    min_ingresso = datetime(year_nasc + 18, month_nasc, day_nasc)
                    
                    if ingresso_date < min_ingresso:
                        errors.append("Data de ingresso deve ser posterior aos 18 anos")
                        
            except Exception:
                pass
        
        # Valida consistência de formação
        pos_graduacao = data.get('pos_graduacao')
        graduacao = data.get('graduacao', '').strip()
        
        if pos_graduacao in ['ESPECIALIZAÇÃO', 'MESTRADO', 'DOUTORADO'] and not graduacao:
            errors.append("Graduação é obrigatória para pós-graduação")
        
        return errors
    
    def validate_teacher_data(self, data):
        """Validação completa dos dados do professor"""
        all_errors = []
        
        try:
            # Campos obrigatórios
            missing_fields = self.validate_required_fields(data)
            if missing_fields:
                all_errors.extend([f"Campo obrigatório: {field}" for field in missing_fields])
            
            # Se há campos obrigatórios faltando, não continua
            if missing_fields:
                return {'valid': False, 'errors': all_errors}
            
            # Validações específicas
            siape = data.get('siape', '').strip()
            if not self.validate_siape(siape):
                all_errors.append("SIAPE deve ter exatamente 7 dígitos numéricos")
            
            # CPF removido por questões de segurança e privacidade
            
            data_nasc = data.get('data_nascimento', '').strip()
            if not self.validate_date(data_nasc):
                all_errors.append("Data de nascimento inválida (formato: DD-MM-AAAA)")
            
            data_ing = data.get('data_ingresso', '').strip()
            if not self.validate_date(data_ing):
                all_errors.append("Data de ingresso inválida (formato: DD-MM-AAAA)")
            
            # Validações de email e telefone (opcionais)
            email = data.get('email', '').strip()
            if email and not self.validate_email(email):
                all_errors.append("Email inválido")
            
            telefone = data.get('telefone', '').strip()
            if telefone and not self.validate_phone(telefone):
                all_errors.append("Telefone inválido")
            
            # Valores restritos
            restricted_errors = self.validate_restricted_values(data)
            all_errors.extend(restricted_errors)
            
            # Regras de negócio
            business_errors = self.validate_business_rules(data)
            all_errors.extend(business_errors)
            
            # Validações de tamanho
            nome = data.get('nome', '').strip()
            if len(nome) < 2:
                all_errors.append("Nome deve ter pelo menos 2 caracteres")
            elif len(nome) > 100:
                all_errors.append("Nome muito longo (máximo 100 caracteres)")
            
            # Verifica se nome contém apenas letras e espaços
            if nome and not re.match(r'^[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+$', nome):
                all_errors.append("Nome deve conter apenas letras e espaços")
            
            return {
                'valid': len(all_errors) == 0,
                'errors': all_errors
            }
            
        except Exception as e:
            logging.error(f"Erro na validação: {e}")
            return {
                'valid': False,
                'errors': ['Erro interno na validação dos dados']
            }
    
    def sanitize_teacher_data(self, data):
        """Limpa e padroniza dados do professor"""
        cleaned_data = data.copy()
        
        try:
            # Limpa e formata campos de texto
            text_fields = ['nome', 'graduacao', 'curso_pos', 'area_atuacao', 
                          'instituicao_graduacao', 'instituicao_pos']
            
            for field in text_fields:
                if field in cleaned_data and cleaned_data[field]:
                    # Remove espaços extras e converte para maiúscula (exceto alguns campos)
                    value = str(cleaned_data[field]).strip()
                    if field == 'nome':
                        cleaned_data[field] = value.upper()
                    else:
                        cleaned_data[field] = value
            
            # Limpa SIAPE (apenas números)
            if 'siape' in cleaned_data:
                siape = re.sub(r'\D', '', str(cleaned_data['siape']))
                cleaned_data['siape'] = siape
            
            # CPF removido por questões de segurança e privacidade
            
            # Formata telefone
            if 'telefone' in cleaned_data and cleaned_data['telefone']:
                phone = re.sub(r'\D', '', str(cleaned_data['telefone']))
                if len(phone) == 11:
                    cleaned_data['telefone'] = f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
                elif len(phone) == 10:
                    cleaned_data['telefone'] = f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
            
            # Remove campos vazios opcionais
            optional_fields = ['email', 'telefone', 'area_atuacao',
                             'graduacao', 'instituicao_graduacao', 'curso_pos', 'instituicao_pos']
            
            for field in optional_fields:
                if field in cleaned_data and not str(cleaned_data[field]).strip():
                    cleaned_data[field] = ''
            
            return cleaned_data
            
        except Exception as e:
            logging.error(f"Erro na limpeza dos dados: {e}")
            return data
