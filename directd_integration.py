"""
Integração com Direct Data API v3
Sistema completo para consultas de dados pessoais no Brasil
"""

import os
import requests
import time
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

from utils.logger import log_consulta
from utils.cache import cache

class DirectDataClient:
    """Cliente para integração com Direct Data API v3"""
    
    def __init__(self):
        self.base_url = "https://apiv3.directd.com.br/api"
        self.token = os.getenv('DIRECTD_TOKEN', '')
        self.timeout = 30
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Faz requisição para a API Direct Data"""
        try:
            # Adicionar token aos parâmetros
            params['TOKEN'] = self.token
            
            url = f"{self.base_url}/{endpoint}"
            
            # Log da consulta
            log_consulta(f"Direct Data - {endpoint}", str(params), "INICIANDO")
            
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Verificar se a consulta foi autorizada
            if data.get('metaDados', {}).get('resultadoId') == 3:
                log_consulta(f"Direct Data - {endpoint}", str(params), "ERRO", 
                           data.get('metaDados', {}).get('mensagem', 'Token inválido'))
                return {
                    'success': False,
                    'error': 'Token inválido ou não autorizado',
                    'message': data.get('metaDados', {}).get('mensagem', '')
                }
            
            # Verificar se há dados de retorno
            if data.get('retorno') is None:
                log_consulta(f"Direct Data - {endpoint}", str(params), "SEM_DADOS")
                return {
                    'success': False,
                    'error': 'Nenhum dado encontrado',
                    'message': 'Consulta realizada mas sem dados disponíveis'
                }
            
            log_consulta(f"Direct Data - {endpoint}", str(params), "SUCESSO")
            
            return {
                'success': True,
                'data': data['retorno'],
                'metadata': data['metaDados']
            }
            
        except requests.exceptions.Timeout:
            log_consulta(f"Direct Data - {endpoint}", str(params), "ERRO", "Timeout")
            return {'success': False, 'error': 'Timeout na consulta'}
            
        except requests.exceptions.RequestException as e:
            log_consulta(f"Direct Data - {endpoint}", str(params), "ERRO", str(e))
            return {'success': False, 'error': f'Erro na requisição: {str(e)}'}
            
        except json.JSONDecodeError:
            log_consulta(f"Direct Data - {endpoint}", str(params), "ERRO", "JSON inválido")
            return {'success': False, 'error': 'Resposta inválida da API'}
            
        except Exception as e:
            log_consulta(f"Direct Data - {endpoint}", str(params), "ERRO", str(e))
            return {'success': False, 'error': f'Erro inesperado: {str(e)}'}
    
    def consultar_por_cpf(self, cpf: str) -> Dict[str, Any]:
        """
        Consulta dados pessoais por CPF
        
        Args:
            cpf: CPF para consulta (apenas números)
            
        Returns:
            Dict com dados pessoais encontrados
        """
        # Limpar CPF (apenas números)
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf_limpo) != 11:
            return {'success': False, 'error': 'CPF deve ter 11 dígitos'}
        
        # Verificar cache
        cache_key = f"directd_cpf_{cpf_limpo}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        params = {'CPF': cpf_limpo}
        result = self._make_request('RegistrationDataBrazil', params)
        
        # Salvar no cache se sucesso
        if result.get("success"):
            cache.set(cache_key, result)
        
        return result
    
    def consultar_por_nome(self, nome: str, sobrenome: str, data_nascimento: str = None) -> Dict[str, Any]:
        """
        Consulta dados pessoais por nome completo
        
        Args:
            nome: Primeiro nome
            sobrenome: Sobrenome
            data_nascimento: Data de nascimento no formato YYYY/MM/DD (opcional)
            
        Returns:
            Dict com dados pessoais encontrados
        """
        params = {
            'NAME': nome.upper(),
            'SURNAME': sobrenome.upper()
        }
        
        if data_nascimento:
            # Converter data para formato esperado (YYYYMMDD)
            try:
                if '/' in data_nascimento:
                    data_formatada = data_nascimento.replace('/', '')
                elif '-' in data_nascimento:
                    data_formatada = data_nascimento.replace('-', '')
                else:
                    data_formatada = data_nascimento
                
                params['DOB'] = data_formatada
            except:
                return {'success': False, 'error': 'Formato de data inválido. Use YYYY/MM/DD'}
        
        # Verificar cache
        cache_key = f"directd_nome_{nome}_{sobrenome}_{data_nascimento or 'sem_data'}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        result = self._make_request('RegistrationDataBrazil', params)
        
        # Salvar no cache se sucesso
        if result.get("success"):
            cache.set(cache_key, result)
        
        return result
    
    def formatar_resultado(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata o resultado da consulta para exibição
        
        Args:
            resultado: Resultado bruto da API
            
        Returns:
            Dict formatado para exibição
        """
        if not resultado.get('success'):
            return resultado
        
        data = resultado.get('data', {})
        
        # Formatar telefones
        telefones = []
        for phone in data.get('phones', []):
            telefones.append({
                'numero': phone.get('phoneNumber', 'N/A'),
                'tipo': phone.get('phoneType', 'N/A')
            })
        
        # Formatar endereços
        enderecos = []
        for address in data.get('addresses', []):
            endereco_completo = f"{address.get('street', '')}, {address.get('number', '')}"
            if address.get('complement'):
                endereco_completo += f", {address.get('complement')}"
            endereco_completo += f" - {address.get('neighborhood', '')}, {address.get('city', '')}/{address.get('state', '')}"
            
            enderecos.append({
                'endereco_completo': endereco_completo,
                'rua': address.get('street', 'N/A'),
                'numero': address.get('number', 'N/A'),
                'complemento': address.get('complement', 'N/A'),
                'bairro': address.get('neighborhood', 'N/A'),
                'cidade': address.get('city', 'N/A'),
                'estado': address.get('state', 'N/A'),
                'cep': address.get('postalCode', 'N/A')
            })
        
        # Formatar emails
        emails = []
        for email in data.get('emails', []):
            emails.append(email.get('emailAddress', 'N/A'))
        
        return {
            'success': True,
            'dados_pessoais': {
                'nome': data.get('name', 'N/A'),
                'cpf': data.get('cpf', 'N/A'),
                'data_nascimento': data.get('dateOfBirth', 'N/A'),
                'idade': data.get('age', 'N/A'),
                'genero': data.get('gender', 'N/A'),
                'nome_mae': data.get('nameMother', 'N/A'),
                'faixa_salarial': data.get('salaryRange', 'N/A')
            },
            'contatos': {
                'telefones': telefones,
                'emails': emails
            },
            'enderecos': enderecos,
            'metadata': resultado.get('metadata', {})
        }
    
    def verificar_configuracao(self) -> Dict[str, Any]:
        """
        Verifica se a API está configurada corretamente
        
        Returns:
            Dict com status da configuração
        """
        if not self.token:
            return {
                'configurado': False,
                'erro': 'Token Direct Data não configurado',
                'instrucoes': 'Configure DIRECTD_TOKEN no arquivo .env'
            }
        
        # Teste simples com CPF inválido para verificar autenticação
        test_result = self._make_request('RegistrationDataBrazil', {'CPF': '00000000000'})
        
        if 'Token inválido' in test_result.get('error', ''):
            return {
                'configurado': False,
                'erro': 'Token Direct Data inválido',
                'instrucoes': 'Verifique o token DIRECTD_TOKEN no arquivo .env'
            }
        
        return {
            'configurado': True,
            'status': 'API Direct Data configurada e funcionando'
        }

# Instância global do cliente
directd_client = DirectDataClient()

def consultar_dados_pessoais_cpf(cpf: str) -> Dict[str, Any]:
    """Função wrapper para consulta por CPF"""
    resultado = directd_client.consultar_por_cpf(cpf)
    return directd_client.formatar_resultado(resultado)

def consultar_dados_pessoais_nome(nome: str, sobrenome: str, data_nascimento: str = None) -> Dict[str, Any]:
    """Função wrapper para consulta por nome"""
    resultado = directd_client.consultar_por_nome(nome, sobrenome, data_nascimento)
    return directd_client.formatar_resultado(resultado)

def verificar_directd_config() -> Dict[str, Any]:
    """Função wrapper para verificar configuração"""
    return directd_client.verificar_configuracao()