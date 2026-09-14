"""
nlp_extractor.py
-----------------
Step 2 of the IDP pipeline: Information Extraction.
Pulls structured fields (amount, date, vendor/invoice number) out of raw OCR text
using regex-based pattern matching. This mirrors how real IDP tools use rules
before/alongside ML for high-precision fields like currency amounts and dates.
"""

import re


def extract_fields(text: str) -> dict:
    fields = {}

    # --- Amount (₹ or $ followed by digits) ---
    amount_match = re.search(r'(?:₹|\$|Rs\.?)\s?[\d,]+\.?\d*', text)
    fields["amount"] = amount_match.group(0) if amount_match else "Not found"

    # --- Date (common formats: 12/05/2025, 12-05-2025, May 12 2025) ---
    date_match = re.search(
        r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})|'
        r'([A-Za-z]{3,9}\s\d{1,2},?\s\d{4})',
        text
    )
    fields["date"] = date_match.group(0) if date_match else "Not found"

    # --- Invoice / Document Number ---
    invoice_match = re.search(
        r'(?:Invoice\s?(?:No|Number|#)?[:\-]?\s?)([A-Za-z0-9\-\/]+)',
        text, re.IGNORECASE
    )
    fields["invoice_number"] = invoice_match.group(1) if invoice_match else "Not found"

    # --- Vendor / Company Name (naive: first capitalized line) ---
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    vendor = "Not found"
    for line in lines[:5]:  # usually vendor name is near the top
        if line.isupper() or line.istitle():
            vendor = line
            break
    fields["vendor"] = vendor

    return fields


if __name__ == "__main__":
    sample_text = """
    ACME SUPPLIES PVT LTD
    Invoice No: INV-2025-0456
    Date: 12/05/2025
    Total Amount: Rs. 45,000
    """
    print(extract_fields(sample_text))
