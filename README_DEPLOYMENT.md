# 📱 OSINT Investigador BR - Guia de Deploy Online

## 🚀 Preparação para Produção

Este projeto está otimizado para rodar online e em dispositivos móveis. Siga este guia para fazer o deploy.

### 📋 Pré-requisitos

- Conta no GitHub
- Escolha uma plataforma de deploy (recomendado: **Vercel** ou **Railway**)
- Tokens das APIs (Direct Data, etc.)

## 🌐 Opções de Deploy

### 1. 🔥 Vercel (Recomendado - Gratuito)

**Vantagens:**
- Deploy automático via GitHub
- HTTPS gratuito
- CDN global
- Perfeito para aplicações Flask

**Passos:**

1. **Prepare o repositório:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - OSINT Investigador BR"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/osint-investigador-br.git
   git push -u origin main
   ```

2. **Configure no Vercel:**
   - Acesse [vercel.com](https://vercel.com)
   - Conecte com GitHub
   - Importe o repositório
   - Configure as variáveis de ambiente (veja seção abaixo)

3. **Deploy automático:**
   - O Vercel detectará automaticamente o `vercel.json`
   - Deploy será feito automaticamente

### 2. 🚂 Railway (Alternativa Excelente)

**Vantagens:**
- Suporte nativo ao Python
- Database integrado
- Deploy simples

**Passos:**

1. **Acesse [railway.app](https://railway.app)**
2. **Conecte com GitHub**
3. **Selecione o repositório**
4. **Configure variáveis de ambiente**
5. **Deploy automático**

### 3. 🔧 Render (Gratuito com limitações)

**Passos:**

1. **Acesse [render.com](https://render.com)**
2. **Conecte repositório GitHub**
3. **Configure:**
   - Build Command: `pip install -r requirements_production.txt`
   - Start Command: `gunicorn web_app_production:app`

## 🔐 Configuração de Variáveis de Ambiente

Configure estas variáveis na plataforma escolhida:

```env
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-super-forte-aqui
DIRECTD_TOKEN=seu-token-direct-data-aqui
BRASILAPI_ENABLED=true
VIACEP_ENABLED=true
CPF_VALIDATION_ENABLED=true
ENABLE_CACHE=true
PORT=5000
```

## 📱 Configuração PWA (Progressive Web App)

O projeto já está configurado como PWA:

- ✅ `manifest.json` configurado
- ✅ Service Worker (`sw.js`)
- ✅ Ícones otimizados
- ✅ Meta tags mobile

### Instalação no Celular:

1. **Android (Chrome):**
   - Acesse o site
   - Menu → "Adicionar à tela inicial"

2. **iOS (Safari):**
   - Acesse o site
   - Botão compartilhar → "Adicionar à Tela de Início"

## 🎯 Otimizações Mobile Implementadas

### CSS Responsivo:
- ✅ Media queries para diferentes tamanhos
- ✅ Touch targets mínimos (44px)
- ✅ Font-size 16px (evita zoom no iOS)
- ✅ Orientação landscape

### Performance:
- ✅ Compressão de assets
- ✅ Cache otimizado
- ✅ Lazy loading
- ✅ Service Worker

## 🔧 Arquivos de Produção

### Principais arquivos criados:

- `web_app_production.py` - Versão otimizada para produção
- `requirements_production.txt` - Dependências específicas
- `Procfile` - Para Heroku/Railway
- `vercel.json` - Para Vercel
- `.env.production` - Template de configuração

## 🚀 Deploy Rápido - Vercel

```bash
# 1. Clone e prepare
git clone seu-repositorio
cd osint-investigador-br

# 2. Instale Vercel CLI
npm i -g vercel

# 3. Login e deploy
vercel login
vercel --prod

# 4. Configure domínio (opcional)
vercel domains add seudominio.com
```

## 📊 Monitoramento

### Health Check:
- Endpoint: `/api/health`
- Monitore a saúde da aplicação

### Logs:
- Vercel: Dashboard → Functions → Logs
- Railway: Dashboard → Deployments → Logs

## 🔒 Segurança em Produção

### Headers implementados:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security`

### CORS configurado para produção

## 📱 Teste Mobile

### Ferramentas de teste:
1. **Chrome DevTools** - Device simulation
2. **BrowserStack** - Testes em dispositivos reais
3. **Lighthouse** - Performance e PWA audit

### Checklist Mobile:
- [ ] Responsividade em diferentes tamanhos
- [ ] Touch targets adequados
- [ ] Velocidade de carregamento
- [ ] Funcionalidade offline (PWA)
- [ ] Instalação como app

## 🆘 Troubleshooting

### Problemas comuns:

1. **Erro 500 no deploy:**
   - Verifique variáveis de ambiente
   - Confira logs da plataforma

2. **APIs não funcionam:**
   - Verifique tokens
   - Confirme CORS settings

3. **PWA não instala:**
   - Verifique HTTPS
   - Confirme manifest.json
   - Teste service worker

## 📞 Suporte

Para problemas específicos:
1. Verifique logs da plataforma
2. Teste localmente primeiro
3. Confirme configurações de produção

---

## 🎉 Resultado Final

Após o deploy, você terá:

- 🌐 **Site online** acessível globalmente
- 📱 **App mobile** instalável
- ⚡ **Performance otimizada**
- 🔒 **Segurança em produção**
- 📊 **Monitoramento ativo**

**URL de exemplo:** `https://osint-investigador-br.vercel.app`

O projeto estará 100% funcional para investigações OSINT em qualquer dispositivo!