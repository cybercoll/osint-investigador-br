#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a API do Portal Legado de Dados Abertos
Focando em datasets da ANATEL e portabilidade numérica
"""

import requests
import json
import time

def test_legado_api():
    """Testa diferentes endpoints do Portal Legado de Dados Abertos"""
    
    # URLs base para testar
    base_urls = [
        "https://legado.dados.gov.br",
        "http://legado.dados.gov.br"
    ]
    
    # Endpoints para testar
    endpoints = [
        "/api/3/action/organization_list",
        "/api/3/action/package_search?q=anatel",
        "/api/3/action/package_search?q=portabilidade",
        "/api/3/action/package_search?fq=organization:anatel",
        "/dataset?organization=agencia-nacional-de-telecomunicacoes-anatel",
        "/api/action/organization_show?id=anatel",
        "/api/action/package_list"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
    }
    
    print("=== TESTE DA API DO PORTAL LEGADO DE DADOS ABERTOS ===\n")
    
    for base_url in base_urls:
        print(f"Testando base URL: {base_url}")
        print("-" * 50)
        
        for endpoint in endpoints:
            full_url = base_url + endpoint
            print(f"\nTestando: {full_url}")
            
            try:
                response = requests.get(full_url, headers=headers, timeout=10)
                print(f"Status HTTP: {response.status_code}")
                print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                print(f"Tamanho da resposta: {len(response.text)} caracteres")
                
                # Verifica se é JSON válido
                if 'application/json' in response.headers.get('Content-Type', ''):
                    try:
                        data = response.json()
                        print("✓ Resposta JSON válida")
                        
                        # Se for uma resposta da API CKAN, verifica o sucesso
                        if isinstance(data, dict) and 'success' in data:
                            print(f"API Success: {data.get('success')}")
                            if data.get('success') and 'result' in data:
                                result = data['result']
                                if isinstance(result, list):
                                    print(f"Número de itens retornados: {len(result)}")
                                    if len(result) > 0:
                                        print(f"Primeiro item: {str(result[0])[:100]}...")
                                elif isinstance(result, dict):
                                    print(f"Resultado (dict): {str(result)[:200]}...")
                        else:
                            print(f"Estrutura da resposta: {str(data)[:200]}...")
                            
                    except json.JSONDecodeError as e:
                        print(f"✗ Erro ao decodificar JSON: {e}")
                        print(f"Primeiros 200 caracteres: {response.text[:200]}")
                else:
                    print("✗ Resposta não é JSON")
                    if response.text.strip().startswith('<'):
                        print("Resposta parece ser HTML")
                    print(f"Primeiros 200 caracteres: {response.text[:200]}")
                    
            except requests.exceptions.RequestException as e:
                print(f"✗ Erro na requisição: {e}")
            
            time.sleep(1)  # Pausa entre requisições
        
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    test_legado_api()