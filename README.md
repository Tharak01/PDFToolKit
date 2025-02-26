# python-pdf-toolkit

A comprehensive Python package for PDF manipulation including compression, conversion to Excel/Word, encryption/decryption, and merging.

## Features

- **PDF Compression**: Reduce PDF file size while maintaining quality
- **PDF to Excel Conversion**: Extract tables from PDFs and convert to Excel format
- **PDF to Word Conversion**: Convert PDFs to editable Word documents
- **PDF Merging**: Combine multiple PDFs into a single document
- **PDF Encryption/Decryption**: Secure your PDFs with password protection
- **Logging Support**: Console logging and Discord webhook integration

## Installation

```bash
# Basic installation
pip install python-pdf-toolkit

# With Excel conversion support
pip install python-pdf-toolkit[excel]

# With Word conversion support
pip install python-pdf-toolkit[word]

# With Discord logging support
pip install python-pdf-toolkit[discord]

# With all optional dependencies
pip install python-pdf-toolkit[all]
```

## Usage

### Python API

```python
from python_pdf_toolkit import PDFToolkit

# Initialize the toolkit
toolkit = PDFToolkit()

# Compress a PDF
compressed_pdf = toolkit.compressor.compress(
    "input.pdf", 
    "compressed.pdf",
    compression_level=7
)

# Convert PDF to Excel
excel_data = toolkit.excel_converter.convert(
    "input.pdf", 
    "output.xlsx"
)

# Convert PDF to Word
word_doc = toolkit.word_converter.convert(
    "input.pdf", 
    "output.docx"
)

# Merge PDFs
merged_pdf = toolkit.merger.merge(
    ["file1.pdf", "file2.pdf", "file3.pdf"], 
    "merged.pdf"
)

# Encrypt a PDF
encrypted_pdf = toolkit.encryptor.encrypt(
    "input.pdf", 
    "your_password", 
    "encrypted.pdf"
)

# Decrypt a PDF
decrypted_pdf = toolkit.encryptor.decrypt(
    "encrypted.pdf", 
    "your_password", 
    "decrypted.pdf"
)
```

### Logging

PDFToolkit provides flexible logging options:

```python
from python_pdf_toolkit.logger import setup_logger

# Set up a standard console logger
logger = setup_logger(
    name="MyPDFApp",
    level="INFO"  # Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
)

# Log messages
logger.info("Starting PDF processing")
logger.warning("Low disk space for output file")
logger.error("Failed to process PDF file")

# Set up Discord webhook logging (requires discord-logger-handler package)
discord_logger = setup_logger(
    name="MyPDFApp",
    level="INFO",
    discord_webhook="https://discord.com/api/webhooks/your_webhook_url"
)

# Log messages with additional context
discord_logger.info("PDF processed successfully", file_name="example.pdf", pages=5)
discord_logger.error("Processing failed", error_code=500, file_path="/path/to/file.pdf")
```

### Command Line Interface

```bash
# Compress a PDF
pdftoolkit compress input.pdf compressed.pdf --level 7

# Convert PDF to Excel
pdftoolkit to-excel input.pdf output.xlsx

# Convert PDF to Word
pdftoolkit to-word input.pdf output.docx

# Merge PDFs
pdftoolkit merge file1.pdf file2.pdf file3.pdf merged.pdf

# Encrypt a PDF
pdftoolkit encrypt input.pdf encrypted.pdf --password your_password

# Decrypt a PDF
pdftoolkit decrypt encrypted.pdf decrypted.pdf --password your_password
```

## Optional Dependencies

- `pdfplumber`: Required for PDF to Excel conversion
- `pdf2docx`: Required for PDF to Word conversion
- `discord-logger-handler`: Required for Discord logging integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
