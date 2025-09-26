
## Arquivo metrics.csv:
- Linhas: 1.375.455
- Colunas: 8
- Sem valores nulos
- Campos principais: account_id, campaign_id, cost_micros, clicks, conversions, impressions, interactions, date
- Observações:
  - date precisa ser convertida para DATE
  - cost_micros pode chegar a valores muito grandes, com isso usar BIGINT
  - clicks, conversions, impressions, interactions estão como float mas são contagens

## Arquivo users.csv:
- Linhas: 2
- Colunas: 3
- Campos: username, password, role
- Observações:
  - Senhas talvez estão em texto puro, precisam ser hasheadas antes do uso
  - Roles existentes: admin, user

## Obs:
- Banco escolhido: SQLite
- Tabelas: metrics e users