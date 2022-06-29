import arrests
import constants
import streamlit as st
import pandas as pd

@st.cache
def get_all_officer_names():
    return (
        arrests
        .arrests
        .query("`ARREST OFFICER NAME` not in @constants.non_officer_names")
        ['ARREST OFFICER NAME']
        .dropna()
        .unique()
    )


@st.cache
def get_badges_by_name(officer_name):
    return (
        arrests
        .arrests
        .query("`ARREST OFFICER NAME` == @officer_name")
        .BADGE
        .unique()
    )


@st.cache
def get_arrests_by_badge(badge):
    return (
        arrests
        .arrests
        .query("BADGE == @badge")
        .drop(columns=['BADGE', 'ARREST OFFICER NAME', 'dummy'])
        .set_index('AB NO')
        .sort_values(by=['ARREST DATE', 'ARREST TIME'])
    )

@st.cache
def get_summaries_by_badge(badge):
    return pd.DataFrame(
        arrests
        .arrests
        .query("BADGE == @badge")
        [['SUMMARY OF FACTS']]
        .value_counts()
        .rename("Number of arrests")
        .nlargest(10)
    )

@st.cache
def get_name_from_badge(badge):
    return arrests.arrests.query('BADGE == @badge')['ARREST OFFICER NAME'].mode().iloc[0]