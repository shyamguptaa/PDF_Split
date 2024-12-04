import os
import re
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Set the path for Tesseract OCR executable if needed
# Uncomment and set the path if Tesseract is not in your PATH
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

def split_pdf_by_patterns(pdf_path, patterns):
    """Split PDF into multiple PDFs based on a list of patterns."""
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
        file_name_with_extension = os.path.basename(pdf_path)
        file_name, _ = os.path.splitext(file_name_with_extension)
        # Check if the text matches any of the patterns
        if any(re.search(pattern, text) for pattern in patterns):
            if pdf_writer:
                # output_filename = f'split_pdf_{(file_name)}_{len(output_files)}.pdf'
                output_filename = f'{len(output_files)}_split_{(file_name)}.pdf'
                with open(output_filename, 'wb') as output_pdf:
                    pdf_writer.write(output_pdf)
                output_files.append(output_filename)
                pdf_writer = None
            
            pdf_writer = PyPDF2.PdfWriter()

        if pdf_writer:
            pdf_writer.add_page(page)

    # Save the last part if it exists
    
    if pdf_writer:
        # output_filename = f'split_pdf_{(file_name)}_{len(output_files)}.pdf'
        output_filename = f'{len(output_files)}_split_{(file_name)}.pdf'
        with open(output_filename, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
        output_files.append(output_filename)

    return output_files

def process_multiple_pdfs(pdf_paths, patterns):
    # """Process multiple PDF files and split them based on patterns."""
    # all_output_files = []
    # for pdf_path in pdf_paths:
    #     output_files = split_pdf_by_patterns(pdf_path, patterns)
    #     all_output_files.extend(output_files)
    # return all_output_files

    """Process multiple PDF files and split them based on patterns."""
    all_output_files = []
    for pdf_path in pdf_paths:
        filename, _ = os.path.splitext(os.path.basename(pdf_path))
        output_folder = os.path.join(os.path.dirname(pdf_path), filename)
        os.makedirs(output_folder, exist_ok=True)
        
        output_files = split_pdf_by_patterns(pdf_path, patterns)
        for i, output_file in enumerate(output_files):
            new_output_file = os.path.join(output_folder, f"{i+1}_split_{filename}.pdf")
            os.rename(output_file, new_output_file)
            all_output_files.append(new_output_file)
    return all_output_files


# Example usage
if __name__ == "__main__":
    
    # multiple file as input
    pdf_paths=[
        r'D:\Folder\example1.pdf',
        r'D:\Folder\example2.pdf',
    ]
    # multiple patterns
    patterns = [r'Pattern_1 ',r'Pattern_2 ']  # Replace with your regex patterns
    
    # Multiple file run command 
    output_files = process_multiple_pdfs(pdf_paths, patterns)

    print("Created PDFs:")
    for file in output_files:
        print(file)