import sqlite3
from typing import Dict, Iterable


class BadRequest(Exception):
    pass

def get_table_columns(conn: sqlite3.Connection, table: str) -> Dict[str, dict]:
    """
    Returns a dict mapping column_name -> column_info for the given table.
    Uses PRAGMA table_info(table). Raises BadRequest if table does not exist.
    """
    cur = conn.execute("PRAGMA table_info(%s)" % quote_identifier(table))
    cols = cur.fetchall()
    if not cols:
        raise BadRequest(f"Table '{table}' does not exist or has no columns.")
    # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
    return {row[1]: {"cid": row[0], "type": row[2], "notnull": row[3], "dflt": row[4], "pk": row[5]} for row in cols}

def quote_identifier(name: str) -> str:
    """
    Quote an identifier for SQLite by wrapping with double quotes and escaping
    any embedded double quotes. This is safe only if 'name' comes from a validated
    source (we validate permitted names against the table schema).
    """
    return '"' + name.replace('"', '""') + '"'

def ensure_columns_exist(valid_columns: Iterable[str], requested_columns: Iterable[str]):
    missing = [c for c in requested_columns if c not in valid_columns]
    if missing:
        raise BadRequest(f"Unknown columns for table: {missing}")

def ensure_collision_key_unique(conn: sqlite3.Connection, table: str, collision_key: str) -> bool:
    """
    Try to check whether collision_key is declared unique (either pk or unique index).
    Returns True if unique, False otherwise. Not strictly required but recommended.
    """
    # check if PK
    cur = conn.execute("PRAGMA table_info(%s)" % quote_identifier(table))
    for row in cur.fetchall():
        name = row[1]
        pk = row[5]
        if name == collision_key and pk:
            return True

    # check unique indexes
    cur = conn.execute("PRAGMA index_list(%s)" % quote_identifier(table))
    for idx_row in cur.fetchall():
        index_name = idx_row[1]
        is_unique = idx_row[2]  # 1 if unique
        if is_unique:
            # get indexed columns
            cur2 = conn.execute("PRAGMA index_info(%s)" % quote_identifier(index_name))
            cols = [r[2] for r in cur2.fetchall()]
            if collision_key in cols:
                return True
    return False
