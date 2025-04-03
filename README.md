# CRUD com Oracle Database

Um projeto simples de CRUD (Create, Read, Update, Delete) desenvolvido em Python com FastAPI e Oracle Database, seguindo o padrão de arquitetura MVC (Model-View-Controller).

## 🧩 Sobre a Arquitetura MVC

Este projeto segue o padrão MVC (Model-View-Controller) onde:

- **Models**: Definem a estrutura dos dados e regras de negócio
- **Views**: Templates HTML que apresentam os dados ao usuário
- **Controllers**: Gerenciam o fluxo entre models e views, processando requisições

No contexto deste projeto:
- As rotas API (`routers/`) atuam como uma camada que trata as entradas do usuário para o controlador
- Os controllers (`controllers/`) atuam como controladores
- Os templates Jinja2 (`templates/`) compõem a camada de visualização
- As classes em `models/` representam a camada de modelo

## 📋 Pré-requisitos

Antes de começar, você precisará ter instalado em sua máquina:

- Python 3.9 ou superior
- Oracle Database 21c XE
- Git (opcional, para clonar o repositório)

## 🏗️ Estrutura do Projeto (MVC)
```
CrudComOracleDB/
├── controllers/     # Lógica de controle (Controller)
├── database/        # Configurações e conexão com o banco
├── models/          # Definições de modelos de dados (Model)
├── routers/         # Definição de rotas da API
├── templates/       # Templates HTML (View)
├── venv/            # Ambiente virtual Python
├── .env             # Variáveis de ambiente
├── main.py          # Ponto de entrada da aplicação
└── requirements.txt # Dependências do projeto
```

## 🚀 Começando

Siga estas instruções para executar o projeto localmente.

### 1. Clonar o repositório (opcional)

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
git checkout Exercicios
cd CrudComOracledb
```

### 2. Configurar ambiente virtual

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate
```

### 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

## 🛠 Configuração do Oracle Database

### Instalação

1. Faça o download do [Oracle Database 21c XE](https://www.oracle.com/br/database/technologies/xe-downloads.html)
2. Extraia o arquivo `.zip` e execute o instalador
3. Siga o assistente de instalação
   - *Recomendação*: Use `manager` como senha para facilitar os testes

### Configuração do Banco de Dados

1. Abra o SQL*Plus (digite `sqlplus` no terminal)
2. Conecte-se como administrador:
   ```
   CONNECT system/manager AS SYSDBA
   ```
3. Verifique os serviços disponíveis:
   ```sql
   SELECT name FROM v$services;
   ```
   Você deverá ver uma saída similar a:
   ```
   NAME
   --------------------------------
   xeXDB
   SYS$BACKGROUND
   SYS$USERS
   xe
   xepdb1
   ```

4. Configure o container e crie um usuário:
   ```sql
   ALTER SESSION SET CONTAINER = XEPDB1;
   CREATE USER seu_usuario IDENTIFIED BY sua_senha;
   GRANT DBA TO seu_usuario;
   ```

5. Teste a conexão:
   ```bash
   sqlplus seu_usuario/sua_senha@localhost/XEPDB1
   ```

## ⚙ Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=xepdb1
```

Substitua os valores pelos seus dados de conexão.

## 🏃 Executando a Aplicação

Com tudo configurado, execute:

```powershell
python main.py
```

Você deverá ver a seguinte saída:

```powershell
INFO:     Started server process [6516]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Acesse [http://127.0.0.1:8000](http://127.0.0.1:8000) no seu navegador para interagir com a aplicação.
