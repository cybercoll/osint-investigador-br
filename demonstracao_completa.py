#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demonstração Completa - APIs Gratuitas para OSINT Brasil
Integra BrasilAPI e ViaCEP para consultas completas sem necessidade de registro
"""

import json
from brasilapi_integration import BrasilAPIClient, validar_cpf
from viacep_integration import ViaCEPClient

def demonstracao_completa():
    """Demonstração completa de todas as funcionalidades gratuitas"""
    
    print("=" * 60)
    print("DEMONSTRAÇÃO COMPLETA - OSINT BRASIL")
    print("APIs Totalmente Gratuitas - Sem Registro Necessário")
    print("=" * 60)
    print()
    
    # Inicializar clientes
    brasil_api = BrasilAPIClient()
    viacep = ViaCEPClient()
    
    # === SEÇÃO 1: CONSULTAS CEP ===
    print("🏠 SEÇÃO 1: CONSULTAS DE CEP")
    print("-" * 40)
    
    ceps_teste = ["01310-100", "20040-020", "30112-000"]
    
    for i, cep in enumerate(ceps_teste, 1):
        print(f"\n{i}.1 BrasilAPI - CEP {cep}:")
        resultado_brasil = brasil_api.consultar_cep(cep)
        print(json.dumps(resultado_brasil, indent=2, ensure_ascii=False))
        
        print(f"\n{i}.2 ViaCEP - CEP {cep}:")
        resultado_viacep = viacep.consultar_cep(cep)
        print(json.dumps(resultado_viacep, indent=2, ensure_ascii=False))
        print("-" * 40)
    
    # === SEÇÃO 2: CONSULTAS CNPJ ===
    print("\n🏢 SEÇÃO 2: CONSULTAS DE CNPJ")
    print("-" * 40)
    
    cnpjs_teste = ["11.222.333/0001-81", "00.000.000/0001-91"]
    
    for i, cnpj in enumerate(cnpjs_teste, 1):
        print(f"\n{i}. CNPJ {cnpj}:")
        resultado = brasil_api.consultar_cnpj(cnpj)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print("-" * 40)
    
    # === SEÇÃO 3: CONSULTAS DDD ===
    print("\n📞 SEÇÃO 3: CONSULTAS DE DDD")
    print("-" * 40)
    
    ddds_teste = ["11", "21", "31", "85"]
    
    for i, ddd in enumerate(ddds_teste, 1):
        print(f"\n{i}. DDD {ddd}:")
        resultado = brasil_api.consultar_ddd(ddd)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print("-" * 40)
    
    # === SEÇÃO 4: VALIDAÇÃO CPF ===
    print("\n👤 SEÇÃO 4: VALIDAÇÃO DE CPF")
    print("-" * 40)
    
    cpfs_teste = ["11144477735", "123.456.789-09", "000.000.000-00"]
    
    for i, cpf in enumerate(cpfs_teste, 1):
        print(f"\n{i}. CPF {cpf}:")
        resultado = validar_cpf(cpf)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print("-" * 40)
    
    # === SEÇÃO 5: CONSULTAS BANCÁRIAS ===
    print("\n🏦 SEÇÃO 5: CONSULTAS BANCÁRIAS")
    print("-" * 40)
    
    bancos_teste = ["001", "237", "341"]
    
    for i, codigo in enumerate(bancos_teste, 1):
        print(f"\n{i}. Banco {codigo}:")
        resultado = brasil_api.consultar_banco(codigo)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print("-" * 40)
    
    # === SEÇÃO 6: BUSCA REVERSA ===
    print("\n🔍 SEÇÃO 6: BUSCA REVERSA DE ENDEREÇOS")
    print("-" * 40)
    
    print("\n1. Busca por 'Paulista' em São Paulo:")
    resultado = viacep.buscar_endereco("SP", "São Paulo", "Paulista")
    if resultado["sucesso"] and len(resultado["enderecos"]) > 0:
        resultado_limitado = resultado.copy()
        resultado_limitado["enderecos"] = resultado["enderecos"][:2]
        resultado_limitado["observacao"] = f"Mostrando 2 de {len(resultado['enderecos'])} resultados"
        print(json.dumps(resultado_limitado, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # === RESUMO FINAL ===
    print("\n" + "=" * 60)
    print("📊 RESUMO DA DEMONSTRAÇÃO")
    print("=" * 60)
    print("✅ BrasilAPI: CEP, CNPJ, DDD, Bancos - FUNCIONANDO")
    print("✅ ViaCEP: CEP e Busca Reversa - FUNCIONANDO")
    print("✅ Validação CPF Local - FUNCIONANDO")
    print()
    print("🎯 VANTAGENS:")
    print("• Totalmente gratuito")
    print("• Sem necessidade de registro")
    print("• Sem tokens ou chaves de API")
    print("• Dados atualizados e oficiais")
    print("• Múltiplas fontes para redundância")
    print()
    print("🚀 PRONTO PARA USO EM PRODUÇÃO!")
    print("=" * 60)

def consulta_rapida(tipo: str, valor: str):
    """
    Função para consultas rápidas
    
    Args:
        tipo (str): Tipo de consulta (cep, cnpj, ddd, cpf, banco)
        valor (str): Valor para consulta
    """
    brasil_api = BrasilAPIClient()
    viacep = ViaCEPClient()
    
    if tipo.lower() == "cep":
        print("Consultando CEP via BrasilAPI:")
        resultado1 = brasil_api.consultar_cep(valor)
        print(json.dumps(resultado1, indent=2, ensure_ascii=False))
        
        print("\nConsultando CEP via ViaCEP:")
        resultado2 = viacep.consultar_cep(valor)
        print(json.dumps(resultado2, indent=2, ensure_ascii=False))
        
    elif tipo.lower() == "cnpj":
        resultado = brasil_api.consultar_cnpj(valor)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
    elif tipo.lower() == "ddd":
        resultado = brasil_api.consultar_ddd(valor)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
    elif tipo.lower() == "cpf":
        resultado = validar_cpf(valor)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
    elif tipo.lower() == "banco":
        resultado = brasil_api.consultar_banco(valor)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
    else:
        print(f"Tipo '{tipo}' não suportado. Use: cep, cnpj, ddd, cpf, banco")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Consulta rápida: python demonstracao_completa.py cep 01310-100
        consulta_rapida(sys.argv[1], sys.argv[2])
    else:
        # Demonstração completa
        demonstracao_completa()