# Templates
TEMPLATE_FOLDER_PATH = "templates/"
MARKDOWN_TEMPLATE_FOLDER_PATH= "templates/markdown/"
MARKDOWN_OUTPUT_FOLDER_PATH = "output/"
MANAGE_TEMPLATE_PATH = "html/manage-db/manage.html"
NOTEBOOK_TEMPLATE_PATH = "html/notebook/notebook.html"


# Database
DB_FILE = "resources/db/database.db"
DDL_SCRIPT_PATH = "resources/sql/ddl.sql"

TABLES = [
    "adverbs_adjectives",
    "nouns",
    "verbs",
    "numbers",
    "prepositions",
    "examples"
]

COLUMNS_WITH_DEFAULT_VALUES = ['id', 'difficulty', 'created_at']
