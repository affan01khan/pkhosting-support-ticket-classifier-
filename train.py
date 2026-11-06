from pathlib import Path
import csv
import json
import random
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.utils.multiclass import unique_labels

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_PATH = DATA_DIR / "support_tickets.csv"
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"

# Build a reproducible synthetic dataset when the CSV is not present.
def create_dataset():
    random.seed(42)
    templates = {
        "Billing": [
            ("I was charged twice for my hosting invoice.", "High"),
            ("My payment was deducted but the invoice is still unpaid.", "High"),
            ("Please explain the extra fee on my monthly bill.", "Medium"),
            ("Can I get a copy of last month's invoice?", "Low"),
            ("My card payment failed during checkout.", "Medium"),
            ("I need to update the billing address on my account.", "Low"),
            ("The renewal amount is different from the advertised price.", "Medium"),
            ("Please confirm whether my refund has been processed.", "Medium"),
            ("I cannot download my tax receipt.", "Low"),
            ("My hosting service was suspended even though I paid today.", "High"),
        ],
        "Technical Issue": [
            ("My website shows a 500 internal server error.", "High"),
            ("The website is loading very slowly since this morning.", "Medium"),
            ("I cannot upload files through the control panel.", "Medium"),
            ("The server is returning a database connection error.", "High"),
            ("My WordPress dashboard is not opening.", "Medium"),
            ("The website is completely offline for all visitors.", "High"),
            ("I need help changing PHP settings for my website.", "Low"),
            ("The SSL certificate warning appears on my homepage.", "High"),
            ("My website backup failed last night.", "Medium"),
            ("I am getting a permission denied error in File Manager.", "Low"),
        ],
        "Domain": [
            ("My domain is not resolving to the hosting server.", "High"),
            ("I want to transfer my domain to PK Hosting.", "Medium"),
            ("Please help me update the domain nameservers.", "Low"),
            ("The domain renewal date looks incorrect.", "Medium"),
            ("My domain registration is still pending.", "Medium"),
            ("I cannot access the DNS management page.", "Medium"),
            ("The domain has expired and my website is unavailable.", "High"),
            ("I need to add an A record for my domain.", "Low"),
            ("The domain transfer authorization code is not arriving.", "Medium"),
            ("My website shows a DNS_PROBE_FINISHED_NXDOMAIN error.", "High"),
        ],
        "Email": [
            ("I cannot send emails from my business email account.", "High"),
            ("Incoming messages are not appearing in my mailbox.", "High"),
            ("Please help me configure email on my mobile phone.", "Low"),
            ("My emails are going to recipients' spam folders.", "Medium"),
            ("The mailbox storage quota has been exceeded.", "Medium"),
            ("I forgot my webmail password and cannot sign in.", "Medium"),
            ("I need to create a new email address for my domain.", "Low"),
            ("Email delivery is delayed by several hours.", "Medium"),
            ("My email client keeps asking for the password.", "Low"),
            ("The mail server says authentication failed.", "High"),
        ],
    }
    prefixes = ["Hello support, ", "Hi team, ", "Good morning, ", "Please assist: ", "Can you check this? "]
    suffixes = [" Please advise on the next steps.", " This is affecting my work.", " I would appreciate a quick update.", ""]
    rows = []
    for category, examples in templates.items():
        for i in range(30):
            message, priority = examples[i % len(examples)]
            if i % 3 == 0:
                message = random.choice(prefixes) + message[0].lower() + message[1:]
            if i % 4 == 0:
                message += random.choice(suffixes)
            rows.append({"ticket_id": f"T{len(rows)+1:03d}", "message": message, "category": category, "priority": priority})
    random.shuffle(rows)
    DATA_DIR.mkdir(exist_ok=True)
    with DATA_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ticket_id", "message", "category", "priority"])
        writer.writeheader()
        writer.writerows(rows)

if not DATA_PATH.exists():
    create_dataset()

MODEL_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
df = pd.read_csv(DATA_PATH)
if len(df) < 120 or df["category"].nunique() < 4:
    raise ValueError("Dataset must contain at least 120 tickets and four categories.")

X = df["message"].astype(str)
y_category = df["category"].astype(str)
y_priority = df["priority"].astype(str)
train_idx, test_idx = train_test_split(
    list(range(len(df))), test_size=0.25, random_state=42, stratify=y_category
)

def make_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True, strip_accents="unicode")),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])

category_model = make_pipeline()
priority_model = make_pipeline()
category_model.fit(X.iloc[train_idx], y_category.iloc[train_idx])
priority_model.fit(X.iloc[train_idx], y_priority.iloc[train_idx])
cat_pred = category_model.predict(X.iloc[test_idx])
pri_pred = priority_model.predict(X.iloc[test_idx])

def confusion_data(y_true, y_pred, labels):
    matrix = confusion_matrix(y_true, y_pred, labels=labels)
    return {"labels": list(labels), "matrix": matrix.tolist()}

report = {
    "dataset_rows": int(len(df)),
    "train_rows": int(len(train_idx)),
    "held_out_test_rows": int(len(test_idx)),
    "random_state": 42,
    "category_accuracy": float(accuracy_score(y_category.iloc[test_idx], cat_pred)),
    "priority_accuracy": float(accuracy_score(y_priority.iloc[test_idx], pri_pred)),
    "category_classification_report": classification_report(y_category.iloc[test_idx], cat_pred, output_dict=True, zero_division=0),
    "priority_classification_report": classification_report(y_priority.iloc[test_idx], pri_pred, output_dict=True, zero_division=0),
    "category_confusion_matrix": confusion_data(y_category.iloc[test_idx], cat_pred, sorted(unique_labels(y_category.iloc[test_idx], cat_pred))),
    "priority_confusion_matrix": confusion_data(y_priority.iloc[test_idx], pri_pred, sorted(unique_labels(y_priority.iloc[test_idx], pri_pred))),
}
joblib.dump({"category_model": category_model, "priority_model": priority_model}, MODEL_DIR / "ticket_classifier.joblib")
with (REPORT_DIR / "evaluation.json").open("w", encoding="utf-8") as handle:
    json.dump(report, handle, indent=2)
print(f"Dataset: {len(df)} | Train: {len(train_idx)} | Held-out test: {len(test_idx)}")
print(f"Category accuracy: {report['category_accuracy']:.3f}")
print(f"Priority accuracy: {report['priority_accuracy']:.3f}")
