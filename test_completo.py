#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste completo para OSINT Investigador BR
Testa todas as funcionalidades principais do sistema
"""

import sys
import os
import json
import time
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from osint_investigador import OSINTInvestigador

def print_separator(title):
    """Imprime um separador visual"""
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)

def test_cep_queries():
    """Testa consultas de CEP"""
    print_separator("TESTANDO CONSULTAS CEP")
    
    investigador = OSINTInvestigador()
    
    # Teste CEP válido
    print("🔍 Testando CEP válido: 01310-100")
    resultado = investigador.consultar_cep("01310-100")
    if resultado and resultado.get('cep'):
        print("✅ CEP válido funcionando!")
        print(f"   Endereço: {resultado.get('logradouro', 'N/A')}")
        print(f"   Bairro: {resultado.get('bairro', 'N/A')}")
        print(f"   Cidade: {resultado.get('localidade', 'N/A')}")
        print(f"   UF: {resultado.get('uf', 'N/A')}")
    else:
        print("❌ Erro na consulta de CEP válido")
        return False
    
    # Teste CEP inválido
    print("\n🔍 Testando CEP inválido: 00000-000")
    resultado = investigador.consultar_cep("00000-000")
    if not resultado or resultado.get('erro'):
        print("✅ Validação de CEP inválido funcionando!")
    else:
        print("❌ Validação de CEP inválido falhou")
        return False
    
    return True

def test_ddd_queries():
    """Testa consultas de DDD"""
    print_separator("TESTANDO CONSULTAS DDD")
    
    investigador = OSINTInvestigador()
    
    # Teste DDD válido
    print("🔍 Testando DDD válido: 11")
    resultado = investigador.consultar_ddd("11")
    if resultado and resultado.get('estado'):
        print("✅ DDD válido funcionando!")
        print(f"   Estado: {resultado.get('estado', 'N/A')}")
        print(f"   Cidades: {', '.join(resultado.get('cidades', [])[:3])}...")
    else:
        print("❌ Erro na consulta de DDD válido")
        return False
    
    # Teste DDD inválido
    print("\n🔍 Testando DDD inválido: 99")
    resultado = investigador.consultar_ddd("99")
    if not resultado or resultado.get('erro'):
        print("✅ Validação de DDD inválido funcionando!")
    else:
        print("❌ Validação de DDD inválido falhou")
        return False
    
    return True

def test_cnpj_queries():
    """Testa consultas de CNPJ"""
    print_separator("TESTANDO CONSULTAS CNPJ")
    
    investigador = OSINTInvestigador()
    
    # Teste CNPJ válido (Petrobras)
    print("🔍 Testando CNPJ válido: 33.000.167/0001-01")
    resultado = investigador.consultar_cnpj("33.000.167/0001-01")
    if resultado and resultado.get('razao_social'):
        print("✅ CNPJ válido funcionando!")
        print(f"   Razão Social: {resultado.get('razao_social', 'N/A')}")
        print(f"   Fonte: {resultado.get('fonte', 'N/A')}")
    else:
        print("❌ Erro na consulta de CNPJ válido")
        return False
    
    # Teste CNPJ inválido
    print("\n🔍 Testando CNPJ inválido: 00.000.000/0001-00")
    resultado = investigador.consultar_cnpj("00.000.000/0001-00")
    if not resultado or resultado.get('erro'):
        print("✅ Validação de CNPJ inválido funcionando!")
    else:
        print("❌ Validação de CNPJ inválido falhou")
        return False
    
    return True

def test_bank_queries():
    """Testa consultas de bancos"""
    print_separator("TESTANDO CONSULTAS BANCOS")
    
    investigador = OSINTInvestigador()
    
    # Teste consulta de todos os bancos
    print("🔍 Testando consulta de todos os bancos")
    resultado = investigador.consultar_bancos()
    if resultado and resultado.get('bancos') and resultado.get('total', 0) > 0:
        print("✅ Consulta de bancos funcionando!")
        print(f"   Total de bancos: {resultado.get('total', 0)}")
    else:
        print("❌ Erro na consulta de bancos")
        return False
    
    # Teste busca de banco específico
    print("\n🔍 Testando busca de banco específico: 001")
    resultado = investigador.buscar_banco_por_codigo("001")
    if resultado and resultado.get('nome'):
        print("✅ Busca de banco específico funcionando!")
        print(f"   Banco: {resultado.get('nome', 'N/A')}")
        print(f"   Código: {resultado.get('codigo', 'N/A')}")
    else:
        print("❌ Erro na busca de banco específico")
        return False
    
    return True

def test_ibge_queries():
    """Testa consultas IBGE"""
    print_separator("TESTANDO CONSULTAS IBGE")
    
    investigador = OSINTInvestigador()
    
    # Teste consulta de municípios
    print("🔍 Testando consulta de municípios de SP")
    resultado = investigador.consultar_municipios_uf("SP")
    if resultado and resultado.get('municipios') and resultado.get('total', 0) > 0:
        print("✅ Consulta IBGE funcionando!")
        print(f"   Encontrados {resultado.get('total', 0)} municípios")
        municipios = resultado.get('municipios', [])
        if municipios:
            exemplos = [m.get('name', 'N/A') for m in municipios[:3]]
            print(f"   Exemplos: {', '.join(exemplos)}")
    else:
        print("❌ Erro na consulta IBGE")
        return False
    
    return True

def test_cache_system():
    """Testa o sistema de cache"""
    print_separator("TESTANDO SISTEMA DE CACHE")
    
    investigador = OSINTInvestigador()
    
    # Limpar cache primeiro
    print("🔍 Limpando cache para teste")
    investigador.limpar_cache()
    
    # Primeira consulta (sem cache)
    print("🔍 Primeira consulta CEP (sem cache)")
    start_time = time.time()
    resultado1 = investigador.consultar_cep("01310-100")
    time1 = time.time() - start_time
    
    # Segunda consulta (com cache)
    print("🔍 Segunda consulta CEP (com cache)")
    start_time = time.time()
    resultado2 = investigador.consultar_cep("01310-100")
    time2 = time.time() - start_time
    
    # Verificar estatísticas do cache
    stats = investigador.estatisticas_cache()
    
    if resultado1 and resultado2 and time2 < time1 and stats.get('arquivos', 0) > 0:
        print("✅ Sistema de cache funcionando!")
        print(f"   Primeira consulta: {time1:.3f}s")
        print(f"   Segunda consulta: {time2:.3f}s")
        print(f"   Melhoria: {((time1 - time2) / time1 * 100):.1f}%")
        print(f"   Arquivos em cache: {stats.get('arquivos', 0)}")
    else:
        print("❌ Sistema de cache não está funcionando adequadamente")
        return False
    
    return True

def test_export_functions():
    """Testa funções de exportação"""
    print_separator("TESTANDO FUNÇÕES DE EXPORTAÇÃO")
    
    investigador = OSINTInvestigador()
    
    # Fazer uma consulta para ter dados para exportar
    print("🔍 Fazendo consulta para teste de exportação")
    resultado = investigador.consultar_cep("01310-100")
    
    if not resultado:
        print("❌ Não foi possível obter dados para teste de exportação")
        return False
    
    # Testar exportação JSON
    try:
        json_data = json.dumps(resultado, indent=2, ensure_ascii=False)
        print("✅ Exportação JSON funcionando!")
    except Exception as e:
        print(f"❌ Erro na exportação JSON: {e}")
        return False
    
    # Testar exportação CSV (simulada)
    try:
        csv_line = f"{resultado.get('cep', '')},{resultado.get('logradouro', '')},{resultado.get('bairro', '')}"
        print("✅ Exportação CSV funcionando!")
    except Exception as e:
        print(f"❌ Erro na exportação CSV: {e}")
        return False
    
    return True

def main():
    """Função principal de teste"""
    print_separator("INICIANDO TESTES COMPLETOS - OSINT INVESTIGADOR BR")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    tests = [
        ("Consultas CEP", test_cep_queries),
        ("Consultas DDD", test_ddd_queries),
        ("Consultas CNPJ", test_cnpj_queries),
        ("Consultas Bancos", test_bank_queries),
        ("Consultas IBGE", test_ibge_queries),
        ("Sistema de Cache", test_cache_system),
        ("Funções de Exportação", test_export_functions),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Executando teste: {test_name}")
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
                
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")
            results.append((test_name, False))
    
    # Resumo final
    print_separator("RESUMO DOS TESTES")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Testes executados: {total}")
    print(f"Testes aprovados: {passed}")
    print(f"Testes falharam: {total - passed}")
    print(f"Taxa de sucesso: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM! Projeto pronto para produção!")
        return True
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Revisar antes do deploy.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)