from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 3  # 3mb

def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 3MB.")