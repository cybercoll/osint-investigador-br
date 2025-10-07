# 🚀 Deploy OSINT Investigador BR - GitHub + Vercel

## 📋 Pré-requisitos

- Conta no GitHub
- Conta no Vercel (gratuita)
- Git instalado no seu computador

## 🔧 Passo 1: Preparar o Repositório Local

### 1.1 Inicializar Git (se ainda não foi feito)
```bash
git init
git add .
git commit -m "Initial commit - OSINT Investigador BR"
```

### 1.2 Verificar arquivos importantes
- ✅ `.gitignore` - Configurado para não subir arquivos sensíveis
- ✅ `web_app_production.py` - Versão otimizada para produção
- ✅ `requirements_production.txt` - Dependências de produção
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `Procfile` - Para outros serviços de deploy

## 🌐 Passo 2: Criar Repositório no GitHub

### 2.1 Acessar GitHub
1. Vá para [github.com](https://github.com)
2. Faça login na sua conta
3. Clique em "New repository" (botão verde)

### 2.2 Configurar Repositório
- **Repository name:** `osint-investigador-br`
- **Description:** `Sistema profissional para investigações OSINT no Brasil - Mobile Ready`
- **Visibility:** Public (recomendado para Vercel gratuito)
- **NÃO** marque "Add a README file" (já temos um)
- **NÃO** marque "Add .gitignore" (já temos um)

### 2.3 Conectar Repositório Local
```bash
git remote add origin https://github.com/SEU_USUARIO/osint-investigador-br.git
git branch -M main
git push -u origin main
```

## ⚡ Passo 3: Deploy no Vercel

### 3.1 Acessar Vercel
1. Vá para [vercel.com](https://vercel.com)
2. Clique em "Sign up" ou "Login"
3. **Conecte com GitHub** (recomendado)

### 3.2 Importar Projeto
1. No dashboard do Vercel, clique em "New Project"
2. Encontre o repositório `osint-investigador-br`
3. Clique em "Import"

### 3.3 Configurar Deploy
- **Framework Preset:** Other
- **Root Directory:** `./` (deixar padrão)
- **Build Command:** (deixar vazio)
- **Output Directory:** (deixar vazio)
- **Install Command:** `pip install -r requirements_production.txt`

### 3.4 Configurar Variáveis de Ambiente
Na seção "Environment Variables", adicione:

```env
FLASK_ENV=production
SECRET_KEY=sua-chave-super-secreta-aqui-mude-em-producao
DIRECTD_TOKEN=seu-token-direct-data-aqui
BRASILAPI_ENABLED=true
VIACEP_ENABLED=true
CPF_VALIDATION_ENABLED=true
ENABLE_CACHE=true
```

**⚠️ IMPORTANTE:** Substitua os valores pelos seus tokens reais!

### 3.5 Fazer Deploy
1. Clique em "Deploy"
2. Aguarde o processo (2-5 minutos)
3. ✅ Deploy concluído!

## 🎉 Passo 4: Verificar Deploy

### 4.1 URL de Produção
Após o deploy, você receberá uma URL como:
```
https://osint-investigador-br-seu-usuario.vercel.app
```

### 4.2 Testar Funcionalidades
- [ ] Interface carrega corretamente
- [ ] Consulta CPF funciona
- [ ] Consulta Nome funciona
- [ ] Consulta Telefone funciona
- [ ] Consulta CEP funciona
- [ ] Consulta DDD funciona
- [ ] Consulta CNPJ funciona

## 📱 Passo 5: Configurar App Mobile (PWA)

### 5.1 Verificar PWA
1. Acesse a URL de produção no celular
2. No Chrome (Android): Menu → "Adicionar à tela inicial"
3. No Safari (iOS): Botão compartilhar → "Adicionar à Tela de Início"

### 5.2 Testar Instalação
- [ ] App aparece na tela inicial
- [ ] Abre em tela cheia (sem barra do navegador)
- [ ] Funciona offline (funcionalidades básicas)
- [ ] Interface responsiva no celular

## 🔄 Passo 6: Atualizações Automáticas

### 6.1 Deploy Automático
Agora, sempre que você fizer push para o GitHub:
```bash
git add .
git commit -m "Sua mensagem de commit"
git push origin main
```

O Vercel automaticamente:
1. Detecta as mudanças
2. Faz novo deploy
3. Atualiza a aplicação online

## 🛠️ Troubleshooting

### Problema: Deploy falha
**Solução:**
1. Verifique os logs no dashboard do Vercel
2. Confirme se todas as variáveis de ambiente estão configuradas
3. Verifique se o `requirements_production.txt` está correto

### Problema: APIs não funcionam
**Solução:**
1. Verifique se os tokens estão corretos nas variáveis de ambiente
2. Confirme se as APIs estão ativas
3. Verifique os logs de erro no Vercel

### Problema: PWA não instala
**Solução:**
1. Verifique se está acessando via HTTPS
2. Confirme se o `manifest.json` está acessível
3. Teste em diferentes navegadores

## 📊 Monitoramento

### Dashboard Vercel
- **Analytics:** Visualizações e performance
- **Functions:** Logs das requisições
- **Deployments:** Histórico de deploys

### URLs Importantes
- **Produção:** `https://seu-projeto.vercel.app`
- **Health Check:** `https://seu-projeto.vercel.app/api/health`
- **Manifest PWA:** `https://seu-projeto.vercel.app/manifest.json`

## 🎯 Resultado Final

Após seguir todos os passos, você terá:

- 🌐 **Site online** acessível globalmente
- 📱 **App instalável** no celular
- 🔄 **Deploy automático** via GitHub
- 📊 **Monitoramento** via Vercel
- ⚡ **Performance otimizada**
- 🔒 **Segurança em produção**

**Exemplo de URL final:** `https://osint-investigador-br.vercel.app`

---

## 🆘 Suporte

Se encontrar problemas:
1. Verifique este guia novamente
2. Consulte os logs no Vercel
3. Teste localmente primeiro
4. Verifique as configurações de produção

**O projeto estará 100% funcional online e mobile! 🚀**