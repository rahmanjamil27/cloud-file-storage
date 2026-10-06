import os

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_file(file, filename):
    file.save(os.path.join(UPLOAD_FOLDER, filename))


def list_files():
    return os.listdir(UPLOAD_FOLDER)


def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
