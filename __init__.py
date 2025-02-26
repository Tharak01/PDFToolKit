"""
PDFToolkit - A comprehensive toolkit for PDF manipulation

PDFToolkit provides a collection of utilities for working with PDF files,
including compression, conversion, encryption, and merging functionality.
"""

__version__ = "0.1.0"
__author__ = "Tharakeshavn Parthasarathy"

from .compressor import PDFCompressor
from .converter import PDFToExcelConverter, PDFToWordConverter
from .encryption import PDFEncryptor
from .merger import PDFMerger
from .validators import validate_pdf
from .logger import setup_logger

class PDFToolkit:    
    def __init__(self, logger=None):
        """
        Initialize the PDFToolkit with optional logger.
        
        Args:
            logger: Optional logger instance. If None, a default logger will be used.
        """
        self.logger = logger if logger else setup_logger("PDFToolkit")
        self.compressor = PDFCompressor(logger=self.logger)
        self.excel_converter = PDFToExcelConverter(logger=self.logger)
        self.word_converter = PDFToWordConverter(logger=self.logger)
        self.encryptor = PDFEncryptor(logger=self.logger)
        self.merger = PDFMerger(logger=self.logger)