"""
OSINT Investigador BR - Classe Principal
Sistema completo para investigações OSINT no Brasil
"""
import requests
import time
from typing import Dict, Any, Optional, List
from utils.validators import (
    validar_cep, validar_ddd, validar_cnpj,
    limpar_cep, limpar_ddd, limpar_cnpj,
    formatar_cep, formatar_cnpj
)
from utils.cache import cache
from utils.logger import log_consulta, log_api_call, log_error, logger
from config import (
    VIACEP_URL, BRASILAPI_DDD_URL, BRASILAPI_CNPJ_URL,
    BRASILAPI_BANKS_URL, BRASILAPI_IBGE_URL, RECEITAWS_CNPJ_URL,
    REQUEST_TIMEOUT
)


class OSINTInvestigador:
    """Classe principal para consultas OSINT brasileiras"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OSINT-Investigador-BR/1.0'
        })
    
    def _fazer_requisicao(self, url: str, api_name: str) -> Optional[Dict[str, Any]]:
        """
        Faz requisição HTTP com tratamento de erros e logging
        
        Args:
            url (str): URL da requisição
            api_name (str): Nome da API para logging
            
        Returns:
            Optional[Dict[str, Any]]: Dados da resposta ou None em caso de erro
        """
        try:
            inicio = time.time()
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            tempo_resposta = time.time() - inicio
            
            log_api_call(api_name, url, response.status_code, tempo_resposta)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            log_error(Exception(f"Timeout na requisição para {api_name}"), f"URL: {url}")
            return None
        except requests.exceptions.RequestException as e:
            log_error(e, f"Erro na requisição para {api_name}")
            return None
        except ValueError as e:
            log_error(e, f"Erro ao decodificar JSON de {api_name}")
            return None
    
    def consultar_cep(self, cep: str) -> Dict[str, Any]:
        """
        Consulta informações de CEP
        
        Args:
            cep (str): CEP a ser consultado
            
        Returns:
            Dict[str, Any]: Dados do CEP ou erro
        """
        # Validação
        if not validar_cep(cep):
            resultado = {"erro": "CEP inválido", "cep": cep}
            log_consulta("CEP", cep, False, "CEP inválido")
            return resultado
        
        cep_limpo = limpar_cep(cep)
        cache_key = f"cep_{cep_limpo}"
        
        # Verifica cache
        cached_result = cache.get(cache_key)
        if cached_result:
            log_consulta("CEP", cep, True, "Cache hit")
            return cached_result
        
        # Faz requisição
        url = VIACEP_URL.format(cep_limpo)
        data = self._fazer_requisicao(url, "ViaCEP")
        
        if not data:
            resultado = {"erro": "Erro na consulta", "cep": cep}
            log_consulta("CEP", cep, False, "Erro na API")
            return resultado
        
        if 'erro' in data:
            resultado = {"erro": "CEP não encontrado", "cep": cep}
            log_consulta("CEP", cep, False, "CEP não encontrado")
            return resultado
        
        # Formata resultado
        resultado = {
            "cep": formatar_cep(data.get("cep", "")),
            "logradouro": data.get("logradouro", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "localidade": data.get("localidade", ""),
            "uf": data.get("uf", ""),
            "ibge": data.get("ibge", ""),
            "gia": data.get("gia", ""),
            "ddd": data.get("ddd", ""),
            "siafi": data.get("siafi", "")
        }
        
        # Salva no cache
        cache.set(cache_key, resultado)
        log_consulta("CEP", cep, True, "Consulta realizada com sucesso")
        
        return resultado
    
    def consultar_ddd(self, ddd: str) -> Dict[str, Any]:
        """
        Consulta informações de DDD
        
        Args:
            ddd (str): DDD a ser consultado
            
        Returns:
            Dict[str, Any]: Dados do DDD ou erro
        """
        # Validação
        if not validar_ddd(ddd):
            resultado = {"erro": "DDD inválido", "ddd": ddd}
            log_consulta("DDD", ddd, False, "DDD inválido")
            return resultado
        
        ddd_limpo = limpar_ddd(ddd)
        cache_key = f"ddd_{ddd_limpo}"
        
        # Verifica cache
        cached_result = cache.get(cache_key)
        if cached_result:
            log_consulta("DDD", ddd, True, "Cache hit")
            return cached_result
        
        # Faz requisição
        url = BRASILAPI_DDD_URL.format(ddd_limpo)
        data = self._fazer_requisicao(url, "BrasilAPI-DDD")
        
        if not data:
            resultado = {"erro": "Erro na consulta", "ddd": ddd}
            log_consulta("DDD", ddd, False, "Erro na API")
            return resultado
        
        if 'message' in data and 'não encontrado' in data['message'].lower():
            resultado = {"erro": "DDD não encontrado", "ddd": ddd}
            log_consulta("DDD", ddd, False, "DDD não encontrado")
            return resultado
        
        # Formata resultado
        resultado = {
            "ddd": ddd_limpo,
            "estado": data.get("state", ""),
            "cidades": data.get("cities", [])
        }
        
        # Salva no cache
        cache.set(cache_key, resultado)
        log_consulta("DDD", ddd, True, "Consulta realizada com sucesso")
        
        return resultado
    
    def consultar_cnpj(self, cnpj: str, fonte: str = "brasilapi") -> Dict[str, Any]:
        """
        Consulta informações de CNPJ
        
        Args:
            cnpj (str): CNPJ a ser consultado
            fonte (str): Fonte da consulta ('brasilapi' ou 'receitaws')
            
        Returns:
            Dict[str, Any]: Dados do CNPJ ou erro
        """
        # Validação
        if not validar_cnpj(cnpj):
            resultado = {"erro": "CNPJ inválido", "cnpj": cnpj}
            log_consulta("CNPJ", cnpj, False, "CNPJ inválido")
            return resultado
        
        cnpj_limpo = limpar_cnpj(cnpj)
        cache_key = f"cnpj_{cnpj_limpo}_{fonte}"
        
        # Verifica cache
        cached_result = cache.get(cache_key)
        if cached_result:
            log_consulta("CNPJ", cnpj, True, f"Cache hit - {fonte}")
            return cached_result
        
        # Escolhe URL baseada na fonte
        if fonte == "receitaws":
            url = RECEITAWS_CNPJ_URL.format(cnpj_limpo)
            api_name = "ReceitaWS"
        else:
            url = BRASILAPI_CNPJ_URL.format(cnpj_limpo)
            api_name = "BrasilAPI-CNPJ"
        
        # Faz requisição
        data = self._fazer_requisicao(url, api_name)
        
        if not data:
            resultado = {"erro": "Erro na consulta", "cnpj": cnpj}
            log_consulta("CNPJ", cnpj, False, f"Erro na API - {fonte}")
            return resultado
        
        # Verifica se encontrou
        if 'status' in data and data['status'] == 'ERROR':
            resultado = {"erro": "CNPJ não encontrado", "cnpj": cnpj}
            log_consulta("CNPJ", cnpj, False, f"CNPJ não encontrado - {fonte}")
            return resultado
        
        # Formata resultado baseado na fonte
        if fonte == "receitaws":
            resultado = {
                "cnpj": formatar_cnpj(cnpj_limpo),
                "razao_social": data.get("nome", ""),
                "nome_fantasia": data.get("fantasia", ""),
                "situacao": data.get("situacao", ""),
                "tipo": data.get("tipo", ""),
                "porte": data.get("porte", ""),
                "natureza_juridica": data.get("natureza_juridica", ""),
                "atividade_principal": data.get("atividade_principal", []),
                "atividades_secundarias": data.get("atividades_secundarias", []),
                "endereco": {
                    "logradouro": data.get("logradouro", ""),
                    "numero": data.get("numero", ""),
                    "complemento": data.get("complemento", ""),
                    "bairro": data.get("bairro", ""),
                    "municipio": data.get("municipio", ""),
                    "uf": data.get("uf", ""),
                    "cep": data.get("cep", "")
                },
                "telefone": data.get("telefone", ""),
                "email": data.get("email", ""),
                "data_abertura": data.get("abertura", ""),
                "capital_social": data.get("capital_social", ""),
                "fonte": "ReceitaWS"
            }
        else:
            resultado = {
                "cnpj": formatar_cnpj(cnpj_limpo),
                "razao_social": data.get("company", {}).get("name", ""),
                "nome_fantasia": data.get("alias", ""),
                "situacao": data.get("status", {}).get("text", ""),
                "tipo": data.get("company", {}).get("equity", ""),
                "natureza_juridica": data.get("company", {}).get("nature", {}).get("text", ""),
                "atividade_principal": data.get("primary_activity", []),
                "atividades_secundarias": data.get("secondary_activities", []),
                "endereco": data.get("address", {}),
                "telefones": data.get("phones", []),
                "emails": data.get("emails", []),
                "data_abertura": data.get("founded", ""),
                "capital_social": data.get("company", {}).get("equity", ""),
                "fonte": "BrasilAPI"
            }
        
        # Salva no cache
        cache.set(cache_key, resultado)
        log_consulta("CNPJ", cnpj, True, f"Consulta realizada com sucesso - {fonte}")
        
        return resultado
    
    def consultar_bancos(self) -> Dict[str, Any]:
        """
        Lista todos os bancos brasileiros
        
        Returns:
            Dict[str, Any]: Lista de bancos ou erro
        """
        cache_key = "bancos_brasileiros"
        
        # Verifica cache
        cached_result = cache.get(cache_key)
        if cached_result:
            log_consulta("BANCOS", "todos", True, "Cache hit")
            return cached_result
        
        # Faz requisição
        data = self._fazer_requisicao(BRASILAPI_BANKS_URL, "BrasilAPI-Banks")
        
        if not data:
            resultado = {"erro": "Erro na consulta de bancos"}
            log_consulta("BANCOS", "todos", False, "Erro na API")
            return resultado
        
        resultado = {
            "bancos": data,
            "total": len(data) if isinstance(data, list) else 0
        }
        
        # Salva no cache (cache mais longo para dados estáticos)
        cache.set(cache_key, resultado)
        log_consulta("BANCOS", "todos", True, f"Consulta realizada - {resultado['total']} bancos")
        
        return resultado
    
    def consultar_municipios_uf(self, uf: str) -> Dict[str, Any]:
        """
        Consulta municípios por UF
        
        Args:
            uf (str): Sigla do estado (UF)
            
        Returns:
            Dict[str, Any]: Lista de municípios ou erro
        """
        if not uf or len(uf) != 2:
            resultado = {"erro": "UF inválida", "uf": uf}
            log_consulta("MUNICIPIOS", uf, False, "UF inválida")
            return resultado
        
        uf_upper = uf.upper()
        cache_key = f"municipios_{uf_upper}"
        
        # Verifica cache
        cached_result = cache.get(cache_key)
        if cached_result:
            log_consulta("MUNICIPIOS", uf, True, "Cache hit")
            return cached_result
        
        # Faz requisição
        url = BRASILAPI_IBGE_URL.format(uf_upper)
        data = self._fazer_requisicao(url, "BrasilAPI-IBGE")
        
        if not data:
            resultado = {"erro": "Erro na consulta", "uf": uf}
            log_consulta("MUNICIPIOS", uf, False, "Erro na API")
            return resultado
        
        resultado = {
            "uf": uf_upper,
            "municipios": data,
            "total": len(data) if isinstance(data, list) else 0
        }
        
        # Salva no cache
        cache.set(cache_key, resultado)
        log_consulta("MUNICIPIOS", uf, True, f"Consulta realizada - {resultado['total']} municípios")
        
        return resultado
    
    def buscar_banco_por_codigo(self, codigo: str) -> Dict[str, Any]:
        """
        Busca banco específico por código
        
        Args:
            codigo (str): Código do banco
            
        Returns:
            Dict[str, Any]: Dados do banco ou erro
        """
        bancos_result = self.consultar_bancos()
        
        if "erro" in bancos_result:
            return bancos_result
        
        for banco in bancos_result["bancos"]:
            if str(banco.get("code", "")) == str(codigo):
                resultado = {
                    "codigo": banco.get("code", ""),
                    "nome": banco.get("name", ""),
                    "nome_completo": banco.get("fullName", ""),
                    "ispb": banco.get("ispb", "")
                }
                log_consulta("BANCO", codigo, True, f"Banco encontrado: {resultado['nome']}")
                return resultado
        
        resultado = {"erro": "Banco não encontrado", "codigo": codigo}
        log_consulta("BANCO", codigo, False, "Banco não encontrado")
        return resultado
    
    def limpar_cache(self) -> Dict[str, str]:
        """
        Limpa todo o cache
        
        Returns:
            Dict[str, str]: Resultado da operação
        """
        try:
            cache.clear()
            logger.info("Cache limpo com sucesso")
            return {"sucesso": "Cache limpo com sucesso"}
        except Exception as e:
            log_error(e, "Erro ao limpar cache")
            return {"erro": "Erro ao limpar cache"}
    
    def estatisticas_cache(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache
        
        Returns:
            Dict[str, Any]: Estatísticas do cache
        """
        try:
            import os
            cache_dir = cache.cache_dir
            
            if not os.path.exists(cache_dir):
                return {"arquivos": 0, "tamanho_mb": 0}
            
            arquivos = 0
            tamanho_total = 0
            
            for filename in os.listdir(cache_dir):
                if filename.endswith('.json'):
                    arquivos += 1
                    filepath = os.path.join(cache_dir, filename)
                    tamanho_total += os.path.getsize(filepath)
            
            return {
                "arquivos": arquivos,
                "tamanho_mb": round(tamanho_total / (1024 * 1024), 2)
            }
        
        except Exception as e:
            log_error(e, "Erro ao obter estatísticas do cache")
            return {"erro": "Erro ao obter estatísticas"}


# Instância global
investigador = OSINTInvestigador()