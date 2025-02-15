import argparse
import sys
from pathlib import Path

from src.db_handler import export_notes
from src.extraction import extract_apkg
from src.utils import cleanup

TEMP_DIR_PATH = Path('.temp')


def main():
    # Define parser & relevant arguments to enable basic CLI functionality:
    parser = argparse.ArgumentParser(
        description='Unpack .apkg archives (Anki Flashcard Deck) into their derivative directories & files/metadata.')
    parser.add_argument('apkg', type=str, help='Path to the apkg archive.')
    parser.add_argument('output', type=str, help='Path to the output directory.', default='./output', nargs='?')

    # Parse arguments for processing:
    args = parser.parse_args()

    # Convert input for paths into more workable format (Path from pathlib):
    apkg_path = Path(args.apkg).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    # Cannot continue if APKG doesn't exist at provided path/is not a file; must also be of type .apkg.
    if not apkg_path.exists():
        sys.exit(f'❌ >> Error: {apkg_path} does not exist.')
    if not apkg_path.is_file():
        sys.exit(f'❌ >> Error: {apkg_path} is not a file.')
    if not apkg_path.suffix.lower() == '.apkg':
        sys.exit(f'❌ >> Error: {apkg_path} is not an .apkg file.')

    # Attempt to create the output directory:
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        sys.exit(
            f'❌ >> Error: Cannot create or access output directory at {output_path}.\n'
            f'📝 >> The following exception was raised: {e}'
        )

    try:
        extract_apkg(apkg_path, TEMP_DIR_PATH)
    except Exception as e:
        sys.exit(
            f'❌ >> Error: Extraction of .apkg archive failed.\n'
            f'📝 >> The following exception was raised: {e}'
        )

    print('✅ >> Extraction successful!')

    try:
        # Construct file path for database location, ensuring it exists before exporting notes.
        db_path = TEMP_DIR_PATH / 'collection.anki21'
        if not db_path.exists() or not db_path.is_file():
            raise Exception('No valid "collection.anki21" database file was found in extracted .apkg contents')

        # Attempt to export notes to user-specified/default output directory:
        export_notes(db_path, output_path)
    except Exception as e:
        sys.exit(f'❌ >> Error: Extraction of .apkg archive failed.\n'
                 f'📝 >> The following exception was raised: {e}'
                 )

    # -- TODO: Write logic to process extracted files. --

    finally:
        # Run cleanup - delete all remnants of unpacked .apkg file from .temp folder.
        cleanup(TEMP_DIR_PATH)


if __name__ == '__main__':
    main()
