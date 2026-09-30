import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from app.config import get_settings
from app.i18n import message

ALLOWED = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}
MAX_IMAGE_PIXELS = 20_000_000


async def save_evidence(upload: UploadFile, language: str) -> str:
    settings = get_settings()
    root = Path(settings.upload_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    data = await upload.read(settings.max_upload_bytes + 1)
    if not data or len(data) > settings.max_upload_bytes:
        raise HTTPException(422, message("invalid_image", language))
    try:
        from io import BytesIO
        with Image.open(BytesIO(data)) as image:
            image.verify()
            kind = image.format
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise ValueError("image dimensions are too large")
        if kind not in ALLOWED:
            raise ValueError("unsupported image type")
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(422, message("invalid_image", language)) from None
    name = f"{uuid.uuid4().hex}{ALLOWED[kind]}"
    target = root / name
    target.write_bytes(data)
    os.chmod(target, 0o600)
    return name
