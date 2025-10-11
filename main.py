from flask import Flask, request, jsonify, Response
import sqlite3
import os
import json

from markdown import render_markdown 

app = Flask(__name__)
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

# TODO: General interface, where you can insert or update an entry just by sending a json object
# TODO: Turn the MD into a website? or you add parameters of what data you'd like to generate?

# Each time you edit the data, a new md file is written 

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

# This endpoint assumes that each table has column "id" as primary key
@app.route("/word", methods=["POST"])
def manage_word():
    """Manage (upsert or delete) a word in the database."""
    body = request.get_json()
    table_name = body.get("table")
    collision_key = body.get("key", "id") # id is the default collision key
    data = body.get("data")
    action = body.get("action", "upsert").lower() # upsert is the default operation

    if not table_name:
        return jsonify({"error": "Table name is required."}), 400

    try:
        if action == "delete":
            if not data or collision_key not in data:
                return jsonify({"error": "Key value is required for deletion."}), 400
            delete_entry(table_name, collision_key, data[collision_key])
            render_markdown()
            return jsonify({"message": f"Entry with {collision_key}='{data[collision_key]}' deleted successfully."}), 200
        else:
            upsert_entry(table_name, collision_key, data)
            render_markdown()
            return jsonify({"message": f"Entry '{data.get(collision_key)}' added/updated successfully!"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    

@app.route("/render", methods=["POST"])
def render():
    """Regenerate the Markdown file from the database."""
    try:
        render_markdown()
        return jsonify({"message": "✅ Markdown file successfully generated."}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/words", methods=["GET"])
def list_entries():
    """Return all entries from a specified table with proper UTF-8 encoding."""
    table_name = request.args.get("table")
    
    if not table_name:
        return Response(json.dumps({"error": "Query parameter 'table' is required."}, ensure_ascii=False, indent=4), 
                        mimetype="application/json", status=400)

    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(f"SELECT * FROM {table_name}")
            rows = c.fetchall()
            data = [dict(row) for row in rows]

        return Response(json.dumps(data, ensure_ascii=False, indent=4), mimetype="application/json", status=200)
    except sqlite3.Error as e:
        return Response(json.dumps({"error": f"Database error: {str(e)}"}, ensure_ascii=False, indent=4), 
                        mimetype="application/json", status=500)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
