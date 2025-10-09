#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

def test_api_routes():
    """Testa as rotas da API usando requests do Python"""
    base_url = "http://localhost:5000"
    
    routes_to_test = [
        "/",
        "/api",
        "/api/telefone/61981437533",
        "/api/cep/01310100",
        "/api/status"
    ]
    
    print("=== TESTE DAS ROTAS COM PYTHON REQUESTS ===")
    
    for route in routes_to_test:
        url = base_url + route
        try:
            print(f"\nTestando: {url}")
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"JSON Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"Text Response: {response.text[:200]}...")
            else:
                print(f"Error Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
        
        print("-" * 60)

def test_post_routes():
    """Testa rotas POST"""
    base_url = "http://localhost:5000"
    
    print("\n=== TESTE DAS ROTAS POST ===")
    
    # Teste da rota de telefone POST
    url = base_url + "/api/consultar/telefone"
    data = {"telefone": "61981437533"}
    
    try:
        print(f"\nTestando POST: {url}")
        print(f"Data: {data}")
        response = requests.post(url, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")

if __name__ == '__main__':
    test_api_routes()
    test_post_routes()