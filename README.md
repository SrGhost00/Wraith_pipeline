# Wraith Pipeline - ETL no Celular (Termux)

Pipeline de dados rodando DuckDB 1.5.5 + Spark 3.5.1 com 512MB RAM no Android.

## Stack
- DuckDB - queries analíticas
- Spark local[1] - 512m driver, UI desabilitada
- SQLite - persistência
- Python

## O que faz
Teste de resiliência com recurso limitado, simulando prod.

## Próximos passos
Airflow + BigQuery

Autor: @wraith_engineering_ - Meli 13/10/2026
