import os
import uuid
import re
from typing import Tuple

from backend.core.config import settings

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
MAX_FILE_SIZE_BYTES = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

MAGIC_SIGNATURES = {
    "png": [b"\x89PNG\r\n\x1a\n"],
    "jpg": [b"\xff\xd8\xff"],
    "jpeg": [b"\xff\xd8\xff"],
    "pdf": [b"%PDF"],
}

MALICIOUS_PAYLOAD_SIGNATURES = [
    b"<?php",
    b"<?= ",
    b"<script",
    b"<SCRIPT",
    b"<% ",
    b"#!/bin/sh",
    b"#!/bin/bash",
    b"eval(",
    b"system(",
    b"passthru(",
    b"shell_exec(",
]

class FileSecurityError(Exception):
    pass

class InvalidFileExtensionError(FileSecurityError):
    pass

class InvalidFileTypeError(FileSecurityError):
    pass

class FileTooLargeError(FileSecurityError):
    pass

def sanitize_filename(filename: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_.-]", "_", filename)
    return cleaned

def validate_and_save_file(filename: str, file_bytes: bytes) -> Tuple[str, str]:
    """Validate file extension, size, magic bytes, and polyglots, then save to upload folder."""
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(f"File size exceeds maximum allowed ({settings.MAX_UPLOAD_SIZE_MB}MB).")

    if "." not in filename:
        raise InvalidFileExtensionError("Filename must contain a valid extension.")
    
    ext = filename.rsplit(".", 1)[1].lower().strip()
    if ext not in ALLOWED_EXTENSIONS:
        raise InvalidFileExtensionError(f"Extension '.{ext}' is not permitted. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    # Magic byte check
    expected_signatures = MAGIC_SIGNATURES.get(ext, [])
    has_valid_magic = any(file_bytes.startswith(sig) for sig in expected_signatures)
    if not has_valid_magic:
        raise InvalidFileTypeError(f"File magic bytes do not match expected format for .{ext}")

    # Malicious payload search
    header_sample = file_bytes[:4096].lower()
    for mal_sig in MALICIOUS_PAYLOAD_SIGNATURES:
        if mal_sig.lower() in header_sample:
            raise InvalidFileTypeError("File rejected: executable or script signature detected in file content.")

    # Save with unique UUID
    os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
    safe_name = f"{uuid.uuid4().hex}_{sanitize_filename(filename)}"
    destination = os.path.join(settings.UPLOAD_FOLDER, safe_name)
    with open(destination, "wb") as f:
        f.write(file_bytes)

    relative_url = f"/uploads/{safe_name}"
    return safe_name, relative_url
