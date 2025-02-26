"""
PDF merging functionality.
"""

import os
import io
from typing import Union, BinaryIO, List, Optional, Tuple
from pypdf import PdfWriter, PdfReader
from .validators import validate_pdf
from .logger import setup_logger


class PDFMerger:
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_logger("PDFMerger")
    
    def merge(self, 
             input_pdfs: List[Union[str, BinaryIO, bytes]], 
             output_path: Optional[str] = None) -> Union[bytes, str, Tuple[bool, str]]:
        """
        Merge multiple PDF files.
        
        Args:
            input_pdfs: List of PDF files (paths, file-like objects, or bytes)
            output_path: Optional path to save the merged PDF. If None, returns the PDF as bytes.
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: 
                - If output_path is None: The merged PDF as bytes
                - If output_path is provided: The path to the saved merged PDF
                - If an error occurs: A tuple (False, error_message)
        """
        try:
            if not input_pdfs:
                self.logger.error("No PDF files provided for merging")
                return False, "No PDF files provided for merging"
                
            if len(input_pdfs) < 2:
                self.logger.error("At least two PDF files are required for merging")
                return False, "At least two PDF files are required for merging"
                
            for i, pdf in enumerate(input_pdfs):
                is_valid, error_message = validate_pdf(pdf)
                if not is_valid:
                    self.logger.error(f"Validation failed for PDF #{i+1}: {error_message}")
                    return False, f"Validation failed for PDF #{i+1}: {error_message}"
            
            merger = PdfWriter()
            
            for i, pdf in enumerate(input_pdfs):
                try:
                    if isinstance(pdf, str):
                        self.logger.info(f"Adding PDF #{i+1} from file: {pdf}")
                        merger.append(pdf)
                    elif hasattr(pdf, 'read') and callable(pdf.read):
                        current_pos = pdf.tell()
                        
                        pdf.seek(0)
                        merger.append(pdf)
                        
                        pdf.seek(current_pos)
                        
                        self.logger.info(f"Adding PDF #{i+1} from file-like object")
                    elif isinstance(pdf, bytes):
                        merger.append(io.BytesIO(pdf))
                        self.logger.info(f"Adding PDF #{i+1} from bytes")
                    else:
                        return False, f"Unsupported input type for PDF #{i+1}"
                except Exception as e:
                    self.logger.error(f"Error adding PDF #{i+1}: {e}")
                    return False, f"Error adding PDF #{i+1}: {str(e)}"
            
            if output_path:
                with open(output_path, 'wb') as f:
                    merger.write(f)
                merger.close()
                self.logger.info(f"Merged PDF saved to: {output_path}")
                return output_path
            else:
                output_buffer = io.BytesIO()
                merger.write(output_buffer)
                merger.close()
                output_buffer.seek(0)
                self.logger.info("PDF merging completed successfully")
                return output_buffer.getvalue()
                
        except Exception as e:
            error_msg = f"An error occurred during PDF merging: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg