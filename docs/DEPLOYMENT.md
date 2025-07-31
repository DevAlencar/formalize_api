# 🚀 Deploy - Formalize API

## 📋 Pré-requisitos

### Servidor
- Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- Mínimo: 2GB RAM, 2 CPU cores, 20GB disco
- Recomendado: 4GB RAM, 4 CPU cores, 50GB disco

### Software
- Docker 20.10+
- Docker Compose 2.0+
- Git
- Certificado SSL (para HTTPS)

## 🔧 Preparação do Servidor

### 1. Atualizar o sistema
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 2. Instalar Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### 3. Instalar Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalação
docker --version
docker compose --version
```

### 4. Configurar Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 8001/tcp    # API
sudo ufw enable

# Firewalld (CentOS)
sudo firewall-cmd --permanent --add-port=22/tcp
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --permanent --add-port=8001/tcp
sudo firewall-cmd --reload
```

## 📁 Deploy da Aplicação

### 1. Clonar o repositório
```bash
git clone https://github.com/DevAlencar/formalize_api.git
cd formalize_api
```

### 2. Configurar variáveis de ambiente
```bash
# Copiar template de produção
cp .env.prod.example .env.prod

# Editar com suas configurações
nano .env.prod
```

### 3. Configurações obrigatórias no `.env.prod`:
```bash
# ALTERE ESTAS CONFIGURAÇÕES
SECRET_KEY='gere-uma-chave-secreta-forte-aqui'
DB_PASSWORD='senha-forte-do-banco'
DB_ROOT_PASSWORD='senha-forte-do-root'
EMAIL_HOST_USER='seu-email@gmail.com'
EMAIL_HOST_PASSWORD='sua-app-password'
MERCADO_PAGO_ACCESS_TOKEN='seu-token-de-producao'
ALLOWED_HOSTS='seudominio.com,www.seudominio.com'
```

### 4. Executar deploy
```bash
# Tornar script executável
chmod +x deploy.sh

# Executar deploy
./deploy.sh
```

## 🔐 Configuração de SSL/HTTPS

### Opção 1: Let's Encrypt (Gratuito)

#### 1. Instalar Certbot
```bash
# Ubuntu/Debian
sudo apt install certbot

# CentOS/RHEL
sudo yum install certbot
```

#### 2. Obter certificado
```bash
sudo certbot certonly --standalone -d seudominio.com -d www.seudominio.com
```

#### 3. Configurar renovação automática
```bash
# Adicionar ao crontab
sudo crontab -e

# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

#### 4. Copiar certificados
```bash
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/seudominio.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/seudominio.com/privkey.pem ssl/key.pem
sudo chown -R $USER:$USER ssl/
```

### Opção 2: Certificado Próprio

#### 1. Gerar certificado auto-assinado (apenas para teste)
```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

#### 2. Configurar Nginx para HTTPS
Edite o arquivo `nginx.conf` e descomente as seções HTTPS:

```nginx
server {
    listen 443 ssl http2;
    server_name seudominio.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... resto da configuração
}
```

## 🌐 Configuração de Proxy Reverso

### Nginx (Recomendado)

#### 1. Instalar Nginx no host
```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx
```

#### 2. Configurar site
```bash
sudo nano /etc/nginx/sites-available/formalize
```

```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Ativar site
```bash
sudo ln -s /etc/nginx/sites-available/formalize /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 📊 Monitoramento

### 1. Logs da aplicação
```bash
# Logs em tempo real
docker compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker compose -f docker-compose.prod.yml logs web
docker compose -f docker-compose.prod.yml logs db
```

### 2. Status dos containers
```bash
docker compose -f docker-compose.prod.yml ps
```

### 3. Uso de recursos
```bash
docker stats
```

### 4. Logs do sistema
```bash
# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs do sistema
sudo journalctl -f -u docker
```

## 🔄 Backup e Restore

