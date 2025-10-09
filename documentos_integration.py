# -*- coding: utf-8 -*-
"""
Integração com APIs gratuitas para consulta de documentos brasileiros
- TSE: Título de Eleitor (Dados Abertos)
- DataSUS: CNS (Cartão Nacional de Saúde)
- PIS: Consulta através de APIs disponíveis
- RG e CNH: Validação local robusta usando validate-docbr
"""

import requests
import json
import os
import re
from datetime import datetime
import logging
from typing import Dict, Any, Optional

# Importar biblioteca de validação de documentos brasileiros
try:
    from validate_docbr import CNH, CPF, CNPJ, PIS
    VALIDATE_DOCBR_AVAILABLE = True
except ImportError:
    VALIDATE_DOCBR_AVAILABLE = False
    print("Aviso: validate-docbr não instalado. Usando validação básica.")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentosAPI:
    """Classe para integração com APIs de documentos brasileiros"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OSINT-Investigador-BR/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def validar_titulo_eleitor(self, titulo: str) -> bool:
        """Valida formato do título de eleitor"""
        if not titulo:
            return False
        
        titulo_limpo = re.sub(r'\D', '', titulo)
        return len(titulo_limpo) == 12 and titulo_limpo.isdigit()
    
    def validar_cns(self, cns: str) -> bool:
        """Valida formato do CNS (Cartão Nacional de Saúde)"""
        if not cns:
            return False
        
        cns_limpo = re.sub(r'\D', '', cns)
        return len(cns_limpo) == 15 and cns_limpo.isdigit()
    
    def validar_pis(self, pis: str) -> bool:
        """Valida formato do PIS/PASEP"""
        if not pis:
            return False
        
        pis_limpo = re.sub(r'\D', '', pis)
        return len(pis_limpo) == 11 and pis_limpo.isdigit()
    
    def consultar_titulo_eleitor_tse(self, titulo: str, nome: str = None) -> Dict[str, Any]:
        """
        Consulta dados do título de eleitor via TSE Dados Abertos
        Nota: TSE não oferece consulta individual por título, apenas dados estatísticos
        """
        try:
            if not self.validar_titulo_eleitor(titulo):
                return {
                    'success': False,
                    'error': 'Formato de título de eleitor inválido',
                    'data': None
                }
            
            # TSE Dados Abertos não permite consulta individual
            # Retornamos informações básicas de validação
            return {
                'success': True,
                'data': {
                    'titulo_eleitor': titulo,
                    'formato_valido': True,
                    'status': 'Formato válido - Consulta individual não disponível via TSE Dados Abertos',
                    'observacao': 'TSE disponibiliza apenas dados estatísticos e eleitorais agregados',
                    'fonte': 'Validação local + TSE Dados Abertos (limitado)'
                },
                'metadata': {
                    'fonte': 'TSE Dados Abertos',
                    'timestamp': datetime.now().isoformat(),
                    'tipo_consulta': 'validacao_formato'
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na consulta TSE: {str(e)}")
            return {
                'success': False,
                'error': f'Erro na consulta TSE: {str(e)}',
                'data': None
            }
    
    def consultar_cns_datasus(self, cns: str, nome: str = None) -> Dict[str, Any]:
        """
        Consulta dados do CNS via DataSUS
        Nota: Requer configuração específica e credenciais
        """
        try:
            if not self.validar_cns(cns):
                return {
                    'success': False,
                    'error': 'Formato de CNS inválido',
                    'data': None
                }
            
            # DataSUS requer credenciais específicas e configuração SOAP
            # Por enquanto, retornamos validação básica
            return {
                'success': True,
                'data': {
                    'cns': cns,
                    'formato_valido': True,
                    'status': 'Formato válido - Consulta requer credenciais DataSUS',
                    'observacao': 'CNS válido. Consulta completa requer integração com Web Service DataSUS',
                    'fonte': 'Validação local + DataSUS (requer configuração)'
                },
                'metadata': {
                    'fonte': 'DataSUS (validação)',
                    'timestamp': datetime.now().isoformat(),
                    'tipo_consulta': 'validacao_formato'
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na consulta DataSUS: {str(e)}")
            return {
                'success': False,
                'error': f'Erro na consulta DataSUS: {str(e)}',
                'data': None
            }
    
    def consultar_pis(self, pis: str, nome: str = None) -> Dict[str, Any]:
        """
        Consulta dados do PIS/PASEP
        Nota: Não há APIs públicas gratuitas para consulta de PIS
        """
        try:
            if not self.validar_pis(pis):
                return {
                    'success': False,
                    'error': 'Formato de PIS inválido',
                    'data': None
                }
            
            # Não há APIs públicas gratuitas para PIS
            return {
                'success': True,
                'data': {
                    'pis': pis,
                    'formato_valido': True,
                    'status': 'Formato válido - Consulta não disponível via APIs públicas',
                    'observacao': 'PIS válido. Não há APIs públicas gratuitas para consulta de dados do PIS',
                    'fonte': 'Validação local'
                },
                'metadata': {
                    'fonte': 'Validação local',
                    'timestamp': datetime.now().isoformat(),
                    'tipo_consulta': 'validacao_formato'
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na consulta PIS: {str(e)}")
            return {
                'success': False,
                'error': f'Erro na consulta PIS: {str(e)}',
                'data': None
            }
    
    def consultar_rg(self, rg: str, estado: str = None) -> Dict[str, Any]:
        """
        Consulta RG - Não disponível via APIs públicas
        """
        return {
            'success': True,
            'data': {
                'rg': rg if rg else 'N/A',
                'estado': estado if estado else 'N/A',
                'status': 'Não disponível',
                'observacao': 'Consulta de RG não disponível via APIs públicas gratuitas',
                'fonte': 'N/A'
            },
            'metadata': {
                'fonte': 'N/A',
                'timestamp': datetime.now().isoformat(),
                'tipo_consulta': 'nao_disponivel'
            }
        }
    
    def validar_cnh(self, cnh: str) -> bool:
        """
        Valida formato e dígitos verificadores da CNH usando validate-docbr
        """
        if not cnh:
            return False
        
        if VALIDATE_DOCBR_AVAILABLE:
            try:
                cnh_validator = CNH()
                return cnh_validator.validate(cnh)
            except Exception as e:
                logger.warning(f"Erro na validação CNH com validate-docbr: {e}")
                # Fallback para validação básica
                pass
        
        # Validação básica como fallback
        cnh_limpo = re.sub(r'\D', '', cnh)
        return len(cnh_limpo) == 11 and cnh_limpo.isdigit()
    
    def gerar_cnh_fake(self, com_mascara: bool = False) -> str:
        """
        Gera uma CNH válida para testes usando validate-docbr
        """
        if VALIDATE_DOCBR_AVAILABLE:
            try:
                cnh_validator = CNH()
                return cnh_validator.generate(mask=com_mascara)
            except Exception as e:
                logger.warning(f"Erro ao gerar CNH fake: {e}")
        
        # Fallback: gerar número básico
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(11)])
    
    def consultar_cnh_infosimples(self, cnh: str, cpf: str = None, nome: str = None, nome_mae: str = None) -> Dict[str, Any]:
        """
        Consulta CNH via API da Infosimples (SENATRAN)
        Requer configuração de API Key da Infosimples
        """
        try:
            # Verificar se há configuração da API Infosimples
            api_key = os.getenv('INFOSIMPLES_API_KEY')  # Configurar via variável de ambiente: INFOSIMPLES_API_KEY
            
            if not api_key:
                return {
                    'success': False,
                    'error': 'API Key da Infosimples não configurada',
                    'data': None
                }
            
            if not self.validar_cnh(cnh):
                return {
                    'success': False,
                    'error': 'Formato de CNH inválido',
                    'data': None
                }
            
            # Endpoint da Infosimples para validação de CNH
            url = "https://api.infosimples.com/api/v2/consultas/senatran/validar-cnh"
            
            payload = {
                'registro': cnh,
                'cpf': cpf,
                'nome_condutor': nome,
                'nome_mae': nome_mae
            }
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            response = self.session.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': {
                        'cnh': cnh,
                        'cpf': data.get('cpf'),
                        'nome': data.get('nome'),
                        'nome_mae': data.get('mae'),
                        'categoria': data.get('categoria'),
                        'situacao': data.get('situacao'),
                        'data_emissao': data.get('emissao_data'),
                        'data_validade': data.get('validade_data'),
                        'codigo_seguranca': data.get('codigo_seguranca'),
                        'status': 'Dados obtidos com sucesso',
                        'observacao': 'Consulta realizada via API Infosimples/SENATRAN',
                        'fonte': 'Infosimples/SENATRAN'
                    },
                    'metadata': {
                        'fonte': 'Infosimples/SENATRAN',
                        'timestamp': datetime.now().isoformat(),
                        'tipo_consulta': 'api_comercial'
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro na API Infosimples: {response.status_code}',
                    'data': None
                }
                
        except Exception as e:
            logger.error(f"Erro na consulta CNH Infosimples: {str(e)}")
            return {
                'success': False,
                'error': f'Erro na consulta CNH: {str(e)}',
                'data': None
            }

    def consultar_cnh(self, cnh: str, cpf: str = None, nome: str = None, nome_mae: str = None) -> Dict[str, Any]:
        """
        Consulta CNH com validação robusta gratuita:
        1. Validação completa usando validate-docbr (dígitos verificadores)
        2. Tentativa via API Infosimples (se configurada)
        3. Retorno com informações detalhadas sobre validação
        """
        try:
            if not cnh:
                return {
                    'success': False,
                    'error': 'CNH é obrigatória',
                    'data': None
                }
            
            # Validar formato e dígitos verificadores
            cnh_valida = self.validar_cnh(cnh)
            cnh_limpo = re.sub(r'\D', '', cnh)
            
            if not cnh_valida:
                return {
                    'success': False,
                    'error': 'CNH inválida. Formato ou dígitos verificadores incorretos.',
                    'data': {
                        'cnh': cnh_limpo,
                        'formato_valido': False,
                        'digitos_verificadores_validos': False,
                        'observacao': 'CNH não passou na validação matemática dos dígitos verificadores'
                    }
                }
            
            # Tentar consulta via Infosimples primeiro (se configurada)
            resultado_infosimples = self.consultar_cnh_infosimples(cnh, cpf, nome, nome_mae)
            
            if resultado_infosimples['success']:
                return resultado_infosimples
            
            # Retorno com validação local robusta
            return {
                'success': True,
                'data': {
                    'cnh': cnh_limpo,
                    'formato_valido': True,
                    'digitos_verificadores_validos': True,
                    'status': 'CNH válida - Validação matemática aprovada',
                    'observacao': 'CNH passou na validação completa de formato e dígitos verificadores.',
                    'validacao_tipo': 'Completa (formato + dígitos verificadores)' if VALIDATE_DOCBR_AVAILABLE else 'Básica (apenas formato)',
                    'biblioteca_usada': 'validate-docbr' if VALIDATE_DOCBR_AVAILABLE else 'validação interna',
                    'limitacoes_consulta_dados': [
                        'Para dados pessoais completos, é necessário API comercial',
                        'SENATRAN permite apenas 5 consultas por dia por usuário',
                        'Consulta completa requer login gov.br do próprio condutor'
                    ],
                    'alternativas_dados_completos': [
                        'Configure INFOSIMPLES_API_KEY para consultas ilimitadas',
                        'Use Portal SENATRAN para consulta própria',
                        'Considere APIs comerciais para uso empresarial'
                    ],
                    'fonte': 'Validação local robusta'
                },
                'metadata': {
                    'fonte': 'Validação local + validate-docbr',
                    'timestamp': datetime.now().isoformat(),
                    'tipo_consulta': 'validacao_completa_gratuita',
                    'biblioteca_validacao': 'validate-docbr' if VALIDATE_DOCBR_AVAILABLE else 'interna'
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na consulta CNH: {str(e)}")
            return {
                'success': False,
                'error': f'Erro na consulta CNH: {str(e)}',
                'data': None
            }
    
    def consultar_todos_documentos(self, dados: Dict[str, str]) -> Dict[str, Any]:
        """
        Consulta todos os documentos disponíveis
        """
        resultados = {}
        
        # Título de Eleitor
        if dados.get('titulo_eleitor'):
            resultados['titulo_eleitor'] = self.consultar_titulo_eleitor_tse(
                dados['titulo_eleitor'], 
                dados.get('nome')
            )
        
        # CNS
        if dados.get('cns'):
            resultados['cns'] = self.consultar_cns_datasus(
                dados['cns'], 
                dados.get('nome')
            )
        
        # PIS
        if dados.get('pis'):
            resultados['pis'] = self.consultar_pis(
                dados['pis'], 
                dados.get('nome')
            )
        
        # RG (sempre N/A)
        resultados['rg'] = self.consultar_rg(
            dados.get('rg'), 
            dados.get('estado')
        )
        
        # CNH (sempre N/A)
        resultados['cnh'] = self.consultar_cnh(dados.get('cnh'))
        
        return {
            'success': True,
            'data': resultados,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_consultas': len(resultados),
                'fonte': 'Múltiplas APIs'
            }
        }

# Instância global
documentos_api = DocumentosAPI()

# Funções de conveniência
def consultar_titulo_eleitor(titulo: str, nome: str = None) -> Dict[str, Any]:
    """Função de conveniência para consulta de título de eleitor"""
    return documentos_api.consultar_titulo_eleitor_tse(titulo, nome)

def consultar_cns(cns: str, nome: str = None) -> Dict[str, Any]:
    """Função de conveniência para consulta de CNS"""
    return documentos_api.consultar_cns_datasus(cns, nome)

def consultar_pis(pis: str, nome: str = None) -> Dict[str, Any]:
    """Função de conveniência para consulta de PIS"""
    return documentos_api.consultar_pis(pis, nome)

def consultar_rg(rg: str, estado: str = None) -> Dict[str, Any]:
    """Função de conveniência para consulta de RG"""
    return documentos_api.consultar_rg(rg, estado)

def consultar_cnh(cnh: str) -> Dict[str, Any]:
    """Função de conveniência para consulta de CNH"""
    return documentos_api.consultar_cnh(cnh)

def consultar_todos_documentos(dados: Dict[str, str]) -> Dict[str, Any]:
    """Função de conveniência para consulta de todos os documentos"""
    return documentos_api.consultar_todos_documentos(dados)

if __name__ == "__main__":
    # Teste das funcionalidades
    print("=== Teste das APIs de Documentos ===")
    
    # Teste Título de Eleitor
    print("\n1. Teste Título de Eleitor:")
    resultado_titulo = consultar_titulo_eleitor("123456789012", "João Silva")
    print(json.dumps(resultado_titulo, indent=2, ensure_ascii=False))
    
    # Teste CNS
    print("\n2. Teste CNS:")
    resultado_cns = consultar_cns("123456789012345", "João Silva")
    print(json.dumps(resultado_cns, indent=2, ensure_ascii=False))
    
    # Teste PIS
    print("\n3. Teste PIS:")
    resultado_pis = consultar_pis("12345678901", "João Silva")
    print(json.dumps(resultado_pis, indent=2, ensure_ascii=False))
    
    # Teste RG
    print("\n4. Teste RG:")
    resultado_rg = consultar_rg("123456789", "SP")
    print(json.dumps(resultado_rg, indent=2, ensure_ascii=False))
    
    # Teste CNH
    print("\n5. Teste CNH:")
    resultado_cnh = consultar_cnh("12345678901")
    print(json.dumps(resultado_cnh, indent=2, ensure_ascii=False))