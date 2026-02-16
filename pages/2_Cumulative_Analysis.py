import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Cumulative Analysis", layout="wide")

# --------------------------------------------------
# STYLE
# --------------------------------------------------
st.markdown("""
<style>
.main { background-color: #f4f7fb; }

.title {
    font-size: 36px;
    font-weight: 800;
    color: #005b96;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
    color: #005b96;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Cumulative Cash Analysis</div>', unsafe_allow_html=True)

# --------------------------------------------------
# DONNÉES (Distribution 1–3 seulement)
# --------------------------------------------------
data = {
    "Distribution": ["Distribution 1", "Distribution 2", "Distribution 3"],
    "Cash_Reach": [1821600000, 1954000000, 2103000000],
    "Cash_Plan": [1943720000, 2050000000, 2200000000]
}

df = pd.DataFrame(data)

# Calcul cumulatif
df["Cumulative_Reach"] = df["Cash_Reach"].cumsum()
df["Cumulative_Plan"] = df["Cash_Plan"].cumsum()

# --------------------------------------------------
# GRAPHIQUE CUMULATIF
# --------------------------------------------------
st.markdown('<div class="section-title">Cumulative Cash to Beneficiaries (Reach)</div>', unsafe_allow_html=True)

fig = px.line(
    df,
    x="Distribution",
    y="Cumulative_Reach",
    markers=True,
)

fig.update_traces(line=dict(color="#005b96", width=4))

fig.update_layout(
    height=450,
    plot_bgcolor="#f4f7fb",
    paper_bgcolor="#f4f7fb",
    yaxis_title="Cumulative Amount (MGA)",
    xaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# BAR COMPARISON
# --------------------------------------------------
st.markdown('<div class="section-title">Distribution Comparison (Reach)</div>', unsafe_allow_html=True)

fig_bar = px.bar(
    df,
    x="Distribution",
    y="Cash_Reach",
    text="Cash_Reach",
    color="Distribution"
)

fig_bar.update_traces(
    texttemplate='%{text:,.0f}',
    textposition='outside'
)

fig_bar.update_layout(
    height=450,
    plot_bgcolor="#f4f7fb",
    paper_bgcolor="#f4f7fb",
    yaxis_title="Amount (MGA)",
    xaxis_title=""
)

st.plotly_chart(fig_bar, use_container_width=True)

# --------------------------------------------------
# INDICATEUR GLOBAL
# --------------------------------------------------
total_cumulative = df["Cash_Reach"].sum()

st.markdown("---")
st.success(f"Total Cumulative Cash Delivered (Distribution 1–3): {total_cumulative:,.0f} MGA")
