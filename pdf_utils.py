"""
PDF utility module for extracting text from PDF files.
"""
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The extracted text content.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""

        # Loop through each page and extract text
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


# --- Quick Test Block ---
# This runs only if you execute this file directly, not when imported.
# --- Quick Test Block ---
if __name__ == "__main__":
    import sys

    # Force UTF-8 encoding for printing to console (Windows fix)
    sys.stdout.reconfigure(encoding='utf-8')

    test_pdf = "resume.pdf"

    print(f"Attempting to read: {test_pdf}")
    extracted_text = extract_text_from_pdf(test_pdf)

    if extracted_text:
        print("\n--- SUCCESS! Extracted Text Preview ---")
        # This handles the printing safely
        try:
            print(extracted_text[:500])
        except UnicodeEncodeError:
            # Fallback if the terminal still complains
            print(extracted_text[:500].encode(
                'ascii', 'ignore').decode('ascii'))
        print("\n-------------------------------------------------------")
    else:
        print("Failed to extract text. Make sure 'resume.pdf' exists.")
