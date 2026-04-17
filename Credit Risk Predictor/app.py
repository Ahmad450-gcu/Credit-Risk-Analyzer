import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime


st.set_page_config(page_title="Private Ledger", page_icon="🏛️", layout="centered")

ICON_BANK = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1C2B3A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="22" x2="21" y2="22"/><line x1="6" y1="18" x2="6" y2="11"/><line x1="10" y1="18" x2="10" y2="11"/><line x1="14" y1="18" x2="14" y2="11"/><line x1="18" y1="18" x2="18" y2="11"/><polygon points="12 2 20 7 4 7"/></svg>"""

ICON_BELL = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1C2B3A" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>"""

ICON_WARN = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>"""

ICON_ZAP = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>"""

ICON_CHECK = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>"""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F0F2F5;
    color: #1C2B3A;
}
.stApp { background-color: #F0F2F5; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 1rem 2rem 1rem; max-width: 480px; margin: 0 auto; }

/* ── Top nav ── */
.top-nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 4px 12px 4px; margin-bottom: 4px;
}
.nav-logo { display: flex; align-items: center; gap: 10px; }
.nav-logo span { font-size: 13px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #1C2B3A; }

/* ── Cards ── */
.card {
    background: #ffffff; border-radius: 20px; padding: 24px;
    margin-bottom: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* ── Section label ── */
.section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: #8A97A8; margin-bottom: 4px;
}

/* ── Big prob number ── */
.prob-number {
    font-family: 'DM Mono', monospace;
    font-size: 52px; font-weight: 500; color: #1C2B3A;
    line-height: 1.0; margin: 6px 0 2px 0;
}
.prob-sub { font-size: 13px; color: #8A97A8; margin-bottom: 14px; }

/* ── Risk bar: 3 zones (0-50 green, 50-75 yellow, 75-100 red) ── */
.risk-bar-wrap {
    position: relative; height: 8px; border-radius: 4px;
    background: linear-gradient(to right,
        #6FCF97 0%, #6FCF97 50%,
        #F2C94C 50%, #F2C94C 75%,
        #EB5757 75%, #EB5757 100%);
    margin-bottom: 8px;
}
.risk-bar-needle {
    position: absolute; top: -4px; height: 16px; width: 3px;
    background: #1C2B3A; border-radius: 2px;
    transform: translateX(-50%);
    transition: left 0.6s ease;
}
.risk-bar-labels {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    font-size: 10px; color: #8A97A8;
}
.risk-bar-labels span:nth-child(2) { text-align: center; }
.risk-bar-labels span:nth-child(3) { text-align: right; }

/* ── Section heading ── */
.section-heading {
    font-size: 13px; font-weight: 600; letter-spacing: 0.10em;
    text-transform: uppercase; color: #1C2B3A;
    border-left: 3px solid #2E4A6A; padding-left: 10px;
    margin: 24px 0 16px 0;
}

/* ── Result cards ── */
.result-high { background: #FFF0F0; border: 1.5px solid #F5A5A5; border-radius: 16px; padding: 20px; margin-top: 16px; }
.result-mod  { background: #FFFBF0; border: 1.5px solid #F2C94C; border-radius: 16px; padding: 20px; margin-top: 16px; }
.result-low  { background: #F0FBF4; border: 1.5px solid #6FCF97; border-radius: 16px; padding: 20px; margin-top: 16px; }
.result-title { font-size: 15px; font-weight: 600; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
.result-prob  { font-family: 'DM Mono', monospace; font-size: 36px; font-weight: 500; }

/* ── CTA button ── */
.stButton > button {
    background: #2E4A6A !important; color: #fff !important;
    border: none !important; border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 600 !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    padding: 16px !important;
}
.stButton > button:hover { background: #1C2B3A !important; }
.cta-disclaimer { font-size: 10px; color: #8A97A8; text-align: center; margin-top: 10px; line-height: 1.5; }

/* ── Inputs: blinking caret ── */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
div[data-baseweb="input"] > div {
    border-radius: 10px !important; border-color: #E5E9EF !important;
    background: #F8FAFC !important;
}
div[data-baseweb="input"] input {
    font-family: 'DM Mono', monospace !important;
    color: #1C2B3A !important;
    caret-color: #2E4A6A !important;
    caret-shape: bar !important;
}
div[data-baseweb="input"] input:focus {
    box-shadow: 0 0 0 2px rgba(46,74,106,0.25) !important;
}
.stNumberInput label {
    font-size: 10px !important; font-weight: 600 !important;
    letter-spacing: 0.12em !important; text-transform: uppercase !important;
    color: #8A97A8 !important;
}
</style>
""", unsafe_allow_html=True)

