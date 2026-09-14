"""
ocr_processor.py
-----------------
Converts an uploaded document (image or PDF) into raw text.
This is "Step 1" of the IDP pipeline: Digitization.
"""

import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os


def extract_text_from_file(filepath: str) -> str:
    """
    Takes a file path (image or pdf) and returns extracted raw text.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        # Convert each PDF page to an image, then OCR each page
        pages = convert_from_path(filepath)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page) + "\n"
        return text
    else:
        # Directly OCR the image file
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)
        return text


if __name__ == "__main__":
    # Quick manual test
    sample = "sample_data/sample_invoice.png"
    if os.path.exists(sample):
        print(extract_text_from_file(sample))
    else:
        print("Place a sample image at sample_data/sample_invoice.png to test.")
