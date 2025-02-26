"""
Validation utilities for PDF files.
"""

import os
import magic
from typing import BinaryIO, Union, Tuple, Optional

MAX_FILE_SIZE = 30 * 1024 * 1024  # 30 MB
ALLOWED_MIME_TYPES = ['application/pdf']


class ValidationError(Exception):
    """Exception raised when PDF validation fails."""
    pass


def validate_pdf_mime(file_content: bytes) -> bool:
    """
    Validate that the file content is a PDF based on MIME type.
    """
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file_content[:1024])
    return file_mime_type in ALLOWED_MIME_TYPES


def validate_pdf_size(file_size: int, max_size: int = MAX_FILE_SIZE) -> bool:
    """
    Validate that the file size is within the allowed limit.
    """
    return file_size <= max_size


def validate_pdf(file: Union[str, BinaryIO, bytes], 
                max_size: int = MAX_FILE_SIZE) -> Tuple[bool, Optional[str]]:
    """
    Validate that the file is a valid PDF and meets size requirements.
    """
    try:
        if isinstance(file, str):
            if not os.path.exists(file):
                return False, f"File not found: {file}"
            
            file_size = os.path.getsize(file)
            if not validate_pdf_size(file_size, max_size):
                return False, f"File size exceeds the maximum limit of {max_size / (1024 * 1024):.2f} MB"
            
            with open(file, 'rb') as f:
                content = f.read(1024)
                if not validate_pdf_mime(content):
                    return False, "File is not a valid PDF"
                
        elif hasattr(file, 'read') and callable(file.read):
            if hasattr(file, 'size'):
                file_size = file.size
                if not validate_pdf_size(file_size, max_size):
                    return False, f"File size exceeds the maximum limit of {max_size / (1024 * 1024):.2f} MB"
            
            current_pos = file.tell()
            
            file.seek(0)
            content = file.read(1024)
            
            file.seek(current_pos)
            
            if not validate_pdf_mime(content):
                return False, "File is not a valid PDF"
                
        elif isinstance(file, bytes):
            if not validate_pdf_size(len(file), max_size):
                return False, f"File size exceeds the maximum limit of {max_size / (1024 * 1024):.2f} MB"
            
            if not validate_pdf_mime(file[:1024]):
                return False, "Content is not a valid PDF"
        else:
            return False, "Unsupported file type"
            
        return True, None
        
    except Exception as e:
        return False, f"Error validating PDF: {str(e)}"