import os
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status

# ✅ settings replace to os.getenv
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

# ─── Allowed file types ───────────────────────────────────────────────────────
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_DOC_TYPES   = {"application/pdf", "application/msword",
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
ALLOWED_ALL_TYPES   = ALLOWED_IMAGE_TYPES | ALLOWED_DOC_TYPES

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


async def upload_file_to_cloudinary(
    file: UploadFile,
    folder: str = "uploads",
    allowed_types: set[str] = ALLOWED_ALL_TYPES,
    max_size: int = MAX_FILE_SIZE,
    public_id: str | None = None,
    transformation: list | None = None,
) -> dict:
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"File type '{file.content_type}' is not allowed. "
                   f"Allowed: {', '.join(sorted(allowed_types))}",
        )

    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max allowed size is {max_size // (1024*1024)} MB.",
        )

    resource_type = "image" if file.content_type in ALLOWED_IMAGE_TYPES else "raw"

    upload_options: dict = {
        "folder": folder,
        "resource_type": resource_type,
        "overwrite": True,
    }
    if public_id:
        upload_options["public_id"] = public_id
    if transformation:
        upload_options["transformation"] = transformation

    try:
        result = cloudinary.uploader.upload(contents, **upload_options)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Cloudinary upload failed: {str(e)}",
        )

    return {
        "url":           result["secure_url"],
        "public_id":     result["public_id"],
        "format":        result.get("format"),
        "resource_type": result.get("resource_type"),
        "bytes":         result.get("bytes"),
    }


async def delete_file_from_cloudinary(
    public_id: str,
    resource_type: str = "image",
) -> bool:
    try:
        result = cloudinary.uploader.destroy(public_id, resource_type=resource_type)
        return result.get("result") == "ok"
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Cloudinary delete failed: {str(e)}",
        )


async def upload_avatar(file: UploadFile, user_id: int | str) -> dict:
    return await upload_file_to_cloudinary(
        file=file,
        folder="avatars",
        allowed_types=ALLOWED_IMAGE_TYPES,
        max_size=5 * 1024 * 1024,
        public_id=f"avatars/user_{user_id}",
        transformation=[
            {"width": 400, "height": 400, "crop": "fill", "gravity": "face"}
        ],
    )


async def upload_post_image(file: UploadFile, post_id: int | str) -> dict:
    return await upload_file_to_cloudinary(
        file=file,
        folder="posts",
        allowed_types=ALLOWED_IMAGE_TYPES,
        public_id=f"posts/post_{post_id}",
    )


async def upload_document(file: UploadFile, owner_id: int | str) -> dict:
    return await upload_file_to_cloudinary(
        file=file,
        folder="documents",
        allowed_types=ALLOWED_DOC_TYPES,
        max_size=20 * 1024 * 1024,
    )