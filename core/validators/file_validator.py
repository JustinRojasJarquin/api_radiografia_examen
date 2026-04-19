from django.core.exceptions import ValidationError

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE_MB = 5
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024


def validate_image(file) -> bytes:
    if file.content_type not in ALLOWED_TYPES:
        raise ValidationError(
            f"Tipo de archivo no permitido. Use: {', '.join(ALLOWED_TYPES)}"
        )

    if file.size > MAX_SIZE_BYTES:
        raise ValidationError(
            f"El archivo excede el tamaño máximo de {MAX_SIZE_MB}MB"
        )

    return file.read()
