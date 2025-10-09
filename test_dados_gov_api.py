#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import time

def test_dados_gov_api():
    """Testa a API do Portal de Dados Abertos (versão legada)"""
    
    print("=== TESTE DA API DO PORTAL DE DADOS ABERTOS (LEGADO) ===")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    # Usar o endpoint legado que ainda funciona
    base_url = 'https://legado.dados.gov.br/api/3'
    
    # Teste 1: Status da API
    print("1. Verificando status da API legada...")
    try:
        response = requests.get(f'{base_url}/action/status_show', headers=headers, timeout=10)
        print(f"   Status HTTP: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                success = data.get('success', False)
                print(f"   API funcionando: {success}")
                
                if success:
                    result = data.get('result', {})
                    print(f"   Versão CKAN: {result.get('ckan_version', 'N/A')}")
            except json.JSONDecodeError:
                print("   Erro: Resposta não é JSON válido")
        else:
            print(f"   Erro HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   Erro: {e}")
    
    print()
    
    # Teste 2: Buscar organização ANATEL
    print("2. Buscando organização ANATEL...")
    try:
        response = requests.get(f'{base_url}/action/organization_show?id=agencia-nacional-de-telecomunicacoes-anatel', 
                              headers=headers, timeout=10)
        print(f"   Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print(f"   Sucesso: {success}")
            
            if success:
                result = data.get('result', {})
                print(f"   Nome da organização: {result.get('display_name', 'N/A')}")
                print(f"   Número de datasets: {result.get('package_count', 0)}")
        else:
            print(f"   Erro HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   Erro: {e}")
    
    print()
    
    # Teste 3: Buscar datasets da ANATEL
    print("3. Buscando datasets da ANATEL...")
    try:
        params = {
            'q': 'organization:agencia-nacional-de-telecomunicacoes-anatel',
            'rows': 20,
            'start': 0
        }
        
        response = requests.get(f'{base_url}/action/package_search', 
                              params=params, headers=headers, timeout=15)
        print(f"   Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print(f"   Sucesso: {success}")
            
            if success:
                result = data.get('result', {})
                count = result.get('count', 0)
                print(f"   Total de datasets encontrados: {count}")
                
                datasets = result.get('results', [])
                print(f"   Datasets retornados nesta consulta: {len(datasets)}")
                
                if datasets:
                    print("   Primeiros 5 datasets:")
                    for i, dataset in enumerate(datasets[:5]):
                        print(f"     {i+1}. {dataset.get('title', 'Sem título')} (ID: {dataset.get('name', 'N/A')})")
        else:
            print(f"   Erro HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   Erro: {e}")
    
    print()
    
    # Teste 4: Buscar especificamente por portabilidade numérica
    print("4. Buscando datasets de portabilidade numérica...")
    try:
        params = {
            'q': 'portabilidade OR "portabilidade numérica" OR "ABR Telecom"',
            'rows': 10,
            'start': 0
        }
        
        response = requests.get(f'{base_url}/action/package_search', 
                              params=params, headers=headers, timeout=15)
        print(f"   Status HTTP: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            print(f"   Sucesso: {success}")
            
            if success:
                result = data.get('result', {})
                count = result.get('count', 0)
                print(f"   Total de datasets encontrados: {count}")
                
                datasets = result.get('results', [])
                if datasets:
                    print("   Datasets encontrados:")
                    for i, dataset in enumerate(datasets):
                        title = dataset.get('title', 'Sem título')
                        name = dataset.get('name', 'N/A')
                        org = dataset.get('organization', {}).get('title', 'N/A')
                        print(f"     {i+1}. {title}")
                        print(f"        ID: {name}")
                        print(f"        Organização: {org}")
                        
                        # Verificar recursos disponíveis
                        resources = dataset.get('resources', [])
                        if resources:
                            print(f"        Recursos ({len(resources)}):")
                            for j, resource in enumerate(resources[:3]):  # Mostrar apenas os 3 primeiros
                                res_name = resource.get('name', 'Sem nome')
                                res_format = resource.get('format', 'N/A')
                                res_url = resource.get('url', 'N/A')
                                print(f"          {j+1}. {res_name} ({res_format})")
                                print(f"             URL: {res_url}")
                        print()
                else:
                    print("   Nenhum dataset encontrado com os termos de busca.")
        else:
            print(f"   Erro HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"   Erro: {e}")

if __name__ == "__main__":
    test_dados_gov_api()