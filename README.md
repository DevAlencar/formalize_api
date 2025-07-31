# 🚀 Formalize API

Uma API Django REST completa para gerenciamento de CNPJ, chatbot inteligente e integração com Mercado Pago.

## 📋 Visão Geral

A Formalize API oferece uma solução completa para:
- 🔐 **Autenticação de usuários** com JWT e verificação por OTP
- 🤖 **Chatbot inteligente** para atendimento automatizado
- 🏢 **Gerenciamento de CNPJ** e viabilidades empresariais
- 💳 **Integração com Mercado Pago** para pagamentos

## 🚀 Início Rápido

### Pré-requisitos
- Docker
- Docker Compose

### Executar com Docker
```bash
# Para desenvolvimento
docker-compose up --build

# Para produção
./deploy.sh
```

### Acessos
- **API**: http://localhost:8001
- **Swagger**: http://localhost:8001/swagger/
- **Admin**: http://localhost:8001/admin/

## 📚 Documentação

- **[🐳 Docker Setup](docs/README-DOCKER.md)** - Configuração completa do Docker
- **[📋 API Endpoints](docs/API_ENDPOINTS.md)** - Mapeamento completo dos endpoints
- **[🔧 Configuração](docs/CONFIGURATION.md)** - Variáveis de ambiente e configurações
- **[🚀 Deploy](docs/DEPLOYMENT.md)** - Guia de deploy para produção

## 🏗️ Arquitetura

```
formalize_api/
├── accounts/          # Autenticação e usuários
├── chatbot/           # Sistema de chatbot
├── CNPJManager/       # Gerenciamento de CNPJ
├── formalize_api/     # Configurações do projeto
├── docs/              # Documentação
└── docker/            # Configurações Docker
```

## 🛠️ Tecnologias

- **Backend**: Django REST Framework
- **Banco**: MySQL 8.0
- **Autenticação**: JWT + OTP
- **Servidor**: Gunicorn
- **Container**: Docker + Docker Compose
- **Pagamentos**: Mercado Pago API

## 📊 Endpoints Principais

| Serviço | Endpoint | Descrição |
|---------|----------|-----------|
| Auth | `/api/v1/accounts/` | Autenticação e usuários |
| Chatbot | `/api/v1/chatbot/` | Sistema de chatbot |
| CNPJ | `/api/v1/cnpjmanager/` | Gestão de CNPJ |
| Docs | `/swagger/` | Documentação interativa |

## 🔧 Desenvolvimento

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Executar migrações
```bash
python manage.py migrate
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Executar servidor
```bash
python manage.py runserver
```

## 🌐 Produção

Para deploy em produção, consulte o [guia completo de deploy](docs/DEPLOYMENT.md).

### Resumo rápido:
```bash
# 1. Configure variáveis de ambiente
cp .env.prod.example .env.prod

# 2. Execute o deploy
./deploy.sh

# 3. Acesse em http://localhost:8001
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

- 📚 [Documentação completa](docs/)
- 🐛 [Reportar bug](../../issues)
- 💡 [Solicitar feature](../../issues)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
