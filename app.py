import streamlit as st
from inference.predict_freight import predict_freight_cost
from inference.invoice_flag import predict_invoice_flag

st.set_page_config(
    page_title="Intelli-Invoice Portal",
    page_icon="🚚",
    layout="wide"
)

st.markdown("""
# 💳 Intelli-Invoice Portal
### AI-Driven Freight Cost Prediction & Invoice Risk Flagging

This internal analytics portal leverages machine learning to
- **Forecast freight costs accurately**
- **Detect risky or abnormal vendor invoices**
- **Reduce financial leakage and manual workload**
""")

# Sidebar
# --------------------------------------------------
st.sidebar.title("🔍 Model Selection")
selected_model = st.sidebar.radio(
    "Choose Prediction Module",
    [
        "Freight Cost Prediction",
        "Invoice Manual Approval Flag"
    ]
)

st.sidebar.markdown("""
---
**Business Impact**
- Improved cost forecasting
- Reduced invoice fraud & anomalies
- Faster finance operations
""")

# ---------------- FREIGHT COST PREDICTION ----------------
if selected_model == "Freight Cost Prediction":
    st.subheader("Predict Freight Cost")

    st.markdown("""
    **Objective:**
    Predict freight cost for a vendor invoice using only **Invoice Amount**
    to support budgeting, forecasting, and vendor negotiations.
    """)

    with st.form("freight_form"):
        dollars = st.number_input(
            "💰 Enter Invoice Amount (₹)",
            min_value=1.0,
            value=18500.0
        )

        submit_freight = st.form_submit_button("Predict Cost")

    if submit_freight:
        input_data = {
            "Dollars": [dollars]
        }

        prediction = predict_freight_cost(input_data)['Predicted_Freight']

        st.success("Prediction completed successfully.")

        st.metric(
            label="📦 Estimated Freight Cost",
            value=f"₹{prediction[0]:,.2f}"
        )
# ---------------- INVOICE FLAG PREDICTION ----------------
elif selected_model == "Invoice Manual Approval Flag":

    st.subheader("🧾 Invoice Manual Approval Prediction")

    st.markdown("""
    **Objective:**
    Predict whether a vendor invoice should be **flagged for manual approval**
    based on abnormal cost, freight, or delivery patterns.
    """)

    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            invoice_quantity = st.number_input(
                "Invoice Quantity",
                min_value=1,
                value=50
            )

            freight = st.number_input(
                "Freight Cost",
                min_value=0.0,
                value=1.73
            )

        with col2:
            invoice_dollars = st.number_input(
                "Invoice Amount(₹)",
                min_value=1.0,
                value=352.95
            )

            total_item_quantity = st.number_input(
                "Total Item Quantity",
                min_value=1,
                value=162
            )

        with col3:
            total_item_dollars = st.number_input(
                "Total Item Amount(₹)",
                min_value=1.0,
                value=2476.0
            )

        submit_flag = st.form_submit_button("Evaluate Invoice Risk")

    if submit_flag:
        input_data = {
            "invoice_quantity": [invoice_quantity],
            "invoice_dollars": [invoice_dollars],
            "Freight": [freight],
            "total_item_quantity": [total_item_quantity],
            "total_item_dollars": [total_item_dollars]
        }

        flag_prediction = predict_invoice_flag(input_data)['Predicted_Flag']
        is_flagged = bool(flag_prediction[0])

        if is_flagged:
            st.error("⚠️ Invoice requires **MANUAL APPROVAL**")
        else:
            st.success("✅ Invoice is **SAFE for Auto-Approval**")