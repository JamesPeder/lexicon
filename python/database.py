import sqlite3
import os
from typing import Dict

from python.database_utils.utils import BadRequest, ensure_columns_exist, get_table_columns, quote_identifier, ensure_collision_key_unique
from python.constants import *

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
    
    # Treat empty string as NULL
    data = {k: (v if v != "" else None) for k, v in data.items()}

    # Remove columns with default values if None
    for col in COLUMNS_WITH_DEFAULT_VALUES:
        if col in data and data[col] is None:
            del data[col]

    columns = list(data.keys())
    values = [data[k] for k in columns]

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row

        table_columns_info = get_table_columns(conn, table_name)
        valid_cols = set(table_columns_info.keys())
        ensure_columns_exist(valid_cols, columns)

        if collision_key not in valid_cols:
            raise BadRequest(f"collision_key '{collision_key}' is not a column in table '{table_name}'")

        if not ensure_collision_key_unique(conn, table_name, collision_key):
            raise BadRequest(f"collision_key '{collision_key}' is not UNIQUE or PRIMARY KEY in '{table_name}'")

        placeholders = ", ".join("?" for _ in columns)
        columns_str = ", ".join(quote_identifier(col) for col in columns)
        update_cols = [col for col in columns if col != collision_key]
        if not update_cols:
            update_str = f"{quote_identifier(collision_key)}=excluded.{quote_identifier(collision_key)}"
        else:
            update_str = ", ".join(f"{quote_identifier(col)}=excluded.{quote_identifier(col)}" for col in update_cols)

        sql = f"""
        INSERT INTO {quote_identifier(table_name)} ({columns_str})
        VALUES ({placeholders})
        ON CONFLICT({quote_identifier(collision_key)}) DO UPDATE SET {update_str};
        """
        
        cur = conn.cursor()
        cur.execute(sql, values)

        # Case 1: new row inserted → lastrowid is valid
        inserted_id = cur.lastrowid

        # Case 2: existing row updated → fetch its id using the collision key
        if not inserted_id:
            cur.execute(
                f"SELECT id FROM {quote_identifier(table_name)} WHERE {quote_identifier(collision_key)} = ?",
                (data[collision_key],)
            )
            row = cur.fetchone()
            inserted_id = row["id"] if row else None

        # Now fetch the full updated/inserted row by id
        if inserted_id:
            cur.execute(
                f"SELECT * FROM {quote_identifier(table_name)} WHERE id = ?",
                (inserted_id,)
            )
            row = cur.fetchone()
        else:
            row = None

        conn.commit()
        return dict(row) if row else None

def delete_entry(table_name: str, collision_key: str, key_value):
    """Delete an entry from the given table based on a key."""
    sql = f"DELETE FROM {table_name} WHERE {collision_key} = ?"
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(sql, (key_value,))
        conn.commit()