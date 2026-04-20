from core.settings.security import create_signed_image_token
from core.validators.file_validator import validate_image
from core.services.cloudinary_service import upload_image, delete_image


def process_and_upload_image(file) -> dict:
    file_bytes = validate_image(file)
    return upload_image(file_bytes)


def remove_image(public_id: str) -> None:
    delete_image(public_id)


def generate_signed_image_url(request, user_id: int, record_id: int, image_url: str) -> str:
    token = create_signed_image_token(
        user_id=user_id,
        record_id=record_id,
        image_url=image_url,
    )

    base_url = request.build_absolute_uri("/api/v1/images/view/")
    return f"{base_url}?token={token}"