from flask import Flask, request, jsonify
import sqlite3
import os

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

# This endpoint assumes that each table has column "id" as primary key
@app.route("/word", methods=["POST"])
def upsert_word():
    """Add or update a noun in the database."""
    body = request.get_json()

    table_name = body['table']
    collision_key = body['key']
    data = body['data']
    
    if not data:
        return jsonify({"error": "JSON data is required."}), 400

    columns = data.keys()
    values = [data[k] for k in columns]

    placeholders = ", ".join("?" for _ in columns)
    columns_str = ", ".join(columns)
    update_str = ", ".join(f"{col}=excluded.{col}" for col in columns if col != "id")  # word is unique key

    sql = f"""
        INSERT INTO {table_name} ({columns_str}) 
        VALUES ({placeholders})
        ON CONFLICT({collision_key if collision_key != None else 'id'}) DO UPDATE SET {update_str}
    """

    response = None
    
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(sql, values)
        conn.commit()
        conn.close()
        response = jsonify({"message": f"Noun '{data.get('word')}' added/updated successfully!"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
    render_markdown()
    return response
    
    

# @app.route("/add_noun", methods=["POST"])
# def add_noun():
#     """Add a new noun to the database."""
#     data = request.get_json()
#     gender = data.get("gender")
#     word = data.get("word")
#     translation = data.get("translation")
#     comment = data.get("comment")  # optional

#     if not gender or not word or not translation:
#         return jsonify({"error": "Gender, word, and translation are required."}), 400

#     try:
#         conn = sqlite3.connect(DB_FILE)
#         c = conn.cursor()
#         c.execute(
#             "INSERT INTO nouns (gender, word, translation, comment) VALUES (?, ?, ?, ?)",
#             (gender, word, translation, comment)
#         )
#         conn.commit()
#         conn.close()
#         return jsonify({"message": f"Noun '{word}' added successfully!"}), 201
#     except sqlite3.IntegrityError as e:
#         return jsonify({"error": f"Integrity error: {str(e)}"}), 400


@app.route("/nouns", methods=["GET"])
def list_users():
    """Return all users."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM nouns")
    rows = c.fetchall()
    conn.close()
    # users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
