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

### Crie a pasta data na raiz do projeto e adicione os arquivos CSV necessários (metrics.csv, users.csv e case.db):

### Crie um ambiente virtual e ative-o:

  python -m venv .venv
  .venv\Scripts\activate

### Atualize o pip:

  pip install --upgrade pip

### Instale as dependências:

  pip install pandas fastapi uvicorn[standard] sqlalchemy pydantic python-dotenv

-Se você for usar formulários com FastAPI, instale também o python-multipart:

  pip install python-multipart

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

Certifique-se de estar com o virtualenv ativo.
