#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar se os dados de teste estão sendo carregados corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dados.data_manager import DataManager

def main():
    print("=== VERIFICAÇÃO DOS DADOS DE TESTE ===\n")
    
    try:
        # Inicializa o gerenciador de dados
        data_manager = DataManager()
        
        # Testa carregamento de todos os professores (modo DIRENS)
        print("1. Testando get_all_teachers() (usado pelo DIRENS):")
        all_teachers = data_manager.get_all_teachers()
        
        print(f"   Total de professores encontrados: {len(all_teachers)}")
        
        # Conta por escola
        schools_count = {}
        for teacher in all_teachers:
            escola = teacher.get('escola', 'Sem escola')
            schools_count[escola] = schools_count.get(escola, 0) + 1
        
        print("\n   Distribuição por escola:")
        for escola, count in sorted(schools_count.items()):
            print(f"   - {escola}: {count} professores")
        
        # Testa carregamento individual por escola
        print("\n2. Testando get_teachers_by_school() para algumas escolas:")
        test_schools = ['AFA', 'CBNB', 'EEAR', 'UNIFA']
        
        for school in test_schools:
            teachers = data_manager.get_teachers_by_school(school)
            print(f"   - {school}: {len(teachers)} professores")
            
            # Mostra nomes dos primeiros 2 professores
            if teachers:
                for i, teacher in enumerate(teachers[:2]):
                    print(f"     • {teacher.get('nome', 'Nome não encontrado')} (SIAPE: {teacher.get('siape', 'N/A')})")
        
        # Verifica se todos têm o campo 'escola'
        print(f"\n3. Verificação de integridade:")
        teachers_without_school = [t for t in all_teachers if not t.get('escola')]
        print(f"   - Professores sem campo 'escola': {len(teachers_without_school)}")
        
        teachers_with_escola_field = [t for t in all_teachers if 'escola' in t]
        print(f"   - Professores com campo 'escola': {len(teachers_with_escola_field)}")
        
        if len(all_teachers) >= 40:
            print("\n✅ SUCESSO: Dados de teste carregados corretamente!")
            print("   A janela de estatísticas DIRENS deve mostrar todos os professores.")
        else:
            print(f"\n⚠️ ATENÇÃO: Esperados pelo menos 40 professores, encontrados {len(all_teachers)}")
        
    except Exception as e:
        print(f"❌ ERRO ao verificar dados: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()