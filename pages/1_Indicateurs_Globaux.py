import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==================================================
# CONFIG
# ==================================================
st.set_page_config(page_title="Indicateurs globaux – ZARA MIRA", layout="wide")

st.markdown("## 📌 Indicateurs globaux du projet – ZARA MIRA")
st.markdown("Suivi des résultats, performance et cibles (baseline → cible).")
st.markdown("---")

# ==================================================
# DONNÉES (Structure identique – Réalisé modifié)
# ==================================================

rows = [

    # ---------------- RESULTAT 1 ----------------
    ("Résultat 1", "Couverture effective des allocations",
     "Nombre de bénéficiaires recevant des paiements (enfants + PHS)",
     "Fokontany", 0, 68000+3500, 76541,
     "Fiche de paiement; HOPE; Listes bénéficiaires"),

    ("Résultat 1", "Capacités des acteurs locaux",
     "% d’acteurs locaux formés (PL, RCJ, TS, CMS…)",
     "Région/district", 0, 100, 0,
     "Registres formation; Rapports; Évaluations post-formation"),

    ("Résultat 1", "Conformité des paiements",
     "Nombre de paiements suivis régulièrement",
     "Sites distribution", 0, 18, 0,
     "États de paiement; HOPE; Rapport narratif SAF"),

    ("Résultat 1", "Appropriation MACC",
     "Taux d’agents évalués compétents après coaching",
     "Région/district", 0, 70, 0,
     "Rapports coaching; Grilles; Feedback bénéficiaires"),

    ("Résultat 1", "Performance GRM",
     "% de plaintes résolues / total plaintes",
     "Fokontany/commune", 0, 90, 0,
     "Système plaintes; Registres; Rapports"),

    ("Résultat 1", "Activités EBE",
     "Fréquence séances thématiques (EBE)",
     "Fokontany", 0, 36, 0,
     "Rapports; Fiches présence"),

    ("Résultat 1", "Sensibilisation MACC",
     "Nombre bénéficiaires sensibilisés MACC",
     "Fokontany", 0, 62250, 0,
     "Fiches AL; Fiches présence"),

    ("Résultat 1", "PEAS – sensibilisation",
     "Nombre de sites avec sessions PEAS",
     "Fokontany", 0, 35, 0,
     "Rapport activité"),

    ("Résultat 1", "PEAS – formation staff",
     "Personnel formé PEAS",
     "Fokontany", 0, 1370, 0,
     "Rapport activité"),

    ("Résultat 1", "EBE – mise en place",
     "Nombre d’EBE créées",
     "Fokontany", 0, 102, 0,
     "Registres; Photographies"),

    # ---------------- RESULTAT 2 ----------------
    ("Résultat 2", "Référencement & prise en charge",
     "Circuit de référence établi",
     "District", 0, 1, 0,
     "Rapport validation"),

    ("Résultat 2", "Comités gestion de cas",
     "Nombre comités gestion cas",
     "District", 0, 3, 0,
     "Rapports; Listes comités"),

    ("Résultat 2", "Réunions gestion de cas",
     "Nombre réunions gestion cas",
     "District", 0, 27, 0,
     "Comptes rendus"),

    ("Résultat 2", "Population cible",
     "Bénéficiaires ciblés intervention protection",
     "Fokontany", 0, 68000+3500, 0,
     "Listes bénéficiaires"),

    ("Résultat 2", "Sensibilisation communautés",
     "Communautés sensibilisées (PE/VBG)",
     "Fokontany", 0, 18000, 0,
     "Fiches présence"),

    ("Résultat 2", "Violences signalées et traitées",
     "Nombre cas violences traités",
     "District", 0, 900, 0,
     "Dossiers cas"),

    ("Résultat 2", "Participation communautaire",
     "% communautés ayant participé campagnes",
     "Région/district", 0, 70, 0,
     "Rapports sensibilisation"),

    ("Résultat 2", "Cas protection identifiés",
     "Cas protection identifiés et pris en charge",
     "Région/district", 0, 100, 0,
     "Base de données cas"),

    ("Résultat 2", "PEAS – engagement",
     "% enfants/adultes engagés PEAS",
     "Fokontany", 0, 80, 0,
     "Rapports activité"),

    # ---------------- RESULTAT 3 ----------------
    ("Résultat 3", "Communication projet",
     "Taux compréhension programme",
     "3 districts", 0, 95, 0,
     "Rapports atelier; Focus group"),

    ("Résultat 3", "Supports communication",
     "Nombre supports communication produits",
     "Districts", 0, 3, 0,
     "Inventaire supports"),

    ("Résultat 3", "Success stories",
     "Nombre histoires de réussite produites",
     "Districts", 0, 6, 0,
     "Liens publications"),
]

df = pd.DataFrame(rows, columns=[
    "Résultat","Volet","Indicateur","Lieu",
    "Baseline","Cible","Réalisé","Moyens de vérification"
])

# ==================================================
# CALCULS
# ==================================================

df["Taux (%)"] = np.where(
    df["Cible"] == 0,
    0,
    (df["Réalisé"] / df["Cible"]) * 100
)

df["Taux (%)"] = df["Taux (%)"].round(1)

# ==================================================
# FILTRES (identique à avant)
# ==================================================

c1, c2 = st.columns([1,2])

with c1:
    result_filter = st.selectbox("Filtrer par Résultat",
                                 ["Tous"] + sorted(df["Résultat"].unique()))

with c2:
    search = st.text_input("Recherche indicateur / volet / MV", "")

df_view = df.copy()

if result_filter != "Tous":
    df_view = df_view[df_view["Résultat"] == result_filter]

if search.strip():
    s = search.lower()
    df_view = df_view[
        df_view["Indicateur"].str.lower().str.contains(s) |
        df_view["Volet"].str.lower().str.contains(s)
    ]

st.markdown("---")

# ==================================================
# KPI SYNTHÈSE
# ==================================================

avg_rate = round(df_view["Taux (%)"].mean(), 1)
nb_ind = len(df_view)
nb_red = (df_view["Taux (%)"] < 50).sum()

k1, k2, k3 = st.columns(3)
k1.metric("Indicateurs affichés", nb_ind)
k2.metric("Taux moyen", f"{avg_rate}%")
k3.metric("Indicateurs <50%", nb_red)

st.markdown("---")

# ==================================================
# TABLEAU
# ==================================================

st.subheader("📋 Tableau de suivi global")
st.dataframe(df_view, use_container_width=True)

# ==================================================
# GRAPHIQUE
# ==================================================

st.subheader("📈 Progression des indicateurs")

fig = px.bar(
    df_view.sort_values("Taux (%)"),
    x="Taux (%)",
    y="Indicateur",
    orientation="h",
    text="Taux (%)",
    color="Résultat",
    range_x=[0,120]
)

fig.update_traces(texttemplate="%{text}%", textposition="outside")
fig.update_layout(height=800)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# LECTURE STRATÉGIQUE
# ==================================================

st.markdown("---")

benef_rate = df.iloc[0]["Taux (%)"]

if benef_rate >= 100:
    st.success("🟢 Objectif bénéficiaires dépassé.")
elif benef_rate >= 90:
    st.info("🟡 Couverture bénéficiaires proche de la cible.")
else:
    st.warning("🟠 Couverture bénéficiaires à renforcer.")

if avg_rate < 30:
    st.error("🔴 Mise en œuvre globale encore faible (hors paiements).")
