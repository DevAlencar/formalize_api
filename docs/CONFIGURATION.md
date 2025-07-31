# ⚙️ Configuração - Formalize API

## 📋 Variáveis de Ambiente

### Arquivo `.env` (Desenvolvimento)
```bash
# Django
SECRET_KEY='django-insecure-yy%e%l*&=+#w5y)^)19$lva9g=*(2^w4i1^($9g3(p=scaj5@6'
DEBUG=True

# Database
DB_NAME=formalize_db
DB_USER=formalize_user
DB_PASSWORD=formalize_password
DB_HOST=db
DB_PORT=3306

# Email
DEFAULT_FROM_EMAIL=estudeaqui6@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=estudeaqui6@gmail.com
EMAIL_HOST_PASSWORD='gtdl fpwv smys juuv'

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN="TEST-4445053995577530-011110-ca6dcae59aabc479efca008fc3de1e7e-2206751800"
```

### Arquivo `.env.prod` (Produção)
```bash
# Django
SECRET_KEY='your-super-secret-key-here-change-this-in-production'
DEBUG=False

# Database
DB_NAME=formalize_db
DB_USER=formalize_user
DB_PASSWORD=your-strong-database-password-here
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=your-strong-root-password-here

# Email
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password-here

# Mercado Pago (Production Keys)
MERCADO_PAGO_ACCESS_TOKEN=your-production-mercado-pago-token

# Domain
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 🔐 Configurações de Segurança

### JWT Settings
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=120),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### CORS Settings
```python
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://yourdomain.com",
]
CORS_ALLOW_CREDENTIALS = True
```

### Session Settings
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 300  # 5 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False  # True em HTTPS
```

## 🗄️ Configuração do Banco de Dados

### MySQL (Produção)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'formalize_db'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'sql_mode': 'traditional',
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 60,
    }
}
```

### SQLite (Desenvolvimento)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 📧 Configuração de Email

### Gmail SMTP
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # App Password, não a senha normal
```

### Como obter App Password do Gmail:
1. Acesse [Google Account Settings](https://myaccount.google.com/)
2. Vá em "Security" → "2-Step Verification"
3. Clique em "App passwords"
4. Gere uma senha para "Mail"
5. Use essa senha no `EMAIL_HOST_PASSWORD`

## 💳 Configuração Mercado Pago

### Credenciais de Teste
```bash
# Para desenvolvimento
MERCADO_PAGO_ACCESS_TOKEN="TEST-4445053995577530-011110-ca6dcae59aabc479efca008fc3de1e7e-2206751800"
```

### Credenciais de Produção
```bash
# Para produção
MERCADO_PAGO_ACCESS_TOKEN="APP_USR-your-production-token-here"
```

### Como obter credenciais:
1. Acesse [Mercado Pago Developers](https://www.mercadopago.com.br/developers/)
2. Crie uma aplicação
3. Copie o Access Token de teste ou produção

## 🚀 Configuração do Gunicorn

### Arquivo `gunicorn.conf.py`
```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8001"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Performance
preload_app = True
threads = 2
```

### Ajustes para diferentes ambientes:

#### Desenvolvimento (poucos recursos)
```python
workers = 2
timeout = 60
threads = 1
```

#### Produção (servidor robusto)
```python
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
threads = 2
```

## 🐳 Configuração Docker

### docker-compose.yml (Desenvolvimento)
```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: formalize_db
      MYSQL_USER: formalize_user
      MYSQL_PASSWORD: formalize_password
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "3306:3306"
    
  web:
    build: .
    ports:
      - "8001:8001"
    environment:
      - DEBUG=True
    depends_on:
      - db
```

### docker-compose.prod.yml (Produção)
```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: ${DB_NAME}
      MYSQL_USER: ${DB_USER}
      MYSQL_PASSWORD: ${DB_PASSWORD}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10
    
  web:
    build: .
    environment:
      - DJANGO_SETTINGS_MODULE=formalize_api.settings_production
      - DEBUG=False
    depends_on:
      db:
        condition: service_healthy
```

## 🔍 Logs e Monitoramento

### Configuração de Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/gunicorn/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}
```

### Visualizar logs em produção:
```bash
# Logs da aplicação
docker compose logs -f web

# Logs do banco
docker compose logs -f db

# Logs do Gunicorn
docker compose exec web tail -f /var/log/gunicorn/django.log
```

## ⚡ Otimizações de Performance

### Cache (Redis)
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Middleware de Cache
```python
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    # ... outros middlewares
    'django.middleware.cache.FetchFromCacheMiddleware',
]

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = 'formalize'
```

## 🔒 Configurações de Segurança para Produção

```python
# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## 🛠️ Troubleshooting

### Problemas comuns:

#### Erro de conexão com MySQL
```bash
# Verificar se o MySQL está rodando
docker compose ps db

# Verificar logs do MySQL
docker compose logs db

# Testar conexão
docker compose exec db mysql -u root -p
```

#### Problemas de permissão
```bash
# Verificar permissões dos arquivos
ls -la

# Corrigir permissões
sudo chown -R $USER:$USER .
chmod +x deploy.sh
```

#### Erro de token Mercado Pago
```bash
# Verificar se o token está correto
echo $MERCADO_PAGO_ACCESS_TOKEN

# Testar API do Mercado Pago
curl -X GET \
  'https://api.mercadopago.com/v1/account/users/me' \
  -H 'Authorization: Bearer YOUR_ACCESS_TOKEN'
```
