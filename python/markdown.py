import os
import sqlite3
from jinja2 import Environment, FileSystemLoader
from python.constants import MARKDOWN_INPUT_FOLDER_PATH, MARKDOWN_OUTPUT_FOLDER_PATH, DB_FILE, TABLES

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


def render_markdown(input_folder=MARKDOWN_INPUT_FOLDER_PATH, output_folder=MARKDOWN_OUTPUT_FOLDER_PATH):
    # 1. Fetch all tables
    all_data = {}
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row  # Fetch rows as dict-like objects
        c = conn.cursor()
        
        for table in TABLES:
            c.execute(f"SELECT * FROM {table}")
            rows = c.fetchall()
            table_data = [{k: (v if v is not None else "") for k, v in dict(row).items()} for row in rows]
            all_data[table] = table_data
    
    # Create example map for efficient lookup
    examples = {}
    for ex in all_data['examples']:
        key = (ex["table_name"], ex["word_id"])
        examples.setdefault(key, []).append(ex)

    # 2. Set up Jinja2
    env = Environment(loader=FileSystemLoader(input_folder))
    env.filters['sort_items'] = sort_items
    env.filters['default_sort'] = default_sort

    # 3. Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # 4. Iterate over all markdown files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".md"):
            template = env.get_template(filename)
            rendered = template.render(tables=all_data, examples=examples)

            output_path = os.path.join(output_folder, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✅ Markdown file generated: {output_path}")
