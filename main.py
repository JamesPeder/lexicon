from flask import Flask, request, jsonify, Response, render_template
import sqlite3
import json

from python.markdown import render_markdown 
from python.database import init_db, select_all_from_table, upsert_entry, delete_entry

app = Flask(__name__)

def handle_delete_operation(table_name, collision_key, data):
    
    # Assert Required Parameters
    if not data or collision_key not in data:
        return jsonify({"error": "Key value is required for deletion."}), 400
    
    # Execute Database Operation
    delete_entry(table_name, collision_key, data[collision_key])
    
    # Trigger Markdown Rerender
    render_markdown()
    
    # Return Response Body
    return jsonify({"message": f"Entry with {collision_key}='{data[collision_key]}' deleted successfully."}), 200


def handle_upsert_operation(table_name, collision_key, data):
    
    # Execute Database Operation
    row = upsert_entry(table_name, collision_key, data)
    
    # Trigger Markdown Rerender
    render_markdown()
    
    # Return Response Body including the inserted/updated row
    return jsonify({
        "message": f"Entry '{data.get(collision_key)}' added/updated successfully!",
        "data": row
    }), 201

@app.route("/word", methods=["POST"])
def manage_word():
    # Parse Json Body
    body = request.get_json()
    table_name = body.get("table")
    collision_key = body.get("key", "id") # id is the default collision key
    data = body.get("data")
    action = body.get("action", "upsert").lower() # upsert is the default operation

    # Assert Required parameters
    if not table_name:
        return jsonify({"error": "Table name is required."}), 400

    # Differentiate Operation
    try:
        if action == "delete":
            return handle_delete_operation(table_name, collision_key, data)
        else:
            return handle_upsert_operation(table_name, collision_key, data)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    

@app.route("/render", methods=["POST"])
def render():
    try:
        render_markdown()
        return jsonify({"message": "✅ Markdown file successfully generated."}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route("/words", methods=["GET"])
def list_entries():
    
    # Parse Url Parameters
    table_name = request.args.get("table")
    
    # Assert Required Parameters
    if not table_name:
        return Response(json.dumps({"error": "Query parameter 'table' is required."}, ensure_ascii=False, indent=4), 
                        mimetype="application/json", status=400)

    try:
        
        # Execute Database Operation
        data = select_all_from_table(table_name)
        
        # Return Response Body
        return Response(json.dumps(data, ensure_ascii=False, indent=4), mimetype="application/json", status=200)
    except sqlite3.Error as e:
        return Response(json.dumps({"error": f"Database error: {str(e)}"}, ensure_ascii=False, indent=4), 
                        mimetype="application/json", status=500)


@app.route("/manage", methods=["GET"])
def manage():
    return render_template("manage.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
