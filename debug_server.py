#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.index import app

def debug_routes():
    """Debug das rotas registradas no Flask"""
    print("=== DEBUG DAS ROTAS ===")
    print(f"Flask app: {app}")
    print(f"URL Map: {app.url_map}")
    print("\nRotas registradas:")
    
    for rule in app.url_map.iter_rules():
        if not rule.rule.startswith('/static'):
            print(f"  {rule.rule} -> {rule.endpoint} (methods: {rule.methods})")
    
    print("\n=== TESTE DE ROTAS ===")
    
    # Teste com test_client
    with app.test_client() as client:
        print("\n1. Testando rota raiz '/':")
        response = client.get('/')
        print(f"   Status: {response.status_code}")
        
        print("\n2. Testando rota '/api':")
        response = client.get('/api')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.get_json()}")
        else:
            print(f"   Error: {response.get_data(as_text=True)}")
        
        print("\n3. Testando rota '/api/telefone/61981437533':")
        response = client.get('/api/telefone/61981437533')
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.get_json()}")
        else:
            print(f"   Error: {response.get_data(as_text=True)}")

def start_debug_server():
    """Inicia o servidor com debug detalhado"""
    print("\n=== INICIANDO SERVIDOR DEBUG ===")
    
    # Configurar Flask para debug máximo
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    
    print("Servidor iniciando em http://localhost:5000")
    print("Pressione Ctrl+C para parar")
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\nServidor parado pelo usuário")

if __name__ == '__main__':
    debug_routes()
    
    print("\n" + "="*50)
    resposta = input("Deseja iniciar o servidor debug? (s/n): ")
    if resposta.lower() in ['s', 'sim', 'y', 'yes']:
        start_debug_server()