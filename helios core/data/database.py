import sqlite3
import pandas as pd

DB_NAME = "helios_data.db"


def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS energy_data (
        Hours INTEGER,
        Solar REAL,
        Demand REAL,
        Solar_used REAL,
        Battery_charged REAL,
        Battery_Discharged REAL,
        Grid_used REAL,
        Exported REAL,
        SOC REAL
    )
    """)

    conn.commit()
    conn.close()


def save_results(df):
    conn = create_connection()
    df.to_sql("energy_data", conn, if_exists="append", index=False)
    conn.close()

def load_data():
    conn = create_connection()

    query = "SELECT * FROM energy_data"
    df = pd.read_sql(query, conn)

    conn.close()
    return df
