from pathlib import Path
import uuid
import backend
from werkzeug.datastructures import FileStorage


def save_file_to_disk(file: FileStorage) -> str:
    """Save file to the UPLOAD_FOLDER / <random_base_name>."""
    # Return the base filename.
    stem = uuid.uuid4().hex
    suffix = Path(file.filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"
    path = backend.app.config["UPLOAD_FOLDER"] / uuid_basename
    file.save(path)
    return uuid_basename
