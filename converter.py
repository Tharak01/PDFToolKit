"""
PDF conversion functionality.
"""
import os
import io
import tempfile
from typing import Union, BinaryIO, Optional, List, Tuple, Dict, Any
import pandas as pd
from .validators import validate_pdf
from .logger import setup_logger


class PDFToExcelConverter:
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_logger("PDFToExcelConverter")
    
    def convert(self, 
               input_pdf: Union[str, BinaryIO, bytes], 
               output_path: Optional[str] = None,
               batch_size: int = 5) -> Union[bytes, str, Tuple[bool, str]]:
        """
        Convert PDF tables to Excel format.
        
        Args:
            input_pdf: Path to a PDF file, file-like object, or bytes content
            output_path: Optional path to save the Excel file. If None, returns the Excel file as bytes.
            batch_size: Number of pages to process in each batch
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: 
                - If output_path is None: The Excel file as bytes
                - If output_path is provided: The path to the saved Excel file
                - If an error occurs or no tables are found: A tuple (False, error_message)
        """
        try:
            is_valid, error_message = validate_pdf(input_pdf)
            if not is_valid:
                self.logger.error(f"Validation failed: {error_message}")
                return False, error_message
                
            try:
                import pdfplumber
            except ImportError:
                self.logger.error("pdfplumber is required for PDF to Excel conversion")
                return False, "pdfplumber is required for PDF to Excel conversion. Install it with 'pip install pdfplumber'."
                
            if isinstance(input_pdf, str):
                with pdfplumber.open(input_pdf) as pdf:
                    return self._extract_and_save_tables(pdf, output_path, batch_size)
            elif hasattr(input_pdf, 'read') and callable(input_pdf.read):
                current_pos = input_pdf.tell()
                
                input_pdf.seek(0)
                content = input_pdf.read()
                
                input_pdf.seek(current_pos)
                
                with pdfplumber.open(io.BytesIO(content)) as pdf:
                    return self._extract_and_save_tables(pdf, output_path, batch_size)
            elif isinstance(input_pdf, bytes):
                with pdfplumber.open(io.BytesIO(input_pdf)) as pdf:
                    return self._extract_and_save_tables(pdf, output_path, batch_size)
            else:
                return False, "Unsupported input type"
                
        except Exception as e:
            error_msg = f"An error occurred during PDF to Excel conversion: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg
    
    def _extract_and_save_tables(self, 
                               pdf, 
                               output_path: Optional[str] = None,
                               batch_size: int = 5) -> Union[bytes, str, Tuple[bool, str]]:
        """
        Extract tables from PDF and save to Excel.
        
        Args:
            pdf: pdfplumber PDF object
            output_path: Path to save Excel file
            batch_size: Number of pages to process in each batch
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: Excel file as bytes, path, or error
        """
        tables_list = []
        total_pages = len(pdf.pages)
        self.logger.info(f"Processing PDF with {total_pages} pages")
        
        for batch_start in range(0, total_pages, batch_size):
            batch_end = min(batch_start + batch_size, total_pages)
            self.logger.info(f"Processing pages {batch_start+1} to {batch_end}")
            
            for page in pdf.pages[batch_start:batch_end]:
                page_tables = page.extract_tables()
                if page_tables:
                    for table in page_tables:
                        if len(table) > 1:
                            header = table[0]
                            data = table[1:]
                            df = pd.DataFrame(data, columns=header)
                        else:
                            df = pd.DataFrame(table)
                        tables_list.append(df)
        
        if not tables_list:
            self.logger.warning("No tables found in the PDF")
            return False, "No tables found in the PDF"
            
        combined_df = pd.concat(tables_list, ignore_index=True)
        
        if output_path:
            combined_df.to_excel(output_path, index=False)
            self.logger.info(f"Excel file saved to: {output_path}")
            return output_path
        else:
            output_buffer = io.BytesIO()
            with pd.ExcelWriter(output_buffer, engine='xlsxwriter') as writer:
                combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
            output_buffer.seek(0)
            self.logger.info("PDF to Excel conversion completed successfully")
            return output_buffer.getvalue()


class PDFToWordConverter:
    def __init__(self, logger=None):
        self.logger = logger if logger else setup_logger("PDFToWordConverter")
    
    def convert(self, 
               input_pdf: Union[str, BinaryIO, bytes], 
               output_path: Optional[str] = None,
               start_page: int = 0,
               end_page: Optional[int] = None) -> Union[bytes, str, Tuple[bool, str]]:
        """
        Convert PDF to Word format.
        
        Args:
            input_pdf: Path to a PDF file, file-like object, or bytes content
            output_path: Optional path to save the Word file. If None, returns the Word file as bytes.
            start_page: First page to convert (0-based)
            end_page: Last page to convert (inclusive), or None for all pages
            
        Returns:
            Union[bytes, str, Tuple[bool, str]]: 
                - If output_path is None: The Word file as bytes
                - If output_path is provided: The path to the saved Word file
                - If an error occurs: A tuple (False, error_message)
        """
        try:
            is_valid, error_message = validate_pdf(input_pdf)
            if not is_valid:
                self.logger.error(f"Validation failed: {error_message}")
                return False, error_message
                
            try:
                from pdf2docx import Converter
            except ImportError:
                self.logger.error("pdf2docx is required for PDF to Word conversion")
                return False, "pdf2docx is required for PDF to Word conversion. Install it with 'pip install pdf2docx'."
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                if isinstance(input_pdf, str):
                    with open(input_pdf, 'rb') as f:
                        temp_pdf.write(f.read())
                elif hasattr(input_pdf, 'read') and callable(input_pdf.read):
                    current_pos = input_pdf.tell()
                    
                    input_pdf.seek(0)
                    temp_pdf.write(input_pdf.read())
                    
                    input_pdf.seek(current_pos)
                elif isinstance(input_pdf, bytes):
                    temp_pdf.write(input_pdf)
                else:
                    return False, "Unsupported input type"
                temp_pdf_path = temp_pdf.name
            
            if output_path:
                temp_docx_path = output_path
                delete_output = False
            else:
                temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                temp_docx.close()
                temp_docx_path = temp_docx.name
                delete_output = True
            
            try:
                self.logger.info(f"Converting PDF to Word (pages {start_page} to {end_page or 'end'})")
                cv = Converter(temp_pdf_path)
                cv.convert(temp_docx_path, start=start_page, end=end_page)
                cv.close()
                
                if output_path:
                    self.logger.info(f"Word file saved to: {output_path}")
                    return output_path
                else:
                    with open(temp_docx_path, 'rb') as f:
                        docx_data = f.read()
                    self.logger.info("PDF to Word conversion completed successfully")
                    return docx_data
                    
            finally:
                try:
                    os.remove(temp_pdf_path)
                    self.logger.debug(f"Deleted temporary PDF file: {temp_pdf_path}")
                except:
                    pass
                    
                if delete_output:
                    try:
                        os.remove(temp_docx_path)
                        self.logger.debug(f"Deleted temporary Word file: {temp_docx_path}")
                    except:
                        pass
                
        except Exception as e:
            error_msg = f"An error occurred during PDF to Word conversion: {str(e)}"
            self.logger.error(error_msg)
            return False, error_msg