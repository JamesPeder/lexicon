import sqlite3
from jinja2 import Environment, FileSystemLoader
from python.constants import *

def sort_items(items, *attributes, reverse=True):
    """
    Sorts a list of objects or dicts by multiple attributes (in descending order by default).
    
    Example:
        {{ tables.numbers | sort_items('difficulty', 'created_at') }}
    """
    if not attributes:
        return items  # nothing to sort by

    # Apply stable sorting in reverse order of priority
    for attr in reversed(attributes):
        items = sorted(
            items,
            key=lambda x: (
                x.get(attr) if isinstance(x, dict) else getattr(x, attr, None)
            ),
            reverse=reverse
        )
    return items

def default_sort(items):
    """
    Sorts items by difficulty (primary) and created_at (secondary), descending order.
    """
    return sort_items(items, 'difficulty', 'created_at')


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
    
    # Create separate example map for efficieny look-up
    examples = {}
    for ex in all_data['examples']:
        key = (ex["table_name"], ex["word_id"])
        examples.setdefault(key, []).append(ex)
        
    # 2. Set up Jinja2
    env = Environment(loader=FileSystemLoader("."))
    env.filters['sort_items'] = sort_items
    env.filters['default_sort'] = default_sort
    template = env.get_template(TEMPLATE_PATH)

    # 3. Render template with all table data
    output_md = template.render(tables=all_data, examples=examples)

    # 4. Write output
    with open(OUTPUT_PATH, "w") as f:
        f.write(output_md)

    print(f"✅ Markdown file generated: {OUTPUT_PATH}")
