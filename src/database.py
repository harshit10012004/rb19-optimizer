import os
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DB_URL, sslmode="require")

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leaderboards (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            rake_mm DECIMAL,
            lap_gain DECIMAL,
            stint_gain DECIMAL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_lap(username, rake_mm, lap_gain, stint_gain):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO leaderboards (username, rake_mm, lap_gain, stint_gain) VALUES (%s, %s, %s, %s)",
        (username, rake_mm, lap_gain, stint_gain)
    )
    conn.commit()
    cur.close()
    conn.close()
