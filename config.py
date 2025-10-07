"""
Configurações do OSINT Investigador BR
"""
import os
from dotenv import load_dotenv

load_dotenv()

# URLs das APIs
VIACEP_URL = "https://viacep.com.br/ws/{}/json/"
BRASILAPI_CEP_V1_URL = "https://brasilapi.com.br/api/cep/v1/{}"
BRASILAPI_CEP_V2_URL = "https://brasilapi.com.br/api/cep/v2/{}"
OPENCEP_URL = "https://opencep.com/v1/{}.json"
APICEP_URL = "https://cdn.apicep.com/file/apicep/{}.json"
BRASILAPI_DDD_URL = "https://brasilapi.com.br/api/ddd/v1/{}"
BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/{}"
BRASILAPI_BANKS_URL = "https://brasilapi.com.br/api/banks/v1"
BRASILAPI_IBGE_URL = "https://brasilapi.com.br/api/ibge/municipios/v1/{}"
RECEITAWS_CNPJ_URL = "https://www.receitaws.com.br/v1/cnpj/{}"
CNPJA_URL = "https://open.cnpja.com/office/{}"

# APIs de Bancos Internacionais
API_NINJAS_SWIFT_URL = "https://api.api-ninjas.com/v1/swiftcode"
API_NINJAS_KEY = os.getenv('API_NINJAS_KEY', '')  # Chave da API Ninjas (opcional)

# APIs de Investigação e Dados Pessoais
DIRECT_DATA_API_URL = "https://apiv3.directd.com.br/api/RegistrationDataBrazil"
DIRECT_DATA_TOKEN = os.getenv('DIRECT_DATA_TOKEN', '')  # Token da Direct Data API

ASSERTIVA_LOCALIZE_API_URL = "https://api.assertivasolucoes.com.br/localize"
ASSERTIVA_LOCALIZE_TOKEN = os.getenv('ASSERTIVA_LOCALIZE_TOKEN', '')  # Token da Assertiva Localize

DESK_DATA_API_URL = "https://api.deskdata.com.br"
DESK_DATA_TOKEN = os.getenv('DESK_DATA_TOKEN', '')  # Token da Desk Data

ANTIFRAUDEBRASIL_API_URL = "https://api.antifraudebrasil.com"
ANTIFRAUDEBRASIL_TOKEN = os.getenv('ANTIFRAUDEBRASIL_TOKEN', '')  # Token da AntiFraudeBrasil

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