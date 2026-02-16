import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
st.set_page_config(page_title="ZARA MIRA – Dashboard", layout="wide")

# --------------------------------------------------
# STYLE
# --------------------------------------------------
st.markdown("""
<style>
.main { background-color: #f4f7fb; }

.dashboard-title{
  font-size:56px; font-weight:900;
  background:linear-gradient(90deg,#c62828,#005b96);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  margin-bottom:10px; text-align:center;
}

.program-title{
  font-size:30px; font-weight:700; color:#005b96;
  margin-bottom:10px; text-align:center;
}

.subtitle{
  font-size:14px; color:#4a5a70; text-align:center;
}

.section-title{
  font-size:22px; font-weight:600;
  margin-top:35px; margin-bottom:15px;
  color:#005b96;
}

.custom-card{
  padding:26px; border-radius:18px;
  box-shadow:0 8px 20px rgba(0,0,0,0.08);
  height:150px; color:white;
}

.card-title{ font-size:14px; margin-bottom:12px; opacity:0.9; }
.card-value{ font-size:28px; font-weight:700; }

.placeholder{
  background:#ffffff;
  border:1px dashed #9fb3c8;
  border-radius:14px;
  padding:18px;
  color:#4a5a70;
  text-align:center;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DONNÉES RÉALISÉES (1–3)
# --------------------------------------------------
realized_data = {
    "Distribution 1": {
        "coverage_period": "4 Months",
        "payment_code": "PP-2670-25-00000001",
        "households_plan": 17788,
        "households_reach": 16487,
        "cash_plan": 1943720000,
        "cash_reach": 1821600000
    },
    "Distribution 2": {
        "coverage_period": "4 Months",
        "payment_code": "PP-2670-25-00000005",
        "households_plan": 17798,
        "households_reach": 16243,
        "cash_plan": 1103700000,
        "cash_reach": 958340000
    },
    "Distribution 3": {
        "coverage_period": "4 Months",
        "payment_code": "PP-2670-25-00000006",
        "households_plan": 28022,
        "households_reach": 26215,
        "cash_plan": 3443280000,
        "cash_reach": 3200900000
    }
}

distributions = [f"Distribution {i}" for i in range(1, 11)]

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown('<div class="dashboard-title">DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="program-title">ZARA MIRA – Multi-Cycle Monitoring</div>', unsafe_allow_html=True)

selected_distribution = st.selectbox("", distributions)

# --------------------------------------------------
# SI NON RÉALISÉ
# --------------------------------------------------
if selected_distribution not in realized_data:
    st.markdown("""
    <div class="placeholder">
      <b>Status:</b> Not yet implemented / Not yet realized.<br>
      This distribution has no operational data available yet.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --------------------------------------------------
# EXTRACTION DONNÉES
# --------------------------------------------------
d = realized_data[selected_distribution]

coverage_rate = (d["households_reach"] / d["households_plan"]) * 100
delivery_rate = (d["cash_reach"] / d["cash_plan"]) * 100
undelivered = d["cash_plan"] - d["cash_reach"]

# Sous-titre dynamique
st.markdown(f"""
<div class="subtitle">
{selected_distribution} | Coverage Period: {d['coverage_period']} <br>
Payment Plan Code: {d['payment_code']}
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.markdown('<div class="section-title">Household & Cash Snapshot</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg,#005b96,#007acc);">
        <div class="card-title">Households Plan</div>
        <div class="card-value">{d['households_plan']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg,#003f73,#005b96);">
        <div class="card-title">Households Reached</div>
        <div class="card-value">{d['households_reach']:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg,#c62828,#e53935);">
        <div class="card-title">Cash to Beneficiary (Plan) – MGA</div>
        <div class="card-value">{d['cash_plan']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="custom-card" style="background: linear-gradient(135deg,#8e0000,#c62828);">
        <div class="card-title">Cash to Beneficiary (Reach) – MGA</div>
        <div class="card-value">{d['cash_reach']:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# GAUGES
# --------------------------------------------------
st.markdown('<div class="section-title">Operational Performance</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)

with col5:
    fig_cov = go.Figure(go.Indicator(
        mode="gauge+number",
        value=coverage_rate,
        title={'text': "Household Coverage (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "#005b96"}}
    ))
    fig_cov.update_layout(height=320)
    st.plotly_chart(fig_cov, use_container_width=True)

with col6:
    fig_fin = go.Figure(go.Indicator(
        mode="gauge+number",
        value=delivery_rate,
        title={'text': "Cash Delivery (%)"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "#c62828"}}
    ))
    fig_fin.update_layout(height=320)
    st.plotly_chart(fig_fin, use_container_width=True)

# --------------------------------------------------
# BREAKDOWN
# --------------------------------------------------
st.markdown('<div class="section-title">Cash Distribution Breakdown</div>', unsafe_allow_html=True)

df = pd.DataFrame({
    "Category": ["Reach", "Undelivered"],
    "Amount": [d["cash_reach"], undelivered]
})

fig_bar = px.bar(
    df,
    x="Amount",
    y="Category",
    orientation="h",
    text="Amount",
    color="Category",
    color_discrete_map={
        "Reach": "#005b96",
        "Undelivered": "#c62828"
    }
)

fig_bar.update_traces(
    texttemplate='%{text:,.0f} MGA',
    textposition='inside',
    insidetextfont=dict(color="white")
)

fig_bar.update_layout(
    height=380,
    plot_bgcolor="#f4f7fb",
    paper_bgcolor="#f4f7fb"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.success(
    f"{selected_distribution} – Coverage: {coverage_rate:.2f}% | Cash Delivery: {delivery_rate:.2f}%"
)
