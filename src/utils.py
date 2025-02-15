import shutil
from pathlib import Path


def cleanup(temp_dir_path: Path):
    try:
        shutil.rmtree(temp_dir_path)
        print('✅ >> Successfully cleaned up extracted files!')
    except FileNotFoundError:
        print(f'❌ >> Error: Directory not found; cleanup not required.')
    except OSError as e:
        print(f'❌ >> Error: Could not remove the temporary directory {temp_dir_path}.'
              f'📝 >> The following exception was raised:\n{e}'
              )
