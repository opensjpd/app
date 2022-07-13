import streamlit as st
import maps
import pydeck as pdk

locations = maps.get_coords()
locations = locations.loc[locations.duplicated()]

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=locations.lat.mean(),
        longitude=locations.lon.mean(),
        zoom=11,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=locations[['lat', 'lon', 'R', 'G', 'B']],
            get_position='[lon, lat]',
            get_color='[R, G, B, 160]',
            get_radius=50,
            opacity=0.1
        ),
    ],
))