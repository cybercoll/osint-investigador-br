# Exemplo de Uso - API Avançada

Este documento demonstra como usar a classe `OSINTInvestigador` para consultas programáticas avançadas.

## 🚀 Inicialização

```python
from osint_investigador import OSINTInvestigador

# Inicializar com configurações padrão
osint = OSINTInvestigador()

# Inicializar com cache desabilitado
osint = OSINTInvestigador(use_cache=False)

# Inicializar com timeout personalizado
osint = OSINTInvestigador(timeout=10)
```

## 📍 Consulta de CEP

### Uso Básico

```python
# Consulta simples
resultado = osint.consultar_cep("01310-100")

if resultado['success']:
    dados = resultado['data']
    print(f"Endereço: {dados['logradouro']}")
    print(f"Bairro: {dados['bairro']}")
    print(f"Cidade: {dados['localidade']}")
    print(f"UF: {dados['uf']}")
else:
    print(f"Erro: {resultado['message']}")
```

### Consulta em Lote

```python
ceps = ["01310-100", "20040-020", "30112-000"]
resultados = []

for cep in ceps:
    resultado = osint.consultar_cep(cep)
    if resultado['success']:
        resultados.append(resultado['data'])
    else:
        print(f"Erro no CEP {cep}: {resultado['message']}")

print(f"Consultados {len(resultados)} CEPs com sucesso")
```

### Análise de Região

```python
def analisar_regiao_por_ceps(ceps):
    """Analisa uma região baseada em uma lista de CEPs"""
    regioes = {}
    
    for cep in ceps:
        resultado = osint.consultar_cep(cep)
        if resultado['success']:
            dados = resultado['data']
            uf = dados['uf']
            cidade = dados['localidade']
            
            if uf not in regioes:
                regioes[uf] = set()
            regioes[uf].add(cidade)
    
    return {uf: list(cidades) for uf, cidades in regioes.items()}

# Exemplo de uso
ceps_investigacao = ["01310-100", "01310-200", "20040-020"]
analise = analisar_regiao_por_ceps(ceps_investigacao)
print("Análise regional:", analise)
```

## 📞 Consulta de DDD

### Uso Básico

```python
# Consulta de DDD
resultado = osint.consultar_ddd("11")

if resultado['success']:
    dados = resultado['data']
    print(f"Estado: {dados['state']}")
    print(f"Cidades: {', '.join(dados['cities'])}")
else:
    print(f"Erro: {resultado['message']}")
```

### Mapeamento de DDDs por Estado

```python
def mapear_ddds_brasil():
    """Mapeia todos os DDDs do Brasil por estado"""
    ddds_brasil = range(11, 100)  # DDDs válidos no Brasil
    mapa_estados = {}
    
    for ddd in ddds_brasil:
        resultado = osint.consultar_ddd(str(ddd))
        if resultado['success']:
            estado = resultado['data']['state']
            if estado not in mapa_estados:
                mapa_estados[estado] = []
            mapa_estados[estado].append(ddd)
    
    return mapa_estados

# Executar mapeamento (pode demorar devido ao cache)
mapa = mapear_ddds_brasil()
for estado, ddds in mapa.items():
    print(f"{estado}: {ddds}")
```

## 🏢 Consulta de CNPJ

### Uso Básico

```python
# Consulta via Brasil API (padrão)
resultado = osint.consultar_cnpj("11222333000181")

# Consulta via ReceitaWS
resultado = osint.consultar_cnpj("11222333000181", fonte="receitaws")

if resultado['success']:
    dados = resultado['data']
    print(f"Razão Social: {dados.get('razao_social', dados.get('nome'))}")
    print(f"CNPJ: {dados['cnpj']}")
    print(f"Situação: {dados.get('descricao_situacao_cadastral', dados.get('situacao'))}")
else:
    print(f"Erro: {resultado['message']}")
```

### Comparação de Fontes

```python
def comparar_fontes_cnpj(cnpj):
    """Compara dados de CNPJ entre diferentes fontes"""
    fontes = ['brasilapi', 'receitaws']
    resultados = {}
    
    for fonte in fontes:
        resultado = osint.consultar_cnpj(cnpj, fonte=fonte)
        if resultado['success']:
            resultados[fonte] = resultado['data']
        else:
            resultados[fonte] = {'erro': resultado['message']}
    
    return resultados

# Exemplo de uso
cnpj = "11222333000181"
comparacao = comparar_fontes_cnpj(cnpj)

for fonte, dados in comparacao.items():
    print(f"\n=== {fonte.upper()} ===")
    if 'erro' in dados:
        print(f"Erro: {dados['erro']}")
    else:
        print(f"Razão Social: {dados.get('razao_social', dados.get('nome'))}")
        print(f"Situação: {dados.get('descricao_situacao_cadastral', dados.get('situacao'))}")
```

