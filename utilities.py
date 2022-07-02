import constants
import tables
import streamlit as st
import pandas as pd


def get_all_officer_names():
    return (
        tables
        .badge_to_name
        .query("Name not in @constants.non_officer_names")
        .Name
        .dropna()
        .sort_values()
        .unique()
    )


def get_badges_by_name(officer_name):
    return (
        tables
        .badge_to_name
        .query("Name == @officer_name")
        .index
        .to_list()
    )


def get_arrests_by_badge(badge):
    return (
        tables
        .arrests()
        .query("BADGE == @badge")
        .drop(columns=['BADGE', 'ARREST OFFICER NAME', 'dummy'])
        .set_index('AB NO')
        .sort_values(by=['ARREST DATE', 'ARREST TIME'])
    )


def get_summaries_by_badge(badge):
    return pd.DataFrame(
        tables
        .arrests()
        .groupby('BADGE', observed=True)
        [['SUMMARY OF FACTS']]
        .value_counts()
        .loc[badge]
        .rename("Number of arrests")
        .nlargest(10)
    )


def get_name_from_badge(badge):
    return tables.badge_to_name.loc[badge].Name