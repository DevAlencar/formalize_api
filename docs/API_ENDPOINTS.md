# 📋 Formalize API - Mapeamento de Endpoints

## 🔗 Base URL
```
http://localhost:8001
```

## 📚 Documentação da API
- **Swagger UI**: `http://localhost:8001/swagger/`
- **ReDoc**: `http://localhost:8001/redoc/`
- **Admin Panel**: `http://localhost:8001/admin/`

---

## 🔐 **1. ACCOUNTS (Autenticação e Usuários)**
Base: `/api/v1/accounts/`

### 1.1 Registro de Usuário
```http
POST /api/v1/accounts/register/
```
**Payload:**
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "confirm_password": "senha123",
  "first_name": "João",
  "last_name": "Silva"
}
```
**Resposta (201):**
```json
{
  "data": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "last_name": "Silva"
  },
  "message": "User created successfully!"
}
```

### 1.2 Reenviar OTP
```http
POST /api/v1/accounts/otp-resend/
```
**Payload:**
```json
{
  "email": "usuario@exemplo.com"
}
```

### 1.3 Verificar Email (OTP)
```http
POST /api/v1/accounts/verify/
```
**Payload:**
```json
{
  "otp": "123456"
}
```

### 1.4 Login
```http
POST /api/v1/accounts/login/
```
**Payload:**
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```
**Resposta (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "first_name": "João"
  }
}
```

### 1.5 Solicitar Reset de Senha
```http
POST /api/v1/accounts/password-reset/
```
**Payload:**
```json
{
  "email": "usuario@exemplo.com"
}
```

### 1.6 Confirmar Reset de Senha
```http
GET /api/v1/accounts/password-reset-confirm/<uidb64>/<token>/
```

### 1.7 Definir Nova Senha
```http
POST /api/v1/accounts/set-new-password/
```
**Payload:**
```json
{
  "password": "novaSenha123",
  "confirm_password": "novaSenha123",
  "uidb64": "...",
  "token": "..."
}
```

### 1.8 Logout
```http
POST /api/v1/accounts/logout/
```
**Headers:**
```
Authorization: Bearer <access_token>
```

---

## 🤖 **2. CHATBOT**
Base: `/api/v1/chatbot/`

### 2.1 Iniciar Conversa
```http
GET /api/v1/chatbot/
```
**Resposta (200):**
```json
{
  "answer": "Olá! Como posso ajudar você hoje?",
  "questions": [
    {"body": "Consultar CNPJ"},
    {"body": "Obter certidões"},
    {"body": "Falar com atendente"}
  ]
}
```

### 2.2 Enviar Mensagem
```http
POST /api/v1/chatbot/
```
**Payload:**
```json
{
  "mensagem": "1"
}
```
**Resposta (200):**
```json
{
  "answer": "Digite o CNPJ que você deseja consultar:",
  "questions": []
}
```

### 2.3 Página do Chat (HTML)
```http
GET /api/v1/chatbot/chat/
```
Retorna uma página HTML para interface do chatbot.

---

## 🏢 **3. CNPJ MANAGER**
Base: `/api/v1/cnpjmanager/`

### 3.1 Viabilidades de Empresa

#### 3.1.1 Listar Viabilidades
```http
GET /api/v1/cnpjmanager/viabilidades/
```

#### 3.1.2 Criar Viabilidade
```http
POST /api/v1/cnpjmanager/viabilidades/
```
**Payload:**
```json
{
  "nome_empresa": "Minha Empresa LTDA",
  "cnae_principal": "6201-5/00",
  "endereco": "Rua das Flores, 123",
  "cidade": "São Paulo",
  "estado": "SP"
}
```

#### 3.1.3 Obter Viabilidade Específica
```http
GET /api/v1/cnpjmanager/viabilidades/{id}/
```

#### 3.1.4 Atualizar Viabilidade
```http
PUT /api/v1/cnpjmanager/viabilidades/{id}/
PATCH /api/v1/cnpjmanager/viabilidades/{id}/
```

#### 3.1.5 Deletar Viabilidade
```http
DELETE /api/v1/cnpjmanager/viabilidades/{id}/
```

### 3.2 Pagamentos (Mercado Pago)

#### 3.2.1 Obter Link de Pagamento
```http
GET /api/v1/cnpjmanager/mercadopago/pagamento/
```
**Headers:**
```
Authorization: Bearer <access_token>
```
**Resposta (200):**
```json
{
  "link": "https://mercadopago.com.br/checkout/v1/redirect?pref_id=..."
}
```

### 3.3 Webhook Mercado Pago

#### 3.3.1 Receber Notificações de Pagamento
```http
POST /api/v1/cnpjmanager/mercadopago/webhook/
```
**Payload (exemplo do Mercado Pago):**
```json
{
  "type": "payment",
  "data": {
    "id": "123456789"
  }
}
```

---

## 🔑 **Autenticação**

### Headers para Endpoints Protegidos
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Renovar Token
```http
POST /api/v1/token/refresh/
```
**Payload:**
```json
{
  "refresh": "<refresh_token>"
}
```

---

## 📝 **Exemplos de Uso com cURL**

### 1. Registrar Usuário
```bash
curl -X POST http://localhost:8001/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123",
    "confirm_password": "senha123",
    "first_name": "João",
    "last_name": "Silva"
  }'
