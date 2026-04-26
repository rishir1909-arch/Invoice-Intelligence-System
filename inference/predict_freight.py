import joblib
import pandas as pd
from pathlib import Path

# -------------------------------
# Robust path handling
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "predict_freight_model.pkl"

FEATURES = ["Dollars"]  # must match training


def load_model(model_path: Path = MODEL_PATH):
    """
    Load trained freight cost prediction model.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at: {model_path}")

    return joblib.load(model_path)


def predict_freight_cost(input_data):
    """
    Predict freight cost for new vendor invoices.
    """
    model = load_model()

    input_df = pd.DataFrame(input_data)

    # -------------------------------
    # Validate input
    # -------------------------------
    missing = [col for col in FEATURES if col not in input_df.columns]
    if missing:
        raise ValueError(f"Missing input columns: {missing}")

    input_df = input_df[FEATURES]

    # -------------------------------
    # Prediction
    # -------------------------------
    input_df["Predicted_Freight"] = model.predict(input_df).round()

    return input_df


if __name__ == "__main__":

    # Example inference run
    sample_data = {
        "Dollars": [18500, 9000]
    }

    prediction = predict_freight_cost(sample_data)
    print(prediction)