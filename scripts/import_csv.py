import pandas as pd
import sqlite3
from pathlib import Path
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "case.db"

def import_csv_to_sqlite():
    print("Iniciando importação dos CSVs...")

    conn = sqlite3.connect(DB_PATH)

    metrics_path = DATA_DIR / "metrics.csv"
    df_metrics = pd.read_csv(metrics_path)
    df_metrics["date"] = pd.to_datetime(df_metrics["date"]).dt.date
    df_metrics.to_sql("metrics", conn, if_exists="replace", index=True, index_label="id")
    print(f"Metrics.csv importado → tabela metrics ({len(df_metrics)} linhas)")

    users_path = DATA_DIR / "users.csv"
    df_users = pd.read_csv(users_path)

    df_users["password"] = df_users["password"].apply(lambda p: pwd_context.hash(str(p)))
    df_users["email"] = df_users["username"].apply(lambda u: f"{u}@gmail.com")

    df_users.to_sql("users", conn, if_exists="replace", index=True, index_label="id")
    print(f"Users.csv importado → tabela users ({len(df_users)} linhas)")

    conn.close()
    print(f"Banco criado/atualizado em: {DB_PATH}")

if __name__ == "__main__":
    import_csv_to_sqlite()