### Backup do Banco de Dados
```bash
# Criar backup
docker compose -f docker-compose.prod.yml exec db mysqldump -u root -p formalize_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup automático (crontab)
0 2 * * * cd /path/to/formalize_api && docker compose -f docker-compose.prod.yml exec db mysqldump -u root -p formalize_db > backups/backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql
```

### Restore do Banco de Dados
```bash
# Restaurar backup
docker compose -f docker-compose.prod.yml exec -T db mysql -u root -p formalize_db < backup_20250131_120000.sql
```

### Backup dos volumes
```bash
# Backup dos dados
docker run --rm -v formalize_api_mysql_data_prod:/data -v $(pwd):/backup ubuntu tar czf /backup/mysql_data_backup.tar.gz /data
```

## 🚀 Deploy Contínuo

### Usando GitHub Actions

#### 1. Criar `.github/workflows/deploy.yml`
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to server
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.SSH_KEY }}
        script: |
          cd /path/to/formalize_api
          git pull origin main
          docker compose -f docker-compose.prod.yml down
          docker compose -f docker-compose.prod.yml up --build -d
```

#### 2. Configurar secrets no GitHub
- `HOST`: IP do servidor
- `USERNAME`: usuário SSH
- `SSH_KEY`: chave privada SSH

### Script de deploy manual
```bash
#!/bin/bash
# deploy-update.sh

echo "🔄 Atualizando Formalize API..."

# Backup do banco
echo "📊 Fazendo backup do banco..."
docker compose -f docker-compose.prod.yml exec db mysqldump -u root -p formalize_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Atualizar código
echo "📥 Atualizando código..."
git pull origin main

# Rebuildar containers
echo "🔨 Rebuilding containers..."
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d

# Executar migrações
echo "🗄️ Executando migrações..."
sleep 30
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

echo "✅ Deploy concluído!"
```

## 🔍 Troubleshooting

### Problemas Comuns

#### 1. Container não inicia
```bash
# Verificar logs
docker compose -f docker-compose.prod.yml logs web

# Verificar configuração
docker compose -f docker-compose.prod.yml config
```

#### 2. Erro de conexão com banco
```bash
# Verificar status do MySQL
docker compose -f docker-compose.prod.yml ps db

# Testar conexão
docker compose -f docker-compose.prod.yml exec db mysql -u root -p
```

#### 3. Problemas de SSL
```bash
# Verificar certificados
openssl x509 -in ssl/cert.pem -text -noout

# Testar HTTPS
curl -I https://seudominio.com
```

#### 4. Erro de permissões
```bash
# Corrigir permissões
sudo chown -R $USER:$USER .
chmod +x deploy.sh
```

### Comandos Úteis

#### Limpar sistema
```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover volumes não utilizados
docker volume prune

# Limpeza completa
docker system prune -a
```

#### Verificar recursos
```bash
# Uso de disco
df -h

# Uso de memória
free -h

# Processos
top
```

## 📈 Otimizações de Performance

### 1. Configurar Swap (se necessário)
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 2. Otimizar MySQL
```bash
# Editar configuração MySQL
docker compose -f docker-compose.prod.yml exec db mysql -u root -p

# Executar no MySQL:
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB
SET GLOBAL query_cache_size = 268435456; -- 256MB
```

### 3. Configurar limite de conexões
No arquivo `gunicorn.conf.py`:
```python
workers = 4  # Ajustar conforme CPU
max_requests = 1000
timeout = 120
```

## 🎯 Checklist de Deploy

- [ ] Servidor configurado e atualizado
- [ ] Docker e Docker Compose instalados
- [ ] Firewall configurado
- [ ] Repositório clonado
- [ ] Arquivo `.env.prod` configurado
- [ ] Certificado SSL configurado (se HTTPS)
- [ ] Deploy executado com sucesso
- [ ] Migrações aplicadas
- [ ] Backup configurado
- [ ] Monitoramento configurado
- [ ] Testes de funcionamento realizados

Pronto! Sua API está rodando em produção! 🚀
