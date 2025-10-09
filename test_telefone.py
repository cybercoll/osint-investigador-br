#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api.index import app

def test_telefone_route():
    """Testa a rota de telefone"""
    with app.test_client() as client:
        # Teste da rota GET
        response = client.get('/api/telefone/61981437533')
        print(f"GET /api/telefone/61981437533")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)}")
        print("-" * 50)
        
        # Teste da rota POST
        response = client.post('/api/consultar/telefone', 
                             json={'telefone': '61981437533'},
                             content_type='application/json')
        print(f"POST /api/consultar/telefone")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)}")
        print("-" * 50)
        
        # Teste da rota /api
        response = client.get('/api')
        print(f"GET /api")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_data(as_text=True)}")

if __name__ == '__main__':
    test_telefone_route()