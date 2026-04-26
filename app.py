import streamlit as st
from inference.predict_freight import predict_freight_cost
from inference.invoice_flag import predict_invoice_flag

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="🚚",
    layout="wide"
)

# =========================
# CUSTOM STYLE (simple but professional)
# =========================
st.markdown("""
    <style>
        .main-title {
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .sub-title {
            font-size: 16px;
            color: #6c757d;
            margin-bottom: 20px;
        }

        .block-card {
            padding: 18px;
            border-radius: 12px;
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("<div class='main-title'>💳 Vendor Invoice Intelligence Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>AI-powered Freight Cost Prediction & Invoice Risk Analysis</div>", unsafe_allow_html=True)

st.divider()

# =========================
# SIDEBAR
# =========================
selected_model = st.sidebar.radio(
    "Select Module",
    ["🚚 Freight Cost Prediction", "🧾 Invoice Risk Flagging"]
)

# =========================================================
# 🚚 FREIGHT COST PREDICTION
# =========================================================
if selected_model == "🚚 Freight Cost Prediction":

    st.markdown("## Freight Cost Prediction")

    st.markdown("<div class='block-card'>", unsafe_allow_html=True)

    with st.form("freight_form"):

        st.write("Enter invoice value to estimate expected freight cost.")

        invoice_rupees = st.number_input(
            "Invoice Amount (₹)",
            min_value=1.0,
            value=18500.0
        )

        submit = st.form_submit_button("Predict Freight Cost")

    st.markdown("</div>", unsafe_allow_html=True)

    if submit:

        input_data = {
            "Dollars": [invoice_rupees]   # backend mapping unchanged
        }

        prediction = predict_freight_cost(input_data)["Predicted_Freight"]

        st.success("Prediction completed successfully")

        st.metric(
            label="Estimated Freight Cost",
            value=f"₹{prediction.iloc[0]:,.2f}"
        )

# =========================================================
# 🧾 INVOICE FLAGGING
# =========================================================
elif selected_model == "🧾 Invoice Risk Flagging":

    st.markdown("## Invoice Risk Analysis")

    st.markdown("<div class='block-card'>", unsafe_allow_html=True)

    with st.form("invoice_flag_form"):

        st.write("Provide invoice details to check whether manual approval is required.")

        col1, col2, col3 = st.columns(3)

        with col1:
            invoice_quantity = st.number_input("Invoice Quantity", min_value=1, value=50)
            freight = st.number_input("Freight Cost (₹)", min_value=0.0, value=1.73)

        with col2:
            invoice_amount = st.number_input("Invoice Amount (₹)", min_value=1.0, value=352.95)
            total_item_quantity = st.number_input("Total Item Quantity", min_value=1, value=162)

        with col3:
            total_item_amount = st.number_input("Total Item Amount (₹)", min_value=1.0, value=2476.0)

        submit_flag = st.form_submit_button("Evaluate Invoice")

    st.markdown("</div>", unsafe_allow_html=True)

    if submit_flag:

        input_data = {
            "invoice_quantity": [invoice_quantity],
            "invoice_dollars": [invoice_amount],
            "Freight": [freight],
            "total_item_quantity": [total_item_quantity],
            "total_item_dollars": [total_item_amount]
        }

        flag_prediction = predict_invoice_flag(input_data)["Predicted_Flag"]
        is_flagged = bool(flag_prediction.iloc[0])

        st.divider()

        if is_flagged:
            st.error("⚠️ Manual Approval Required")
            st.caption("This invoice shows anomalies or mismatch patterns.")
        else:
            st.success("✅ Auto-Approved")
            st.caption("Invoice appears consistent and safe for processing.")