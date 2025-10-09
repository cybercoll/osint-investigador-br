#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

def test_api_endpoints():
    """Testa diferentes endpoints da API do Portal de Dados Abertos"""
    
    print("=== TESTE DE ENDPOINTS DA API DO PORTAL DE DADOS ABERTOS ===")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    # Testar diferentes endpoints possíveis
    endpoints = [
        'https://dados.gov.br/api/datasets',
        'https://dados.gov.br/api/v1/datasets',
        'https://dados.gov.br/api/3/action/package_list',
        'https://dados.gov.br/dados/api/datasets',
        'https://api.dados.gov.br/datasets',
        'https://dados.gov.br/api/organizations',
        'https://dados.gov.br/api/search'
    ]
    
    for i, endpoint in enumerate(endpoints, 1):
        try:
            print(f'{i}. Testando: {endpoint}')
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f'   Status: {response.status_code}')
            
            content_type = response.headers.get('Content-Type', 'N/A')
            print(f'   Content-Type: {content_type}')
            print(f'   Tamanho: {len(response.text)} chars')
            
            if response.status_code == 200:
                if 'json' in content_type.lower():
                    try:
                        data = response.json()
                        print(f'   JSON válido: Sim')
                        if isinstance(data, dict):
                            keys = list(data.keys())[:5]
                            print(f'   Chaves: {keys}')
                        elif isinstance(data, list):
                            print(f'   Lista com {len(data)} itens')
                    except Exception as je:
                        print(f'   JSON válido: Não - {je}')
                else:
                    first_chars = repr(response.text[:100])
                    print(f'   Primeiros 100 chars: {first_chars}')
            elif response.status_code == 404:
                print('   Endpoint não encontrado')
            elif response.status_code == 403:
                print('   Acesso negado')
            else:
                print(f'   Erro HTTP: {response.status_code}')
                
            print()
            
        except Exception as e:
            print(f'   Erro: {e}')
            print()

if __name__ == "__main__":
    test_api_endpoints()