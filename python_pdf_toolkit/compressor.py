"""
PDF compression functionality.
"""
import os
import io
from typing import Union, BinaryIO, Optional, Tuple
from pypdf import PdfWriter, PdfReader
from .validators import validate_pdf
from .logger import setup_logger


class PDFCompressor:
    def __init__(self, logger=None):
        """
        Initialize the PDF compressor.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger if logger else setup_logger("PDFCompressor")
    
    def compress(self, 
                input_pdf: Union[str, BinaryIO, bytes], 
                output_path: Optional[str] = None,
                compression_level: int = 5) -> Union[bytes, str, Tuple[bool, str]]:
        """
        Compress the input PDF.
        
        Args:
            input_pdf: Path to a PDF file, file-like object, or bytes content
            output_path: Optional path to save the compressed PDF. If None, returns the PDF as bytes.
            compression_level: Compression level (1-10), where 10 is highest compression
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: 
                - If output_path is None: The compressed PDF as bytes
                - If output_path is provided: The path to the saved compressed PDF
                - If an error occurs: A tuple (False, error_message)
        """
        try:
            is_valid, error_message = validate_pdf(input_pdf)
            if not is_valid:
                self.logger.error(f"Validation failed: {error_message}")
                return False, error_message
                
            compression_level = min(max(1, compression_level), 10)
            compress_level = compression_level * 2 if compression_level < 5 else 9
            self.logger.debug(f"Using compression level: {compress_level}")
            
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
                
            for page in writer.pages:
                for img in getattr(page, 'images', []):
                    img.replace(img.image, quality=60)
                page.compress_content_streams(level=compress_level)
                
            writer.compress_identical_objects(remove_identicals=False, remove_orphans=True)
            
            if output_path:
                with open(output_path, 'wb') as f:
                    writer.write(f)
                writer.close()
                self.logger.info(f"Compressed PDF saved to: {output_path}")
                return output_path
            else:
                output_buffer = io.BytesIO()
                writer.write(output_buffer)
                writer.close()
                output_buffer.seek(0)
                self.logger.info("PDF compression completed successfully")
                return output_buffer.getvalue()
                
        except Exception as e:
            error_msg = f"An error occurred during compression: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg