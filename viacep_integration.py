#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integração com ViaCEP - API Gratuita para Consulta de CEP
Totalmente gratuita, sem necessidade de registro ou token
"""

import requests
import json
from typing import Dict, Any, Optional

class ViaCEPClient:
    """Cliente para integração com ViaCEP"""
    
    def __init__(self):
        self.base_url = "https://viacep.com.br/ws"
        self.timeout = 10
    
    def consultar_cep(self, cep: str) -> Dict[str, Any]:
        """
        Consulta informações de um CEP
        
        Args:
            cep (str): CEP para consulta (com ou sem formatação)
            
        Returns:
            Dict com informações do CEP
        """
        try:
            # Remove formatação do CEP
            cep_limpo = ''.join(filter(str.isdigit, cep))
            
            if len(cep_limpo) != 8:
                return {
                    "sucesso": False,
                    "erro": "CEP deve conter 8 dígitos",
                    "fonte": "ViaCEP (Gratuita)"
                }
            
            url = f"{self.base_url}/{cep_limpo}/json/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verifica se o CEP existe
                if 'erro' in data:
                    return {
                        "sucesso": False,
                        "erro": "CEP não encontrado",
                        "cep": cep_limpo,
                        "fonte": "ViaCEP (Gratuita)"
                    }
                
                return {
                    "sucesso": True,
                    "cep": cep_limpo,
                    "cep_formatado": f"{cep_limpo[:5]}-{cep_limpo[5:]}",
                    "dados": {
                        "logradouro": data.get("logradouro", ""),
                        "complemento": data.get("complemento", ""),
                        "bairro": data.get("bairro", ""),
                        "localidade": data.get("localidade", ""),
                        "uf": data.get("uf", ""),
                        "ibge": data.get("ibge", ""),
                        "gia": data.get("gia", ""),
                        "ddd": data.get("ddd", ""),
                        "siafi": data.get("siafi", "")
                    },
                    "fonte": "ViaCEP (Gratuita)"
                }
            else:
                return {
                    "sucesso": False,
                    "erro": f"Erro na API: {response.status_code}",
                    "fonte": "ViaCEP (Gratuita)"
                }
                
        except requests.exceptions.Timeout:
            return {
                "sucesso": False,
                "erro": "Timeout na consulta",
                "fonte": "ViaCEP (Gratuita)"
            }
        except requests.exceptions.RequestException as e:
            return {
                "sucesso": False,
                "erro": f"Erro de conexão: {str(e)}",
                "fonte": "ViaCEP (Gratuita)"
            }
        except Exception as e:
            return {
                "sucesso": False,
                "erro": f"Erro inesperado: {str(e)}",
                "fonte": "ViaCEP (Gratuita)"
            }
    
    def buscar_endereco(self, uf: str, cidade: str, logradouro: str) -> Dict[str, Any]:
        """
        Busca CEPs por endereço
        
        Args:
            uf (str): Estado (2 letras)
            cidade (str): Nome da cidade
            logradouro (str): Nome da rua/logradouro
            
        Returns:
            Dict com lista de CEPs encontrados
        """
        try:
            if len(uf) != 2 or len(cidade) < 3 or len(logradouro) < 3:
                return {
                    "sucesso": False,
                    "erro": "UF deve ter 2 letras, cidade e logradouro pelo menos 3 caracteres",
                    "fonte": "ViaCEP (Gratuita)"
                }
            
            url = f"{self.base_url}/{uf}/{cidade}/{logradouro}/json/"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    return {
                        "sucesso": True,
                        "total_encontrados": len(data),
                        "enderecos": data,
                        "fonte": "ViaCEP (Gratuita)"
                    }
                else:
                    return {
                        "sucesso": False,
                        "erro": "Nenhum endereço encontrado",
                        "fonte": "ViaCEP (Gratuita)"
                    }
            else:
                return {
                    "sucesso": False,
                    "erro": f"Erro na API: {response.status_code}",
                    "fonte": "ViaCEP (Gratuita)"
                }
                
        except Exception as e:
            return {
                "sucesso": False,
                "erro": f"Erro: {str(e)}",
                "fonte": "ViaCEP (Gratuita)"
            }
    
    def testar_conectividade(self) -> Dict[str, Any]:
        """Testa conectividade com ViaCEP"""
        return self.consultar_cep("01310-100")  # CEP da Av. Paulista, SP

def consultar_cep_viacep(cep: str) -> Dict[str, Any]:
    """
    Função de conveniência para consultar CEP
    
    Args:
        cep (str): CEP para consulta
        
    Returns:
        Dict com informações do CEP
    """
    client = ViaCEPClient()
    return client.consultar_cep(cep)

def main():
    """Demonstração da integração ViaCEP"""
    print("=== DEMONSTRAÇÃO VIACEP - API GRATUITA ===\n")
    
    client = ViaCEPClient()
    
    # Teste de conectividade
    print("1. TESTE DE CONECTIVIDADE:")
    resultado = client.testar_conectividade()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    
    # Consulta CEP específico
    print("2. CONSULTA CEP (01310-100 - Av. Paulista):")
    resultado = client.consultar_cep("01310-100")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    
    # Consulta outro CEP
    print("3. CONSULTA CEP (20040-020 - Centro RJ):")
    resultado = client.consultar_cep("20040020")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    
    # Busca por endereço
    print("4. BUSCA POR ENDEREÇO (SP/São Paulo/Paulista):")
    resultado = client.buscar_endereco("SP", "São Paulo", "Paulista")
    if resultado["sucesso"] and len(resultado["enderecos"]) > 0:
        # Mostra apenas os primeiros 3 resultados
        resultado_limitado = resultado.copy()
        resultado_limitado["enderecos"] = resultado["enderecos"][:3]
        resultado_limitado["observacao"] = f"Mostrando 3 de {len(resultado['enderecos'])} resultados"
        print(json.dumps(resultado_limitado, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    print()
    
    # CEP inválido
    print("5. TESTE CEP INVÁLIDO:")
    resultado = client.consultar_cep("00000-000")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()