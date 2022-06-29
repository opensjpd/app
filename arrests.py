import streamlit as st
import pandas as pd
import constants

@st.cache
def _load_arrests():
    df = (
        pd.read_csv(
            'datasets/Arrests_All.csv',
            dtype={
                'PIN': str,
                'SEX': 'category',
                'RACE': 'category',
                'ETHNICITY': 'category',
                'ARREST TIME': str,
                'ARREST REASON': 'category',
                'ARREST TYPE': 'category',
                'BEAT': 'category',
                'CURRENT STATUS': 'category',
                'YOUNG OFFENDER': 'category'
            },
            parse_dates=['ARREST DATE']
        )
    )

    df.RACE.fillna('U', inplace=True)
    df.ETHNICITY.fillna('U', inplace=True)
    
    return (
        df
        .replace(constants.race_codes) # Decode RACE
        .replace(constants.race_codes.rename(columns={'RACE': 'ETHNICITY'})) # Decode ETHNICITY
        .astype({'RACE': 'category', 'ETHNICITY': 'category'}) # Fix the dtypes
        .merge(constants.race_groups, how='left', left_on='RACE', right_index=True)
        .drop(columns=['GO NO']) # We want just a single row for each arrest
        .drop_duplicates()
        .assign(dummy=0) # Makes overall stats easier to generate
    )

arrests = _load_arrests()
