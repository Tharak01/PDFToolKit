"""
Command-line interface for PDFToolkit.
"""

import os
import argparse
import sys
from typing import List, Optional

from . import PDFToolkit, setup_logger


def parse_args(args: Optional[List[str]] = None):
    """
    Parse command line arguments.
    
    Args:
        args: Command line arguments (if None, use sys.argv)
        
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="PDFToolkit - A comprehensive toolkit for PDF manipulation"
    )
    
    # Set up global options
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Set logging level")
    parser.add_argument("--discord-webhook", help="Discord webhook URL for logging (optional)")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress a PDF file")
    compress_parser.add_argument("input_pdf", help="Input PDF file path")
    compress_parser.add_argument("output_pdf", help="Output PDF file path")
    compress_parser.add_argument("--level", "-l", type=int, choices=range(1, 11), default=5, help="Compression level (1-10)")
    
    # Convert to Excel command
    excel_parser = subparsers.add_parser("to-excel", help="Convert PDF to Excel")
    excel_parser.add_argument("input_pdf", help="Input PDF file path")
    excel_parser.add_argument("output_excel", help="Output Excel file path")
    excel_parser.add_argument("--batch-size", "-b", type=int, default=5, help="Batch size for processing pages")
    
    # Convert to Word command
    word_parser = subparsers.add_parser("to-word", help="Convert PDF to Word")
    word_parser.add_argument("input_pdf", help="Input PDF file path")
    word_parser.add_argument("output_word", help="Output Word file path")
    word_parser.add_argument("--start-page", "-s", type=int, default=0, help="First page to convert (0-based)")
    word_parser.add_argument("--end-page", "-e", type=int, help="Last page to convert (inclusive)")
    
    # Merge command
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDF files")
    merge_parser.add_argument("input_pdfs", nargs="+", help="Input PDF files to merge")
    merge_parser.add_argument("output_pdf", help="Output PDF file path")
    
    # Encrypt command
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a PDF file")
    encrypt_parser.add_argument("input_pdf", help="Input PDF file path")
    encrypt_parser.add_argument("output_pdf", help="Output PDF file path")
    encrypt_parser.add_argument("--password", "-p", required=True, help="Password for encryption")
    encrypt_parser.add_argument("--algorithm", "-a", default="AES-256-R5", help="Encryption algorithm")
    
    # Decrypt command
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a PDF file")
    decrypt_parser.add_argument("input_pdf", help="Input PDF file path")
    decrypt_parser.add_argument("output_pdf", help="Output PDF file path")
    decrypt_parser.add_argument("--password", "-p", required=True, help="Password for decryption")
    
    return parser.parse_args(args)


def main():
    """
    Main entry point for the command-line interface.
    """
    args = parse_args()
    
    # Setup logger
    log_level = "DEBUG" if args.verbose else args.log_level
    logger = setup_logger("PDFToolkit-CLI", level=log_level, discord_webhook=args.discord_webhook)
    
    # Create PDFToolkit instance
    toolkit = PDFToolkit(logger=logger)
    
    # Execute the requested command
    if args.command == "compress":
        logger.info(f"Compressing PDF: {args.input_pdf} -> {args.output_pdf} (level: {args.level})")
        result = toolkit.compressor.compress(
            args.input_pdf, 
            args.output_pdf, 
            compression_level=args.level
        )
        if result == args.output_pdf:
            logger.info("Compression completed successfully")
            return 0
        else:
            logger.error(f"Compression failed: {result[1]}")
            return 1
            
    elif args.command == "to-excel":
        logger.info(f"Converting PDF to Excel: {args.input_pdf} -> {args.output_excel}")
        result = toolkit.excel_converter.convert(
            args.input_pdf, 
            args.output_excel, 
            batch_size=args.batch_size
        )
        if result == args.output_excel:
            logger.info("Conversion to Excel completed successfully")
            return 0
        else:
            logger.error(f"Conversion to Excel failed: {result[1]}")
            return 1
            
    elif args.command == "to-word":
        logger.info(f"Converting PDF to Word: {args.input_pdf} -> {args.output_word}")
        result = toolkit.word_converter.convert(
            args.input_pdf, 
            args.output_word, 
            start_page=args.start_page, 
            end_page=args.end_page
        )
        if result == args.output_word:
            logger.info("Conversion to Word completed successfully")
            return 0
        else:
            logger.error(f"Conversion to Word failed: {result[1]}")
            return 1
            
    elif args.command == "merge":
        logger.info(f"Merging PDF files: {args.input_pdfs} -> {args.output_pdf}")
        result = toolkit.merger.merge(
            args.input_pdfs, 
            args.output_pdf
        )
        if result == args.output_pdf:
            logger.info("Merging completed successfully")
            return 0
        else:
            logger.error(f"Merging failed: {result[1]}")
            return 1
            
    elif args.command == "encrypt":
        logger.info(f"Encrypting PDF: {args.input_pdf} -> {args.output_pdf}")
        result = toolkit.encryptor.encrypt(
            args.input_pdf, 
            args.password, 
            args.output_pdf, 
            algorithm=args.algorithm
        )
        if result == args.output_pdf:
            logger.info("Encryption completed successfully")
            return 0
        else:
            logger.error(f"Encryption failed: {result[1]}")
            return 1
            
    elif args.command == "decrypt":
        logger.info(f"Decrypting PDF: {args.input_pdf} -> {args.output_pdf}")
        result = toolkit.encryptor.decrypt(
            args.input_pdf, 
            args.password, 
            args.output_pdf
        )
        if result == args.output_pdf:
            logger.info("Decryption completed successfully")
            return 0
        else:
            logger.error(f"Decryption failed: {result[1]}")
            return 1
            
    else:
        logger.error("No command specified")
        return 1


if __name__ == "__main__":
    sys.exit(main())