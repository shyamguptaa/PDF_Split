# PDF Splitter with OCR Capabilities - Multiple Pattern & Files

This Python script splits a PDF file into multiple PDF files based on a specified text pattern. It supports both text-based and image-based PDFs using OCR capabilities.

## Requirements

- Python 3.x
- pip (Python package installer)

## Installation

1. **Install Python**: Download and install Python from [python.org](https://www.python.org/downloads/).

2. **Install Tesseract OCR**:
   - **For Windows**:
     1. Download the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
     2. Run the downloaded installer and follow the prompts. By default, Tesseract will be installed in `C:\Program Files\Tesseract-OCR`.
     3. Add Tesseract to your system PATH:
        - Right-click on "This PC" or "My Computer" and select "Properties".
        - Click on "Advanced system settings".
        - Click on the "Environment Variables" button.
        - In the "System variables" section, find the `Path` variable and select it, then click "Edit".
        - Click "New" and add the path to the Tesseract installation, e.g., `C:\Program Files\Tesseract-OCR`.
        - Click "OK" to close all dialog boxes.
     4. Verify the installation by opening Command Prompt and typing:
        ```bash
        tesseract --version
        ```

   - **For macOS**:
     1. Install Homebrew (if you haven't already) by running the following command in Terminal:
        ```bash
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        ```
     2. Install Tesseract by running:
        ```bash
        brew install tesseract
        ```
     3. Verify the installation by typing:
        ```bash
        tesseract --version
        ```

   - **For Linux (Ubuntu/Debian)**:
     1. Update the package list by running:
        ```bash
        sudo apt-get update
        ```
     2. Install Tesseract by running:
        ```bash
        sudo apt-get install tesseract-ocr
        ```
     3. Verify the installation by typing:
        ```bash
        tesseract --version
        ```

3. **Install Required Python Packages**:
   Open a terminal or command prompt and run the following command:
   ```bash
   pip install PyPDF2 pdf2image pytesseract Pillow
   ```

4. **Usage**:
   Open a terminal or command prompt and navigate to the directory where python(.py) is located.
    - **File Usage-Features**:
     1. For Single Pattern:
        ```bash
            python split_pdf_single_pattern.py
        
        -Example
         pdf_path = r'D:\Folder\example.pdf'  # Use raw string  Replace with your PDF file path
         pattern = r'Pattern'  # Replace with your regex pattern
         Output File =split_pdf_1.pdf
        ```
     2. For Multiple Pattern_ with Folder Created with the File Name and splited Files Inside the Folder:
        ```bash
            python split_pdf_mullti_pattern.py
        
        -Example
        
        pdf_path = [r'D:\Folder\example1.pdf',r'D:\Folder\example2.pdf']  # Use raw string Replace with your PDF file path
        pattern = [r'Pattern1',r'Pattern2']  # Replace with your regex pattern
        Output File ={i+1}_split_{filename}.pdf
        ```
   