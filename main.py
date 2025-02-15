import argparse
import sys
from pathlib import Path

from src.extraction import extract_apkg


def main():
    # Define parser & relevant arguments to enable basic CLI functionality:
    parser = argparse.ArgumentParser(
        description='Unpack .apkg archives (Anki Flashcard Deck) into their derivative directories & files/metadata.')
    parser.add_argument('apkg', type=str, help='Path to the apkg archive.')
    parser.add_argument('output', type=str, help='Path to the output directory.', default='./output')

    # Parse arguments for processing:
    args = parser.parse_args()

    # Convert input for paths into more workable format (Path from pathlib):
    apkg_path = Path(args.apkg)
    output_path = Path(args.output)

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
            f'❌ >> Error: Cannot create or access output directory at {output_path}.'
            f'📝 >> The following exception was raised:\n{e}'
        )

    try:
        extract_apkg(apkg_path, output_path)
    except Exception as e:
        sys.exit(
            f'❌ >> Error: Extraction of .apkg archive failed.'
            f'📝 >> The following exception was raised:\n{e}'
        )

    print('✅ >> Extraction successful!')

    # -- TODO: Write logic to process extracted files. --

    exit(0)


if __name__ == '__main__':
    main()
