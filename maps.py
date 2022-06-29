import streamlit as st
import arrests
import pandas as pd
import seaborn as sns
import constants
import numpy as np

@st.cache
def get_coords(query = None):
    geocoding = pd.read_csv('datasets/geocoded.csv', index_col=0)
    # Filter if a query is provided
    filtered_arrests = arrests.arrests.query(query) if query else arrests.arrests
    return (
        filtered_arrests
        .merge(
            geocoding,
            left_on='ARREST LOCATION',
            right_index=True,
            how='left'
        )
        .merge(
            map_colors(),
            left_on='RACE_GROUP',
            right_index=True,
            how='left',
        )
        [['RACE_GROUP', 'Formatted', 'lat', 'lon', 'R', 'G', 'B']]
        .dropna(subset=['lat', 'lon'])
        .astype({'lat': 'float64', 'lon': 'float64'})
    )

@st.cache
def map_colors():
    n = constants.race_groups.RACE_GROUP.nunique()
    # There's probably a cleaner way to do this
    df = pd.DataFrame(
        (sns.color_palette()[0:n]),
        columns=['R','G','B'],
        index=constants.race_groups.RACE_GROUP.unique()
    ).apply(lambda x: x * 255)
    return df
