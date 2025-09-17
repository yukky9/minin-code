from config import MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_size(file_content_length):
    return file_content_length <= MAX_CONTENT_LENGTH
