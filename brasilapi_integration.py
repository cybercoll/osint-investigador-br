"""
Integração com BrasilAPI - API 100% GRATUITA SEM REGISTRO
URL: https://brasilapi.com.br/
Documentação: https://brasilapi.com.br/docs

VANTAGENS:
- Totalmente gratuita
- Sem necessidade de registro
- Sem tokens necessários
- Dados reais brasileiros
- Feita por brasileiros para brasileiros
"""

import requests
import json
from typing import Dict, Any, Optional
import time

class BrasilAPIClient:
    """Cliente para integração com BrasilAPI - 100% gratuita sem registro"""
    
    def __init__(self):
        """Inicializa o cliente da BrasilAPI"""
        self.base_url = "https://brasilapi.com.br/api"
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'OSINT-Investigador-BR/1.0'
        }
        
    def consultar_cep(self, cep: str) -> Dict[str, Any]:
        """
        Consulta dados de CEP na BrasilAPI
        
        Args:
            cep: CEP a ser consultado (com ou sem formatação)
            
        Returns:
            Dict com dados do CEP ou erro
        """
        try:
            # Remove formatação do CEP
            cep_limpo = ''.join(filter(str.isdigit, cep))
            
            if len(cep_limpo) != 8:
                return {
                    'sucesso': False,
                    'erro': 'CEP deve conter 8 dígitos',
                    'cep': cep
                }
            
            # Endpoint para consulta de CEP
            url = f"{self.base_url}/cep/v1/{cep_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'cep': cep_limpo,
                    'dados': {
                        'cep': data.get('cep'),
                        'logradouro': data.get('street'),
                        'bairro': data.get('neighborhood'),
                        'cidade': data.get('city'),
                        'estado': data.get('state'),
                        'coordenadas': {
                            'latitude': data.get('location', {}).get('coordinates', {}).get('latitude'),
                            'longitude': data.get('location', {}).get('coordinates', {}).get('longitude')
                        }
                    },
                    'fonte': 'BrasilAPI (Gratuita)'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'CEP não encontrado',
                    'cep': cep_limpo
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'cep': cep_limpo
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'cep': cep
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'cep': cep
            }
    
    def consultar_cnpj(self, cnpj: str) -> Dict[str, Any]:
        """
        Consulta dados de CNPJ na BrasilAPI
        
        Args:
            cnpj: CNPJ a ser consultado (com ou sem formatação)
            
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
            url = f"{self.base_url}/cnpj/v1/{cnpj_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'cnpj': cnpj_limpo,
                    'dados': {
                        'razao_social': data.get('company_name'),
                        'nome_fantasia': data.get('trade_name'),
                        'cnpj': data.get('tax_id'),
                        'situacao': data.get('registration_status'),
                        'endereco': {
                            'logradouro': data.get('address', {}).get('street'),
                            'numero': data.get('address', {}).get('number'),
                            'bairro': data.get('address', {}).get('neighborhood'),
                            'cidade': data.get('address', {}).get('city'),
                            'estado': data.get('address', {}).get('state'),
                            'cep': data.get('address', {}).get('zip_code')
                        },
                        'telefone': data.get('phone'),
                        'email': data.get('email'),
                        'atividade_principal': data.get('main_activity', {}).get('text'),
                        'data_abertura': data.get('founded_date'),
                        'capital_social': data.get('equity_capital')
                    },
                    'fonte': 'BrasilAPI (Gratuita)'
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
    
    def consultar_ddd(self, ddd: str) -> Dict[str, Any]:
        """
        Consulta informações de DDD na BrasilAPI
        
        Args:
            ddd: Código DDD a ser consultado
            
        Returns:
            Dict com dados do DDD ou erro
        """
        try:
            # Remove formatação do DDD
            ddd_limpo = ''.join(filter(str.isdigit, ddd))
            
            if len(ddd_limpo) != 2:
                return {
                    'sucesso': False,
                    'erro': 'DDD deve conter 2 dígitos',
                    'ddd': ddd
                }
            
            # Endpoint para consulta de DDD
            url = f"{self.base_url}/ddd/v1/{ddd_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'ddd': ddd_limpo,
                    'dados': {
                        'estado': data.get('state'),
                        'cidades': data.get('cities', [])
                    },
                    'fonte': 'BrasilAPI (Gratuita)'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'DDD não encontrado',
                    'ddd': ddd_limpo
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'ddd': ddd_limpo
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'ddd': ddd
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'ddd': ddd
            }
    
    def consultar_banco(self, codigo: str) -> Dict[str, Any]:
        """
        Consulta informações de banco pelo código
        
        Args:
            codigo: Código do banco (3 dígitos)
            
        Returns:
            Dict com dados do banco ou erro
        """
        try:
            # Remove formatação do código
            codigo_limpo = ''.join(filter(str.isdigit, codigo))
            
            if len(codigo_limpo) != 3:
                return {
                    'sucesso': False,
                    'erro': 'Código do banco deve conter 3 dígitos',
                    'codigo': codigo
                }
            
            # Endpoint para consulta de banco
            url = f"{self.base_url}/banks/v1/{codigo_limpo}"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'codigo': codigo_limpo,
                    'dados': {
                        'nome': data.get('name'),
                        'codigo': data.get('code'),
                        'nome_completo': data.get('fullName')
                    },
                    'fonte': 'BrasilAPI (Gratuita)'
                }
            elif response.status_code == 404:
                return {
                    'sucesso': False,
                    'erro': 'Banco não encontrado',
                    'codigo': codigo_limpo
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}',
                    'codigo': codigo_limpo
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta',
                'codigo': codigo
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}',
                'codigo': codigo
            }
    
    def listar_bancos(self) -> Dict[str, Any]:
        """
        Lista todos os bancos disponíveis
        
        Returns:
            Dict com lista de bancos ou erro
        """
        try:
            # Endpoint para listar bancos
            url = f"{self.base_url}/banks/v1"
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'sucesso': True,
                    'dados': data,
                    'total': len(data),
                    'fonte': 'BrasilAPI (Gratuita)'
                }
            else:
                return {
                    'sucesso': False,
                    'erro': f'Erro na API: {response.status_code}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'sucesso': False,
                'erro': 'Timeout na consulta'
            }
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro inesperado: {str(e)}'
            }
    
    def testar_conectividade(self) -> Dict[str, Any]:
        """
        Testa a conectividade com a BrasilAPI
        
        Returns:
            Dict com resultado do teste
        """
        try:
            # Testa com um CEP conhecido (Palácio do Planalto)
            resultado_cep = self.consultar_cep('70150900')
            
            if resultado_cep['sucesso']:
                return {
                    'sucesso': True,
                    'mensagem': 'Conectividade com BrasilAPI OK',
                    'teste_realizado': 'Consulta CEP 70150-900 (Palácio do Planalto)',
                    'dados_teste': resultado_cep['dados']
                }
            else:
                return {
                    'sucesso': False,
                    'erro': 'Falha no teste de conectividade',
                    'detalhes': resultado_cep['erro']
                }
                
        except Exception as e:
            return {
                'sucesso': False,
                'erro': f'Erro no teste: {str(e)}'
            }

# Função de conveniência para uso direto
def consultar_dados_brasilapi(tipo: str, valor: str) -> Dict[str, Any]:
    """
    Função de conveniência para consultar dados na BrasilAPI
    
    Args:
        tipo: Tipo de consulta ('cep', 'cnpj', 'ddd', 'banco')
        valor: Valor a ser consultado
        
    Returns:
        Dict com resultado da consulta
    """
    client = BrasilAPIClient()
    
    if tipo.lower() == 'cep':
        return client.consultar_cep(valor)
    elif tipo.lower() == 'cnpj':
        return client.consultar_cnpj(valor)
    elif tipo.lower() == 'ddd':
        return client.consultar_ddd(valor)
    elif tipo.lower() == 'banco':
        return client.consultar_banco(valor)
    else:
        return {
            'sucesso': False,
            'erro': f'Tipo de consulta não suportado: {tipo}',
            'tipos_suportados': ['cep', 'cnpj', 'ddd', 'banco']
        }

# Validador de CPF gratuito (sem API externa)
def validar_cpf(cpf: str) -> Dict[str, Any]:
    """
    Valida CPF usando algoritmo oficial (sem API externa)
    
    Args:
        cpf: CPF a ser validado
        
    Returns:
        Dict com resultado da validação
    """
    try:
        # Remove formatação
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf_limpo) != 11:
            return {
                'sucesso': False,
                'valido': False,
                'erro': 'CPF deve conter 11 dígitos',
                'cpf': cpf
            }
        
        # Verifica se todos os dígitos são iguais
        if cpf_limpo == cpf_limpo[0] * 11:
            return {
                'sucesso': True,
                'valido': False,
                'erro': 'CPF com todos os dígitos iguais é inválido',
                'cpf': cpf_limpo
            }
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcula segundo dígito verificador
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verifica se os dígitos calculados conferem
        valido = (int(cpf_limpo[9]) == digito1 and int(cpf_limpo[10]) == digito2)
        
        return {
            'sucesso': True,
            'valido': valido,
            'cpf': cpf_limpo,
            'cpf_formatado': f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}',
            'fonte': 'Validação Local (Gratuita)'
        }
        
    except Exception as e:
        return {
            'sucesso': False,
            'erro': f'Erro na validação: {str(e)}',
            'cpf': cpf
        }

if __name__ == "__main__":
    # Demonstração das funcionalidades
    print("🇧🇷 DEMONSTRAÇÃO BRASILAPI - 100% GRATUITA SEM REGISTRO")
    print("=" * 60)
    
    client = BrasilAPIClient()
    
    # Teste de conectividade
    print("\n1. TESTE DE CONECTIVIDADE:")
    resultado = client.testar_conectividade()
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # Teste CEP
    print("\n2. CONSULTA CEP (01310-100 - Av. Paulista):")
    resultado = client.consultar_cep("01310100")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # Teste DDD
    print("\n3. CONSULTA DDD (11 - São Paulo):")
    resultado = client.consultar_ddd("11")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    # Teste validação CPF
    print("\n4. VALIDAÇÃO CPF (11144477735):")
    resultado = validar_cpf("11144477735")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))