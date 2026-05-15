import pickle
import pandas as pd


MODEL_PATH = "models/underwriting_risk_model.pkl"


def load_model():
    with open(MODEL_PATH, "rb") as file:
        model_package = pickle.load(file)

    return model_package


def predict_risk_category(applicant):
    model_package = load_model()

    model = model_package["model"]
    label_encoders = model_package["label_encoders"]
    target_encoder = model_package["target_encoder"]
    features = model_package["features"]

    applicant_df = pd.DataFrame([applicant])

    for col in ["credit_tier", "zip_risk"]:
        applicant_df[col] = label_encoders[col].transform(applicant_df[col])

    applicant_df = applicant_df[features]

    prediction = model.predict(applicant_df)[0]
    probability = model.predict_proba(applicant_df)[0]

    risk_category = target_encoder.inverse_transform([prediction])[0]

    probability_dict = {
        target_encoder.classes_[i]: round(float(probability[i]) * 100, 2)
        for i in range(len(target_encoder.classes_))
    }

    return risk_category, probability_dict