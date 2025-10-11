import sqlite3
from jinja2 import Environment, FileSystemLoader

TEMPLATE_PATH = "resources/notebook.md"
OUTPUT_PATH = "resources/preview.md"
DB_FILE = "database.db"

TABLES = [
    "adverbs_adjectives",
    "nouns",
    "verbs",
    "numbers"
]

def render_markdown():

    # 1. Fetch all tables
    all_data = {}
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row  # Fetch rows as dict-like objects
        c = conn.cursor()
        
        for table in TABLES:
            c.execute(f"SELECT * FROM {table}")
            rows = c.fetchall()
            # Convert rows to list of dicts, replacing None with ""
            table_data = []
            for row in rows:
                row_dict = {k: (v if v is not None else "") for k, v in dict(row).items()}
                table_data.append(row_dict)
            all_data[table] = table_data

    # 2. Set up Jinja2
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(TEMPLATE_PATH)

    # 3. Render template with all table data
    output_md = template.render(tables=all_data)

    # 4. Write output
    with open(OUTPUT_PATH, "w") as f:
        f.write(output_md)

    print(f"✅ Markdown file generated: {OUTPUT_PATH}")