### Análise de Lista de CNPJs

```python
def analisar_lista_cnpjs(cnpjs):
    """Analisa uma lista de CNPJs e gera relatório"""
    relatorio = {
        'total': len(cnpjs),
        'sucessos': 0,
        'erros': 0,
        'ativos': 0,
        'inativos': 0,
        'empresas': []
    }
    
    for cnpj in cnpjs:
        resultado = osint.consultar_cnpj(cnpj)
        if resultado['success']:
            relatorio['sucessos'] += 1
            dados = resultado['data']
            
            # Verificar se está ativo (pode variar por fonte)
            situacao = dados.get('descricao_situacao_cadastral', dados.get('situacao', ''))
            if 'ativa' in situacao.lower():
                relatorio['ativos'] += 1
            else:
                relatorio['inativos'] += 1
            
            relatorio['empresas'].append({
                'cnpj': cnpj,
                'nome': dados.get('razao_social', dados.get('nome')),
                'situacao': situacao
            })
        else:
            relatorio['erros'] += 1
    
    return relatorio

# Exemplo de uso
cnpjs_investigacao = ["11222333000181", "00000000000191"]
relatorio = analisar_lista_cnpjs(cnpjs_investigacao)

print(f"Total: {relatorio['total']}")
print(f"Sucessos: {relatorio['sucessos']}")
print(f"Erros: {relatorio['erros']}")
print(f"Ativos: {relatorio['ativos']}")
print(f"Inativos: {relatorio['inativos']}")
```

## 🏦 Consulta de Bancos

### Listar Todos os Bancos

```python
# Listar todos os bancos
resultado = osint.listar_bancos()

if resultado['success']:
    bancos = resultado['data']
    print(f"Total de bancos: {len(bancos)}")
    
    # Mostrar os 10 primeiros
    for banco in bancos[:10]:
        print(f"{banco['code']} - {banco['name']}")
else:
    print(f"Erro: {resultado['message']}")
```

### Buscar Banco Específico

```python
# Buscar banco por código
resultado = osint.consultar_banco("001")

if resultado['success']:
    banco = resultado['data']
    print(f"Código: {banco['code']}")
    print(f"Nome: {banco['name']}")
    print(f"Nome Completo: {banco['fullName']}")
else:
    print(f"Erro: {resultado['message']}")
```

### Análise de Bancos por Tipo

```python
def analisar_tipos_bancos():
    """Analisa tipos de bancos baseado nos nomes"""
    resultado = osint.listar_bancos()
    
    if not resultado['success']:
        return None
    
    bancos = resultado['data']
    tipos = {
        'publicos': [],
        'privados': [],
        'cooperativas': [],
        'digitais': [],
        'outros': []
    }
    
    palavras_publico = ['banco do brasil', 'caixa', 'bndes', 'banco central']
    palavras_cooperativa = ['cooperativa', 'coop', 'sicredi', 'sicoob']
    palavras_digital = ['nubank', 'inter', 'original', 'neon', 'c6']
    
    for banco in bancos:
        nome_lower = banco['name'].lower()
        
        if any(palavra in nome_lower for palavra in palavras_publico):
            tipos['publicos'].append(banco)
        elif any(palavra in nome_lower for palavra in palavras_cooperativa):
            tipos['cooperativas'].append(banco)
        elif any(palavra in nome_lower for palavra in palavras_digital):
            tipos['digitais'].append(banco)
        else:
            tipos['outros'].append(banco)
    
    return tipos

# Executar análise
analise = analisar_tipos_bancos()
if analise:
    for tipo, lista in analise.items():
        print(f"{tipo.capitalize()}: {len(lista)} bancos")
```

## 🏙️ Consulta de Municípios

### Listar Municípios por Estado

```python
# Consultar municípios de São Paulo
resultado = osint.consultar_municipios_uf("SP")

if resultado['success']:
    municipios = resultado['data']
    print(f"São Paulo tem {len(municipios)} municípios")
    
    # Mostrar os 10 primeiros
    for municipio in municipios[:10]:
        print(f"{municipio['codigo_ibge']} - {municipio['nome']}")
else:
    print(f"Erro: {resultado['message']}")
```

### Análise Demográfica por Região

