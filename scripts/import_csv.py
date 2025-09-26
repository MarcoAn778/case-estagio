import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "case.db"

def import_csv_to_sqlite():
    print("Iniciando importação dos CSVs...")

    conn = sqlite3.connect(DB_PATH)

    metrics_path = DATA_DIR / "metrics.csv"
    df_metrics = pd.read_csv(metrics_path)
    df_metrics["date"] = pd.to_datetime(df_metrics["date"]).dt.date

    df_metrics.to_sql("metrics", conn, if_exists="replace", index=False)
    print(f"Importado metrics.csv → tabela metrics ({len(df_metrics)} linhas)")

    users_path = DATA_DIR / "users.csv"
    df_users = pd.read_csv(users_path)

    df_users.to_sql("users", conn, if_exists="replace", index=False)
    print(f"Importado users.csv → tabela users ({len(df_users)} linhas)")

    conn.close()
    print(f"Banco criado/atualizado em: {DB_PATH}")

if __name__ == "__main__":
    import_csv_to_sqlite()
