import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000

data = pd.DataFrame({
    "applicant_id": range(1, n + 1),
    "age": np.random.randint(18, 75, n),
    "vehicle_age": np.random.randint(0, 20, n),
    "prior_claims": np.random.randint(0, 6, n),
    "accidents": np.random.randint(0, 4, n),
    "violations": np.random.randint(0, 5, n),
    "credit_tier": np.random.choice(["Excellent", "Good", "Fair", "Poor"], n),
    "zip_risk": np.random.choice(["Low", "Medium", "High"], n),
    "coverage_limit": np.random.choice([25000, 50000, 100000, 250000], n),
    "deductible": np.random.choice([250, 500, 1000, 2000], n)
})

credit_score_map = {
    "Excellent": 5,
    "Good": 10,
    "Fair": 20,
    "Poor": 30
}

zip_score_map = {
    "Low": 5,
    "Medium": 15,
    "High": 30
}

data["risk_score"] = (
    data["prior_claims"] * 10 +
    data["accidents"] * 15 +
    data["violations"] * 8 +
    data["vehicle_age"] * 1.5 +
    data["credit_tier"].map(credit_score_map) +
    data["zip_risk"].map(zip_score_map)
)

data["risk_score"] = data["risk_score"].clip(0, 100)

def underwriting_decision(score):
    if score < 40:
        return "Approve"
    elif score < 70:
        return "Approve with Adjusted Premium"
    elif score < 85:
        return "Refer to Underwriter"
    else:
        return "Reject"

data["underwriting_decision"] = data["risk_score"].apply(underwriting_decision)

base_premium = 1000

data["premium_recommendation"] = (
    base_premium *
    (1 + data["risk_score"] / 100) *
    (data["coverage_limit"] / 50000) *
    (500 / data["deductible"])
)

data["premium_recommendation"] = data["premium_recommendation"].round(2)

data.to_csv("data/insurance_applications.csv", index=False)

print("Synthetic insurance underwriting data created successfully.")
print(data.head())