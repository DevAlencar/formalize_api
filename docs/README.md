# 📚 Documentação - Formalize API

Bem-vindo à documentação completa da Formalize API!

## 📖 Índice da Documentação

### 🚀 Início Rápido
- **[README Principal](../README.md)** - Visão geral do projeto
- **[🐳 Docker Setup](README-DOCKER.md)** - Configuração e uso do Docker

### 🔧 Configuração
- **[⚙️ Configuração](CONFIGURATION.md)** - Variáveis de ambiente e settings
- **[🚀 Deploy](DEPLOYMENT.md)** - Guia completo de deploy para produção

### 📋 API
- **[📋 Endpoints](API_ENDPOINTS.md)** - Mapeamento completo da API
- **[Swagger UI](http://localhost:8001/swagger/)** - Documentação interativa
- **[ReDoc](http://localhost:8001/redoc/)** - Documentação alternativa

## 🎯 Links Rápidos

| Ação | Link |
|------|------|
| 🚀 Executar desenvolvimento | `docker-compose up --build` |
| 🚀 Executar produção | `./deploy.sh` |
| 📊 Ver logs | `docker compose logs -f` |
| 🌐 Acessar API | http://localhost:8001 |
| 📚 Swagger | http://localhost:8001/swagger/ |
| ⚙️ Admin | http://localhost:8001/admin/ |

## 📁 Estrutura da Documentação

```
docs/
├── README.md              # Este arquivo (índice)
├── README-DOCKER.md       # Setup e uso do Docker
├── API_ENDPOINTS.md       # Mapeamento completo da API
├── CONFIGURATION.md       # Configurações e variáveis
└── DEPLOYMENT.md          # Deploy para produção
```

## 🏗️ Arquitetura do Projeto

```
formalize_api/
├── 📁 accounts/           # Sistema de autenticação
│   ├── models.py         # User, OneTimePassword
│   ├── views.py          # Register, Login, OTP
│   ├── serializers.py    # Validação de dados
│   └── urls.py           # Rotas de autenticação
│
├── 📁 chatbot/            # Sistema de chatbot
│   ├── views.py          # ChatBotView
│   ├── state_machine.py  # Máquina de estados
│   ├── states.py         # Estados do chat
│   └── state_handlers/   # Handlers por estado
│
├── 📁 CNPJManager/        # Gestão de CNPJ
│   ├── models.py         # ViabilidadeEmpresa, Payment
│   ├── views.py          # CRUD + Mercado Pago
│   └── utils/            # Utilitários
│
├── 📁 formalize_api/      # Configurações Django
│   ├── settings.py       # Configurações principais
│   ├── settings_production.py  # Configurações de produção
│   ├── urls.py           # URLs principais
│   └── wsgi.py           # WSGI application
│
├── 📁 docs/               # Documentação
├── 🐳 Dockerfile          # Imagem Docker
├── 🐳 docker-compose.yml  # Desenvolvimento
├── 🐳 docker-compose.prod.yml  # Produção
├── ⚙️ gunicorn.conf.py    # Configuração Gunicorn
└── 🚀 deploy.sh           # Script de deploy
```

## 🔄 Fluxo de Desenvolvimento

1. **Setup inicial**
   ```bash
   git clone <repo>
   cd formalize_api
   cp .env.prod.example .env
   ```

2. **Desenvolvimento**
   ```bash
   docker-compose up --build
   # Desenvolver e testar
   ```

3. **Deploy**
   ```bash
   cp .env.prod.example .env.prod
   # Configurar .env.prod
   ./deploy.sh
   ```

## 🧪 Testando a API

### 1. Teste básico
```bash
curl http://localhost:8001/api/v1/chatbot/
```

### 2. Registro de usuário
```bash
curl -X POST http://localhost:8001/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","confirm_password":"test123","first_name":"Test","last_name":"User"}'
```

### 3. Login
```bash
curl -X POST http://localhost:8001/api/v1/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## 🔧 Solução de Problemas Comuns

### Porta em uso
```bash
# Verificar o que está usando a porta
sudo netstat -tlnp | grep :8001

# Parar serviços conflitantes
sudo systemctl stop apache2
sudo systemctl stop nginx
```

### Problemas de permissão
```bash
sudo chown -R $USER:$USER .
chmod +x deploy.sh
```

### Banco de dados não conecta
```bash
# Verificar status
docker compose ps

# Ver logs
docker compose logs db
```

## 📞 Suporte

- 📚 **Documentação**: Consulte os arquivos em `docs/`
- 🐛 **Bugs**: [Criar issue](../../issues)
- 💡 **Features**: [Solicitar feature](../../issues)
- 📧 **Contato**: [Email do desenvolvedor]

## 🎓 Recursos Adicionais

- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [Docker Docs](https://docs.docker.com/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [MySQL Docs](https://dev.mysql.com/doc/)
- [Mercado Pago API](https://www.mercadopago.com.br/developers/)

---

📝 **Nota**: Esta documentação é constantemente atualizada. Se encontrar alguma informação desatualizada, por favor, [reporte](../../issues).

⭐ **Dica**: Use o Swagger UI em http://localhost:8001/swagger/ para uma documentação interativa da API!
