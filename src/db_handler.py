import json
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
        raise DBExportError(f'❌ >> Failed to export notes to {export_to}\n'
                            f'📝 >> The following exception was raised: {e}'
                            )

    # Try to connect to .anki21 database (SQLite) file:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise DBExportError(f'❌ >> Failed to connect to the database {db_path}\n'
                            f'📝 >> The following exception was raised: {e}'
                            )

    # Execute SQL query to fetch notes from database:
    try:
        cursor.execute('SELECT id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data FROM notes')
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        conn.close()
        raise DBExportError(f'❌ >> Failed to fetch notes from database.\n'
                            f'📝 >> The following exception was raised: {e}'
                            )

    exported_count: int = 0
    for row in rows:
        try:
            # Organise data stored in SQL for given row into a JSON object:
            note_id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data = row
            note_data: dict = {
                'id': note_id,
                'guid': guid,
                'mid': mid,
                'mod': mod,
                'usn': usn,
                'tags': tags.strip().split(' ') if tags else None,
                'fields': [fld for fld in flds.split('\x1f') if fld] if flds else None,
                'sort_field': sfld,
                'csum': csum,
                'flags': flags,
                'data': data if data else None
            }

            # Save data to a JSON file within output directory, and then increment exported count by 1.
            note_filename = export_to / f'note_{note_id}.json'
            with open(note_filename, 'w', encoding='utf-8') as f:
                json.dump(note_data, f, ensure_ascii=False, indent=4)
            exported_count += 1
        except Exception as e:
            print(f'❌ >> Failed to export note with ID <{row[0]}>.\n'
                  f'📝 >> The following exception was raised: {e}'
                  )

    try:
        conn.close()
    except Exception as e:
        print(f'❌ >> Failed to close connection to database.\n'
              f'📝 >> The following exception was raised: {e}'
              )

    print(f'✅ >> Exported {exported_count} notes to {export_to}.')
