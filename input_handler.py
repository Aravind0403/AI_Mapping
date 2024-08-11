from pdf_extractor import extract_text_from_pdf
from note_handler import read_text_from_note
import os
import pandas as pd  # For handling Excel files
import striprtf  # For handling RTF files


def get_text_from_file(file_path):
    """
    Extracts text content from a file, handling various formats.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The extracted text content.
    """

    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() == '.txt':
        return read_text_from_note(file_path)
    elif file_extension.lower() == '.xlsx' or file_extension.lower() == '.xls':  # Excel files
        try:
            df = pd.read_excel(file_path)
            return df.to_string(index=False)  # Convert DataFrame to string
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return ""
    elif file_extension.lower() == '.rtf':  # RTF files
        try:
            with open(file_path, 'r') as file:
                rtf_content = file.read()
                return striprtf.rtf_to_text(rtf_content)
        except Exception as e:
            print(f"Error reading RTF file: {e}")
            return ""
    # Add more elif blocks for other formats as needed

    else:
        print(f"Unsupported file format: {file_extension}")
        return ""