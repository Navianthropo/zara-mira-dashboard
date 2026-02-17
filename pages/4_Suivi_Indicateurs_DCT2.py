import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="DCT 2 – Suivi Global", layout="wide")

st.markdown("## 📊 DCT 2 – Suivi Global des Indicateurs")
st.markdown("### Activités 1, 2 et 3")
st.markdown("---")


# ==================================================
# 🔵 ACTIVITÉ 1 – SUIVI & SUPERVISION
# ==================================================

st.markdown("## 🔹 Activité 1 – Paiement & Supervision")

data_act1 = {
    "Indicateur": [
        "CMS impliqués",
        "AL recrutés & formés",
        "IS formés",
        "Superviseurs impliqués",
        "Sites de paiement",
        "Vagues de paiement",
        "Sites avec ombrage conforme"
    ],
    "Planifié": [400, 60, 30, 6, 33, 2, 33],
    "Réalisé": [404, 63, 31, 6, 33, 2, 12]  # 🔵 Réalisation théorique
}

df1 = pd.DataFrame(data_act1)
df1["Écart"] = df1["Réalisé"] - df1["Planifié"]
df1["Taux (%)"] = round((df1["Réalisé"] / df1["Planifié"]) * 100, 1)

global_act1 = round(df1["Taux (%)"].mean(), 1)

st.metric("Taux Global Activité 1", f"{global_act1}%")
st.dataframe(df1, use_container_width=True)

fig1 = px.bar(df1.sort_values("Taux (%)"),
              x="Taux (%)", y="Indicateur",
              orientation="h", text="Taux (%)",
              color="Taux (%)",
              color_continuous_scale=["#c62828","#ff9800","#2e8b57"],
              range_x=[0,120])
fig1.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")


# ==================================================
# 🔵 ACTIVITÉ 2 – GRM
# ==================================================

st.markdown("## 🔹 Activité 2 – Mécanisme de Plaintes (GRM)")

data_act2 = {
    "Indicateur": [
        "Ligne verte dédiée",
        "Boîtes à doléances installées",
        "Plaintes traitées (%)",
        "Couverture géographique"
    ],
    "Planifié": [1, 102, 90, 102],
    "Réalisé": [1, 102, 88, 102]  # 🔵 Réalisation théorique
}

df2 = pd.DataFrame(data_act2)
df2["Écart"] = df2["Réalisé"] - df2["Planifié"]
df2["Taux (%)"] = round((df2["Réalisé"] / df2["Planifié"]) * 100, 1)

global_act2 = round(df2["Taux (%)"].mean(), 1)

st.metric("Taux Global Activité 2", f"{global_act2}%")
st.dataframe(df2, use_container_width=True)

fig2 = px.bar(df2.sort_values("Taux (%)"),
              x="Taux (%)", y="Indicateur",
              orientation="h", text="Taux (%)",
              color="Taux (%)",
              color_continuous_scale=["#c62828","#ff9800","#2e8b57"],
              range_x=[0,120])
fig2.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")


# ==================================================
# 🔵 ACTIVITÉ 3 – EBE & ACTEURS COMMUNAUTAIRES
# ==================================================

st.markdown("## 🔹 Activité 3 – EBE & Acteurs Communautaires")

data_act3 = {
    "Indicateur": [
        "Espaces de Bien-Être (EBE)",
        "Parents Leaders mobilisés",
        "Relais Communautaires Jeunes (RCJ)",
        "Fokontany avec RCJ"
    ],
    "Planifié": [102, 742, 102, 102],
    "Réalisé": [95, 700, 102, 102]  # 🔵 Réalisation théorique
}

df3 = pd.DataFrame(data_act3)
df3["Écart"] = df3["Réalisé"] - df3["Planifié"]
df3["Taux (%)"] = round((df3["Réalisé"] / df3["Planifié"]) * 100, 1)

global_act3 = round(df3["Taux (%)"].mean(), 1)

st.metric("Taux Global Activité 3", f"{global_act3}%")
st.dataframe(df3, use_container_width=True)

fig3 = px.bar(df3.sort_values("Taux (%)"),
              x="Taux (%)", y="Indicateur",
              orientation="h", text="Taux (%)",
              color="Taux (%)",
              color_continuous_scale=["#c62828","#ff9800","#2e8b57"],
              range_x=[0,120])
fig3.update_traces(texttemplate='%{text}%', textposition='outside')
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")


# ==================================================
# 🔵 SCORE GLOBAL DCT 2 (pondération stratégique)
# ==================================================

# Pondération : Act1=40%, Act2=30%, Act3=30%
global_dct2 = round(
    (global_act1 * 0.4) +
    (global_act2 * 0.3) +
    (global_act3 * 0.3),
    1
)

st.markdown("## 🎯 Score Global DCT 2")
st.metric("Performance Globale Pondérée", f"{global_dct2}%")

if global_dct2 >= 90:
    st.success("🟢 Performance élevée – Conformité forte.")
elif global_dct2 >= 75:
    st.info("🟡 Performance satisfaisante – Améliorations mineures.")
elif global_dct2 >= 60:
    st.warning("🟠 Performance intermédiaire – Ajustements requis.")
else:
    st.error("🔴 Performance faible – Actions correctives nécessaires.")
