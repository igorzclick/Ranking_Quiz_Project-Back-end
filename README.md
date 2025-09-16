# 🎮 Think Fast - API de Jogadores

## 📌 Sobre o Projeto

Think Fast é uma API para gerenciamento de jogadores, permitindo cadastro, autenticação e operações relacionadas a jogadores. O sistema utiliza autenticação JWT para proteger rotas e garantir a segurança das operações.

## 🚀 Funcionalidades Atuais

### 1️⃣ Cadastro de Jogadores

- Registro de novos jogadores com username, email e senha
- Validação de dados para evitar duplicidade

### 2️⃣ Autenticação

- Login com username ou email
- Geração de tokens JWT (access token e refresh token)
- Proteção de rotas com autenticação

### 3️⃣ Gerenciamento de Jogadores

- Listagem de jogadores
- Busca de jogador por ID
- Atualização de dados do jogador
- Remoção de jogador

## 🛠️ Tecnologias Utilizadas

- Python
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- APIFlask

## ⚙️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. Clone o repositório:

```bash
git clone https://github.com/igorzclick/Ranking_Quiz_Project-Back-end.git
cd think-fast
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente (crie um arquivo .env baseado no .env.example):

```
JWT_SECRET_KEY=sua_chave_secreta
JWT_ACCESS_TOKEN_EXPIRES=3600
```

4. Execute a aplicação:

```bash
python run.py
```

## 📡 Endpoints da API

### Cadastro e Autenticação

#### Cadastro de Jogador

- **Endpoint**: `/player/register`
- **Método**: `POST`
- **Corpo da Requisição**:

```json
{
    **"username": "jogador1",**

    **"email": "jogador1@exemplo.com",**

    **"password": "senha123"**

}
```

- **Resposta de Sucesso**:

```json
{
    **"message": "Player created successfully"**

}
```

#### Login

- **Endpoint**: `/auth/login`
- **Método**: `POST`
- **Corpo da Requisição**:

```json
{
    **"username": "jogador1",**

    **"password": "senha123"**

}
```

ou

```json
{
    **"username": "jogador1@exemplo.com",**

    **"password": "senha123"**

}
```

- **Resposta de Sucesso**:

```json
{
    **"message": "Login successful",**

    **"access\_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",**

    **"refresh\_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."**

}
```

### Rotas Protegidas (Requerem Autenticação)

#### Listar Todos os Jogadores

- **Endpoint**: `/player`
- **Método**: `GET`
- **Cabeçalho**: `Authorization: Bearer {access\_token}`
- **Resposta de Sucesso**:

```json
{
    **"players": \[**

      **{**

        **"id": 1,**

        **"username": "jogador1",**

        **"email": "jogador1@exemplo.com"**

      **},**

      **{**

        **"id": 2,**

        **"username": "jogador2",**

        **"email": "jogador2@exemplo.com"**

      **}**

    **]**

}
```

#### Obter Jogador por ID

- **Endpoint**: `/player/{id}`
- **Método**: `GET`
- **Cabeçalho**: `Authorization: Bearer {access\_token}`
- **Resposta de Sucesso**:

```json
{
    **"player": {**

      **"id": 1,**

      **"username": "jogador1",**

      **"email": "jogador1@exemplo.com"**

    **}**

}
```

#### Atualizar Jogador

- **Endpoint**: `/player/{id}`
- **Método**: `PUT`
- **Cabeçalho**: `Authorization: Bearer {access\_token}`
- **Corpo da Requisição**:

```json
{
    **"username": "jogador1\_atualizado",**

    **"email": "jogador1\_novo@exemplo.com"**

}
```

- **Resposta de Sucesso**:

```json
{
    **"message": "Player updated successfully"**

}
```

#### Excluir Jogador

- **Endpoint**: `/player/{id}`
- **Método**: `DELETE`
- **Cabeçalho**: `Authorization: Bearer {access\_token}`
- **Resposta de Sucesso**:

```json
{
    **"message": "Player deleted successfully"**

}
```

#### Atualizar Token

- **Endpoint**: `/auth/refresh`
- **Método**: `POST`
- **Cabeçalho**: `Authorization: Bearer {refresh\_token}`
- **Resposta de Sucesso**:

```json
{
    **"access\_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."**

}
```

## 🔒 Autenticação

O sistema utiliza autenticação JWT (JSON Web Token). Para acessar rotas protegidas:

1. Faça login para obter o token de acesso
2. Inclua o token no cabeçalho das requisições:

```
Authorization: Bearer {seu_token_aqui}
```

## 📝 Observações

- Senhas são armazenadas em texto puro no momento (em um ambiente de produção, seria necessário implementar hash de senhas)
- O login pode ser feito tanto com username quanto com email
- Tokens de acesso expiram conforme configuração (padrão: 1 hora)
