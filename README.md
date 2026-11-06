# PK Hosting Support Ticket Classifier & Priority Tagger

A Streamlit application that predicts the category and priority of a customer-support message and displays model confidence.

## Features
- Four categories: Billing, Technical Issue, Domain, Email
- Three priority labels: Low, Medium, High
- TF-IDF text features and Logistic Regression classifiers
- Separate probability-based confidence estimates for category and priority
- Reproducible 75/25 train/test evaluation with 30 held-out tickets
- Confusion matrices and precision/recall/F1 reports saved as JSON
- Streamlit interface

## Dataset
The training script creates `data/support_tickets.csv` with 120 synthetic examples if the CSV is not already present. The generated data contains no real customer messages or personal information. It is intended for demonstration and coursework, not production use.

## Local setup
Use Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment:
- Windows: `.venv\\Scripts\\activate`
- macOS/Linux: `source .venv/bin/activate`

Install dependencies and train:
```bash
pip install -r requirements.txt
python train.py
```

Run the app:
```bash
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Evaluation
The training script uses a stratified 75/25 split with `random_state=42`. It writes:
- `reports/evaluation.json`: accuracy, classification reports and confusion matrices
- `models/ticket_classifier.joblib`: trained models used by the app
- `data/support_tickets.csv`: generated synthetic dataset

The Streamlit app trains the model automatically on first startup if the model file is missing.

## Deploy on Streamlit Community Cloud
1. Push this repository to GitHub.
2. Visit https://share.streamlit.io/ and sign in.
3. Choose **New app**, select this repository, branch `main`, and file path `app.py`.
4. Deploy. The app trains the models on first startup; first launch may take a little longer.
5. Copy the public app URL for your submission.

## Limitations
- The dataset is small, synthetic and deliberately simplified.
- Repeated template patterns can make held-out accuracy look higher than real-world performance.
- Real customer language, spelling errors, multilingual messages, rare issues and messages containing multiple requests may reduce accuracy.
- Confidence values are probability estimates and may not be calibrated.
- Priority labels reflect the synthetic examples, not a formal service-level policy.
- Human review is required before acting on predictions.

## Future improvements
- Expand the dataset with reviewed, consented real support messages.
- Define a written priority policy with support staff.
- Calibrate confidence and monitor model errors before production use.
