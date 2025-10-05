# Exemplo de Uso: Consulta de CEP

Este exemplo demonstra como utilizar o script `consulta_cep.py` para obter informações de endereço a partir de um Código de Endereçamento Postal (CEP).

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

2. Execute o script `consulta_cep.py` e forneça o CEP quando solicitado:

   ```bash
   python3 consulta_cep.py
   ```

   Ou, se você tornou o script executável:

   ```bash
   ./consulta_cep.py
   ```

## Exemplo de Execução

```bash
ubuntu@sandbox:~/osint-investigador-br/scripts$ python3 consulta_cep.py
Digite o CEP para consulta: 01001000
--- Dados do CEP ---
Cep: 01001-000
Logradouro: Praça da Sé
Complemento: lado ímpar
Bairro: Sé
Localidade: São Paulo
Uf: SP
Ibge: 3550308
Gia: 1004
Ddd: 11
Siafi: 7107
```

## Exemplo com CEP inválido

```bash
ubuntu@sandbox:~/osint-investigador-br/scripts$ python3 consulta_cep.py
Digite o CEP para consulta: 99999999
CEP 99999999 não encontrado.
```
