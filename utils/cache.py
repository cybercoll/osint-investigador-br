"""
Sistema de cache simples para consultas OSINT
"""
import json
import os
import time
from typing import Any, Optional
from config import CACHE_ENABLED, CACHE_TIMEOUT


class SimpleCache:
    """Cache simples baseado em arquivos"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self.enabled = CACHE_ENABLED
        self.timeout = CACHE_TIMEOUT
        
        # Cria diretório de cache se não existir
        if self.enabled and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _get_cache_file(self, key: str) -> str:
        """Gera nome do arquivo de cache"""
        # Substitui caracteres especiais por underscore
        safe_key = "".join(c if c.isalnum() else "_" for c in key)
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Recupera valor do cache
        
        Args:
            key (str): Chave do cache
            
        Returns:
            Optional[Any]: Valor do cache ou None se não encontrado/expirado
        """
        if not self.enabled:
            return None
        
        cache_file = self._get_cache_file(key)
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Verifica se o cache expirou
            if time.time() - cache_data['timestamp'] > self.timeout:
                os.remove(cache_file)
                return None
            
            return cache_data['data']
        
        except (json.JSONDecodeError, KeyError, OSError):
            # Remove arquivo corrompido
            try:
                os.remove(cache_file)
            except OSError:
                pass
            return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Armazena valor no cache
        
        Args:
            key (str): Chave do cache
            value (Any): Valor a ser armazenado
        """
        if not self.enabled:
            return
        
        cache_file = self._get_cache_file(key)
        
        cache_data = {
            'timestamp': time.time(),
            'data': value
        }
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass  # Falha silenciosa se não conseguir escrever
    
    def clear(self) -> None:
        """Remove todos os arquivos de cache"""
        if not self.enabled or not os.path.exists(self.cache_dir):
            return
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except OSError:
            pass
    
    def clear_expired(self) -> None:
        """Remove apenas arquivos de cache expirados"""
        if not self.enabled or not os.path.exists(self.cache_dir):
            return
        
        current_time = time.time()
        
        try:
            for filename in os.listdir(self.cache_dir):
                if not filename.endswith('.json'):
                    continue
                
                filepath = os.path.join(self.cache_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        cache_data = json.load(f)
                    
                    if current_time - cache_data['timestamp'] > self.timeout:
                        os.remove(filepath)
                
                except (json.JSONDecodeError, KeyError, OSError):
                    # Remove arquivo corrompido
                    try:
                        os.remove(filepath)
                    except OSError:
                        pass
        
        except OSError:
            pass


# Instância global do cache
cache = SimpleCache()