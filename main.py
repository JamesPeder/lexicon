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

    
@app.route("/manage", methods=["GET"])
def manage():
    """HTML interface to view, edit, delete, search, and re-render words with paging."""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Word Database Manager</title>
<style>
    body { font-family: Arial, sans-serif; margin: 40px; background: #fafafa; }
    select, input, button { margin: 5px; padding: 6px 10px; border-radius: 6px; border: 1px solid #ccc; }
    button { cursor: pointer; background: #007bff; color: white; border: none; }
    button:hover { background: #0056b3; }
    table { border-collapse: collapse; width: 100%; margin-top: 15px; background: white; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f2f2f2; position: sticky; top: 0; }
    td[contenteditable="true"] { background: #fff9c4; }
    .actions { display: flex; gap: 5px; }
    .toolbar { margin-top: 10px; }
    input.filter { width: 95%; box-sizing: border-box; padding: 4px; }
</style>
</head>
<body>

<h1>📘 Greek Words Database Manager</h1>

<div class="toolbar">
    <label for="table">Select Table:</label>
    <select id="table" onchange="loadTable()">
        <option value="nouns">nouns</option>
        <option value="verbs">verbs</option>
        <option value="numbers">numbers</option>
        <option value="adverbs_adjectives">adverbs_adjectives</option>
    </select>
    <button onclick="loadTable()">🔄 Refresh</button>
    <button onclick="addRow()">➕ Add New Row</button>
    <button onclick="rerender()">🔁 Re-render Markdown</button>

    Page size:
    <select id="pageSize" onchange="changePageSize(this.value)">
        <option>10</option>
        <option>25</option>
        <option>50</option>
        <option>100</option>
    </select>

    <button onclick="prevPage()">⬅️ Prev</button>
    <span id="pageInfo">Page 1</span>
    <button onclick="nextPage()">➡️ Next</button>
</div>

<div id="tableData"></div>

<script>
let currentTable = "";
let tableData = [];    // full data from backend
let filteredData = []; // filtered by search
let currentPage = 1;
let pageSize = 10;

async function loadTable() {
    currentTable = document.getElementById('table').value;
    document.getElementById('tableData').innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`/words?table=${currentTable}`);
        tableData = await response.json();
        filteredData = tableData.slice();
        currentPage = 1;
        renderTablePage();
    } catch (err) {
        document.getElementById('tableData').innerHTML = `<p style="color:red;">Error: ${err}</p>`;
    }
}

function renderTablePage() {
    const tbodyStart = (currentPage - 1) * pageSize;
    const tbodyEnd = tbodyStart + pageSize;
    const pageData = filteredData.slice(tbodyStart, tbodyEnd);

    const container = document.getElementById('tableData');
    container.innerHTML = "";

    if (pageData.length === 0) {
        container.innerHTML = "<p>No data</p>";
        document.getElementById("pageInfo").textContent = "Page 0";
        return;
    }

    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const trHead = document.createElement('tr');

    // headers
    Object.keys(pageData[0]).forEach(k => {
        const th = document.createElement('th');
        th.textContent = k;

        // search input
        const input = document.createElement('input');
        input.className = 'filter';
        input.dataset.key = k;
        input.addEventListener('input', filterTable);
        th.appendChild(document.createElement('br'));
        th.appendChild(input);
        trHead.appendChild(th);
    });

    // actions header
    const thActions = document.createElement('th');
    thActions.textContent = "Actions";
    trHead.appendChild(thActions);

    thead.appendChild(trHead);
    table.appendChild(thead);

    const tbody = document.createElement('tbody');

    pageData.forEach(row => {
        const tr = document.createElement('tr');
        Object.keys(row).forEach(k => {
            const td = document.createElement('td');
            td.setAttribute('data-key', k);
            td.setAttribute('contenteditable', 'true');
            td.textContent = row[k] ?? '';
            tr.appendChild(td);
        });

        const tdActions = document.createElement('td');
        tdActions.className = 'actions';
        tdActions.innerHTML = `<button onclick='saveRow(this)'>💾 Save</button>
                               <button onclick='deleteRow(this)'>🗑️ Delete</button>`;
        tr.appendChild(tdActions);

        tbody.appendChild(tr);
    });

    table.appendChild(tbody);
    container.appendChild(table);

    // update page info
    const totalPages = Math.ceil(filteredData.length / pageSize);
    document.getElementById("pageInfo").textContent = `Page ${currentPage} / ${totalPages}`;
}

function filterTable() {
    const filters = {};
    document.querySelectorAll('.filter').forEach(input => {
        const key = input.dataset.key;
        const val = input.value.trim().toLowerCase();
        if (val !== "") filters[key] = val;
    });

    filteredData = tableData.filter(row => {
        return Object.entries(filters).every(([key, val]) =>
            (row[key] ?? "").toString().toLowerCase().includes(val)
        );
    });

    currentPage = 1;
    renderTablePage();
}

function changePageSize(size) {
    pageSize = parseInt(size);
    currentPage = 1;
    renderTablePage();
}

function prevPage() {
    if(currentPage > 1) {
        currentPage--;
        renderTablePage();
    }
}

function nextPage() {
    if(currentPage < Math.ceil(filteredData.length / pageSize)) {
        currentPage++;
        renderTablePage();
    }
}

function addRow() {
    const table = document.querySelector("#tableData table tbody");
    if (!table) return alert("Please select a table first.");

    const headers = Array.from(document.querySelectorAll("#tableData thead th"))
        .map(th => th.innerText)
        .filter(h => h && h !== "Actions");

    const newRow = document.createElement("tr");
    headers.forEach(h => {
        newRow.innerHTML += `<td contenteditable="true" data-key="${h}"></td>`;
    });
    newRow.innerHTML += `<td class="actions">
                            <button onclick='saveRow(this)'>💾 Save</button>
                            <button onclick='deleteRow(this)'>🗑️ Delete</button>
                         </td>`;

    // append at the end of current page in filteredData
    const insertIndex = (currentPage - 1) * pageSize + table.rows.length;
    filteredData.splice(insertIndex, 0, {}); // placeholder
    tableData.push({}); // global storage
    table.appendChild(newRow);
}

async function saveRow(btn) {
    const row = btn.closest('tr');
    const cells = row.querySelectorAll('td[data-key]');
    const data = {};

    cells.forEach(cell => {
        const key = cell.dataset.key;
        const value = cell.innerText.trim();
        if (value !== "") data[key] = value;
    });

    const key = Object.keys(data).includes('word') ? 'word'
              : Object.keys(data).includes('number') ? 'number'
              : 'id';

    if (!data.id) delete data.id;

    const body = { table: currentTable, key, data };
    const res = await fetch('/word', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    alert(JSON.stringify(await res.json(), null, 2));
    loadTable();
}

async function deleteRow(btn) {
    const row = btn.closest('tr');
    const cells = row.querySelectorAll('td[data-key]');
    const data = {};
    cells.forEach(cell => {
        const key = cell.dataset.key;
        const value = cell.innerText.trim();
        if (value !== "") data[key] = value;
    });

    const key = Object.keys(data).includes('word') ? 'word'
              : Object.keys(data).includes('number') ? 'number'
              : 'id';

    const body = { table: currentTable, key, action: 'delete', data };
    const res = await fetch('/word', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    alert(JSON.stringify(await res.json(), null, 2));
    loadTable();
}

async function rerender() {
    const res = await fetch('/render', { method: 'POST' });
    alert(JSON.stringify(await res.json(), null, 2));
}

// auto-load
window.onload = loadTable;
</script>
</body>
</html>
    """


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
