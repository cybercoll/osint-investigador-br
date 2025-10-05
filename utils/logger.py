"""
Sistema de logging para OSINT Investigador BR
"""
import logging
import os
from datetime import datetime
from config import LOG_LEVEL, LOG_FILE


def setup_logger(name: str = "osint_investigador") -> logging.Logger:
    """
    Configura e retorna logger para o projeto
    
    Args:
        name (str): Nome do logger
        
    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evita duplicação de handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    file_handler = logging.FileHandler(
        os.path.join('logs', LOG_FILE),
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_consulta(tipo: str, parametro: str, sucesso: bool, detalhes: str = "") -> None:
    """
    Registra uma consulta realizada
    
    Args:
        tipo (str): Tipo da consulta (CEP, DDD, CNPJ, etc.)
        parametro (str): Parâmetro consultado
        sucesso (bool): Se a consulta foi bem-sucedida
        detalhes (str): Detalhes adicionais
    """
    logger = setup_logger()
    
    status = "SUCESSO" if sucesso else "ERRO"
    mensagem = f"Consulta {tipo} - Parâmetro: {parametro} - Status: {status}"
    
    if detalhes:
        mensagem += f" - Detalhes: {detalhes}"
    
    if sucesso:
        logger.info(mensagem)
    else:
        logger.error(mensagem)


def log_api_call(api: str, endpoint: str, status_code: int, tempo_resposta: float) -> None:
    """
    Registra chamada para API externa
    
    Args:
        api (str): Nome da API
        endpoint (str): Endpoint chamado
        status_code (int): Código de status HTTP
        tempo_resposta (float): Tempo de resposta em segundos
    """
    logger = setup_logger()
    
    mensagem = f"API {api} - Endpoint: {endpoint} - Status: {status_code} - Tempo: {tempo_resposta:.2f}s"
    
    if 200 <= status_code < 300:
        logger.info(mensagem)
    elif 400 <= status_code < 500:
        logger.warning(mensagem)
    else:
        logger.error(mensagem)


def log_error(erro: Exception, contexto: str = "") -> None:
    """
    Registra erro com contexto
    
    Args:
        erro (Exception): Exceção ocorrida
        contexto (str): Contexto onde ocorreu o erro
    """
    logger = setup_logger()
    
    mensagem = f"Erro: {str(erro)}"
    if contexto:
        mensagem = f"{contexto} - {mensagem}"
    
    logger.error(mensagem, exc_info=True)


# Logger global
logger = setup_logger()