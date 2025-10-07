"""
Integração com API Brasil - Serviços gratuitos para dados brasileiros
URL: https://apibrasil.com.br/
Documentação: https://apibrasil.com.br/docs
"""

import requests
import json
import os
from typing import Dict, Any, Optional
import time

class APIBrasilClient:
    """Cliente para integração com API Brasil - Mais de 50 serviços gratuitos"""
    
    def __init__(self, token: Optional[str] = None):
        """
        Inicializa o cliente da API Brasil
        
        Args:
            token: Token de acesso da API Brasil
        """
        self.token = token or os.getenv('API_BRASIL_TOKEN')
        self.base_url = "https://apibrasil.com.br/api"
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
    def consultar_cpf(self, cpf: str) -> Dict[str, Any]:
        """
        Consulta dados de CPF na API Brasil
        
        Args:
            cpf: Número do CPF (apenas números)
            
        Returns:
            Dict com dados do CPF ou erro
        """
        try:
            # Remove formatação do CPF
            cpf_limpo = ''.join(filter(str.isdigit, cpf))
            
            if len(cpf_limpo) != 11:
                return {
                    'sucesso': False,
                    'erro': 'CPF deve conter 11 dígitos',
                    'cpf': cpf
                }
            
            # Endpoint para consulta de CPF
            url = f"{self.base_url}/cpf/{cpf_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'cpf': cpf_limpo,
                    'dados': data,
                    'fonte': 'API Brasil'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'CPF não encontrado',
                    'cpf': cpf_limpo
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'cpf': cpf_limpo
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'cpf': cpf
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'cpf': cpf
            }
    
    def consultar_cnpj(self, cnpj: str) -> Dict[str, Any]:
        """
        Consulta dados de CNPJ na API Brasil
        
        Args:
            cnpj: Número do CNPJ (apenas números)
            
        Returns:
            Dict com dados do CNPJ ou erro
        """
        try:
            # Remove formatação do CNPJ
            cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
            
            if len(cnpj_limpo) != 14:
                return {
                    'sucesso': False,
                    'erro': 'CNPJ deve conter 14 dígitos',
                    'cnpj': cnpj
                }
            
            # Endpoint para consulta de CNPJ
            url = f"{self.base_url}/cnpj/{cnpj_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'cnpj': cnpj_limpo,
                    'dados': data,
                    'fonte': 'API Brasil'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'CNPJ não encontrado',
                    'cnpj': cnpj_limpo
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'cnpj': cnpj_limpo
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'cnpj': cnpj
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'cnpj': cnpj
            }
    
    def consultar_telefone(self, telefone: str) -> Dict[str, Any]:
        """
        Consulta dados de telefone na API Brasil
        
        Args:
            telefone: Número do telefone
            
        Returns:
            Dict com dados do telefone ou erro
        """
        try:
            # Remove formatação do telefone
            telefone_limpo = ''.join(filter(str.isdigit, telefone))
            
            # Endpoint para consulta de telefone
            url = f"{self.base_url}/telefone/{telefone_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'telefone': telefone_limpo,
                    'dados': data,
                    'fonte': 'API Brasil'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'Telefone não encontrado',
                    'telefone': telefone_limpo
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'telefone': telefone_limpo
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'telefone': telefone
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'telefone': telefone
            }
    
    def consultar_veiculo(self, placa: str) -> Dict[str, Any]:
        """
        Consulta dados de veículo pela placa na API Brasil
        
        Args:
            placa: Placa do veículo
            
        Returns:
            Dict com dados do veículo ou erro
        """
        try:
            # Remove espaços e converte para maiúsculo
            placa_limpa = placa.replace(' ', '').replace('-', '').upper()
            
            # Endpoint para consulta de veículo
            url = f"{self.base_url}/veiculo/{placa_limpa}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'placa': placa_limpa,
                    'dados': data,
                    'fonte': 'API Brasil'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'Veículo não encontrado',
                    'placa': placa_limpa
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'placa': placa_limpa
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'placa': placa
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'placa': placa
            }
    
    def testar_conectividade(self) -> Dict[str, Any]:
        """
        Testa a conectividade com a API Brasil
        
        Returns:
            Dict com resultado do teste
        """
        try:
            if not self.token:
                return {
                    'sucesso': False,
                    'erro': 'Token não configurado',
                    'instrucoes': 'Configure API_BRASIL_TOKEN no arquivo .env'
                }
            
            # Testa com um CPF de exemplo (formato válido mas fictício)
            url = f"{self.base_url}/status"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return {
                    'sucesso': True,
                    'mensagem': 'Conectividade com API Brasil OK',
                    'status': response.json() if response.content else 'API ativa'
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro de conectividade: {response.status_code}',
                    'detalhes': response.text if response.content else 'Sem detalhes'
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na conexão com API Brasil'
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}'
            }

# Função de conveniência para uso direto
def consultar_dados_api_brasil(tipo: str, valor: str, token: Optional[str] = None) -> Dict[str, Any]:
    """
    Função de conveniência para consultar dados na API Brasil
    
    Args:
        tipo: Tipo de consulta ('cpf', 'cnpj', 'telefone', 'veiculo')
        valor: Valor a ser consultado
        token: Token da API (opcional, usa .env se não fornecido)
        
    Returns:
        Dict com resultado da consulta
    """
    client = APIBrasilClient(token)
    
    if tipo.lower() == 'cpf':
        return client.consultar_cpf(valor)
    elif tipo.lower() == 'cnpj':
        return client.consultar_cnpj(valor)
    elif tipo.lower() == 'telefone':
        return client.consultar_telefone(valor)
    elif tipo.lower() == 'veiculo':
        return client.consultar_veiculo(valor)
    else:
        return {
            'sucesso': False,
            'erro': f'Tipo de consulta não suportado: {tipo}',
            'tipos_suportados': ['cpf', 'cnpj', 'telefone', 'veiculo']
        }

if __name__ == "__main__":
    # Teste básico
    client = APIBrasilClient()
    resultado = client.testar_conectividade()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))