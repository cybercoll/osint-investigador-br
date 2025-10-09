# APIs Gratuitas - OSINT Investigador BR

## 📋 Resumo das APIs Implementadas

Este documento lista todas as APIs gratuitas implementadas no sistema OSINT Investigador BR, incluindo suas funcionalidades, limitações e alternativas.

## 🆔 Validação de Documentos Brasileiros

### CNH (Carteira Nacional de Habilitação) ✅ NOVO!

**Status**: ✅ **Implementado com validação robusta e gratuita**

**Biblioteca**: `validate-docbr` (Python)

**Funcionalidades**:
- ✅ Validação completa de formato (11 dígitos)
- ✅ Validação matemática dos dígitos verificadores
- ✅ Geração de CNHs válidas para testes
- ✅ Fallback inteligente para validação básica
- ✅ Mensagens informativas sobre limitações

**Exemplo de uso**:
```python
from documentos_integration import consultar_cnh

# CNH válida
resultado = consultar_cnh("31121208834")
# Retorna: success=True com validação completa

# CNH inválida
resultado = consultar_cnh("12345678901")
# Retorna: success=False com detalhes do erro
```

**Limitações**:
- ❌ Não fornece dados pessoais do condutor
- ❌ Não acessa base de dados do SENATRAN
- ⚠️ Para dados completos, necessário:
  - API comercial (ex: Infosimples)
  - Portal SENATRAN (5 consultas/dia por usuário)
  - Login gov.br do próprio condutor

**Alternativas para dados completos**:
1. Configure `INFOSIMPLES_API_KEY` para consultas ilimitadas
2. Use Portal SENATRAN para consulta própria
3. Considere APIs comerciais para uso empresarial

### CPF (Cadastro de Pessoas Físicas)

**Status**: ✅ **Implementado com validação robusta**

**Biblioteca**: `validate-docbr` (Python)

**Funcionalidades**:
- ✅ Validação de formato
- ✅ Validação de dígitos verificadores
- ✅ Geração de CPFs válidos para teste

### CNPJ (Cadastro Nacional da Pessoa Jurídica)

**Status**: ✅ **Implementado com validação robusta**

**Biblioteca**: `validate-docbr` (Python)

**Funcionalidades**:
- ✅ Validação de formato
- ✅ Validação de dígitos verificadores
- ✅ Geração de CNPJs válidos para teste

### PIS/PASEP

**Status**: ✅ **Implementado com validação robusta**

**Biblioteca**: `validate-docbr` (Python)

**Funcionalidades**:
- ✅ Validação de formato
- ✅ Validação de dígitos verificadores

## 🏠 Consulta de Endereços

### ViaCEP
**Status**: ✅ **Implementado**
- ✅ Consulta gratuita e ilimitada
- ✅ Dados completos de endereço
- ✅ Suporte a CEPs com hífen ou sem

### BrasilAPI CEP
**Status**: ✅ **Implementado como fallback**
- ✅ Backup para ViaCEP
- ✅ Mesma funcionalidade

## 📞 Consulta de Telefones

### Portabilidade Numérica
**Status**: ✅ **Implementado**
- ✅ Identificação da operadora atual
- ✅ Histórico de portabilidade
- ✅ Validação de formato

### DDD e Localização
**Status**: ✅ **Implementado**
- ✅ Identificação de estado/região por DDD
- ✅ Validação de números brasileiros

## 🌐 Outras APIs

### BrasilAPI
**Status**: ✅ **Implementado**
- ✅ Consulta de bancos
- ✅ Consulta de feriados
- ✅ Dados de municípios

### IBGE
**Status**: ✅ **Implementado**
- ✅ Dados de municípios
- ✅ Informações geográficas

## ⚠️ Limitações Gerais

### Documentos com Dados Pessoais
Para documentos que requerem acesso a bases governamentais (CNH, RG, Título de Eleitor, CNS), o sistema oferece:

1. **Validação Robusta Gratuita**: Formato e dígitos verificadores
2. **Informações Educativas**: Sobre como obter dados completos
3. **Alternativas Comerciais**: Para uso empresarial

### Recomendações de Uso

**Para Desenvolvedores**:
- Use as validações gratuitas para verificar formato e consistência
- Implemente APIs comerciais apenas quando necessário dados completos
- Sempre informe aos usuários sobre as limitações

**Para Usuários Finais**:
- Validações gratuitas são suficientes para verificar se um documento é válido
- Para dados pessoais, use os portais oficiais do governo
- Considere APIs pagas apenas para uso empresarial intensivo

## 🔧 Configuração

### Dependências Necessárias
```bash
pip install validate-docbr requests flask
```

### Variáveis de Ambiente Opcionais
```bash
# Para consultas CNH ilimitadas (opcional)
INFOSIMPLES_API_KEY=sua_chave_aqui
```

## 📈 Estatísticas de Uso

- **CNH**: Validação 100% gratuita e robusta
- **CPF/CNPJ**: Validação 100% gratuita
- **CEP**: Consulta 100% gratuita e ilimitada
- **Telefone**: Portabilidade 100% gratuita
- **Outros documentos**: Validação de formato gratuita

## 🎯 Próximos Passos

1. ✅ Implementação de validação CNH robusta - **CONCLUÍDO**
2. 🔄 Melhorias na interface web
3. 📊 Implementação de estatísticas de uso
4. 🔍 Expansão para outros tipos de documentos

---

**Última atualização**: Outubro 2024
**Versão**: 2.0 - Validação CNH Robusta Implementada