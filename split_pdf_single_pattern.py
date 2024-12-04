import os
import re
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Set the path for Tesseract OCR executable if needed
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using PyPDF2 and OCR for images."""
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text() or ""
        
        # If the page has images, use OCR
        if '/XObject' in page['/Resources']:
            images = page['/Resources']['/XObject'].get_object()
            for img in images:
                if images[img]['/Subtype'] == '/Image':
                    img_data = images[img].get_data()
                    with open(f'temp_image_{page_num}.png', 'wb') as img_file:
                        img_file.write(img_data)
                    text += extract_text_from_image(f'temp_image_{page_num}.png')
                    os.remove(f'temp_image_{page_num}.png')
    
    return text

def split_pdf_by_pattern(pdf_path, pattern):
    """Split PDF into multiple PDFs based on a specific pattern."""
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    pdf_writer = None
    output_files = []
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text() or ""
        
        # If the page has images, use OCR
        if '/XObject' in page['/Resources']:
            images = page['/Resources']['/XObject'].get_object()
            for img in images:
                if images[img]['/Subtype'] == '/Image':
                    img_data = images[img].get_data()
                    with open(f'temp_image_{page_num}.png', 'wb') as img_file:
                        img_file.write(img_data)
                    text += extract_text_from_image(f'temp_image_{page_num}.png')
                    os.remove(f'temp_image_{page_num}.png')
        
        # Check if the text matches the pattern
        if re.search(pattern, text):
            if pdf_writer:
                output_filename = f'split_pdf_{len(output_files)}.pdf'
                with open(output_filename, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)
                output_files.append(output_filename)
                pdf_writer = None
            
            pdf_writer = PyPDF2.PdfWriter()

        if pdf_writer:
            pdf_writer.add_page(page)

    # Save the last part if it exists
    if pdf_writer:
        output_filename = f'split_pdf_{len(output_files)}.pdf'
        with open(output_filename, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        output_files.append(output_filename)

    return output_files

# Example usage
pdf_path = r'D:\Project_codes\pdf_split\Civil V REV- 2019 _C_ Scheme.pdf'  # Use raw string  # Replace with your PDF file path
pattern = r'Q.No.1'  # Replace with your regex pattern
output_files = split_pdf_by_pattern(pdf_path, pattern)

print("Created PDFs:")
for file in output_files:
    print(file)