import joblib
import pandas as pd
from pathlib import Path

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "models" / "predict_flag_invoice.pkl"

FEATURES = [
    "invoice_quantity",
    "invoice_dollars",
    "Freight",
    "total_item_quantity",
    "total_item_dollars"
]


def load_model(model_path: Path = MODEL_PATH):
    """
    Load trained classifier model.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at: {model_path}")

    return joblib.load(model_path)


def predict_invoice_flag(input_data):
    """
    Predict invoice flag for new vendor invoices.
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
    input_df["Predicted_Flag"] = model.predict(input_df)

    return input_df


if __name__ == "__main__":
    # ✅ Correct sample input
    sample_data = {
        "invoice_quantity": [100, 50],
        "invoice_dollars": [18500, 9000],
        "Freight": [200, 120],
        "total_item_quantity": [95, 48],
        "total_item_dollars": [18490, 9050]
    }

    prediction = predict_invoice_flag(sample_data)
    print(prediction)