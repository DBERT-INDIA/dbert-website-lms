import os
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse

from backend.core.config import settings
from backend.services.file_security_service import (
    validate_and_save_file, FileSecurityError,
    InvalidFileExtensionError, InvalidFileTypeError, FileTooLargeError
)

router = APIRouter(prefix="/uploads", tags=["File Storage"])

@router.post("", summary="Upload Verified Document or Image")
async def upload_file(file: UploadFile = File(...)):
    """Uploads file with magic-byte verification, polyglot rejection, and sandboxing."""
    file_bytes = await file.read()
    try:
        safe_name, relative_url = validate_and_save_file(file.filename, file_bytes)
        return {
            "status": "success",
            "filename": safe_name,
            "url": relative_url,
            "size_bytes": len(file_bytes)
        }
    except (InvalidFileExtensionError, InvalidFileTypeError, FileTooLargeError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Upload failed: {str(e)}")

@router.get("/{filename}", summary="Download / View Uploaded File")
async def get_uploaded_file(filename: str):
    """Serve uploaded file securely."""
    # Defend against path traversal
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(settings.UPLOAD_FOLDER, safe_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return FileResponse(file_path)
