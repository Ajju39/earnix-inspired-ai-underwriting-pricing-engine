def calculate_risk_score(applicant):
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

    risk_score = (
        applicant["prior_claims"] * 10 +
        applicant["accidents"] * 15 +
        applicant["violations"] * 8 +
        applicant["vehicle_age"] * 1.5 +
        credit_score_map[applicant["credit_tier"]] +
        zip_score_map[applicant["zip_risk"]]
    )

    return min(round(risk_score, 2), 100)


def get_underwriting_decision(risk_score):
    if risk_score < 40:
        return "Approve"
    elif risk_score < 70:
        return "Approve with Adjusted Premium"
    elif risk_score < 85:
        return "Refer to Underwriter"
    else:
        return "Reject"


def calculate_premium(risk_score, coverage_limit, deductible):
    base_premium = 1000

    premium = (
        base_premium *
        (1 + risk_score / 100) *
        (coverage_limit / 50000) *
        (500 / deductible)
    )

    return round(premium, 2)


def generate_explanation(applicant, risk_score, decision, premium):
    reasons = []

    if applicant["prior_claims"] >= 2:
        reasons.append("multiple prior claims")

    if applicant["accidents"] >= 1:
        reasons.append("accident history")

    if applicant["violations"] >= 2:
        reasons.append("driving violations")

    if applicant["vehicle_age"] >= 10:
        reasons.append("older vehicle")

    if applicant["credit_tier"] in ["Fair", "Poor"]:
        reasons.append("higher credit risk tier")

    if applicant["zip_risk"] == "High":
        reasons.append("high-risk ZIP location")

    if not reasons:
        reasons.append("low overall risk profile")

    explanation = (
        f"The applicant received a risk score of {risk_score}. "
        f"The underwriting decision is '{decision}'. "
        f"The recommended premium is ${premium}. "
        f"The main risk drivers are: {', '.join(reasons)}."
    )

    return explanation