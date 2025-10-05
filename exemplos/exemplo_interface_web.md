# Exemplo de Uso - Interface Web

Este documento demonstra como usar a interface web moderna do OSINT Investigador BR.

## 🌐 Acessando a Interface Web

### 1. Iniciar o Servidor

```bash
# No diretório do projeto
python web_app.py
```

### 2. Acessar no Navegador

Abra seu navegador e acesse: `http://localhost:5000`

## 🎯 Funcionalidades da Interface

### Consulta de CEP

1. **Acesse a aba "CEP"**
2. **Digite o CEP** no formato `00000-000` (a máscara é aplicada automaticamente)
3. **Clique em "Consultar"**
4. **Visualize os resultados** com informações completas do endereço
5. **Exporte os dados** em JSON ou CSV se necessário

**Exemplo de CEP**: `01310-100` (Av. Paulista, São Paulo)

### Consulta de DDD

1. **Acesse a aba "DDD"**
2. **Digite o código DDD** (apenas números, máximo 2 dígitos)
3. **Clique em "Consultar"**
4. **Visualize o estado e cidades** associadas ao DDD
5. **Exporte os dados** se necessário

**Exemplo de DDD**: `11` (São Paulo - Capital e região metropolitana)

### Consulta de CNPJ

1. **Acesse a aba "CNPJ"**
2. **Digite o CNPJ** no formato `00.000.000/0000-00` (formatação automática)
3. **Selecione a fonte** (Brasil API ou ReceitaWS)
4. **Clique em "Consultar"**
5. **Visualize as informações empresariais**
6. **Exporte os dados** se necessário

**Exemplo de CNPJ**: `11222333000181`

### Lista de Bancos

1. **Acesse a aba "Bancos"**
2. **Opções disponíveis**:
   - **Listar Todos**: Clique em "Listar Todos os Bancos"
   - **Buscar Específico**: Digite o código do banco e clique em "Buscar"
3. **Visualize a tabela** com códigos, nomes e nomes completos
4. **Exporte a lista** se necessário

**Exemplo de código de banco**: `001` (Banco do Brasil)

### Consulta de Municípios

1. **Acesse a aba "Municípios"**
2. **Selecione o estado** no dropdown
3. **Clique em "Consultar"**
4. **Visualize a tabela** com códigos IBGE e nomes dos municípios
5. **Exporte a lista** se necessário

### Gerenciamento de Cache

1. **Acesse a aba "Cache"**
2. **Visualize as estatísticas**:
   - Total de entradas
   - Entradas válidas
   - Entradas expiradas
   - Tamanho do cache
3. **Ações disponíveis**:
   - **Atualizar estatísticas**: Clique em "Atualizar"
   - **Limpar cache**: Clique em "Limpar Cache" (requer confirmação)

## 📊 Recursos Avançados

### Exportação de Dados

Todos os resultados podem ser exportados em dois formatos:

- **JSON**: Formato estruturado para integração com outras ferramentas
- **CSV**: Formato tabular para análise em planilhas

### Feedback Visual

A interface oferece feedback visual completo:

- **Loading States**: Indicadores de carregamento durante consultas
- **Mensagens de Sucesso**: Confirmação de operações bem-sucedidas
- **Mensagens de Erro**: Detalhes sobre problemas encontrados
- **Validação em Tempo Real**: Formatação automática de campos

### Design Responsivo

A interface é totalmente responsiva e funciona em:

- **Desktop**: Experiência completa com todas as funcionalidades
- **Tablet**: Layout adaptado para telas médias
- **Mobile**: Interface otimizada para smartphones

## 🔧 Configurações da Interface

### Personalização

Você pode personalizar a interface editando:

- **CSS**: Modifique `templates/index.html` para alterar estilos
- **JavaScript**: Edite `static/js/app.js` para modificar comportamentos
- **Configurações**: Ajuste `config.py` para alterar URLs e timeouts

### Integração com APIs

A interface consome os seguintes endpoints:

```
GET  /api/cep/<cep>           # Consulta CEP
GET  /api/ddd/<ddd>           # Consulta DDD
GET  /api/cnpj/<cnpj>         # Consulta CNPJ
GET  /api/bancos              # Lista bancos
GET  /api/bancos/<codigo>     # Busca banco específico
GET  /api/municipios/<uf>     # Lista municípios por UF
GET  /api/cache/stats         # Estatísticas do cache
POST /api/cache/clear         # Limpar cache
POST /api/export              # Exportar dados
```

## 🚨 Tratamento de Erros

A interface trata diversos tipos de erro:

### Erros de Validação
- **CEP inválido**: Deve conter 8 dígitos
- **DDD inválido**: Deve conter 2 dígitos
- **CNPJ inválido**: Deve conter 14 dígitos
- **UF não selecionada**: Deve escolher um estado

### Erros de API
- **Timeout**: Quando a API não responde no tempo esperado
- **Dados não encontrados**: Quando o código consultado não existe
- **Limite de taxa**: Quando muitas consultas são feitas rapidamente
- **Erro de conexão**: Quando não é possível conectar à API

### Erros de Sistema
- **Cache indisponível**: Problemas com o sistema de cache
- **Erro de exportação**: Problemas ao gerar arquivos de exportação

## 💡 Dicas de Uso

### Performance
- **Use o cache**: Consultas repetidas são servidas do cache local
- **Exporte dados**: Salve resultados importantes para análise posterior
- **Monitore o cache**: Limpe periodicamente para liberar espaço

### Segurança
- **Dados públicos**: Todas as consultas usam apenas dados públicos
- **Sem armazenamento**: Dados pessoais não são armazenados permanentemente
- **Auditoria**: Todas as operações são registradas nos logs

### Produtividade
- **Navegação por abas**: Alterne rapidamente entre funcionalidades
- **Formatação automática**: Deixe a interface formatar os dados
- **Exportação rápida**: Use os botões de exportação para salvar resultados

## 🔍 Casos de Uso Práticos

### Investigação de Endereço
1. Consulte o CEP para obter informações completas
2. Use o código IBGE para consultar outros municípios da região
3. Exporte os dados para análise posterior

### Análise Empresarial
1. Consulte o CNPJ na Brasil API para informações básicas
2. Consulte na ReceitaWS para dados complementares
3. Compare os resultados das duas fontes
4. Exporte para relatório

### Mapeamento Regional
1. Consulte DDDs de uma região específica
2. Liste municípios dos estados identificados
3. Cruze informações para análise geográfica
4. Exporte dados consolidados

---

**💡 Dica**: Mantenha a interface aberta em uma aba separada para consultas rápidas durante suas investigações OSINT!