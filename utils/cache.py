import time
from typing import Any, Optional, Dict
from threading import Lock

try:
    from config import CACHE_ENABLED, CACHE_TIMEOUT
except ImportError:
    CACHE_ENABLED = True
    CACHE_TIMEOUT = 3600

class SimpleCache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        if not CACHE_ENABLED:
            return None
            
        with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                
                if time.time() > entry['expires_at']:
                    del self._cache[key]
                    return None
                
                entry['last_accessed'] = time.time()
                return entry['value']
            
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if not CACHE_ENABLED:
            return
            
        if ttl is None:
            ttl = CACHE_TIMEOUT
            
        with self._lock:
            self._cache[key] = {
                'value': value,
                'created_at': time.time(),
                'last_accessed': time.time(),
                'expires_at': time.time() + ttl
            }
    
    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> int:
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count
    
    def cleanup_expired(self) -> int:
        if not CACHE_ENABLED:
            return 0
            
        current_time = time.time()
        expired_keys = []
        
        with self._lock:
            for key, entry in self._cache.items():
                if current_time > entry['expires_at']:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            current_time = time.time()
            total_items = len(self._cache)
            expired_items = 0
            
            for entry in self._cache.values():
                if current_time > entry['expires_at']:
                    expired_items += 1
            
            return {
                'enabled': CACHE_ENABLED,
                'total_items': total_items,
                'active_items': total_items - expired_items,
                'expired_items': expired_items,
                'default_ttl': CACHE_TIMEOUT
            }
    
    def has_key(self, key: str) -> bool:
        return self.get(key) is not None

cache = SimpleCache()