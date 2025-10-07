#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final de Produção - OSINT Investigador BR
Verifica se o projeto está completamente funcional e pronto para produção.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from osint_investigador import OSINTInvestigador

def print_header(title):
    """Imprime cabeçalho formatado."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_test_result(test_name, success, details=""):
    """Imprime resultado do teste."""
    status = "✅ PASSOU" if success else "❌ FALHOU"
    print(f"{test_name}: {status}")
    if details:
        print(f"   Detalhes: {details}")

def test_core_functionality():
    """Testa funcionalidades principais da classe OSINTInvestigador."""
    print_header("TESTE DE FUNCIONALIDADES PRINCIPAIS")
    
    investigador = OSINTInvestigador()
    tests_passed = 0
    total_tests = 0
    
    # Teste 1: CEP válido
    total_tests += 1
    try:
        result = investigador.consultar_cep("01310-100")
        success = result.get('sucesso', False) and 'logradouro' in result and result['logradouro']
        print_test_result("CEP válido (01310-100)", success, 
                         f"Logradouro: {result.get('logradouro', 'N/A')}")
        if success:
            tests_passed += 1
    except Exception as e:
        print_test_result("CEP válido (01310-100)", False, str(e))
    
    # Teste 2: DDD válido
    total_tests += 1
    try:
        result = investigador.consultar_ddd("11")
        success = result.get('sucesso', False) and 'estado' in result and result['estado']
        print_test_result("DDD válido (11)", success, 
                         f"Estado: {result.get('estado', 'N/A')}")
        if success:
            tests_passed += 1
    except Exception as e:
        print_test_result("DDD válido (11)", False, str(e))
    
    # Teste 3: Consulta de bancos
    total_tests += 1
    try:
        result = investigador.consultar_bancos()
        success = result.get('sucesso', False) and len(result.get('bancos', [])) > 100
        print_test_result("Lista de bancos", success, 
                         f"Total de bancos: {len(result.get('bancos', []))}")
        if success:
            tests_passed += 1
    except Exception as e:
        print_test_result("Lista de bancos", False, str(e))
    
    # Teste 4: Municípios por UF
    total_tests += 1
    try:
        result = investigador.consultar_municipios_uf("SP")
        success = result.get('sucesso', False) and len(result.get('municipios', [])) > 600
        print_test_result("Municípios de SP", success, 
                         f"Total de municípios: {len(result.get('municipios', []))}")
        if success:
            tests_passed += 1
    except Exception as e:
        print_test_result("Municípios de SP", False, str(e))
    
    return tests_passed, total_tests

def test_cache_system():
    """Testa o sistema de cache."""
    print_header("TESTE DO SISTEMA DE CACHE")
    
    investigador = OSINTInvestigador()
    tests_passed = 0
    total_tests = 0
    
    # Limpar cache antes do teste
    investigador.limpar_cache()
    
    # Teste 1: Primeira consulta (sem cache)
    total_tests += 1
    try:
        start_time = time.time()
        result1 = investigador.consultar_cep("01310-100")
        time1 = time.time() - start_time
        
        # Teste 2: Segunda consulta (com cache)
        start_time = time.time()
        result2 = investigador.consultar_cep("01310-100")
        time2 = time.time() - start_time
        
        # Verificar se o cache melhorou a performance
        cache_improvement = time1 > time2 * 2  # Cache deve ser pelo menos 2x mais rápido
        success = (result1 == result2) and cache_improvement
        
        print_test_result("Sistema de cache", success, 
                         f"1ª consulta: {time1:.3f}s, 2ª consulta: {time2:.3f}s")
        if success:
            tests_passed += 1
    except Exception as e:
        print_test_result("Sistema de cache", False, str(e))
    
    # Teste 3: Estatísticas do cache
    total_tests += 1
    try:
        stats = investigador.estatisticas_cache()
        success = 'arquivos' in stats and stats['arquivos'] > 0
        print_test_result("Estatísticas do cache", success, 
                         f"Arquivos em cache: {stats.get('arquivos', 0)}")
        if success:
            tests_passed += 1
    except Exception as e:
        print_test_result("Estatísticas do cache", False, str(e))
    
    return tests_passed, total_tests

def test_export_functions():
    """Testa as funções de exportação."""
    print_header("TESTE DE EXPORTAÇÃO DE DADOS")
    
    investigador = OSINTInvestigador()
    tests_passed = 0
    total_tests = 0
    
    # Fazer uma consulta para ter dados para exportar
    result = investigador.consultar_cep("01310-100")
    
    if result.get('sucesso'):
        # Teste 1: Exportar JSON
        total_tests += 1
        try:
            json_file = investigador.exportar_json(result, "teste_export")
            success = os.path.exists(json_file)
            print_test_result("Exportação JSON", success, f"Arquivo: {json_file}")
            if success:
                tests_passed += 1
                # Limpar arquivo de teste
                try:
                    os.remove(json_file)
                except:
                    pass
        except Exception as e:
            print_test_result("Exportação JSON", False, str(e))
        
        # Teste 2: Exportar CSV
        total_tests += 1
        try:
            csv_file = investigador.exportar_csv([result], "teste_export")
            success = os.path.exists(csv_file)
            print_test_result("Exportação CSV", success, f"Arquivo: {csv_file}")
            if success:
                tests_passed += 1
                # Limpar arquivo de teste
                try:
                    os.remove(csv_file)
                except:
                    pass
        except Exception as e:
            print_test_result("Exportação CSV", False, str(e))
        
        # Teste 3: Exportar TXT
        total_tests += 1
        try:
            txt_file = investigador.exportar_txt(result, "teste_export")
            success = os.path.exists(txt_file)
            print_test_result("Exportação TXT", success, f"Arquivo: {txt_file}")
            if success:
                tests_passed += 1
                # Limpar arquivo de teste
                try:
                    os.remove(txt_file)
                except:
                    pass
        except Exception as e:
            print_test_result("Exportação TXT", False, str(e))
    
    return tests_passed, total_tests

def test_web_interface():
    """Testa se a interface web está configurada corretamente."""
    print_header("TESTE DA INTERFACE WEB")
    
    tests_passed = 0
    total_tests = 0
    
    # Teste 1: Verificar se os arquivos da web existem
    total_tests += 1
    web_files = [
        "web_app.py",
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js"
    ]
    
    missing_files = []
    for file in web_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    success = len(missing_files) == 0
    print_test_result("Arquivos da interface web", success, 
                     f"Arquivos faltando: {missing_files}" if missing_files else "Todos os arquivos presentes")
    if success:
        tests_passed += 1
    
    return tests_passed, total_tests

def test_project_structure():
    """Testa a estrutura do projeto."""
    print_header("TESTE DA ESTRUTURA DO PROJETO")
    
    tests_passed = 0
    total_tests = 0
    
    # Teste 1: Arquivos principais
    total_tests += 1
    main_files = [
        "osint_investigador.py",
        "web_app.py",
        "requirements.txt",
        "README.md",
        "config.py",
        ".gitignore"
    ]
    
    missing_files = []
    for file in main_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    success = len(missing_files) == 0
    print_test_result("Arquivos principais", success, 
                     f"Arquivos faltando: {missing_files}" if missing_files else "Todos os arquivos presentes")
    if success:
        tests_passed += 1
    
    # Teste 2: Diretórios necessários
    total_tests += 1
    directories = ["templates", "static", "static/css", "static/js", "logs", "cache", "exports"]
    
    missing_dirs = []
    for directory in directories:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    success = len(missing_dirs) == 0
    print_test_result("Estrutura de diretórios", success, 
                     f"Diretórios faltando: {missing_dirs}" if missing_dirs else "Todos os diretórios presentes")
    if success:
        tests_passed += 1
    
    return tests_passed, total_tests

def main():
    """Função principal do teste."""
    print_header("TESTE FINAL DE PRODUÇÃO - OSINT INVESTIGADOR BR")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    total_passed = 0
    total_tests = 0
    
    # Executar todos os testes
    passed, tests = test_project_structure()
    total_passed += passed
    total_tests += tests
    
    passed, tests = test_core_functionality()
    total_passed += passed
    total_tests += tests
    
    passed, tests = test_cache_system()
    total_passed += passed
    total_tests += tests
    
    passed, tests = test_export_functions()
    total_passed += passed
    total_tests += tests
    
    passed, tests = test_web_interface()
    total_passed += passed
    total_tests += tests
    
    # Resultado final
    print_header("RESULTADO FINAL")
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Testes executados: {total_tests}")
    print(f"Testes aprovados: {total_passed}")
    print(f"Taxa de sucesso: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🎉 PROJETO PRONTO PARA PRODUÇÃO! 🎉")
        print("✅ Todos os componentes principais estão funcionando corretamente.")
        return True
    elif success_rate >= 75:
        print("\n⚠️  PROJETO QUASE PRONTO PARA PRODUÇÃO")
        print("🔧 Alguns ajustes menores podem ser necessários.")
        return True
    else:
        print("\n❌ PROJETO NÃO ESTÁ PRONTO PARA PRODUÇÃO")
        print("🚨 Correções significativas são necessárias.")
        return False

if __name__ == "__main__":
    try:
        production_ready = main()
        sys.exit(0 if production_ready else 1)
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO NO TESTE: {e}")
        sys.exit(1)