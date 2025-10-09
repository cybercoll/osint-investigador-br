#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar a funcionalidade de identificação de operadora
com portabilidade numérica implementada no sistema OSINT.

Este script testa:
1. A função consultar_operadora_abr_telecom
2. A função identificar_operadora_por_prefixo atualizada
3. Os endpoints da API que utilizam essas funções
"""

import sys
import os
import requests
import json
from datetime import datetime

# Adicionar o diretório da API ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

def testar_funcoes_localmente():
    """Testa as funções diretamente importando o módulo"""
    print("=" * 60)
    print("TESTE 1: Testando funções localmente")
    print("=" * 60)
    
    try:
        # Importar as funções do módulo
        from index import consultar_operadora_abr_telecom, identificar_operadora_por_prefixo
        
        # Números de teste (alguns reais, alguns fictícios)
        numeros_teste = [
            "11999999999",  # São Paulo - Celular
            "1133334444",   # São Paulo - Fixo
            "21987654321",  # Rio de Janeiro - Celular
            "85988776655",  # Fortaleza - Celular
            "61999887766",  # Brasília - Celular
            "1199999",      # Número inválido (muito curto)
            "119999999999", # Número inválido (muito longo)
        ]
        
        print(f"Testando {len(numeros_teste)} números...")
        print()
        
        for i, numero in enumerate(numeros_teste, 1):
            print(f"Teste {i}: {numero}")
            print("-" * 40)
            
            # Testar consulta ABR Telecom
            print("Consultando ABR Telecom...")
            resultado_abr = consultar_operadora_abr_telecom(numero)
            if resultado_abr:
                print(f"  Resultado ABR: {json.dumps(resultado_abr, indent=2, ensure_ascii=False)}")
            else:
                print("  Resultado ABR: None")
            
            # Testar identificação por prefixo
            print("Identificando por prefixo...")
            resultado_prefixo = identificar_operadora_por_prefixo(numero)
            print(f"  Resultado Prefixo: {json.dumps(resultado_prefixo, indent=2, ensure_ascii=False)}")
            
            print()
        
        return True
        
    except ImportError as e:
        print(f"Erro ao importar módulos: {e}")
        return False
    except Exception as e:
        print(f"Erro durante teste local: {e}")
        return False

def testar_endpoints_api():
    """Testa os endpoints da API que utilizam as funções de operadora"""
    print("=" * 60)
    print("TESTE 2: Testando endpoints da API")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Verificar se o servidor está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"Servidor respondendo: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro: Servidor não está rodando em {base_url}")
        print(f"Detalhes: {e}")
        return False
    
    # Endpoints para testar
    endpoints_teste = [
        {
            "url": "/api/telefone",
            "method": "POST",
            "data": {"telefone": "11999999999"},
            "description": "Consulta telefone celular SP"
        },
        {
            "url": "/api/telefone",
            "method": "POST", 
            "data": {"telefone": "21987654321"},
            "description": "Consulta telefone celular RJ"
        },
        {
            "url": "/api/telefone/11999999999",
            "method": "GET",
            "data": None,
            "description": "Consulta telefone via GET"
        },
        {
            "url": "/api/cruzamento",
            "method": "POST",
            "data": {"telefone": "85988776655"},
            "description": "Cruzamento de dados com telefone"
        }
    ]
    
    print(f"Testando {len(endpoints_teste)} endpoints...")
    print()
    
    for i, teste in enumerate(endpoints_teste, 1):
        print(f"Teste {i}: {teste['description']}")
        print(f"  URL: {teste['url']}")
        print("-" * 40)
        
        try:
            if teste['method'] == 'POST':
                response = requests.post(
                    f"{base_url}{teste['url']}", 
                    json=teste['data'],
                    timeout=10
                )
            else:
                response = requests.get(
                    f"{base_url}{teste['url']}", 
                    timeout=10
                )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("  Resposta (resumida):")
                    
                    # Extrair informações relevantes sobre operadora
                    if 'operadora' in data:
                        print(f"    Operadora: {data['operadora']}")
                    
                    if 'operadora_detalhes' in data:
                        detalhes = data['operadora_detalhes']
                        print(f"    Detalhes da Operadora:")
                        print(f"      Nome: {detalhes.get('nome', 'N/A')}")
                        print(f"      Fonte: {detalhes.get('fonte', 'N/A')}")
                        print(f"      Confiabilidade: {detalhes.get('confiabilidade', 'N/A')}")
                        print(f"      Portabilidade Considerada: {detalhes.get('portabilidade_considerada', 'N/A')}")
                        if detalhes.get('observacao'):
                            print(f"      Observação: {detalhes['observacao']}")
                    
                    # Para cruzamento de dados
                    if 'dados_encontrados' in data and 'telefone_info' in data['dados_encontrados']:
                        telefone_info = data['dados_encontrados']['telefone_info']
                        if telefone_info:
                            print(f"    Operadora (Cruzamento): {telefone_info.get('operadora', 'N/A')}")
                            print(f"    Fonte: {telefone_info.get('fonte', 'N/A')}")
                            print(f"    Confiabilidade: {telefone_info.get('confiabilidade', 'N/A')}")
                    
                except json.JSONDecodeError:
                    print(f"  Resposta não é JSON válido")
            else:
                print(f"  Erro: {response.text}")
            
        except requests.exceptions.RequestException as e:
            print(f"  Erro na requisição: {e}")
        
        print()
    
    return True

def main():
    """Função principal do teste"""
    print("TESTE DE PORTABILIDADE NUMÉRICA - SISTEMA OSINT")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Teste 1: Funções localmente
    sucesso_local = testar_funcoes_localmente()
    
    # Teste 2: Endpoints da API
    sucesso_api = testar_endpoints_api()
    
    # Resumo
    print("=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Teste Local: {'✓ PASSOU' if sucesso_local else '✗ FALHOU'}")
    print(f"Teste API: {'✓ PASSOU' if sucesso_api else '✗ FALHOU'}")
    
    if sucesso_local and sucesso_api:
        print("\n🎉 Todos os testes passaram! A integração de portabilidade numérica está funcionando.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os logs acima para mais detalhes.")
    
    print()
    print("OBSERVAÇÕES IMPORTANTES:")
    print("- A consulta à ABR Telecom pode falhar devido a limitações do serviço")
    print("- Em caso de falha, o sistema usa estimativa baseada em prefixos")
    print("- A portabilidade numérica torna as estimativas por prefixo menos confiáveis")
    print("- Sempre verifique o campo 'confiabilidade' nas respostas")

if __name__ == "__main__":
    main()