import PyPDF2

def extract_text_from_pdf(pdf_file_path):
    """
    Extracts text content from a PDF file.

    Args:
        pdf_file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content.
    """

    try:
        pdf_file = open(pdf_file_path, 'rb')  # Open the PDF file in binary read mode
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()


        pdf_file.close()
        return text

    except FileNotFoundError:
        print(f"Error: File not found at {pdf_file_path}")
        return ""
    except PyPDF2.errors.PdfReadError:
        print(f"Error: Unable to read the PDF file at {pdf_file_path}")
        return ""