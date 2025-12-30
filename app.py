import streamlit as st
import pickle
import pandas as pd
import numpy as np
import base64

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(page_title="Churn Predictor", layout="centered")

# -------------------------------------------------
# Background + FINAL CSS
# -------------------------------------------------
def set_background(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        header, footer {{ visibility: hidden; }}

        .title-box {{
            background-color: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 18px;
            text-align: center;
            font-size: 42px;
            font-weight: 900;
            color: black;
            margin-bottom: 35px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        }}

        .section-title {{
            text-align: center;
            color: white;
            font-weight: 900;
            background-color: rgba(0,0,0,0.7);
            padding: 35px;
            border-radius: 35px;
            margin-bottom: 35px;
        }}

        .label-box {{
            background-color: rgba(0,0,0,0.75);
            padding: 8px 16px;
            border-radius: 10px;
            margin: 12px 0 6px 0;
            display: inline-block;
        }}

        div[data-baseweb="input"] input {{
            font-size: 26px !important;
            font-weight: 800 !important;
            color: black !important;
            background-color: white !important;
            border: 4px solid black !important;
            border-radius: 14px !important;
            padding: 12px 16px !important;
            text-align: left !important;
        }}

        div[data-baseweb="select"] > div {{
            font-size: 26px !important;
            font-weight: 800 !important;
            color: black !important;
            background-color: white !important;
            border: 4px solid black !important;
            border-radius: 14px !important;
        }}

        .result-box {{
            background-color: rgba(255,255,255,0.97);
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            font-size: 34px;
            font-weight: 900;
            color: black;
            margin-top: 45px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 6px solid;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("assets/ChurnBank.jpeg")

# -------------------------------------------------
# Load model
# -------------------------------------------------
with open("catboost_cat_model (1).pkl", "rb") as f:
    model = pickle.load(f)

# -------------------------------------------------
# Title
# -------------------------------------------------
st.markdown('<div class="title-box">🏦Bank Customer Churn Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">PLEASE ENTER YOUR CUSTOMER DETAILS</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Inputs (ALL WITH UNIQUE KEYS)
# -------------------------------------------------
st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Credit Score</p></div>', unsafe_allow_html=True)
CreditScore = st.number_input("", 300, 900, 650, step=1, label_visibility="collapsed", key="credit_score")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Gender</p></div>', unsafe_allow_html=True)
Gender = st.selectbox("", ["Female", "Male"], label_visibility="collapsed", key="gender")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Age</p></div>', unsafe_allow_html=True)
Age = st.number_input("", 18, 100, 35, step=1, label_visibility="collapsed", key="age")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Tenure (Years)</p></div>', unsafe_allow_html=True)
Tenure = st.number_input("", 0, 10, 5, step=1, label_visibility="collapsed", key="tenure")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Account Balance</p></div>', unsafe_allow_html=True)
Balance = st.number_input("", min_value=0.0, value=50000.0, step=1000.0, label_visibility="collapsed", key="balance")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Number of Products</p></div>', unsafe_allow_html=True)
NumOfProducts = st.number_input("", 1, 4, 2, step=1, label_visibility="collapsed", key="num_products")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Has Credit Card?</p></div>', unsafe_allow_html=True)
HasCrCard = st.selectbox("", ["Yes", "No"], label_visibility="collapsed", key="has_card")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Is Active Member?</p></div>', unsafe_allow_html=True)
IsActiveMember = st.selectbox("", ["Yes", "No"], label_visibility="collapsed", key="is_active")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Estimated Salary</p></div>', unsafe_allow_html=True)
EstimatedSalary = st.number_input("", min_value=0.0, value=75000.0, step=1000.0, label_visibility="collapsed", key="salary")

st.markdown('<div class="label-box"><p style="font-size:32px;font-weight:700;color:white;margin:0;">Country</p></div>', unsafe_allow_html=True)
Geography = st.selectbox("", ["France", "Germany", "Spain"], label_visibility="collapsed", key="country")

# -------------------------------------------------
# Encoding & Feature Engineering
# -------------------------------------------------
Gender = 1 if Gender == "Male" else 0
HasCrCard = 1 if HasCrCard == "Yes" else 0
IsActiveMember = 1 if IsActiveMember == "Yes" else 0
Germany = 1 if Geography == "Germany" else 0
Spain = 1 if Geography == "Spain" else 0

Log_Balance = np.log1p(Balance)
Sqrt_EstimatedSalary = np.sqrt(EstimatedSalary)
Log_Age = np.log1p(Age)

Balance_per_Product = Balance / (NumOfProducts + 1)
Non_France = 1 if (Germany or Spain) else 0
Age_Balance = Age * Balance
CreditScore_IsActive = CreditScore * IsActiveMember
Tenure_NumOfProducts = Tenure * NumOfProducts
Age_Gender = Age * Gender

input_data = pd.DataFrame([[
    CreditScore, Gender, Age, Tenure, Balance, NumOfProducts,
    HasCrCard, IsActiveMember, EstimatedSalary,
    Germany, Spain,
    Log_Balance, Sqrt_EstimatedSalary, Log_Age,
    Balance_per_Product, Non_France, Age_Balance,
    CreditScore_IsActive, Tenure_NumOfProducts, Age_Gender
]])

# -------------------------------------------------
# Prediction
# -------------------------------------------------
if st.button("🏦 PREDICT CHURN", use_container_width=True):
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    if prediction == 1:
        st.markdown(
            f'<div class="result-box" style="border-color:red;">❌ CUSTOMER WILL CHURN<br><br>Probability: {probability:.2%}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="result-box" style="border-color:green;">✅ CUSTOMER WILL STAY<br><br>Probability: {(1-probability):.2%}</div>',
            unsafe_allow_html=True
        )


