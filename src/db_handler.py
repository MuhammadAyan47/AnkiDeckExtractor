import sqlite3
from pathlib import Path


class DBExportError(Exception):
    pass


def export_notes(db_path: Path, export_to: Path):
    # Specify "notes" subdirectory within desired export path:
    export_to = export_to.expanduser().resolve() / 'notes'

    # Try to create aforementioned subdirectory:
    try:
        export_to.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise DBExportError(f'❌ >> Failed to export notes to {export_to}'
                            f'📝 >> The following exception was raised:\n{e}'
                            )

    # Try to connect to .anki21 database (SQLite) file:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise DBExportError(f'❌ >> Failed to connect to the database {db_path}'
                            f'📝 >> The following exception was raised:\n{e}'
                            )

    # TODO: Continue...
