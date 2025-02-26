"""
PDF encryption and decryption functionality.
"""

import os
import io
from typing import Union, BinaryIO, Optional, Tuple
from pypdf import PdfWriter, PdfReader
from .validators import validate_pdf
from .logger import setup_logger


class PDFEncryptor:
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_logger("PDFEncryptor")
    
    def encrypt(self, 
               input_pdf: Union[str, BinaryIO, bytes], 
               password: str,
               output_path: Optional[str] = None,
               algorithm: str = "AES-256-R5") -> Union[bytes, str, Tuple[bool, str]]:
        """
        Encrypt the input PDF with a password.
        
        Args:
            input_pdf: Path to a PDF file, file-like object, or bytes content
            password: Password to encrypt the PDF with
            output_path: Optional path to save the encrypted PDF. If None, returns the PDF as bytes.
            algorithm: Encryption algorithm to use
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: 
                - If output_path is None: The encrypted PDF as bytes
                - If output_path is provided: The path to the saved encrypted PDF
                - If an error occurs: A tuple (False, error_message)
        """
        try:
            is_valid, error_message = validate_pdf(input_pdf)
            if not is_valid:
                self.logger.error(f"Validation failed: {error_message}")
                return False, error_message
                
            if not password:
                self.logger.error("Password is required for encryption")
                return False, "Password is required for encryption"
            
            if isinstance(input_pdf, str):
                reader = PdfReader(input_pdf)
                self.logger.info(f"Reading PDF from file: {input_pdf}")
            elif hasattr(input_pdf, 'read') and callable(input_pdf.read):
                current_pos = input_pdf.tell()
                
                input_pdf.seek(0)
                reader = PdfReader(input_pdf)
                
                input_pdf.seek(current_pos)
                
                self.logger.info("Reading PDF from file-like object")
            elif isinstance(input_pdf, bytes):
                reader = PdfReader(io.BytesIO(input_pdf))
                self.logger.info("Reading PDF from bytes")
            else:
                return False, "Unsupported input type"
                
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
                
            writer.encrypt(password, algorithm=algorithm)
            
            if output_path:
                with open(output_path, 'wb') as f:
                    writer.write(f)
                writer.close()
                self.logger.info(f"Encrypted PDF saved to: {output_path}")
                return output_path
            else:
                output_buffer = io.BytesIO()
                writer.write(output_buffer)
                writer.close()
                output_buffer.seek(0)
                self.logger.info("PDF encryption completed successfully")
                return output_buffer.getvalue()
                
        except Exception as e:
            error_msg = f"An error occurred during encryption: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def decrypt(self, 
               input_pdf: Union[str, BinaryIO, bytes], 
               password: str,
               output_path: Optional[str] = None) -> Union[bytes, str, Tuple[bool, str]]:
        """
        Decrypt the input PDF with a password.
        
        Args:
            input_pdf: Path to a PDF file, file-like object, or bytes content
            password: Password to decrypt the PDF
            output_path: Optional path to save the decrypted PDF. If None, returns the PDF as bytes.
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: 
                - If output_path is None: The decrypted PDF as bytes
                - If output_path is provided: The path to the saved decrypted PDF
                - If an error occurs: A tuple (False, error_message)
        """
        try:
            is_valid, error_message = validate_pdf(input_pdf)
            if not is_valid:
                self.logger.error(f"Validation failed: {error_message}")
                return False, error_message
                
            if not password:
                self.logger.error("Password is required for decryption")
                return False, "Password is required for decryption"
            
            if isinstance(input_pdf, str):
                reader = PdfReader(input_pdf)
                self.logger.info(f"Reading PDF from file: {input_pdf}")
            elif hasattr(input_pdf, 'read') and callable(input_pdf.read):
                current_pos = input_pdf.tell()
                
                input_pdf.seek(0)
                reader = PdfReader(input_pdf)
                
                input_pdf.seek(current_pos)
                
                self.logger.info("Reading PDF from file-like object")
            elif isinstance(input_pdf, bytes):
                reader = PdfReader(io.BytesIO(input_pdf))
                self.logger.info("Reading PDF from bytes")
            else:
                return False, "Unsupported input type"
                
            if not reader.is_encrypted:
                self.logger.warning("The PDF is not encrypted")
                return False, "The PDF is not encrypted"
                
            try:
                reader.decrypt(password)
            except Exception:
                self.logger.error("Incorrect password or failed to decrypt the PDF")
                return False, "Incorrect password or failed to decrypt the PDF"
                
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
                
            if output_path:
                with open(output_path, 'wb') as f:
                    writer.write(f)
                writer.close()
                self.logger.info(f"Decrypted PDF saved to: {output_path}")
                return output_path
            else:
                output_buffer = io.BytesIO()
                writer.write(output_buffer)
                writer.close()
                output_buffer.seek(0)
                self.logger.info("PDF decryption completed successfully")
                return output_buffer.getvalue()
                
        except Exception as e:
            error_msg = f"An error occurred during decryption: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg