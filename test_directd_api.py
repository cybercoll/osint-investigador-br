#!/usr/bin/env python3
"""
Script para testar diretamente a API Direct Data
"""

import requests
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_direct_data_api():
    """Testa a API Direct Data diretamente"""
    
    # Configurações
    token = os.getenv('DIRECTD_TOKEN', 'B8A26730-37E3-4C74-B92E-26EABC7D1324')
    base_url = "https://apiv3.directd.com.br/api"
    
    # CPF de teste (pode ser um CPF válido para teste)
    cpf_teste = "57919178134"  # CPF usado nos logs
    
    print(f"🔍 Testando API Direct Data")
    print(f"Token: {token}")
    print(f"CPF de teste: {cpf_teste}")
    print("-" * 50)
    
    # Parâmetros da requisição
    params = {
        'CPF': cpf_teste,
        'TOKEN': token
    }
    
    endpoint = f"{base_url}/RegistrationDataBrazil"
    
    try:
        print(f"📡 Fazendo requisição para: {endpoint}")
        print(f"📋 Parâmetros: {params}")
        
        # Tentar primeiro como GET com parâmetros na URL
        response = requests.get(
            endpoint,
            params=params,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Resposta JSON recebida:")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                
                # Analisar a estrutura da resposta
                print("\n🔍 Análise da resposta:")
                
                if 'metaDados' in data:
                    meta = data['metaDados']
                    print(f"  - Resultado ID: {meta.get('resultadoId')}")
                    print(f"  - Mensagem: {meta.get('mensagem')}")
                    print(f"  - Status: {meta.get('status')}")
                
                if 'retorno' in data:
                    retorno = data['retorno']
                    if retorno is None:
                        print("  ⚠️  Campo 'retorno' é None - Nenhum dado encontrado")
                    else:
                        print(f"  ✅ Campo 'retorno' contém dados: {type(retorno)}")
                        if isinstance(retorno, dict):
                            print(f"     Chaves disponíveis: {list(retorno.keys())}")
                        elif isinstance(retorno, list):
                            print(f"     Lista com {len(retorno)} itens")
                else:
                    print("  ❌ Campo 'retorno' não encontrado na resposta")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao decodificar JSON: {e}")
                print(f"📄 Resposta raw: {response.text}")
        else:
            print(f"❌ Erro HTTP {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout na requisição")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    test_direct_data_api()