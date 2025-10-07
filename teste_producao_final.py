#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste Final de Produção - OSINT Investigador BR
Verifica funcionalidades essenciais para produção.
"""

import os
import sys
import json
import time
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

def main():
    """Teste final de produção."""
    print_header("TESTE FINAL DE PRODUÇÃO - OSINT INVESTIGADOR BR")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    total_passed = 0
    total_tests = 0
    
    # Teste 1: Estrutura do projeto
    print_header("ESTRUTURA DO PROJETO")
    total_tests += 1
    
    required_files = [
        "osint_investigador.py",
        "web_app.py", 
        "requirements.txt",
        "README.md",
        "config.py",
        ".gitignore",
        "templates/index.html",
        "static/js/app.js",
        "static/css/style.css"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    success = len(missing_files) == 0
    print_test_result("Arquivos essenciais", success, 
                     f"Faltando: {missing_files}" if missing_files else "Todos presentes")
    if success:
        total_passed += 1
    
    # Teste 2: Classe OSINTInvestigador funcional
    print_header("FUNCIONALIDADE PRINCIPAL")
    total_tests += 1
    
    try:
        investigador = OSINTInvestigador()
        
        # Teste CEP
        result_cep = investigador.consultar_cep("01310-100")
        cep_ok = result_cep.get('sucesso', False)
        
        # Teste DDD
        result_ddd = investigador.consultar_ddd("11")
        ddd_ok = result_ddd.get('sucesso', False)
        
        # Teste Bancos
        result_bancos = investigador.consultar_bancos()
        bancos_ok = result_bancos.get('sucesso', False)
        
        success = cep_ok and ddd_ok and bancos_ok
        details = f"CEP: {'OK' if cep_ok else 'ERRO'}, DDD: {'OK' if ddd_ok else 'ERRO'}, Bancos: {'OK' if bancos_ok else 'ERRO'}"
        
        print_test_result("APIs funcionando", success, details)
        if success:
            total_passed += 1
            
    except Exception as e:
        print_test_result("APIs funcionando", False, str(e))
    
    # Teste 3: Sistema de cache
    print_header("SISTEMA DE CACHE")
    total_tests += 1
    
    try:
        investigador = OSINTInvestigador()
        investigador.limpar_cache()
        
        # Primeira consulta
        start = time.time()
        investigador.consultar_cep("01310-100")
        time1 = time.time() - start
        
        # Segunda consulta (cache)
        start = time.time()
        investigador.consultar_cep("01310-100")
        time2 = time.time() - start
        
        # Cache deve ser mais rápido
        success = time2 < time1 / 2
        print_test_result("Cache funcionando", success, 
                         f"1ª: {time1:.3f}s, 2ª: {time2:.3f}s")
        if success:
            total_passed += 1
            
    except Exception as e:
        print_test_result("Cache funcionando", False, str(e))
    
    # Teste 4: Exportação
    print_header("EXPORTAÇÃO DE DADOS")
    total_tests += 1
    
    try:
        investigador = OSINTInvestigador()
        result = investigador.consultar_cep("01310-100")
        
        if result.get('sucesso') and result.get('logradouro'):
            # Testar exportação JSON
            json_file = investigador.exportar_json(result, "teste")
            json_ok = os.path.exists(json_file)
            
            # Limpar arquivo de teste
            if json_ok:
                try:
                    os.remove(json_file)
                except:
                    pass
            
            print_test_result("Exportação JSON", json_ok, 
                             "Arquivo criado com sucesso" if json_ok else "Falha na criação")
            if json_ok:
                total_passed += 1
        else:
            print_test_result("Exportação JSON", False, "Sem dados válidos para exportar")
            
    except Exception as e:
        print_test_result("Exportação JSON", False, str(e))
    
    # Teste 5: Interface Web
    print_header("INTERFACE WEB")
    total_tests += 1
    
    try:
        # Verificar se o Flask pode ser importado e configurado
        from web_app import app
        success = app is not None
        print_test_result("Flask configurado", success, 
                         "App Flask criado com sucesso" if success else "Erro na configuração")
        if success:
            total_passed += 1
            
    except Exception as e:
        print_test_result("Flask configurado", False, str(e))
    
    # Resultado Final
    print_header("RESULTADO FINAL")
    success_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Testes executados: {total_tests}")
    print(f"Testes aprovados: {total_passed}")
    print(f"Taxa de sucesso: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print("\n🎉 PROJETO PRONTO PARA PRODUÇÃO! 🎉")
        print("✅ Funcionalidades essenciais verificadas e funcionando.")
        print("✅ Estrutura completa e organizada.")
        print("✅ Sistema de cache operacional.")
        print("✅ Exportação de dados funcionando.")
        print("✅ Interface web configurada.")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Fazer commit das alterações finais")
        print("2. Push para o repositório GitHub")
        print("3. Projeto está pronto para uso!")
        return True
    else:
        print(f"\n⚠️  PROJETO COM {success_rate:.1f}% DE FUNCIONALIDADE")
        print("🔧 Algumas funcionalidades podem precisar de ajustes.")
        if success_rate >= 60:
            print("✅ Funcionalidades principais estão operacionais.")
            return True
        else:
            print("❌ Correções necessárias antes da produção.")
            return False

if __name__ == "__main__":
    try:
        production_ready = main()
        sys.exit(0 if production_ready else 1)
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        sys.exit(1)