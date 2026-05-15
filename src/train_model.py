import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder


DATA_PATH = "data/insurance_applications.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "underwriting_risk_model.pkl")


def create_risk_label(score):
    if score < 40:
        return "Low Risk"
    elif score < 70:
        return "Medium Risk"
    else:
        return "High Risk"


def train_model():
    df = pd.read_csv(DATA_PATH)

    df["risk_category"] = df["risk_score"].apply(create_risk_label)

    features = [
        "age",
        "vehicle_age",
        "prior_claims",
        "accidents",
        "violations",
        "credit_tier",
        "zip_risk",
        "coverage_limit",
        "deductible"
    ]

    target = "risk_category"

    model_df = df[features + [target]].copy()

    label_encoders = {}

    for col in ["credit_tier", "zip_risk"]:
        encoder = LabelEncoder()
        model_df[col] = encoder.fit_transform(model_df[col])
        label_encoders[col] = encoder

    target_encoder = LabelEncoder()
    model_df[target] = target_encoder.fit_transform(model_df[target])

    X = model_df[features]
    y = model_df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=8
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("Model Training Completed")
    print(f"Accuracy: {accuracy:.2f}")
    print(classification_report(y_test, predictions, target_names=target_encoder.classes_))

    os.makedirs(MODEL_DIR, exist_ok=True)

    model_package = {
        "model": model,
        "label_encoders": label_encoders,
        "target_encoder": target_encoder,
        "features": features
    }

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model_package, file)

    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_model()