# Earnix-Inspired AI Underwriting & Pricing Engine

## Project Overview

This project is an Earnix-inspired AI underwriting and pricing decision engine for the insurance industry. It simulates how insurers evaluate applicant risk, automate underwriting decisions, recommend personalized premiums, and explain key risk drivers using a Streamlit dashboard.

This is not built using the actual Earnix platform. It is a portfolio project inspired by public insurance underwriting, pricing, and AI decisioning concepts.

## Business Problem

Insurance companies process large volumes of policy applications. Traditional underwriting can be manual, time-consuming, and inconsistent. This project demonstrates how data, machine learning, and rule-based decision logic can help support faster underwriting decisions and personalized pricing.

## Key Features

- Synthetic insurance application data generation
- Rule-based underwriting risk scoring
- Machine learning risk classification using scikit-learn
- Automated underwriting decisions
- Personalized premium recommendation
- GenAI-style underwriting explanation
- Streamlit dashboard with KPIs and visual charts

## Tech Stack

- Python
- Pandas
- NumPy
- scikit-learn
- Streamlit
- Matplotlib

## Project Architecture

```text
Insurance Applicant Inputs
        ↓
Risk Score Calculation
        ↓
ML Risk Classification
        ↓
Underwriting Decision Logic
        ↓
Premium Recommendation
        ↓
GenAI-Style Explanation

## To run this code
cd C:\Users\ganna\Downloads\Projects\earnix-inspired-ai-underwriting-pricing-engine
.\venv\Scripts\Activate.ps1
python src/generate_data.py
python src/train_model.py
streamlit run app/main.py
        ↓
Streamlit Dashboard
