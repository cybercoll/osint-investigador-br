"""
Configurações do OSINT Investigador BR
"""
import os
from dotenv import load_dotenv

load_dotenv()

# URLs das APIs
VIACEP_URL = "https://viacep.com.br/ws/{}/json/"
BRASILAPI_DDD_URL = "https://brasilapi.com.br/api/ddd/v1/{}"
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/{}"
BRASILAPI_BANKS_URL = "https://brasilapi.com.br/api/banks/v1"
BRASILAPI_IBGE_URL = "https://brasilapi.com.br/api/ibge/municipios/v1/{}"
RECEITAWS_CNPJ_URL = "https://www.receitaws.com.br/v1/cnpj/{}"

# Configurações de Cache
CACHE_ENABLED = True
CACHE_TIMEOUT = 3600  # 1 hora em segundos

# Configurações de Logging
LOG_LEVEL = "INFO"
LOG_FILE = "osint_investigador.log"

# Configurações da API Web
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
FLASK_DEBUG = False

# Rate Limiting
RATE_LIMIT_REQUESTS = 60  # requests por minuto
RATE_LIMIT_WINDOW = 60    # janela em segundos

# Timeouts
REQUEST_TIMEOUT = 10  # segundos