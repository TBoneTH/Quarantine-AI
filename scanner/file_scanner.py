import os

def get_file_info(filepath):
    filename = os.path.basename(filepath)
    extension = os.path.splitext(filepath)[1]

    size_bytes = os.path.getsize(filepath)
    size_mb = round(size_bytes / (1024 * 1024), 2)

    return {
        "filename": filename,
        "extension": extension,
        "size_mb": size_mb
    }