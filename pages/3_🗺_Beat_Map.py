import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import seaborn as sns

st.markdown("# Beat Map")

beats = pd.read_json('datasets/beats.json')
beats

labels = pd.read_json('datasets/beat_labels.json')
labels

#with open('datasets/L.geojson') as f:
#    geo = json.load(f)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=37.3391893,
        longitude=-121.8520819,
        zoom=11,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "PolygonLayer",
            data=beats,
            get_polygon="polygons",
            get_fill_color="[31, 119, 180, 50]",
            get_line_color="[31, 119, 180, 255]",
            get_line_width=15,
        ),
        pdk.Layer(
            "TextLayer",
            data=labels,
            get_text="name",
            get_position="coordinates",
            get_size=20
        )
    ],

))

