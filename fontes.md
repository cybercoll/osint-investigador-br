# Fontes e APIs Utilizadas

Este documento detalha as fontes de dados e APIs utilizadas no projeto OSINT Investigador BR, com foco em fontes públicas brasileiras.

## 1. ViaCEP

- **Descrição:** Serviço web gratuito e de alto desempenho para consulta de Código de Endereçamento Postal (CEP) do Brasil.
- **URL:** [https://viacep.com.br/](https://viacep.com.br/)
- **Tipo:** API RESTful
- **Uso:** Utilizado para obter informações de endereço (logradouro, bairro, cidade, estado) a partir de um CEP.
- **Exemplo de Requisição (GET):** `https://viacep.com.br/ws/{cep}/json/`
- **Exemplo de Resposta (JSON):**
```json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "complemento": "lado ímpar",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP",
  "ibge": "3550308",
  "gia": "1004",
  "ddd": "11",
  "siafi": "7107"
}
```
- **Observações:** Não requer autenticação. Ideal para consultas de CEP individuais. O script `consulta_cep.py` utiliza esta API.




## 2. Consulta de CPF

- **Status:** Não foi encontrada uma API pública e gratuita na Brasil API ou em outras fontes pesquisadas que permita a consulta de dados de CPF de forma irrestrita e legal para o público em geral. As APIs existentes geralmente são pagas, restritas a órgãos governamentais ou empresas com permissão específica para acesso a dados fiscais.
- **Observações:** A consulta de CPF é um dado sensível e protegido pela Lei Geral de Proteção de Dados (LGPD) no Brasil. Qualquer ferramenta que ofereça consulta de CPF deve estar em conformidade com a legislação e ter uma base legal para o tratamento desses dados. Para este projeto, focaremos em dados públicos que não violem a LGPD.



## 3. Brasil API - DDD

- **Descrição:** Permite consultar informações sobre um código DDD (Discagem Direta à Distância) específico, retornando o estado correspondente e a lista completa de cidades que utilizam esse código de área.
- **URL:** [https://brasilapi.com.br/docs#tag/DDD](https://brasilapi.com.br/docs#tag/DDD)
- **Tipo:** API RESTful
- **Uso:** Pode ser utilizada para inferir a localização geográfica de um número de telefone a partir do seu DDD. Não fornece dados do titular do telefone.
- **Exemplo de Requisição (GET):** `https://brasilapi.com.br/api/ddd/v1/{ddd}`
- **Exemplo de Resposta (JSON):**
```json
{
  "state": "SP",
  "cities": [
    "EMBU",
    "VARZEA PAULISTA",
    "VARGEM GRANDE PAULISTA",
    "ITUPEVA",
    "JUNDIAI",
    "CABREUVA",
    "CAIEIRAS",
    "FRANCO DA ROCHA",
    "MAIRIPORA",
    "CAMPO LIMPO PAULISTA",
    "ITATIBA",
    "LOUVEIRA",
    "VINHEDO",
    "VALINHOS",
    "CAMPINAS",
    "SUMARE",
    "HORTOLANDIA",
    "MONTE MOR",
    "INDAIATUBA",
    "SALTO",
    "ITU",
    "PORTO FELIZ",
    "SOROCABA",
    "VOTORANTIM",
    "SAO ROQUE",
    "MAIRINQUE",
    "ALUMÍNIO",
    "ARACOIABA DA SERRA",
    "BOITUVA",
    "TATUI",
    "CERQUILHO",
    "TIETE",
    "LARANJAL PAULISTA",
    "PIRACICABA",
    "RIO CLARO",
    "LIMEIRA",
    "AMERICANA",
    "SANTA BARBARA D'OESTE",
    "NOVA ODESSA",
    "PAULINIA",
    "COSMOPOLIS",
    "ARTUR NOGUEIRA",
    "JAGUARIUNA",
    "PEDREIRA",
    "MORUNGABA",
    "BRAGANCA PAULISTA",
    "ATIBAIA",
    "NAZARE PAULISTA",
    "PIRACAIA",
    "JARINU",
    "VARGEM",
    "SAO PAULO"
  ]
}
```
- **Observações:** Não há uma API pública e gratuita que permita a consulta de dados do titular de um número de telefone no Brasil, devido à proteção de dados pessoais. O foco será em informações publicamente disponíveis e legais.


n## 4. Redes Sociaisn
- **Descrição:** A coleta de dados de redes sociais é uma parte crucial da investigação OSINT. No entanto, a maioria das plataformas (LinkedIn, Instagram, Twitter/X, etc.) possui APIs restritas que não permitem a extração em massa de dados de perfis de usuários para fins de investigação pública e gratuita. As buscas geralmente são manuais ou utilizam ferramentas específicas que podem ter limitações.
- **Fontes e Ferramentas (Manuais/Externas):**
  - **LinkedIn:** É possível realizar buscas por cargos, empresas e localidades. A URL pode ser manipulada para buscas específicas: `https://www.linkedin.com/jobs/search/?keywords=SEU_ALVO&location=Brasil`
  - **Instagram:** A busca por imagens e perfis pode ser feita diretamente na plataforma. Ferramentas externas como o `aware-online.com` oferecem funcionalidades de busca, mas devem ser usadas com cautela e em conformidade com os termos de serviço.
  - **Twitter/X:** A busca avançada da plataforma é uma ferramenta poderosa para filtrar tweets por palavras-chave, datas, localização e idioma. Exemplo de URL de busca: `https://twitter.com/search?q=seu_alvo+lang%3Apt&src=typed_query`
- **Observações:** A automação da coleta de dados de redes sociais frequentemente viola os termos de serviço das plataformas. A abordagem para este projeto será focar em técnicas de busca manual e na documentação de como utilizar as ferramentas de busca das próprias plataformas de forma eficaz e ética, sem o uso de scripts automatizados que possam ser considerados abusivos.

