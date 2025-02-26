#!/usr/bin/env python
"""
Comprehensive test suite for PDFToolkit package.
"""

import os
import unittest
import tempfile
import shutil
from pathlib import Path
import pandas as pd
import Python_pdf_toolkit
from python_pdf_toolkit import PDFToolkit
from pdf_toolkit.logger import setup_logger


class TestPDFToolkit(unittest.TestCase):
    """Test all major functionalities of the PDFToolkit package."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests."""
        # Create a temp directory for all test files
        cls.test_dir = tempfile.mkdtemp()
        
        # Create a simple test PDF file
        cls.test_pdf_path = os.path.join(cls.test_dir, "test_input.pdf")
        
        # Initialize toolkit
        cls.toolkit = PDFToolkit()
        
        # Create a sample PDF if you have PyPDF2 or reportlab installed
        # For this test, we'll assume you have a test.pdf file
        # If not, the tests will be skipped
        cls.sample_pdf_exists = False
        
        # For testing purposes, we'll check if a sample PDF exists
        sample_path = os.path.join(os.path.dirname(__file__), "samples", "sample.pdf")
        if os.path.exists(sample_path):
            shutil.copy(sample_path, cls.test_pdf_path)
            cls.sample_pdf_exists = True
        
        # Set up test loggers
        cls.console_logger = setup_logger(name="TestConsoleLogger", level="DEBUG")
        
        # For Discord logger, we'll only initialize if webhook URL is provided
        discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")
        if discord_webhook:
            cls.discord_logger = setup_logger(
                name="TestDiscordLogger", 
                level="INFO",
                discord_webhook=discord_webhook
            )
        else:
            cls.discord_logger = None

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are done."""
        # Remove temp directory and all its contents
        shutil.rmtree(cls.test_dir)

    def setUp(self):
        """Set up before each test."""
        # Create output paths for each test
        self.compressed_pdf = os.path.join(self.test_dir, "compressed.pdf")
        self.encrypted_pdf = os.path.join(self.test_dir, "encrypted.pdf")
        self.decrypted_pdf = os.path.join(self.test_dir, "decrypted.pdf")
        self.merged_pdf = os.path.join(self.test_dir, "merged.pdf")
        self.excel_output = os.path.join(self.test_dir, "output.xlsx")
        self.word_output = os.path.join(self.test_dir, "output.docx")
        
        # Test password
        self.test_password = "test_password123"

    def test_logger_console(self):
        """Test console logging functionality."""
        self.console_logger.debug("Debug test message")
        self.console_logger.info("Info test message")
        self.console_logger.warning("Warning test message")
        self.console_logger.error("Error test message")
        self.console_logger.critical("Critical test message")
        
        # No assertion needed as we're just ensuring it doesn't raise exceptions

    def test_logger_discord(self):
        """Test Discord webhook logging if configured."""
        if not self.discord_logger:
            self.skipTest("Discord webhook URL not provided")
        
        # Test with different log levels and extra fields
        self.discord_logger.info(
            "Info test message from PDFToolkit tests", 
            test_name="test_logger_discord"
        )
        self.discord_logger.error(
            "Error test message", 
            error_code=500, 
            test_file=self.test_pdf_path
        )
        
        # No assertion needed as we're just ensuring it doesn't raise exceptions

    def test_compress_pdf(self):
        """Test PDF compression functionality."""
        if not self.sample_pdf_exists:
            self.skipTest("Sample PDF not available")
        
        # Compress the test PDF
        result = self.toolkit.compressor.compress(
            self.test_pdf_path,
            self.compressed_pdf,
            compression_level=7
        )
        
        # Check if compression worked
        self.assertTrue(os.path.exists(self.compressed_pdf))
        self.assertTrue(os.path.getsize(self.compressed_pdf) > 0)
        
        # Log the result
        self.console_logger.info(
            f"Compressed PDF size: {os.path.getsize(self.compressed_pdf)} bytes"
        )

    def test_encrypt_decrypt_pdf(self):
        """Test PDF encryption and decryption functionality."""
        if not self.sample_pdf_exists:
            self.skipTest("Sample PDF not available")
        
        # Encrypt the test PDF
        self.toolkit.encryptor.encrypt(
            self.test_pdf_path,
            self.test_password,
            self.encrypted_pdf
        )
        
        # Check if encryption worked
        self.assertTrue(os.path.exists(self.encrypted_pdf))
        
        # Decrypt the encrypted PDF
        self.toolkit.encryptor.decrypt(
            self.encrypted_pdf,
            self.test_password,
            self.decrypted_pdf
        )
        
        # Check if decryption worked
        self.assertTrue(os.path.exists(self.decrypted_pdf))
        
        # Log the result
        self.console_logger.info("Encryption and decryption test completed")

    def test_merge_pdfs(self):
        """Test PDF merging functionality."""
        if not self.sample_pdf_exists:
            self.skipTest("Sample PDF not available")
        
        # Create a duplicate of test PDF to have something to merge
        duplicate_pdf = os.path.join(self.test_dir, "duplicate.pdf")
        shutil.copy(self.test_pdf_path, duplicate_pdf)
        
        # Merge the test PDFs
        self.toolkit.merger.merge(
            [self.test_pdf_path, duplicate_pdf],
            self.merged_pdf
        )
        
        # Check if merge worked
        self.assertTrue(os.path.exists(self.merged_pdf))
        
        # Log the result
        self.console_logger.info(
            f"Merged PDF size: {os.path.getsize(self.merged_pdf)} bytes"
        )

    @unittest.expectedFailure
    def test_to_excel_conversion(self):
        """Test PDF to Excel conversion functionality."""
        if not self.sample_pdf_exists:
            self.skipTest("Sample PDF not available")
        
        try:
            # Try importing pdfplumber to see if it's available
            import pdfplumber
            
            # Convert the test PDF to Excel
            self.toolkit.excel_converter.convert(
                self.test_pdf_path,
                self.excel_output
            )
            
            # Check if conversion worked
            self.assertTrue(os.path.exists(self.excel_output))
            
            # Try loading the Excel file with pandas to verify it's valid
            df = pd.read_excel(self.excel_output)
            
            # Log the result
            self.console_logger.info(
                f"Converted Excel file has {len(df)} rows and {len(df.columns)} columns"
            )
        except ImportError:
            self.skipTest("pdfplumber not installed")

    @unittest.expectedFailure
    def test_to_word_conversion(self):
        """Test PDF to Word conversion functionality."""
        if not self.sample_pdf_exists:
            self.skipTest("Sample PDF not available")
        
        try:
            # Try importing pdf2docx to see if it's available
            from pdf2docx import Converter
            
            # Convert the test PDF to Word
            self.toolkit.word_converter.convert(
                self.test_pdf_path,
                self.word_output
            )
            
            # Check if conversion worked
            self.assertTrue(os.path.exists(self.word_output))
            
            # Log the result
            self.console_logger.info(
                f"Converted Word file size: {os.path.getsize(self.word_output)} bytes"
            )
        except ImportError:
            self.skipTest("pdf2docx not installed")


if __name__ == "__main__":
    unittest.main()