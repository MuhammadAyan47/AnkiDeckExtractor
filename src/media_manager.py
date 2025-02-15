import json
import shutil
from pathlib import Path

from constants import Constants


class MediaExportError(Exception):
    pass


def export_media(export_to: Path):
    # Specify "media" subdirectory within desired export path:
    export_to = export_to.expanduser().resolve() / 'media'

    # Try to create aforementioned subdirectory:
    try:
        export_to.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise MediaExportError(f'❌ >> Failed to export media to {export_to}\n'
                               f'📝 >> The following exception was raised: {e}'
                               )

    # Attempt to find and parse the media JSON mapping file:
    try:
        mapping_file = Constants.TEMP_DIR_PATH / 'media'
        if not mapping_file.is_file():
            raise Exception('No valid "media" mapping file (JSON) was found in extracted .apkg contents.')

        with open(mapping_file, 'r', encoding='utf-8') as f:
            mappings: dict[str, str] = json.load(f)
    except json.JSONDecodeError as e:
        raise MediaExportError('❌ >> Media mappings file contains invalid JSON.\n'
                               f'📝 >> The following exception was raised: {e}'
                               )
    except Exception as e:
        raise MediaExportError(f'❌ >> Could not find media mappings file.\n'
                               f'📝 >> The following exception was raised: {e}'
                               )

    # If there is nothing mapped, we can't find any media for the deck.
    if not mappings or len(mappings) == 0:
        print('🤨 >> No media found for this Anki deck.')
        return

    files: list[str] = [file.name for file in Constants.TEMP_DIR_PATH.iterdir() if
                        file.is_file()]  # List of file names within .temp folder.

    # Copy metric tracker variables:
    successful_copies = 0
    total_media_count = 0

    # Iterate over each key to then associate/copy media files as required:
    for file in files:
        # Skip all non-digit files; these are not media files.
        if not file.isdigit():
            continue
        total_media_count += 1

        # Attempt to get the value (i.e. original media file name) from media JSON mappings.
        try:
            value = mappings.get(file)
            if value is None:
                raise KeyError(f'Key "{file}" not found in mappings.')
        except KeyError as e:
            # Skip this item; no matching media file (name) found!
            print(f'❌ >> {file} does not exist.\n'
                  f'📝 >> The following exception was raised: {e}'
                  )
            continue
        except Exception as e:
            raise MediaExportError(f'❌ >> An unexpected error occurred while accessing the mappings.\n'
                                   f'📝 >> The following exception was raised: {e}'
                                   )

        try:
            unmapped_media_path = Constants.TEMP_DIR_PATH / file
            mapped_media_path = export_to / value  # i.e. value = 170999.mp3

            shutil.copy2(unmapped_media_path, mapped_media_path)
            successful_copies += 1
        except Exception as e:
            print(
                f'❌ >> Could not process media file "{file}" with mapping value "{value}".\n'
                f'📝 >> The following exception was raised: {e}'
            )
            continue

    print(f'✅ >> Completed media extraction! {successful_copies} / {total_media_count} files copied.')
