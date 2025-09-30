# Case-estagio
Este projeto é um **case de estágio da .monks** que utiliza Python, FastAPI e SQLite para gerenciar métricas e usuários a partir de arquivos CSV.  

> Este projeto foi configurado e testado no **Windows**.

# Guia para o Back end
## Pré-requisitos

- Python 3.13 ou superior
- Git
- Editor de código (VS Code recomendado)

## Instalação

### **Clone o repositório**:

  git clone https://github.com/MarcoAn778/case-estagio.git

### Crie a pasta data na raiz do projeto e adicione os arquivos CSV necessários (metrics.csv, users.csv):

### Crie um ambiente virtual e ative-o:

  python -m venv .venv
  
  .venv\Scripts\activate

### Atualize o pip:

  pip install --upgrade pip

### Instale as dependências:

  pip install -r requirements.txt

## Rodando a aplicação

### Ative o virtualenv, caso não esteja ativo:

  .venv\Scripts\activate


### Execute o servidor FastAPI:

  uvicorn api.main:app --reload


### Acesse a API no navegador ou no Postman:

   http://localhost:8000


### Para documentação interativa das rotas (Swagger UI):

  /docs

## Testes

### Para rodar os testes automatizados:

  python -m pytest api/tests -v

  -v ativa o modo verbose para mostrar detalhes dos testes.

# Guia para o Front end

O frontend foi desenvolvido em React + Vite e está localizado dentro da pasta frontend/.

## Pré-requisitos

  Node.js 20 ou superior

  npm (instalado junto com o Node)

## Instalação

### Entre na pasta do frontend:

 cd frontend

### Instale as dependências:

 npm install

## Rodando a aplicação

### Dentro da pasta frontend, rode:

 npm run dev


### O servidor de desenvolvimento será iniciado em:

 http://localhost:5173
