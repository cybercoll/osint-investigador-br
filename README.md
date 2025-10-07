# OSINT Investigador BR

Uma ferramenta completa e robusta para investigações OSINT (Open Source Intelligence) focada em fontes brasileiras. Este projeto oferece uma interface web moderna, scripts Python avançados e recursos para coleta ética de informações públicas sobre CEP, DDD, CNPJ, bancos e municípios.

## 🌟 Principais Funcionalidades

- **Interface Web Moderna**: Interface responsiva com Bootstrap 5
- **Consulta de CEP**: Busca completa de endereços via ViaCEP
- **Consulta de DDD**: Identificação de estados e cidades por código de área
- **Consulta de CNPJ**: Informações empresariais via Brasil API e ReceitaWS
- **Bancos Brasileiros**: Lista completa de instituições financeiras
- **Municípios IBGE**: Consulta de municípios por estado
- **Sistema de Cache**: Cache inteligente para otimizar consultas
- **Exportação de Dados**: Suporte a JSON e CSV
- **Logging Completo**: Auditoria de todas as operações
- **Validação Avançada**: Validação e formatação automática de dados

## 📁 Estrutura do Projeto

```
osint-investigador-br/
├── web_app.py                    # Aplicação Flask principal
├── osint_investigador.py         # Classe principal para consultas
├── config.py                     # Configurações centralizadas
├── requirements.txt              # Dependências do projeto
├── utils/
│   ├── __init__.py
│   ├── validators.py             # Validação de dados brasileiros
│   ├── cache.py                  # Sistema de cache
│   └── logger.py                 # Sistema de logging
├── templates/
│   └── index.html                # Interface web moderna
├── static/
│   └── js/
│       └── app.js                # JavaScript da interface
├── scripts/                      # Scripts originais (mantidos)
│   ├── consulta_cep.py
│   └── consulta_ddd.py
├── exemplos/                     # Documentação e exemplos
├── logs/                         # Arquivos de log
├── cache/                        # Arquivos de cache
├── bookmarks.md                  # Links úteis para OSINT
├── fontes.md                     # Documentação das fontes
└── README.md                     # Este arquivo
```

## 🚀 Instalação e Uso

### 1. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Interface Web

```bash
python web_app.py
```

Acesse: `http://localhost:5000`

### 3. Usar via Linha de Comando

```python
from osint_investigador import OSINTInvestigador

# Inicializar
osint = OSINTInvestigador()

# Consultar CEP
resultado = osint.consultar_cep("01310-100")

# Consultar DDD
resultado = osint.consultar_ddd("11")

# Consultar CNPJ
resultado = osint.consultar_cnpj("11222333000181")

# Listar bancos
bancos = osint.listar_bancos()

# Consultar municípios
municipios = osint.consultar_municipios_uf("SP")
```

## 🎯 APIs e Fontes de Dados

### APIs Utilizadas:
- **ViaCEP**: Consulta de endereços por CEP
- **Brasil API**: DDD, CNPJ, bancos e municípios IBGE
- **ReceitaWS**: Consulta alternativa de CNPJ

### Funcionalidades por API:

| Funcionalidade | API Principal | API Alternativa | Cache | Validação |
|---------------|---------------|-----------------|-------|-----------|
| CEP | ViaCEP | - | ✅ | ✅ |
| DDD | Brasil API | - | ✅ | ✅ |
| CNPJ | Brasil API | ReceitaWS | ✅ | ✅ |
| Bancos | Brasil API | - | ✅ | - |
| Municípios | Brasil API | - | ✅ | ✅ |

## 🔧 Configurações Avançadas

### Cache
- **Localização**: `./cache/`
- **Tempo de vida**: 24 horas (configurável)
- **Formato**: JSON
- **Limpeza automática**: Entradas expiradas

### Logging
- **Localização**: `./logs/`
- **Níveis**: INFO, WARNING, ERROR
- **Rotação**: Diária
- **Auditoria**: Todas as consultas são registradas

### Validação
- **CEP**: Formato brasileiro (00000-000)
- **DDD**: Códigos válidos (11-99)
- **CNPJ**: Validação de formato e dígitos verificadores
- **UF**: Estados brasileiros válidos

## 🌐 Interface Web

### Características:
- **Design Responsivo**: Compatível com desktop e mobile
- **Navegação por Abas**: Organização intuitiva das funcionalidades
- **Feedback Visual**: Loading states e mensagens de erro/sucesso
- **Exportação**: Download direto em JSON ou CSV
- **Gerenciamento de Cache**: Visualização e limpeza via interface

### Endpoints da API:
- `GET /api/cep/<cep>` - Consulta CEP
- `GET /api/ddd/<ddd>` - Consulta DDD
- `GET /api/cnpj/<cnpj>` - Consulta CNPJ
- `GET /api/bancos` - Lista bancos
- `GET /api/bancos/<codigo>` - Busca banco específico
- `GET /api/municipios/<uf>` - Lista municípios por UF
- `GET /api/cache/stats` - Estatísticas do cache
- `POST /api/cache/clear` - Limpar cache
- `POST /api/export` - Exportar dados

## ⚖️ Aspectos Éticos e Legais

Este projeto foi desenvolvido com foco na **investigação OSINT** e **coleta de dados públicos**.

### Princípios:
- ✅ **Dados Públicos**: Uso exclusivo de informações públicas
- ✅ **APIs Oficiais**: Apenas fontes confiáveis e autorizadas
- ✅ **Investigação**: Ferramenta para pesquisa e análise OSINT
- ✅ **Transparência**: Código aberto e auditável
- ✅ **Rate Limiting**: Respeito aos limites das APIs
- ✅ **Auditoria**: Log completo de todas as operações

### Limitações Éticas:
- ❌ Não consulta CPF (dados pessoais sensíveis)
- ❌ Não acessa redes sociais via API (termos de serviço)
- ❌ Não armazena dados pessoais permanentemente
- ❌ Não realiza scraping não autorizado

## 📊 Monitoramento e Performance

### Métricas Disponíveis:
- **Cache Hit Rate**: Taxa de acerto do cache
- **Tempo de Resposta**: Latência das consultas
- **Uso de APIs**: Contadores por fonte de dados
- **Erros**: Tracking de falhas e exceções

### Otimizações:
- **Cache Inteligente**: Reduz chamadas desnecessárias às APIs
- **Validação Prévia**: Evita consultas inválidas
- **Timeout Configurável**: Controle de tempo limite
- **Retry Logic**: Tentativas automáticas em caso de falha

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. **Fork** o projeto
2. **Crie** uma branch para sua feature
3. **Mantenha** o foco na ética e legalidade
4. **Teste** suas alterações
5. **Envie** um Pull Request

### Diretrizes:
- Respeite os princípios éticos do projeto
- Documente novas funcionalidades
- Inclua testes quando aplicável

## 📄 Licença

Este projeto é disponibilizado para fins **educacionais** e de **pesquisa**. Use com responsabilidade e ética.

## 🆘 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma **Issue** no GitHub
- Consulte a **documentação** na pasta `exemplos/`
- Verifique os **logs** em caso de erros

---

**⚠️ Aviso Legal**: Esta ferramenta deve ser usada apenas para fins legítimos e éticos. O usuário é responsável pelo uso adequado e pelo cumprimento das leis aplicáveis.

## Uso dos Scripts Adicionais

### Consulta de CEP
