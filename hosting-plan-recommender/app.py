import streamlit as st

st.set_page_config(page_title="PKHosting Plan Recommender", page_icon="🌐", layout="centered")

PLANS = {
    "Personal Hosting": {"monthly": 699, "annual": 6990, "websites": 1, "storage": 5, "emails": 5,
        "backup": "Daily backups with 1-day retention",
        "best_for": "One personal website, portfolio, blog or small starter site",
        "features": ["Free migration", "Free SSL", "WordPress setup help", "5 email accounts"]},
    "Business Hosting": {"monthly": 1999, "annual": 19990, "websites": 5, "storage": 25, "emails": 25,
        "backup": "Daily backups with 3-day retention",
        "best_for": "Growing businesses and small teams hosting several websites",
        "features": ["Free migration", "Free SSL", "Managed DNS help", "Priority setup", "25 email accounts"]},
    "Professional Hosting": {"monthly": 3999, "annual": 39990, "websites": 10, "storage": 50, "emails": 50,
        "backup": "Daily backups with 5-day retention",
        "best_for": "Software houses, agencies and companies managing multiple websites",
        "features": ["Free migration", "Free SSL", "Priority support", "Developer-friendly setup", "50 email accounts"]},
}

st.markdown("""
<style>
.main {max-width: 850px;}
.hero {padding: 1.35rem 1.5rem; border-radius: 16px; background: #102b50; color: white; margin-bottom: 1.2rem;}
.hero h1 {color: white; margin: 0 0 .35rem 0; font-size: 2rem;}
.hero p {color: #dce8f6; margin: 0;}
div.stButton > button {border-radius: 9px; font-weight: 600;}
</style>
<div class="hero"><h1>Find the right hosting plan</h1>
<p>Answer four quick questions and get a recommendation for your website.</p></div>
""", unsafe_allow_html=True)

st.write("Tell us a little about your website. You can review the recommendation before ordering.")

with st.form("plan_finder"):
    site_type = st.selectbox("1. What type of website are you planning to host?", [
        "Personal blog or portfolio", "Business or company website",
        "Online store or booking website", "Agency or software house websites",
        "Web application or custom project"])
    website_count = st.selectbox("2. How many websites do you need to host?",
        ["1 website", "2–5 websites", "6–10 websites", "More than 10 websites"])
    storage_need = st.selectbox("3. How much storage do you expect to need?",
        ["Up to 5 GB", "6–25 GB", "26–50 GB", "More than 50 GB", "Not sure yet"])
    workload = st.selectbox("4. Which option best describes your expected traffic or technical needs?", [
        "New website or low traffic", "Regular business traffic",
        "Busy website or resource-heavy workload",
        "I need root access, server control or a custom server setup"])
    submitted = st.form_submit_button("Recommend a plan", use_container_width=True)

def recommend_plan(site_type, website_count, storage_need, workload):
    if (website_count == "More than 10 websites" or storage_need == "More than 50 GB"
        or workload == "I need root access, server control or a custom server setup"
        or site_type == "Web application or custom project"):
        return "Consultation", ("Your requirements may be beyond standard shared hosting. "
            "Contact PKHosting to discuss a suitable Cloud VPS or dedicated server option.")
    if (website_count == "6–10 websites" or storage_need == "26–50 GB"
        or workload == "Busy website or resource-heavy workload"
        or site_type == "Agency or software house websites"):
        return "Professional Hosting", ("You indicated a need for several websites, more storage or a heavier workload. "
            "Professional Hosting offers the largest shared plan allowance.")
    if (website_count == "2–5 websites" or storage_need == "6–25 GB"
        or workload == "Regular business traffic"
        or site_type in ["Business or company website", "Online store or booking website"]):
        return "Business Hosting", ("Your answers point to a growing website or business that may need more room than a starter plan. "
            "Business Hosting supports up to five websites and 25 GB SSD storage.")
    return "Personal Hosting", ("Your answers fit a small or new website with modest storage needs. "
        "Personal Hosting is the entry-level option for one website.")

if submitted:
    plan_name, reason = recommend_plan(site_type, website_count, storage_need, workload)
    st.divider()
    st.subheader("Your recommendation")
    if plan_name == "Consultation":
        st.info(reason)
        st.markdown("[Explore PKHosting VPS and dedicated options](https://www.pkhosting.com/pricing/)")
    else:
        plan = PLANS[plan_name]
        st.success(f"Recommended plan: {plan_name}")
        st.markdown(f"### Rs. {plan['monthly']:,} / month")
        st.caption(f"Annual billing: Rs. {plan['annual']:,} per year. These are recurring listed rates; check the order page for current terms.")
        st.write(reason)
        st.markdown(f"**Best for:** {plan['best_for']}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Websites", f"Up to {plan['websites']}")
        c2.metric("SSD storage", f"{plan['storage']} GB")
        c3.metric("Email accounts", str(plan["emails"]))
        st.markdown("**Included features**")
        for feature in plan["features"]:
            st.write(f"✓ {feature}")
        st.caption(plan["backup"])
        st.link_button("View plan details", "https://www.pkhosting.com/hosting/")
    st.markdown("---")
    st.markdown("**Need help choosing?** Contact PKHosting before ordering if your requirements are unusual.")
    st.link_button("Visit PKHosting", "https://www.pkhosting.com/")

st.markdown("---")
st.caption("Recommendations are based on the answers provided and the published shared-hosting allowances. Bandwidth is unmetered subject to fair-use terms. Prices and package details may change.")
st.caption("Source: PKHosting official hosting plans and pricing.")
