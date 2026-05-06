from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.orm import Session                          #  sync
from app.dependencies import get_current_user, require_admin
from app.database import get_db
from app.schemas import UploadResponse, UserResponse        #  UserResponse
from app.services.upload import (
    upload_file_to_cloudinary,
    upload_avatar,
    upload_document,
    delete_file_from_cloudinary,
    ALLOWED_IMAGE_TYPES,
    ALLOWED_ALL_TYPES,
)
import app.crud as crud

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_any_file(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),  # ✅
):
    return await upload_file_to_cloudinary(
        file=file,
        folder=f"users/{current_user.id}/uploads",
        allowed_types=ALLOWED_ALL_TYPES,
    )


@router.post("/image", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),  # ✅
):
    return await upload_file_to_cloudinary(
        file=file,
        folder=f"users/{current_user.id}/images",
        allowed_types=ALLOWED_IMAGE_TYPES,
    )


@router.post("/document", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_doc(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),  # ✅
):
    return await upload_document(file=file, owner_id=current_user.id)


@router.post("/avatar", response_model=UploadResponse, status_code=status.HTTP_200_OK)
async def upload_user_avatar(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user), # ✅
    db: Session = Depends(get_db),                          # ✅ sync Session
):
    result = await upload_avatar(file=file, user_id=current_user.id)
    crud.update_user_avatar(db, user_id=current_user.id, avatar_url=result["url"])  # ✅ await নেই
    return result


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_file(
    public_id: str,
    resource_type: str = "image",
    _: UserResponse = Depends(require_admin),     # ✅ cleaner
):
    success = await delete_file_from_cloudinary(public_id=public_id, resource_type=resource_type)
    return {"deleted": success, "public_id": public_id}