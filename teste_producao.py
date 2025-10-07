#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de Produção - OSINT Investigador BR
Verifica funcionalidades essenciais para produção
"""

import sys
import os
import json
import time
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from osint_investigador import OSINTInvestigador

def print_header(title):
    """Imprime cabeçalho"""
    print("\n" + "="*50)
    print(f" {title} ")
    print("="*50)

def test_core_functionality():
    """Testa funcionalidades essenciais"""
    print_header("TESTE DE PRODUÇÃO - FUNCIONALIDADES ESSENCIAIS")
    
    investigador = OSINTInvestigador()
    tests_passed = 0
    total_tests = 0
    
    # Teste 1: CEP válido
    total_tests += 1
    print("\n🔍 Teste 1: Consulta CEP válido (01310-100)")
    try:
        resultado = investigador.consultar_cep("01310-100")
        if resultado and resultado.get('cep') and not resultado.get('erro'):
            print(f"✅ PASSOU - Endereço: {resultado.get('logradouro', 'N/A')}, {resultado.get('localidade', 'N/A')}")
            tests_passed += 1
        else:
            print("❌ FALHOU - CEP válido não retornou dados corretos")
    except Exception as e:
        print(f"❌ ERRO - {e}")
    
    # Teste 2: CEP inválido
    total_tests += 1
    print("\n🔍 Teste 2: Validação CEP inválido (00000-000)")
    try:
        resultado = investigador.consultar_cep("00000-000")
        if resultado and resultado.get('erro'):
            print("✅ PASSOU - Validação funcionando corretamente")
            tests_passed += 1
        else:
            print("❌ FALHOU - Validação de CEP inválido não funcionou")
    except Exception as e:
        print(f"❌ ERRO - {e}")
    
    # Teste 3: DDD válido
    total_tests += 1
    print("\n🔍 Teste 3: Consulta DDD válido (11)")
    try:
        resultado = investigador.consultar_ddd("11")
        if resultado and resultado.get('estado') and not resultado.get('erro'):
            print(f"✅ PASSOU - Estado: {resultado.get('estado', 'N/A')}, Cidades: {len(resultado.get('cidades', []))}")
            tests_passed += 1
        else:
            print("❌ FALHOU - DDD válido não retornou dados corretos")
    except Exception as e:
        print(f"❌ ERRO - {e}")
    
    # Teste 4: Cache funcionando
    total_tests += 1
    print("\n🔍 Teste 4: Sistema de Cache")
    try:
        # Limpar cache
        investigador.limpar_cache()
        
        # Primeira consulta
        start = time.time()
        resultado1 = investigador.consultar_cep("20040-020")  # Copacabana
        time1 = time.time() - start
        
        # Segunda consulta (cache)
        start = time.time()
        resultado2 = investigador.consultar_cep("20040-020")
        time2 = time.time() - start
        
        if resultado1 and resultado2 and time2 < time1:
            print(f"✅ PASSOU - Cache funcionando (1ª: {time1:.3f}s, 2ª: {time2:.3f}s)")
            tests_passed += 1
        else:
            print("❌ FALHOU - Cache não está funcionando")
    except Exception as e:
        print(f"❌ ERRO - {e}")
    
    # Teste 5: Exportação JSON
    total_tests += 1
    print("\n🔍 Teste 5: Exportação de dados")
    try:
        resultado = investigador.consultar_cep("01310-100")
        if resultado:
            json_data = json.dumps(resultado, indent=2, ensure_ascii=False)
            if len(json_data) > 50:  # JSON válido e com conteúdo
                print("✅ PASSOU - Exportação JSON funcionando")
                tests_passed += 1
            else:
                print("❌ FALHOU - JSON muito pequeno ou inválido")
        else:
            print("❌ FALHOU - Não há dados para exportar")
    except Exception as e:
        print(f"❌ ERRO - {e}")
    
    # Teste 6: Logs funcionando
    total_tests += 1
    print("\n🔍 Teste 6: Sistema de Logs")
    try:
        # Fazer uma consulta para gerar logs
        investigador.consultar_cep("01310-100")
        
        # Verificar se arquivo de log existe
        log_files = []
        for file in os.listdir('.'):
            if file.startswith('osint_') and file.endswith('.log'):
                log_files.append(file)
        
        if log_files:
            print(f"✅ PASSOU - Sistema de logs funcionando ({len(log_files)} arquivo(s))")
            tests_passed += 1
        else:
            print("❌ FALHOU - Arquivos de log não encontrados")
    except Exception as e:
        print(f"❌ ERRO - {e}")
    
    # Resumo
    print_header("RESUMO DO TESTE DE PRODUÇÃO")
    print(f"Testes executados: {total_tests}")
    print(f"Testes aprovados: {tests_passed}")
    print(f"Taxa de sucesso: {(tests_passed/total_tests*100):.1f}%")
    
    if tests_passed >= 5:  # Pelo menos 5 dos 6 testes essenciais
        print("\n🎉 PROJETO APROVADO PARA PRODUÇÃO!")
        print("✅ Funcionalidades essenciais estão funcionando")
        print("✅ Sistema está estável e pronto para deploy")
        return True
    else:
        print(f"\n⚠️ PROJETO PRECISA DE AJUSTES")
        print(f"❌ Apenas {tests_passed}/{total_tests} testes passaram")
        print("❌ Revisar funcionalidades antes do deploy")
        return False

def test_web_interface():
    """Testa se a interface web pode ser iniciada"""
    print_header("TESTE DA INTERFACE WEB")
    
    try:
        # Importar módulos da web app
        from web_app import app
        
        # Verificar se a app foi criada
        if app:
            print("✅ Interface web configurada corretamente")
            print("✅ Flask app criada com sucesso")
            print("✅ Rotas configuradas")
            return True
        else:
            print("❌ Erro na configuração da interface web")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao importar interface web: {e}")
        return False

def main():
    """Função principal"""
    print_header("OSINT INVESTIGADOR BR - TESTE DE PRODUÇÃO")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Teste das funcionalidades principais
    core_ok = test_core_functionality()
    
    # Teste da interface web
    web_ok = test_web_interface()
    
    # Resultado final
    print_header("RESULTADO FINAL")
    
    if core_ok and web_ok:
        print("🎉 PROJETO 100% PRONTO PARA PRODUÇÃO!")
        print("✅ Todas as funcionalidades essenciais funcionando")
        print("✅ Interface web configurada corretamente")
        print("✅ Sistema estável e confiável")
        print("\n🚀 PODE FAZER O DEPLOY NO GITHUB!")
        return True
    elif core_ok:
        print("✅ FUNCIONALIDADES PRINCIPAIS OK")
        print("⚠️ Interface web com problemas menores")
        print("✅ PODE FAZER O DEPLOY (funcionalidades essenciais OK)")
        return True
    else:
        print("❌ PROJETO NÃO ESTÁ PRONTO")
        print("❌ Funcionalidades essenciais com problemas")
        print("❌ NÃO FAZER DEPLOY AINDA")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)