```python
def analisar_municipios_regiao(ufs):
    """Analisa municípios de uma região"""
    analise = {
        'total_municipios': 0,
        'por_estado': {},
        'maiores_cidades': []
    }
    
    for uf in ufs:
        resultado = osint.consultar_municipios_uf(uf)
        if resultado['success']:
            municipios = resultado['data']
            analise['por_estado'][uf] = len(municipios)
            analise['total_municipios'] += len(municipios)
            
            # Adicionar algumas cidades grandes (baseado no nome)
            cidades_grandes = [m for m in municipios if any(
                palavra in m['nome'].lower() 
                for palavra in ['são paulo', 'rio de janeiro', 'belo horizonte', 
                               'salvador', 'brasília', 'fortaleza', 'recife']
            )]
            analise['maiores_cidades'].extend(cidades_grandes)
    
    return analise

# Analisar região Sudeste
sudeste = ['SP', 'RJ', 'MG', 'ES']
analise_sudeste = analisar_municipios_regiao(sudeste)

print(f"Total de municípios no Sudeste: {analise_sudeste['total_municipios']}")
print("Por estado:")
for uf, total in analise_sudeste['por_estado'].items():
    print(f"  {uf}: {total} municípios")
```

## 🗄️ Gerenciamento de Cache

### Estatísticas do Cache

```python
# Obter estatísticas do cache
stats = osint.obter_estatisticas_cache()

print(f"Total de entradas: {stats['total_entries']}")
print(f"Entradas válidas: {stats['valid_entries']}")
print(f"Entradas expiradas: {stats['expired_entries']}")
print(f"Tamanho do cache: {stats['cache_size']} bytes")
```

### Limpeza do Cache

```python
# Limpar todo o cache
resultado = osint.limpar_cache()

if resultado['success']:
    print("Cache limpo com sucesso")
else:
    print(f"Erro ao limpar cache: {resultado['message']}")

# Limpar apenas entradas expiradas
resultado = osint.limpar_cache_expirado()
print(f"Entradas expiradas removidas: {resultado.get('removed_count', 0)}")
```

## 🔄 Processamento em Lote

### Exemplo Completo de Investigação

```python
def investigacao_completa(dados_entrada):
    """
    Realiza investigação completa com múltiplas fontes
    
    dados_entrada = {
        'ceps': ['01310-100', '20040-020'],
        'ddds': ['11', '21'],
        'cnpjs': ['11222333000181']
    }
    """
    relatorio = {
        'enderecos': [],
        'telefones': [],
        'empresas': [],
        'resumo': {}
    }
    
    # Processar CEPs
    if 'ceps' in dados_entrada:
        for cep in dados_entrada['ceps']:
            resultado = osint.consultar_cep(cep)
            if resultado['success']:
                relatorio['enderecos'].append(resultado['data'])
    
    # Processar DDDs
    if 'ddds' in dados_entrada:
        for ddd in dados_entrada['ddds']:
            resultado = osint.consultar_ddd(ddd)
            if resultado['success']:
                relatorio['telefones'].append(resultado['data'])
    
    # Processar CNPJs
    if 'cnpjs' in dados_entrada:
        for cnpj in dados_entrada['cnpjs']:
            resultado = osint.consultar_cnpj(cnpj)
            if resultado['success']:
                relatorio['empresas'].append(resultado['data'])
    
    # Gerar resumo
    relatorio['resumo'] = {
        'total_enderecos': len(relatorio['enderecos']),
        'total_telefones': len(relatorio['telefones']),
        'total_empresas': len(relatorio['empresas']),
        'estados_identificados': list(set([
            end['uf'] for end in relatorio['enderecos']
        ] + [
            tel['state'] for tel in relatorio['telefones']
        ]))
    }
    
    return relatorio

# Exemplo de uso
dados = {
    'ceps': ['01310-100', '20040-020'],
    'ddds': ['11', '21'],
    'cnpjs': ['11222333000181']
}

relatorio_completo = investigacao_completa(dados)
print("Relatório de Investigação:")
print(f"Endereços encontrados: {relatorio_completo['resumo']['total_enderecos']}")
print(f"Telefones analisados: {relatorio_completo['resumo']['total_telefones']}")
print(f"Empresas consultadas: {relatorio_completo['resumo']['total_empresas']}")
print(f"Estados identificados: {', '.join(relatorio_completo['resumo']['estados_identificados'])}")
```

## 🔧 Configurações Avançadas

### Personalização de Timeout

```python
# Configurar timeout específico para consultas lentas
osint_lento = OSINTInvestigador(timeout=30)

# Para consultas rápidas
osint_rapido = OSINTInvestigador(timeout=5)
```

### Desabilitar Cache Temporariamente

```python
# Consulta sem usar cache (sempre busca na API)
resultado = osint.consultar_cep("01310-100", use_cache=False)
```

### Logging Personalizado

```python
import logging

# Configurar nível de log mais detalhado
logging.getLogger('osint_investigador').setLevel(logging.DEBUG)

# Agora todas as operações serão logadas em detalhes
resultado = osint.consultar_cnpj("11222333000181")
```

---

**💡 Dica**: Use essas funções avançadas para criar seus próprios scripts de investigação personalizados!