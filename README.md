# Intelligent Document Processing (IDP) System

An end-to-end system that mimics what Capgemini's Intelligent Automation
practice builds for clients: it takes a scanned document (invoice, contract,
ID, resume), reads it with OCR, pulls out structured data, classifies the
document type with ML, and stores everything in a dashboard.

---

## 1. What each part does (say this in the interview)

| File | Role | What to say if asked |
|---|---|---|
| `ocr_processor.py` | Converts image/PDF → raw text | "I used Tesseract OCR via pytesseract; PDFs are converted to images first with pdf2image." |
| `nlp_extractor.py` | Pulls amount, date, invoice #, vendor from raw text | "I used regex-based rule extraction — high precision for structured fields like currency and dates, which is how many real IDP pipelines start before adding ML/NER." |
| `classifier.py` | Labels the doc as Invoice/Contract/ID Proof/Resume | "TF-IDF vectorizes the text, and Multinomial Naive Bayes classifies it — a lightweight, fast baseline for text classification." |
| `database.py` | Stores results in SQLite | "No external DB server needed, easy to demo, but the schema would map directly to Postgres/SQL Server in production." |
| `app.py` | Flask backend, wires the pipeline together | "Single upload endpoint runs OCR → extraction → classification → storage in sequence." |
| `templates/index.html` + `static/style.css` | Dashboard UI | "Simple upload form and results table." |

**One-line pitch for your resume:**
> "Built an Intelligent Document Processing system (Flask, Tesseract OCR, scikit-learn) that automates data extraction and classification from invoices/contracts — reducing manual review effort, a real use case in enterprise automation (similar to Capgemini's IDP offerings)."

---

## 2. Setup — from scratch

### Step 1: Install system-level OCR engine
Tesseract is a system binary, not just a Python package.

**On Ubuntu/Debian (or WSL):**
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

**On Windows:**
1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it, then add the install folder to your PATH.
3. Install Poppler for Windows (needed for PDF support): https://github.com/oschwartz10612/poppler-windows/releases — extract and add its `bin` folder to PATH.

**On Mac:**
```bash
brew install tesseract poppler
```

### Step 2: Create the project folder & virtual environment
```bash
mkdir capgemini-idp-project
cd capgemini-idp-project
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### Step 3: Copy in all the project files
Place `app.py`, `ocr_processor.py`, `nlp_extractor.py`, `classifier.py`,
`database.py`, `requirements.txt`, the `templates/` folder, and `static/`
folder into this directory (all included in the zip you downloaded).

### Step 4: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the app
```bash
python app.py
```
Open your browser at **http://localhost:5000**

### Step 6: Test it
Upload any invoice/contract image (a screenshot of a sample invoice works
fine — search "sample invoice image" online, or scan a bill). You'll see it
appear in the table below with extracted vendor, date, amount, and type.

---

