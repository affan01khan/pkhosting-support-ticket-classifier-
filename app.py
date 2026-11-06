from pathlib import Path
import subprocess
import sys
import streamlit as st
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "ticket_classifier.joblib"

st.set_page_config(page_title="PK Hosting Support Ticket Classifier", page_icon="🎫", layout="centered")

@st.cache_resource
def load_models():
    # Streamlit Cloud starts from a clean checkout; train once if the model is absent.
    if not MODEL_PATH.exists():
        result = subprocess.run([sys.executable, str(BASE_DIR / "train.py")], cwd=BASE_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("Model training failed: " + result.stderr[-1500:])
    return joblib.load(MODEL_PATH)

bundle = load_models()
category_model = bundle["category_model"]
priority_model = bundle["priority_model"]

st.title("🎫 PK Hosting Support Ticket Classifier")
st.caption("Predict a support ticket category and priority with model confidence.")
st.info("Coursework demo using synthetic examples only. A support agent should review every prediction.")

ticket = st.text_area(
    "Enter a customer support message",
    placeholder="Example: My website is showing a 500 internal server error...",
    height=150,
)

if st.button("Classify ticket", type="primary", use_container_width=True):
    if not ticket.strip():
        st.warning("Please enter a support message first.")
    else:
        cat_probs = category_model.predict_proba([ticket])[0]
        cat_idx = int(cat_probs.argmax())
        pri_probs = priority_model.predict_proba([ticket])[0]
        pri_idx = int(pri_probs.argmax())
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Predicted category", category_model.classes_[cat_idx])
            st.caption(f"Category confidence: {cat_probs[cat_idx]:.1%}")
        with c2:
            st.metric("Predicted priority", priority_model.classes_[pri_idx])
            st.caption(f"Priority confidence: {pri_probs[pri_idx]:.1%}")
        st.subheader("Confidence by category")
        st.bar_chart(pd.DataFrame({"Confidence": cat_probs}, index=category_model.classes_))
        st.subheader("Confidence by priority")
        st.bar_chart(pd.DataFrame({"Confidence": pri_probs}, index=priority_model.classes_))
        st.caption("Confidence is a model probability estimate, not a guarantee of correctness.")

with st.expander("About this demo"):
    st.write("TF-IDF and Logistic Regression models trained on 120 synthetic support tickets. This demo is not intended for production support decisions.")
