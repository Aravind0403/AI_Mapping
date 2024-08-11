def read_text_from_note(note_file_path):
    """
    Reads text content from a note file (plain text or Notion export).

    Args:
        note_file_path (str): The path to the note file.

    Returns:
        str: The text content of the note.
    """

    try:
        with open(note_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    except FileNotFoundError:
        print(f"Error: File not found at {note_file_path}")
        return ""
def read_text_from_rtf(note_file_path):
    """
    Reads text content from a note file (plain text or Notion export).

    Args:
        note_file_path (str): The path to the note file.

    Returns:
        str: The text content of the note.
    """

    try:
        with open(note_file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    except FileNotFoundError:
        print(f"Error: File not found at {note_file_path}")
        return ""