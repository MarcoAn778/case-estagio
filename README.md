# case-estagio
Repositório para o case técnico de estágio em Engenharia.

## Decisões do Dia 1
- Banco de dados: **SQLite** (pela simplicidade e portabilidade)
- Arquivos analisados: `metrics.csv` (1.3M linhas, 8 colunas), `users.csv` (2 linhas)
- Criação das tabelas e importação dos dados a partir dos CSVs
- Ajustes necessários:
  - Senhas de usuários precisam ser hasheadas(Caso essas não sejam senhas hasheadas)
- Próximos passos: setup do backend (FastAPI), 