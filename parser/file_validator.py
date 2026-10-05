import magic
import os
from fastapi import UploadFile
import fitz


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".doc"
}

ALLOWED_MIME_TYPES = {
    "application/pdf",

    "application/msword",

    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

ALLOWED_MAGIC = {
    "application/pdf",

    "application/msword",

    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

MAX_FILE_SIZE = 20 * 1024 * 1024      # 20 MB

MAX_PAGES = 10


def validate_extension(filename: str):

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported extension: {extension}"

    return True, "Valid extension"


def validate_magic(file_path: str):

    mime = magic.from_file(file_path, mime=True)

    if mime not in ALLOWED_MAGIC:
        return False, f"Magic type mismatch: {mime}"

    return True, "Valid file signature"


def validate_mime_type(file_path: str):

    mime = magic.from_file(file_path, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        return False, f"Unsupported MIME type: {mime}"

    return True, "Valid MIME type"


def validate_file_size(file_path: str):

    size = os.path.getsize(file_path)

    if size > MAX_FILE_SIZE:
        return False, f"File size exceeds {MAX_FILE_SIZE / (1024 * 1024)} MB"

    return True, "Valid file size"


def validate_page_count(file_path: str):

    extension = os.path.splitext(file_path)[1].lower()

    if extension != ".pdf":
        return True, "Page validation skipped"

    try:

        document = fitz.open(file_path)

        page_count = len(document)

        document.close()

    except Exception as e:

        return False, str(e)

    if page_count > MAX_PAGES:

        return False, f"PDF contains {page_count} pages (limit {MAX_PAGES})"

    return True, "Valid page count"



def validate_upload( file_path: str):

    try:
        document = fitz.open(file_path)

        document.close()

        #return True

    except Exception:
        return False,"File Corrupt"
    #print("xd")
    validators = [

        validate_extension(file_path),

        validate_mime_type(file_path),

        validate_magic(file_path),

        validate_file_size(file_path),

        validate_page_count(file_path)

    ]

    for valid, message in validators:

        if not valid:
            return False, message

    return True, "Validation successful"



#print(validate_upload("./cvs/cvs/cv14.pdf"))