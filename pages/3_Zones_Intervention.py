import json
import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Zones d'Intervention", layout="wide")

# --------------------------------------------------
# STYLE
# --------------------------------------------------
st.markdown("""
<style>
.main { background-color: #f4f7fb; }

.page-title {
    font-size: 34px;
    font-weight: 800;
    color: #005b96;
}

.subtitle {
    color: #4a5a70;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">Zones d’Intervention & Bénéficiaires</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Cartographie dynamique des communes ciblées</div>', unsafe_allow_html=True)
st.markdown("---")

# --------------------------------------------------
# DONNÉES SOCIALES
# --------------------------------------------------

data = [
    ["BEFOTAKA","ANTANINARENINA","MG25222032",3723,92,29],
    ["BEFOTAKA","BEFOTAKA SUD","MG25222011",5680,158,50],
    ["BEFOTAKA","BEHARENA","MG25222052",4403,114,50],
    ["MIDONGY-ATSIMO","ANKAZOVELO","MG25215012",3377,29,48],
    ["MIDONGY-ATSIMO","NOSIFENO","MG25215011",10618,117,104],
    ["MIDONGY-ATSIMO","MALIORANO","MG25215032",4125,41,19],
    ["VONDROZO","VONDROZO","MG25217011",5573,125,79],
    ["VONDROZO","MANAMBIDALA","MG25217012",11327,238,49],
    ["VONDROZO","ANANDRAVY","MG25217013",4964,105,74],
    ["VONDROZO","MAHATSINJO","MG25217030",15095,372,228],
    ["VONDROZO","VOHIMARY","MG25217071",7656,167,39],
]

df = pd.DataFrame(data, columns=[
    "District","Commune","ADM3_PCODE",
    "Enfants","Handicap","Femmes_Enceintes"
])

# --------------------------------------------------
# KPI GLOBALS
# --------------------------------------------------

st.markdown("## Indicateurs Globaux Bénéficiaires")

total_enfants = df["Enfants"].sum()
total_handicap = df["Handicap"].sum()
total_femmes = df["Femmes_Enceintes"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("👶 Total Enfants Éligibles", f"{total_enfants:,}")

with col2:
    st.metric("♿ Total Personnes Handicapées", f"{total_handicap:,}")

with col3:
    st.metric("🤰 Total Femmes Enceintes", f"{total_femmes:,}")

st.markdown("---")

# --------------------------------------------------
# LOAD GEOJSON
# --------------------------------------------------

@st.cache_data
def load_geojson(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

adm2 = load_geojson("data/zara_mira_adm2.geojson")
adm3 = load_geojson("data/zara_mira_adm3.geojson")

# --------------------------------------------------
# GROUPES COULEURS
# --------------------------------------------------

group_red = df[df["District"]=="BEFOTAKA"]["ADM3_PCODE"].tolist()
group_green = df[df["District"]=="MIDONGY-ATSIMO"]["ADM3_PCODE"].tolist()
group_blue = df[df["District"]=="VONDROZO"]["ADM3_PCODE"].tolist()

# --------------------------------------------------
# MAP
# --------------------------------------------------

m = folium.Map(
    location=[-22.0, 47.0],
    zoom_start=7,
    tiles="CartoDB positron",
    control_scale=True
)

def style_adm2(feature):
    return {
        "fillColor": "#005b96",
        "color": "#005b96",
        "weight": 2,
        "fillOpacity": 0.10,
    }

def style_adm3(feature):
    pcode = feature["properties"]["ADM3_PCODE"]

    if pcode in group_red:
        color = "#c62828"      # Befotaka
    elif pcode in group_green:
        color = "#2e7d32"      # Midongy Atsimo
    elif pcode in group_blue:
        color = "#005b96"      # Vondrozo
    else:
        return {
            "fillColor": "#cfd8dc",
            "color": "#90a4ae",
            "weight": 1,
            "fillOpacity": 0.05,
        }

    return {
        "fillColor": color,
        "color": color,
        "weight": 2,
        "fillOpacity": 0.7,
    }

# Add District Layer
folium.GeoJson(
    adm2,
    style_function=style_adm2,
    tooltip=folium.GeoJsonTooltip(
        fields=["ADM2_EN"],
        aliases=["District:"],
        sticky=True
    )
).add_to(m)

# Add Communes with popup indicators
for feature in adm3["features"]:
    pcode = feature["properties"]["ADM3_PCODE"]
    commune_name = feature["properties"]["ADM3_EN"]
    district_name = feature["properties"]["ADM2_EN"]

    stats = df[df["ADM3_PCODE"]==pcode]

    if not stats.empty:
        enfants = stats.iloc[0]["Enfants"]
        handicap = stats.iloc[0]["Handicap"]
        femmes = stats.iloc[0]["Femmes_Enceintes"]

        popup_html = f"""
        <b>Commune:</b> {commune_name}<br>
        <b>District:</b> {district_name}<br>
        <hr>
        👶 Enfants: {enfants:,}<br>
        ♿ Handicap: {handicap:,}<br>
        🤰 Femmes enceintes: {femmes:,}
        """
    else:
        popup_html = f"<b>{commune_name}</b><br>Non ciblée"

    folium.GeoJson(
        feature,
        style_function=style_adm3,
        popup=popup_html
    ).add_to(m)

st_folium(m, width=None, height=750)

# --------------------------------------------------
# RÉSUMÉ PAR DISTRICT
# --------------------------------------------------

st.markdown("---")
st.subheader("Résumé par District")

district_summary = df.groupby("District")[["Enfants","Handicap","Femmes_Enceintes"]].sum()

st.dataframe(district_summary)
