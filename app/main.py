import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.genai_explanation import generate_genai_style_explanation



from src.underwriting_engine import (
    calculate_risk_score,
    get_underwriting_decision,
    calculate_premium,
    generate_explanation
)

from src.ml_predictor import predict_risk_category


st.set_page_config(
    page_title="Earnix-Inspired AI Underwriting & Pricing Engine",
    layout="wide"
)

st.title("Earnix-Inspired AI Underwriting & Pricing Engine")

st.write(
    "This portfolio project simulates insurance underwriting, ML-based risk prediction, "
    "personalized premium recommendation, and business-friendly decision explanations."
)

st.sidebar.header("Applicant Details")

age = st.sidebar.slider("Age", 18, 75, 35)
vehicle_age = st.sidebar.slider("Vehicle Age", 0, 20, 5)
prior_claims = st.sidebar.slider("Prior Claims", 0, 5, 1)
accidents = st.sidebar.slider("Accidents", 0, 3, 0)
violations = st.sidebar.slider("Violations", 0, 4, 0)
credit_tier = st.sidebar.selectbox("Credit Tier", ["Excellent", "Good", "Fair", "Poor"])
zip_risk = st.sidebar.selectbox("ZIP Risk", ["Low", "Medium", "High"])
coverage_limit = st.sidebar.selectbox("Coverage Limit", [25000, 50000, 100000, 250000])
deductible = st.sidebar.selectbox("Deductible", [250, 500, 1000, 2000])

applicant = {
    "age": age,
    "vehicle_age": vehicle_age,
    "prior_claims": prior_claims,
    "accidents": accidents,
    "violations": violations,
    "credit_tier": credit_tier,
    "zip_risk": zip_risk,
    "coverage_limit": coverage_limit,
    "deductible": deductible
}

risk_score = calculate_risk_score(applicant)
decision = get_underwriting_decision(risk_score)
premium = calculate_premium(risk_score, coverage_limit, deductible)
explanation = generate_explanation(applicant, risk_score, decision, premium)

try:
    ml_risk_category, ml_probabilities = predict_risk_category(applicant)
except FileNotFoundError:
    ml_risk_category = "Model not trained"
    ml_probabilities = {}

genai_explanation = generate_genai_style_explanation(
    applicant,
    risk_score,
    decision,
    premium,
    ml_risk_category
)
col1, col2, col3, col4 = st.columns(4)

col1.metric("Rule-Based Risk Score", risk_score)
col2.metric("ML Risk Category", ml_risk_category)
col3.metric("Underwriting Decision", decision)
col4.metric("Recommended Premium", f"${premium:,.2f}")

st.subheader("Underwriting Explanation")
st.info(explanation)
st.subheader("GenAI-Style Underwriting Summary")
st.success(genai_explanation)
st.subheader("Applicant Input Summary")
st.dataframe(pd.DataFrame([applicant]), use_container_width=True)

st.subheader("ML Risk Probability")

if ml_probabilities:
    probability_df = pd.DataFrame({
        "Risk Category": list(ml_probabilities.keys()),
        "Probability": list(ml_probabilities.values())
    })

    st.dataframe(probability_df, use_container_width=True)

    fig, ax = plt.subplots()
    ax.bar(probability_df["Risk Category"], probability_df["Probability"])
    ax.set_xlabel("Risk Category")
    ax.set_ylabel("Probability %")
    ax.set_title("ML Risk Prediction Probability")
    st.pyplot(fig)
else:
    st.warning("ML model not found. Please run: python src/train_model.py")


st.subheader("Portfolio Dashboard")

try:
    df = pd.read_csv("data/insurance_applications.csv")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("Total Applications", len(df))
    kpi2.metric("Average Risk Score", round(df["risk_score"].mean(), 2))
    kpi3.metric("Average Premium", f"${df['premium_recommendation'].mean():,.2f}")
    kpi4.metric("High-Risk Applications", len(df[df["risk_score"] >= 70]))

    st.write("### Underwriting Decision Distribution")
    decision_counts = df["underwriting_decision"].value_counts().reset_index()
    decision_counts.columns = ["Decision", "Count"]

    fig2, ax2 = plt.subplots()
    ax2.bar(decision_counts["Decision"], decision_counts["Count"])
    ax2.set_xlabel("Underwriting Decision")
    ax2.set_ylabel("Count")
    ax2.set_title("Decision Distribution")
    plt.xticks(rotation=20)
    st.pyplot(fig2)

    st.write("### Risk Score Distribution")
    fig3, ax3 = plt.subplots()
    ax3.hist(df["risk_score"], bins=20)
    ax3.set_xlabel("Risk Score")
    ax3.set_ylabel("Application Count")
    ax3.set_title("Risk Score Distribution")
    st.pyplot(fig3)

    st.write("### Average Premium by ZIP Risk")
    zip_premium = df.groupby("zip_risk")["premium_recommendation"].mean().reset_index()

    fig4, ax4 = plt.subplots()
    ax4.bar(zip_premium["zip_risk"], zip_premium["premium_recommendation"])
    ax4.set_xlabel("ZIP Risk")
    ax4.set_ylabel("Average Premium")
    ax4.set_title("Average Premium by ZIP Risk")
    st.pyplot(fig4)

except FileNotFoundError:
    st.warning("Data file not found. Please run: python src/generate_data.py")


st.subheader("Decision Logic")

st.write("""
- Risk Score below 40: Approve
- Risk Score between 40 and 69: Approve with Adjusted Premium
- Risk Score between 70 and 84: Refer to Underwriter
- Risk Score 85 and above: Reject
""")