#Load model artefacts 
@st.cache_resource
def load_artifacts():
    model        = joblib.load("best_xgboost_model.pkl")
    imputer      = joblib.load("imputer.pkl")
    scaler       = joblib.load("scaler.pkl")
    feature_cols = joblib.load("feature_columns.pkl")
    cap_vals     = joblib.load("cap_values.pkl")
    return model, imputer, scaler, feature_cols, cap_vals

model, imputer, scaler, feature_columns, cap_values = load_artifacts()

#Session state 
if "pred_result" not in st.session_state: st.session_state.pred_result = None

# Risk tier helper 
def risk_tier(prob):
    """prob is 0-1; score = prob*100. Tiers: 0-50 low, 51-75 moderate, 76-100 high."""
    score = prob * 100
    if score <= 50:
        return "low",      "Low Risk",      "#27AE60", "badge-low"
    elif score <= 75:
        return "moderate", "Moderate Risk", "#F2994A", "badge-mod"
    else:
        return "high",     "High Risk",     "#EB5757",  "badge-high"

# Top nav 
st.markdown(f"""
<div class="top-nav">
  <div class="nav-logo">
    {ICON_BANK}
    <span>Private Ledger</span>
  </div>
  <div>{ICON_BELL}</div>
</div>
""", unsafe_allow_html=True)

#Prediction status card 
result = st.session_state.pred_result
if result is not None:
    prob = result["prob"]
    tier, tier_label, tier_color, _ = risk_tier(prob)
    needle_pct = prob * 100
else:
    prob = 0.000
    tier_label = "Awaiting Analysis"
    tier_color = "#8A97A8"
    needle_pct = 0

st.markdown(f"""
<div class="card">
  <div class="section-label">Current Prediction Status</div>
  <div class="prob-number">{prob:.3f}</div>
  <div class="prob-sub">Probability of Default</div>
  <div class="risk-bar-wrap">
    <div class="risk-bar-needle" style="left:{needle_pct:.1f}%"></div>
  </div>
  <div class="risk-bar-labels">
    <span>Low Risk</span>
    <span style="color:#F2C94C;">Moderate</span>
    <span>High Risk</span>
  </div>
  <div style="margin-top:10px;font-size:12px;font-weight:600;color:{tier_color};">{tier_label}</div>
</div>
""", unsafe_allow_html=True)

# Liquidity & Exposure
st.markdown('<div class="section-heading">Liquidity &amp; Exposure</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    revolving = st.number_input("REVOLVING UTILIZATION", min_value=0.0, max_value=10.0,
                                value=0.0, step=0.01, format="%.2f",
                                help="% of total unsecured credit balance")
with col2:
    debt_ratio = st.number_input("DEBT RATIO", min_value=0.0, max_value=10.0,
                                 value=0.0, step=0.01, format="%.2f",
                                 help="Monthly debt / Monthly assets")

# Capacity Metrics
st.markdown('<div class="section-heading">Capacity Metrics</div>', unsafe_allow_html=True)
cap_col1, cap_col2 = st.columns(2)
with cap_col1:
    age = st.number_input("AGE", min_value=18, max_value=110, value=18)
with cap_col2:
    dependents = st.number_input("DEPENDENTS", min_value=0, max_value=20, value=0)
monthly_income = st.number_input("MONTHLY INCOME ($)", min_value=0.0,
                                 value=0.0, step=100.0, format="%.0f")

