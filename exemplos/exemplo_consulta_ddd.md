# Exemplo de Uso: Consulta de DDD

Este exemplo demonstra como utilizar o script `consulta_ddd.py` para obter informações de estado e cidades associadas a um Código de Discagem Direta (DDD).

## Pré-requisitos

Certifique-se de ter o Python instalado em seu sistema e a biblioteca `requests`. Caso não tenha, instale-a com o seguinte comando:

```bash
pip install requests
```

## Como usar

1. Navegue até o diretório `scripts/` do projeto:

   ```bash
   cd osint-investigador-br/scripts/
   ```

2. Execute o script `consulta_ddd.py` e forneça o DDD quando solicitado:

   ```bash
   python3 consulta_ddd.py
   ```

   Ou, se você tornou o script executável:

   ```bash
   ./consulta_ddd.py
   ```

## Exemplo de Execução

```bash
ubuntu@sandbox:~/osint-investigador-br/scripts$ python3 consulta_ddd.py
Digite o DDD para consulta: 11
--- Dados do DDD ---
Estado: SP
Cidades:
- EMBU
- VARZEA PAULISTA
- VARGEM GRANDE PAULISTA
- ITUPEVA
- JUNDIAI
- CABREUVA
- CAIEIRAS
- FRANCO DA ROCHA
- MAIRIPORA
- CAMPO LIMPO PAULISTA
- ITATIBA
- LOUVEIRA
- VINHEDO
- CAMPINAS
- SUMARE
- HORTOLANDIA
- MONTE MOR
- INDAIATUBA
- SALTO
- ITU
- PORTO FELIZ
- SOROCABA
- VOTORANTIM
- SAO ROQUE
- MAIRINQUE
- ALUMÍNIO
- ARACOIABA DA SERRA
- BOITUVA
- TATUI
- CERQUILHO
- TIETE
- LARANJAL PAULISTA
- PIRACICABA
- RIO CLARO
- LIMEIRA
- AMERICANA
- SANTA BARBARA D'OESTE
- NOVA ODESSA
- PAULINIA
- COSMOPOLIS
- ARTUR NOGUEIRA
- JAGUARIUNA
- PEDREIRA
- MORUNGABA
- BRAGANCA PAULISTA
- ATIBAIA
- NAZARE PAULISTA
- PIRACAIA
- JARINU
- VARGEM
- SAO PAULO
```

## Exemplo com DDD inválido

```bash
ubuntu@sandbox:~/osint-investigador-br/scripts$ python3 consulta_ddd.py
Digite o DDD para consulta: 00
DDD 00 não encontrado.
```
