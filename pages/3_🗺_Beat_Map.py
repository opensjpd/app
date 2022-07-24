import streamlit as st
import pandas as pd
import geopandas as gpd
import tables
from streamlit_folium import folium_static

st.set_page_config(page_title="Beat Map - Open SJPD", page_icon=":oncoming_police_car:", layout="wide")

gdf = gpd.read_file('datasets/shapefiles/Police_Beat.shp')
arrests = tables.arrests()

beat_vs_race = (
    pd
    .crosstab(arrests.BEAT, arrests.RACE_GROUP, normalize='index')
    .apply(lambda x: (x * 100).round(0))
)

races = arrests.RACE_GROUP.unique().sort_values()

st.markdown("# Beat Map")
st.markdown("San José is split into distinct regions known as police beats. \
    The map shows where people of different races are arrested. For example **{:.0f}%** of arrests made in beat **L6** were of \
    **Asian Americans or Pacific Islanders**.".format(beat_vs_race.loc['L6']['ASIAN/PACIFIC ISLANDER']))
with st.sidebar:
    selected_race = st.selectbox('Color Map by Race', options=races)

m = (
    gdf
    .drop(columns=['ID1', 'AREA'])
    .merge(
        beat_vs_race,
        how='inner',
        left_on='Beat',
        right_on='BEAT'
    )
    .explore(
        column=selected_race,
        legend=True,
        tooltip=False,
        popup=['Beat', selected_race],
        cmap='plasma',
    )
)

folium_static(m)