# Historical Integrity
st.markdown('<div class="section-heading">Historical Integrity</div>', unsafe_allow_html=True)
past_30_59  = st.number_input("30–59 DAYS PAST DUE",  min_value=0, max_value=20, value=0, help="Last 24 months window")
past_60_89  = st.number_input("60–89 DAYS PAST DUE",  min_value=0, max_value=20, value=0, help="Last 24 months window")
past_90     = st.number_input("90+ DAYS PAST DUE",    min_value=0, max_value=20, value=0, help="Major delinquencies")
open_lines  = st.number_input("OPEN CREDIT LINES",    min_value=0, max_value=50, value=0, help="Instalment & Revolving")
real_estate = st.number_input("REAL ESTATE LOANS",    min_value=0, max_value=20, value=0, help="Mortgages & HE Lines")

# Run button
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
run = st.button("▶  RUN RISK ANALYSIS", use_container_width=True)
st.markdown("""
<div class="cta-disclaimer">
By executing this analysis, you acknowledge that predictions are based on
historical datasets and do not constitute final credit decisions.
</div>
""", unsafe_allow_html=True)

if run:
    input_data = pd.DataFrame([{
        "RevolvingUtilizationOfUnsecuredLines": revolving,
        "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": past_30_59,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": monthly_income,
        "NumberOfOpenCreditLinesAndLoans": open_lines,
        "NumberOfTimes90DaysLate": past_90,
        "NumberRealEstateLoansOrLines": real_estate,
        "NumberOfTime60-89DaysPastDueNotWorse": past_60_89,
        "NumberOfDependents": dependents
    }])

    for col in ["NumberOfTime30-59DaysPastDueNotWorse",
                "NumberOfTimes90DaysLate",
                "NumberOfTime60-89DaysPastDueNotWorse"]:
        input_data[col] = input_data[col].replace({96: 0, 98: 0})

    input_data[["MonthlyIncome", "NumberOfDependents"]] = imputer.transform(
        input_data[["MonthlyIncome", "NumberOfDependents"]]
    )
    input_data["RevolvingUtilizationOfUnsecuredLines"] = input_data["RevolvingUtilizationOfUnsecuredLines"].clip(
        upper=cap_values["RevolvingUtilizationOfUnsecuredLines"]
    )
    input_data["DebtRatio"]     = input_data["DebtRatio"].clip(upper=cap_values["DebtRatio"])
    input_data["MonthlyIncome"] = input_data["MonthlyIncome"].clip(upper=cap_values["MonthlyIncome"])

    input_data_scaled = pd.DataFrame(
        scaler.transform(input_data), columns=input_data.columns
    )

    pred     = model.predict(input_data_scaled)[0]
    prob_val = model.predict_proba(input_data_scaled)[0][1]

    new_result = {
        "pred":   int(pred),
        "prob":   prob_val,
        "time":   datetime.now().strftime("%b %d, %Y  %H:%M"),
        "income": monthly_income,
        "age":    age,
    }
    st.session_state.pred_result = new_result
    st.rerun()

# Result banner
if result is not None:
    p = result["prob"]
    tier, tier_label, tier_color, _ = risk_tier(p)
    if tier == "high":
        css_cls, icon_svg, msg = "result-high", ICON_WARN, "Probability of default exceeds acceptable threshold."
    elif tier == "moderate":
        css_cls, icon_svg, msg = "result-mod",  ICON_ZAP,  "Customer profile shows elevated risk — review recommended."
    else:
        css_cls, icon_svg, msg = "result-low",  ICON_CHECK, "Customer profile is within acceptable risk parameters."

    st.markdown(f"""
    <div class="{css_cls}">
      <div class="result-title" style="color:{tier_color}">{icon_svg} {tier_label}</div>
      <div class="result-prob"  style="color:{tier_color}">{p:.2%}</div>
      <div style="font-size:12px;color:#8A97A8;margin-top:6px;">{msg}</div>
    </div>""", unsafe_allow_html=True)
