from pathlib import Path


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

    # TODO: Continue...
