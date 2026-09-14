"""
classifier.py
--------------
Step 3 of the IDP pipeline: Document Classification.
Trains a simple TF-IDF + Naive Bayes model to classify a document as
Invoice / Contract / ID Proof / Resume, based on its OCR text.

In an interview, explain: "I used TF-IDF to turn text into numeric
vectors, and Multinomial Naive Bayes because it's fast, works well on
small text datasets, and is a standard baseline for text classification."
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

MODEL_PATH = "doc_classifier.pkl"

# Small labeled training set (in a real project this would be hundreds of
# real documents; here it's enough to demonstrate the pipeline working).
TRAINING_DATA = [
    ("Invoice No 4521 Total Amount Due Rs 20000 Payment Terms Net 30", "Invoice"),
    ("Tax Invoice GSTIN Bill To Ship To Subtotal Grand Total", "Invoice"),
    ("Invoice Number Date Due Date Description Quantity Unit Price Total", "Invoice"),
    ("Bill of Sale Item Price Quantity Total Payment Due Upon Receipt", "Invoice"),

    ("This Agreement is made between Party A and Party B Terms and Conditions", "Contract"),
    ("Service Agreement Effective Date Termination Clause Confidentiality", "Contract"),
    ("Non Disclosure Agreement Whereas the parties agree Governing Law Jurisdiction", "Contract"),
    ("Employment Contract Salary Notice Period Probation Clause Signed By", "Contract"),

    ("Government of India Permanent Account Number Date of Birth Signature", "ID Proof"),
    ("Aadhar Card Unique Identification Authority Address Photo", "ID Proof"),
    ("Passport Number Nationality Place of Birth Date of Issue Date of Expiry", "ID Proof"),
    ("Driving License Vehicle Class Issued By Valid Till Blood Group", "ID Proof"),

    ("Curriculum Vitae Work Experience Education Skills Objective Career", "Resume"),
    ("Resume Professional Summary Technical Skills Projects Certifications", "Resume"),
    ("Python Java SQL Machine Learning Internship Bachelor of Technology Email Phone LinkedIn Github", "Resume"),
    ("Objective Seeking a challenging role Education Work Experience Achievements Hobbies", "Resume"),
    ("Name Email Phone Address Skills Programming Languages Frameworks Projects Education", "Resume"),
]
def train_model():
    texts = [t for t, label in TRAINING_DATA]
    labels = [label for t, label in TRAINING_DATA]

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB())
    ])
    pipeline.fit(texts, labels)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    return pipeline


def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    return train_model()


def classify_document(text: str) -> str:
    model = load_or_train_model()
    prediction = model.predict([text])[0]
    return prediction


if __name__ == "__main__":
    train_model()
    print(classify_document("Invoice Number 123 Total Amount 5000 Due Date 12/05/2025"))
