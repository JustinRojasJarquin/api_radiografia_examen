from core.validators.file_validator import validate_image
from core.services.cloudinary_service import upload_image, delete_image


def process_and_upload_image(file) -> dict:
    file_bytes = validate_image(file)
    return upload_image(file_bytes)


def remove_image(public_id: str) -> None:
    delete_image(public_id)
