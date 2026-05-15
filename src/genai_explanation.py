def generate_genai_style_explanation(applicant, risk_score, decision, premium, ml_risk_category):
    explanation = f"""
    Underwriting Summary:

    The applicant has been classified as {ml_risk_category} based on the provided insurance application details.

    The overall rule-based risk score is {risk_score}, and the underwriting decision is: {decision}.

    The recommended premium is ${premium:,.2f}.

    Key Risk Factors Reviewed:
    - Prior claims: {applicant["prior_claims"]}
    - Accidents: {applicant["accidents"]}
    - Driving violations: {applicant["violations"]}
    - Vehicle age: {applicant["vehicle_age"]} years
    - Credit tier: {applicant["credit_tier"]}
    - ZIP risk level: {applicant["zip_risk"]}
    - Coverage limit: ${applicant["coverage_limit"]:,}
    - Deductible: ${applicant["deductible"]:,}

    Business Recommendation:

    This decision can help underwriting teams quickly identify whether the applicant can be approved automatically, approved with pricing adjustments, referred to a human underwriter, or rejected based on risk appetite.
    """

    return explanation