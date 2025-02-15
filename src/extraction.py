import zipfile
from pathlib import Path


class ExtractionError(Exception):
    pass


def extract_apkg(apkg_path: Path, extract_to: Path):
    try:
        with zipfile.ZipFile(apkg_path, 'r') as zf:
            zf.extractall(extract_to)
    except zipfile.BadZipFile as e:
        raise ExtractionError(
            f'❌ >> The file {apkg_path} is not a valid .apkg archive.'
            f'📝 >> The following exception was raised:\n{e}'
        )
    except FileNotFoundError as e:
        raise ExtractionError(f'❌ >> File not found during extraction.'
                              f'📝 >> The following exception was raised:\n{e}'
                              )
    except PermissionError as e:
        raise ExtractionError(
            f'❌ >> Permission denied during extraction of {apkg_path}.'
            f'📝 >> The following exception was raised:\n{e}'
        )
    except Exception as e:
        raise ExtractionError(
            f'❌ >> An unexpected error occurred during extraction.'
            f'📝 >> The following exception was raised:\n{e}'
        )
