from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf-toolkit",
    version="0.1.0",
    author="Tharakeshavan Parthasarathy",
    author_email="Ptharak01@gmail.com",
    description="A comprehensive toolkit for PDF manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tharak01/PDFToolKit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "pypdf==5.3.0",
        "python-magic==0.4.27",
        "pandas==2.2.3",
        "xlsxwriter==3.2.2",
    ],
    extras_require={
        "excel": ["pdfplumber==0.11.5"],
        "word": ["pdf2docx==0.5.8"],
        "discord": [
            "discord-logger-handler==0.1.2",
        ],
        "all": [
            "pdfplumber==0.11.5",
            "pdf2docx==0.5.8", 
            "discord-logger-handler==0.1.2",
        ],
    },
    entry_points={
        "console_scripts": [
            "pdftoolkit=pdf_toolkit.cli:main",
        ],
    },
)