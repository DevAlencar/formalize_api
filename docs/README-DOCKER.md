# Formalize API - Docker Setup

Este projeto contém a API Django Formalize com configuração Docker para desenvolvimento e produção.

## Pré-requisitos

- Docker
- Docker Compose

## 🚀 Produção

### Configuração Rápida para Produção

1. **Configure as variáveis de ambiente:**
```bash
cp .env.prod.example .env.prod
# Edite .env.prod com suas configurações de produção
```

2. **Execute o deploy:**
```bash
./deploy.sh
```

### Configuração Manual para Produção

1. **Construir e iniciar os containers de produção:**
```bash
docker-compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
```

2. **Executar migrações:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

3. **Criar superusuário:**
```bash
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### Serviços de Produção

- **Nginx (Reverse Proxy)**: Disponível em `http://localhost` (porta 80)
- **API Django**: Disponível em `http://localhost:8001` (acesso direto)
- **MySQL Database**: Disponível em `localhost:3306`
  - Database: `formalize_db`
  - User: conforme configurado em `.env.prod`

### Características de Produção

- ✅ **Gunicorn** como servidor WSGI
- ✅ **Nginx** como reverse proxy
- ✅ **Health checks** para monitoramento
- ✅ **Logs estruturados** em `/logs`
- ✅ **Configurações de segurança** otimizadas
- ✅ **Cache de conexões** de banco de dados
- ✅ **Compressão Gzip** no Nginx
- ✅ **Rate limiting** para proteção contra DDoS
- ✅ **Usuário não-root** nos containers

## 🛠️ Desenvolvimento

### Como executar para desenvolvimento

1. **Construir e iniciar os containers:**
```bash
docker compose up --build
```

2. **Executar apenas (após primeira build):**
```bash
docker compose up
```

3. **Executar em background:**
```bash
docker compose up -d
```

## Serviços de Desenvolvimento

- **API Django**: Disponível em `http://localhost:8001`
- **MySQL Database**: Disponível em `localhost:3306`
  - Database: `formalize_db`
  - User: `formalize_user`
  - Password: `formalize_password`
  - Root Password: `rootpassword`

## Comandos úteis

### Parar os containers
```bash
docker compose down
```

### Parar e remover volumes (remove dados do banco)
```bash
docker compose down -v
```

### Visualizar logs
```bash
docker compose logs -f web
docker compose logs -f db
```

### Executar comandos Django
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic
```

### Acessar o container
```bash
docker compose exec web bash
docker compose exec db mysql -u root -p
```

## Estrutura

- `Dockerfile`: Configuração da imagem da aplicação Django
- `docker-compose.yml`: Orquestração dos serviços (web + database)
- `init.sql`: Script de inicialização do banco de dados
- `.dockerignore`: Arquivos ignorados durante a build da imagem

## Configuração

As configurações podem ser alteradas através das variáveis de ambiente no arquivo `.env` ou diretamente no `docker-compose.yml`.

## Troubleshooting

Se você encontrar problemas de conexão com o banco de dados, aguarde alguns segundos para que o MySQL inicialize completamente, ou verifique os logs:

```bash
docker compose logs db
```
