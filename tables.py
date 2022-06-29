import streamlit as st
import pandas as pd
import scipy.stats
from arrests import arrests
import constants

# Given a dataframe and a groupby column, return a MultiIndex-d
# dataframe of aggregate stats along with RACE and SEX crosstabs
@st.cache
def _generate_stats(df, groupby):
    df_dict = {
        'Basic': df.groupby(groupby).agg(**constants.stat_list),
        'Race': pd.crosstab(df[groupby], df.RACE_GROUP, normalize='index', dropna=False),
        'Sex': pd.crosstab(df[groupby], df.SEX, normalize='index', dropna=False),
        'Status': pd.crosstab(df[groupby], df['CURRENT STATUS'], normalize='index', dropna=False),
    }
    for key, df in df_dict.items():
        df.columns = pd.MultiIndex.from_tuples([(key, x) for x in df.columns])
        
    df_list = list(df_dict.values())
    return df_list[0].join(df_list[1:])


# Return badges of officers with stop counts at or above median
# These are the only officers we will generate comparative stats for
@st.cache
def above_average():
    return (
        officer_stats
        .loc[
            officer_stats.Basic.StopCount >= officer_stats.Basic.StopCount.median()
        ]
        .index
    )

# Limit to officers with StopCounts above median
@st.cache
def _get_officer_zscores():
    return (
        officer_stats
        .query("BADGE in @above_average()")
        .drop(columns=[
            ('Basic', 'FirstStop'), 
            ('Basic', 'LastStop'), 
            ('Basic', 'TopStopReason'), 
            ('Basic', 'UniqueOfficers'),
            ('Basic', 'ServiceDuration'),
            ('Basic', 'UniqueStopDays'),
            ('Basic', 'UniquePersons'),
            ('Sex', 'M'),
            ('Status', 'CITED'),
        ])
        .apply(scipy.stats.zscore)
        .assign(total=lambda df: df.agg(lambda s: sum(abs(s)), axis=1))
    )


# Limit to officers with StopCounts above median
@st.cache
def _get_officer_percentiles():
    return (
        officer_stats
        .query("BADGE in @above_average()")
        .drop(columns=[
            ('Basic', 'FirstStop'), 
            ('Basic', 'LastStop'), 
            ('Basic', 'TopStopReason'),
        ])
        .apply(lambda x: pd.DataFrame.rank(x, pct=True))
    )

@st.cache
def get_stat_medians():
    return (
        officer_stats
        .drop(columns=[
            ('Basic', 'FirstStop'),
            ('Basic', 'LastStop'),
            ('Basic', 'TopStopReason')
        ])
        .median()
    )

# Globals
overall_stats = _generate_stats(arrests, 'dummy').loc[0]
officer_stats = _generate_stats(arrests.query("BADGE not in @constants.non_badges"), 'BADGE')
medians = get_stat_medians()

officer_zscores = _get_officer_zscores()
officer_percentiles = _get_officer_percentiles()