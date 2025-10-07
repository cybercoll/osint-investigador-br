"""
Integração com Direct Data API - Versão Paga
Sistema completo para consultas de dados pessoais no Brasil
API: https://app.directd.com.br/
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
    """Cliente para integração com Direct Data API - Versão Paga"""
    
    def __init__(self):
        self.base_url = "https://app.directd.com.br/api"
        self.token = os.getenv('DIRECTD_TOKEN', 'B8A26730-37E3-4C74-B92E-26EABC7D1324')
        self.timeout = 30
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Faz requisição para a API Direct Data - Versão Paga"""
        try:
            # Headers para API paga
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            url = f"{self.base_url}/{endpoint}"
            
            # Log da consulta
            log_consulta(f"Direct Data Paga - {endpoint}", str(params), "INICIANDO")
            
            # Para API paga, usar POST com JSON
            response = requests.post(url, json=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Verificar se a consulta foi bem-sucedida (estrutura da API paga)
            if not data.get('success', True):
                error_msg = data.get('message', 'Erro na consulta')
                log_consulta(f"Direct Data Paga - {endpoint}", str(params), "ERRO", error_msg)
                return {
                    'success': False,
                    'error': error_msg,
                    'message': data.get('details', '')
                }
            
            # Verificar se há dados de retorno
            if not data.get('data'):
                log_consulta(f"Direct Data Paga - {endpoint}", str(params), "SEM_DADOS")
                return {
                    'success': False,
                    'error': 'Nenhum dado encontrado',
                    'message': 'Consulta realizada mas sem dados disponíveis'
                }
            
            log_consulta(f"Direct Data Paga - {endpoint}", str(params), "SUCESSO")
            
            return {
                'success': True,
                'data': data['data'],
                'metadata': data.get('metadata', {})
            }
            
        except requests.exceptions.Timeout:
            log_consulta(f"Direct Data Paga - {endpoint}", str(params), "ERRO", "Timeout")
            return {'success': False, 'error': 'Timeout na consulta'}
            
        except requests.exceptions.RequestException as e:
            log_consulta(f"Direct Data Paga - {endpoint}", str(params), "ERRO", str(e))
            return {'success': False, 'error': f'Erro na requisição: {str(e)}'}
            
        except Exception as e:
            log_consulta(f"Direct Data Paga - {endpoint}", str(params), "ERRO", str(e))
            return {'success': False, 'error': f'Erro inesperado: {str(e)}'}
    
    def consultar_por_cpf(self, cpf: str) -> Dict[str, Any]:
        """
        Consulta dados pessoais por CPF - API Paga
        
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
        cache_key = f"directd_paga_cpf_{cpf_limpo}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        params = {'cpf': cpf_limpo}
        result = self._make_request('pessoa/cpf', params)
        
        # Salvar no cache se sucesso
        if result.get("success"):
            cache.set(cache_key, result)
        
        return result
    
    def consultar_por_nome(self, nome: str, sobrenome: str, data_nascimento: str = None) -> Dict[str, Any]:
        """
        Consulta dados pessoais por nome completo - API Paga
        
        Args:
            nome: Primeiro nome
            sobrenome: Sobrenome
            data_nascimento: Data de nascimento no formato YYYY-MM-DD (opcional)
            
        Returns:
            Dict com dados pessoais encontrados
        """
        params = {
            'nome': nome.strip(),
            'sobrenome': sobrenome.strip()
        }
        
        if data_nascimento:
            # Formato esperado: YYYY-MM-DD
            params['data_nascimento'] = data_nascimento
        
        # Verificar cache
        cache_key = f"directd_paga_nome_{nome}_{sobrenome}_{data_nascimento or 'sem_data'}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        result = self._make_request('pessoa/nome', params)
        
        # Salvar no cache se sucesso
        if result.get("success"):
            cache.set(cache_key, result)
    
    def formatar_resultado(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formata o resultado da consulta para exibição - API Paga
        
        Args:
            resultado: Resultado bruto da API
            
        Returns:
            Dict formatado para exibição
        """
        if not resultado.get('success'):
            return resultado
        
        data = resultado.get('data', {})
        
        # Estrutura da API paga pode ser diferente
        pessoa = data.get('pessoa', data)
        
        # Formatar telefones
        telefones = []
        for phone in pessoa.get('telefones', []):
            telefones.append({
                'numero': phone.get('numero', 'N/A'),
                'tipo': phone.get('tipo', 'N/A'),
                'operadora': phone.get('operadora', 'N/A')
            })
        
        # Formatar endereços
        enderecos = []
        for endereco in pessoa.get('enderecos', []):
            endereco_completo = f"{endereco.get('logradouro', '')}, {endereco.get('numero', '')}"
            if endereco.get('complemento'):
                endereco_completo += f", {endereco.get('complemento')}"
            
            enderecos.append({
                'endereco': endereco_completo,
                'bairro': endereco.get('bairro', 'N/A'),
                'cidade': endereco.get('cidade', 'N/A'),
                'uf': endereco.get('uf', 'N/A'),
                'cep': endereco.get('cep', 'N/A')
            })
        
        # Formatar emails
        emails = []
        for email in pessoa.get('emails', []):
            emails.append({
                'email': email.get('endereco', email.get('email', 'N/A')),
                'tipo': email.get('tipo', 'N/A')
            })
        
        # Dados pessoais
        dados_pessoais = {
            'nome': pessoa.get('nome', 'N/A'),
            'cpf': pessoa.get('cpf', 'N/A'),
            'data_nascimento': pessoa.get('data_nascimento', 'N/A'),
            'idade': pessoa.get('idade', 'N/A'),
            'sexo': pessoa.get('sexo', 'N/A'),
            'mae': pessoa.get('nome_mae', 'N/A'),
            'pai': pessoa.get('nome_pai', 'N/A'),
            'situacao_cpf': pessoa.get('situacao_cpf', 'N/A')
        }
        
        # Dados profissionais
        dados_profissionais = []
        for trabalho in pessoa.get('vinculos_profissionais', []):
            dados_profissionais.append({
                'empresa': trabalho.get('empresa', 'N/A'),
                'cargo': trabalho.get('cargo', 'N/A'),
                'cnpj': trabalho.get('cnpj', 'N/A'),
                'situacao': trabalho.get('situacao', 'N/A')
            })
        
        return {
            'success': True,
            'dados_pessoais': dados_pessoais,
            'telefones': telefones,
            'enderecos': enderecos,
            'emails': emails,
            'dados_profissionais': dados_profissionais,
            'total_telefones': len(telefones),
            'total_enderecos': len(enderecos),
            'total_emails': len(emails),
            'metadata': resultado.get('metadata', {})
        }
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
        Verifica se a API paga está configurada corretamente
        
        Returns:
            Dict com status da configuração
        """
        if not self.token:
            return {
                'configurado': False,
                'erro': 'Token Direct Data não configurado',
                'detalhes': 'Configure a variável DIRECTD_TOKEN no arquivo .env'
            }
        
        try:
            # Teste simples com a API paga
            test_result = self._make_request('pessoa/cpf', {'cpf': '00000000000'})
            
            if test_result.get('success') or 'error' in test_result:
                return {
                    'configurado': True,
                    'status': 'API Direct Data (Paga) configurada e funcionando',
                    'base_url': self.base_url,
                    'token_configurado': True
                }
            else:
                return {
                    'configurado': False,
                    'erro': 'Erro na comunicação com a API',
                    'detalhes': test_result.get('error', 'Erro desconhecido')
                }
        except Exception as e:
            return {
                'configurado': False,
                'erro': f'Erro ao verificar configuração: {str(e)}',
                'detalhes': 'Verifique se o token está correto e a API está acessível'
            }


# Instância global do cliente
directd_client = DirectDataClient()

def consultar_dados_pessoais_cpf(cpf: str) -> Dict[str, Any]:
    """Função wrapper para consulta por CPF"""
    return directd_client.consultar_por_cpf(cpf)

def consultar_dados_pessoais_nome(nome: str, sobrenome: str, data_nascimento: str = None) -> Dict[str, Any]:
    """Função wrapper para consulta por nome"""
    return directd_client.consultar_por_nome(nome, sobrenome, data_nascimento)

def verificar_directd_config() -> Dict[str, Any]:
    """Função wrapper para verificar configuração"""
    return directd_client.verificar_configuracao()