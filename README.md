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

## 3. Likely interview questions & how to answer

**Q: Why OCR + regex instead of just an LLM?**
A: "For a resume project I wanted to show I understand the traditional
pipeline (OCR → rule-based extraction → ML classification) which is cheaper
and more explainable than an LLM call for every document — real IDP systems
still use this hybrid approach for cost and latency reasons. I'd mention
that swapping the classifier for a fine-tuned transformer, or adding an LLM
step for messy/unstructured extraction, is a natural next iteration."

**Q: How would you improve accuracy?**
A: "Train the classifier on a larger, real labeled dataset instead of 8
examples; use spaCy's NER instead of regex for entity extraction; add image
pre-processing (deskew, denoise) before OCR to improve text quality."

**Q: How would you scale this for production?**
A: "Move SQLite to PostgreSQL, put the OCR/classification pipeline behind a
task queue (Celery + Redis) so uploads don't block the request, and
containerize with Docker for deployment on cloud (Capgemini itself works
heavily with AWS/Azure/GCP for clients)."

**Q: What's the business impact?**
A: "This kind of automation is what firms pay Capgemini's Business Services
practice for — cutting manual data-entry time in invoice/contract processing
by a large percentage, reducing human error, and speeding up downstream
approvals."

**Q: Walk me through what happens when I upload a file.**
A: Walk through `app.py`'s `/upload` route line by line — save file → OCR →
regex extraction → classify → save to DB → redirect to dashboard.

---

## 4. Optional upgrades if you have more time before the interview
- Swap Naive Bayes for a fine-tuned DistilBERT classifier (mention you know
  the trade-off: more accurate but heavier/slower).
- Add authentication (Flask-Login) so it looks like a real internal tool.
- Deploy it for free on Render/Railway and put a live link on your resume —
  a working live demo stands out far more than a GitHub link alone.
