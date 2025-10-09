#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar o serviço Consulta Número da ABR Telecom
Verificando possibilidades de integração para dados de portabilidade numérica
"""

import requests
import json
import time
from urllib.parse import urljoin

def test_abr_telecom_service():
    """Testa o serviço Consulta Número da ABR Telecom"""
    
    base_url = "https://consultanumero.abrtelecom.com.br"
    
    # URLs para testar
    test_urls = [
        "/",
        "/consultanumero/consulta/consultaHistoricoRecenteCtg",
        "/api",
        "/api/consulta",
        "/consultanumero/api",
        "/consultanumero/consulta/consultaSituacaoAtual",
        "/consultanumero/consulta/consultaHistoricoRecente"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    print("=== TESTE DO SERVIÇO CONSULTA NÚMERO - ABR TELECOM ===\n")
    
    for endpoint in test_urls:
        full_url = urljoin(base_url, endpoint)
        print(f"Testando: {full_url}")
        
        try:
            response = requests.get(full_url, headers=headers, timeout=15, allow_redirects=True)
            print(f"Status HTTP: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            print(f"Tamanho da resposta: {len(response.text)} caracteres")
            
            # Verifica se há redirecionamentos
            if response.history:
                print(f"Redirecionamentos: {len(response.history)}")
                for i, resp in enumerate(response.history):
                    print(f"  {i+1}. {resp.status_code} -> {resp.url}")
                print(f"URL final: {response.url}")
            
            # Analisa o conteúdo da resposta
            content_type = response.headers.get('Content-Type', '').lower()
            
            if 'application/json' in content_type:
                try:
                    data = response.json()
                    print("✓ Resposta JSON válida")
                    print(f"Estrutura: {str(data)[:300]}...")
                except json.JSONDecodeError as e:
                    print(f"✗ Erro ao decodificar JSON: {e}")
            
            elif 'text/html' in content_type:
                print("Resposta HTML detectada")
                # Procura por formulários ou APIs mencionadas no HTML
                html_content = response.text.lower()
                
                if 'api' in html_content:
                    print("✓ Menção a 'API' encontrada no HTML")
                
                if 'consulta' in html_content:
                    print("✓ Funcionalidade de 'consulta' encontrada")
                
                if 'form' in html_content:
                    print("✓ Formulário encontrado no HTML")
                
                # Procura por endpoints ou URLs de API
                if '/api/' in html_content:
                    print("✓ Possível endpoint de API encontrado")
                
                # Verifica se há JavaScript que pode indicar chamadas AJAX
                if 'ajax' in html_content or 'fetch' in html_content or 'xmlhttprequest' in html_content:
                    print("✓ Possíveis chamadas AJAX/API detectadas")
            
            else:
                print(f"Tipo de conteúdo: {content_type}")
            
            # Mostra uma amostra do conteúdo
            print(f"Amostra do conteúdo (primeiros 200 chars):")
            print(f"{response.text[:200]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro na requisição: {e}")
        
        print("-" * 60)
        time.sleep(2)  # Pausa entre requisições para ser respeitoso

def test_consulta_numero_form():
    """Testa se é possível fazer uma consulta programática"""
    
    print("\n=== TESTE DE CONSULTA PROGRAMÁTICA ===\n")
    
    # URL do serviço de consulta
    consulta_url = "https://consultanumero.abrtelecom.com.br/consultanumero/consulta/consultaSituacaoAtual"
    
    # Número de teste (formato genérico)
    test_number = "11999999999"  # Número fictício para teste
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # Dados do formulário (baseado na análise do site)
    form_data = {
        'numeroTelefone': test_number,
        'codigoAcesso': test_number
    }
    
    print(f"Tentando consulta para número: {test_number}")
    
    try:
        # Primeiro, faz GET para obter possíveis tokens CSRF
        get_response = requests.get(consulta_url, headers=headers, timeout=10)
        print(f"GET Status: {get_response.status_code}")
        
        # Depois tenta POST com os dados
        post_response = requests.post(consulta_url, data=form_data, headers=headers, timeout=10)
        print(f"POST Status: {post_response.status_code}")
        print(f"POST Content-Type: {post_response.headers.get('Content-Type', 'N/A')}")
        print(f"POST Response: {post_response.text[:300]}...")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Erro na consulta: {e}")

if __name__ == "__main__":
    test_abr_telecom_service()
    test_consulta_numero_form()