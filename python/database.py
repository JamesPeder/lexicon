import sqlite3
import os


DB_FILE = "database.db"
DDL_SCRIPT_PATH = "sql/ddl.sql"


def init_db():
    if os.path.exists(DDL_SCRIPT_PATH):
        ddl_script = ""
        
        with open(DDL_SCRIPT_PATH, "r") as file:
            ddl_script = file.read()
            
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.executescript(ddl_script)
        conn.commit()
        conn.close()
        print("✅ Database initialised and ddl script executed.")
    else:
        print("ℹ️ No ddl script available for database.")

def select_all_from_table(table_name):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        rows = c.fetchall()
        data = [dict(row) for row in rows]
        
    return data

def upsert_entry(table_name: str, collision_key: str, data: dict):
    """Insert or update an entry in the given table."""
    if not data:
        raise ValueError("Data dictionary cannot be empty.")

    columns = data.keys()
    values = [data[k] for k in columns]

    placeholders = ", ".join("?" for _ in columns)
    columns_str = ", ".join(columns)
    update_str = ", ".join(f"{col}=excluded.{col}" for col in columns if col != collision_key)

    sql = f"""
        INSERT INTO {table_name} ({columns_str})
        VALUES ({placeholders})
        ON CONFLICT({collision_key}) DO UPDATE SET {update_str}
    """

    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(sql, values)
        conn.commit()

def delete_entry(table_name: str, collision_key: str, key_value):
    """Delete an entry from the given table based on a key."""
    sql = f"DELETE FROM {table_name} WHERE {collision_key} = ?"
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(sql, (key_value,))
        conn.commit()