```

### 2. Fazer Login
```bash
curl -X POST http://localhost:8001/api/v1/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@exemplo.com",
    "password": "senha123"
  }'
```

### 3. Iniciar Chatbot
```bash
curl -X GET http://localhost:8001/api/v1/chatbot/ \
  -H "Content-Type: application/json"
```

### 4. Obter Link de Pagamento
```bash
curl -X GET http://localhost:8001/api/v1/cnpjmanager/mercadopago/pagamento/ \
  -H "Authorization: Bearer <seu_access_token>" \
  -H "Content-Type: application/json"
```

---

## 📝 **Exemplos com Python (requests)**

### 1. Registrar e Fazer Login
```python
import requests

BASE_URL = "http://localhost:8001"

# Registrar usuário
register_data = {
    "email": "teste@exemplo.com",
    "password": "senha123",
    "confirm_password": "senha123",
    "first_name": "João",
    "last_name": "Silva"
}

response = requests.post(f"{BASE_URL}/api/v1/accounts/register/", json=register_data)
print("Registro:", response.json())

# Fazer login
login_data = {
    "email": "teste@exemplo.com",
    "password": "senha123"
}

response = requests.post(f"{BASE_URL}/api/v1/accounts/login/", json=login_data)
tokens = response.json()
access_token = tokens["access_token"]

print("Login:", tokens)
```

### 2. Usar Chatbot
```python
import requests

BASE_URL = "http://localhost:8001"

# Iniciar chatbot
session = requests.Session()
response = session.get(f"{BASE_URL}/api/v1/chatbot/")
print("Início:", response.json())

# Enviar mensagem
message_data = {"mensagem": "Consultar CNPJ"}
response = session.post(f"{BASE_URL}/api/v1/chatbot/", json=message_data)
print("Resposta:", response.json())
```

### 3. Obter Link de Pagamento
```python
import requests

BASE_URL = "http://localhost:8001"
access_token = "seu_access_token_aqui"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.get(f"{BASE_URL}/api/v1/cnpjmanager/mercadopago/pagamento/", headers=headers)
print("Link de pagamento:", response.json())
```

---

## 📱 **Exemplos com JavaScript (Fetch)**

### 1. Fazer Login
```javascript
const baseURL = 'http://localhost:8001';

async function login(email, password) {
  const response = await fetch(`${baseURL}/api/v1/accounts/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  });
  
  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);
  return data;
}
```

### 2. Usar API com Token
```javascript
async function getPaymentLink() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${baseURL}/api/v1/cnpjmanager/mercadopago/pagamento/`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  });
  
  return await response.json();
}
```

---

## ⚠️ **Códigos de Status HTTP**

| Código | Significado |
|--------|-------------|
| 200 | OK - Sucesso |
| 201 | Created - Recurso criado |
| 400 | Bad Request - Dados inválidos |
| 401 | Unauthorized - Token inválido/ausente |
| 403 | Forbidden - Sem permissão |
| 404 | Not Found - Recurso não encontrado |
| 500 | Internal Server Error - Erro do servidor |

---

## 🔧 **Testando a API**

1. **Inicie a aplicação:**
   ```bash
   ./deploy.sh
   ```

2. **Acesse a documentação interativa:**
   - Swagger: http://localhost:8001/swagger/
   - ReDoc: http://localhost:8001/redoc/

3. **Use ferramentas como:**
   - Postman
   - Insomnia
   - cURL
   - Thunder Client (VS Code)

4. **Para desenvolvimento, monitore os logs:**
   ```bash
   docker compose logs -f web
   ```
