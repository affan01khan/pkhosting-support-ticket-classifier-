# PKHosting Hosting Plan Recommender

A Streamlit app that asks four questions about a customer's website and recommends a suitable PKHosting shared-hosting plan.

## Features
- Exactly four customer questions
- Recommendations for Personal, Business and Professional Hosting
- A consultation path for requirements that may need VPS or dedicated hosting
- Published monthly and annual plan rates
- Direct links to PKHosting plan information

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Open https://share.streamlit.io/
2. Connect your GitHub account.
3. Select this repository and the `main` branch.
4. Set the app file path to `hosting-plan-recommender/app.py`.
5. Deploy.

## Plan information
Plan resources and prices are based on PKHosting's published pages:
- https://www.pkhosting.com/hosting/
- https://www.pkhosting.com/pricing/

Listed recurring rates: Personal Rs. 699/month, Business Rs. 1,999/month, Professional Rs. 3,999/month. Confirm the live checkout page for current terms and promotions.
