import cloudinary.uploader
import core.settings.cloudinary_config  # noqa: F401 - initializes cloudinary config


def upload_image(file_bytes: bytes, folder: str = "radiography") -> dict:
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,
        resource_type="image",
    )
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }


def delete_image(public_id: str) -> None:
    cloudinary.uploader.destroy(public_id)
