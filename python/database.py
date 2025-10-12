import sqlite3
import os
from typing import Dict

from python.database_utils.utils import BadRequest, ensure_columns_exist, get_table_columns, quote_identifier, ensure_collision_key_unique

DB_FILE = "database.db"
DDL_SCRIPT_PATH = "sql/ddl.sql"
COLUMNS_WITH_DEFAULT_VALUES = ['id', 'difficulty', 'created_at']


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


def upsert_entry(table_name: str, collision_key: str, data: Dict):
    """
    Safely insert or update an entry in the given table.

    - Validates table and columns against the DB schema using PRAGMA.
    - Constructs SQL using only validated identifiers.
    - Uses parameterized values for user data.
    - Raises BadRequest for invalid input.
    """
    if not data:
        raise BadRequest("Data dictionary cannot be empty.")
    
    # If we recieve an empty string, assume Null value in DB
    data = {k: (v if v != "" else None) for k, v in data.items()}

    # Remove 'id', 'difficulty', 'created_at' if value is None, as theses have default values
    for col in COLUMNS_WITH_DEFAULT_VALUES:
        if col in data and data[col] is None:
            del data[col]

    # Normalize keys to a deterministic order
    columns = list(data.keys())
    values = [data[k] for k in columns]

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row

        # Validate table and columns against schema
        table_columns_info = get_table_columns(conn, table_name)  # raises BadRequest if table missing
        valid_cols = set(table_columns_info.keys())
        ensure_columns_exist(valid_cols, columns)

        # Validate collision_key exists in the table
        if collision_key not in valid_cols:
            raise BadRequest(f"collision_key '{collision_key}' is not a column in table '{table_name}'")

        # Optional: ensure collision_key is unique/primary (recommended)
        if not ensure_collision_key_unique(conn, table_name, collision_key):
            raise BadRequest(f"collision_key '{collision_key}' is not UNIQUE or PRIMARY KEY in '{table_name}'")

        # Build safe SQL using quoted identifiers (we only use validated names)
        placeholders = ", ".join("?" for _ in columns)
        columns_str = ", ".join(quote_identifier(col) for col in columns)
        # For update set, skip the collision_key (you typically don't update the unique key)
        update_cols = [col for col in columns if col != collision_key]
        if not update_cols:
            # If collision_key is the only column provided, do nothing on update
            update_str = f"{quote_identifier(collision_key)}=excluded.{quote_identifier(collision_key)}"
        else:
            update_str = ", ".join(f"{quote_identifier(col)}=excluded.{quote_identifier(col)}" for col in update_cols)

        # Note: ON CONFLICT(...) requires the specified column to be UNIQUE or PK.
        sql = f"""
        INSERT INTO {quote_identifier(table_name)} ({columns_str})
        VALUES ({placeholders})
        ON CONFLICT({quote_identifier(collision_key)}) DO UPDATE SET {update_str};
        """

        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()


def delete_entry(table_name: str, collision_key: str, key_value):
    """Delete an entry from the given table based on a key."""
    sql = f"DELETE FROM {table_name} WHERE {collision_key} = ?"
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(sql, (key_value,))
        conn.commit()