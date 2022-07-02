import streamlit as st
import pandas as pd
import scipy.stats
import constants

#@st.cache
def arrests():
    df = (
        pd.read_csv(
            'datasets/Arrests_All.csv',
            dtype={
                'PIN': 'category',
                'SEX': 'category',
                'RACE': 'category',
                'ETHNICITY': 'category',
                'ARREST TIME': 'category',
                'ARREST REASON': 'category',
                'ARREST TYPE': 'category',
                'BEAT': 'category',
                'CURRENT STATUS': 'category',
                'YOUNG OFFENDER': 'category',
                'SUMMARY OF FACTS': 'category',
                'ARREST LOCATION': 'category',
                'BADGE': 'category',
                'ARREST OFFICER NAME': 'category',
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
        .reset_index(drop=True)
        .assign(dummy=True) # Makes overall stats easier to generate
    )


# Given a dataframe and a groupby column, return a MultiIndex-d
# dataframe of aggregate stats along with RACE and SEX crosstabs
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
def above_average():
    return (
        officer_stats
        .loc[
            officer_stats.Basic.StopCount >= officer_stats.Basic.StopCount.median()
        ]
        .index
    )

#@st.cache
def _get_badge_to_name():
    return (
        arrests()
        .groupby('BADGE')
        .agg(
            Name=('ARREST OFFICER NAME', lambda x: pd.Series.mode(x).get(0))
        )
        .fillna('UNKNOWN')
    )

# Limit to officers with StopCounts above median
def _get_officer_zscores():
    return (
        officer_stats
        .query("BADGE in @above_average()")
        .drop(columns=[
            ('Basic', 'FirstStop'), 
            ('Basic', 'LastStop'), 
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
def _get_officer_percentiles():
    return (
        officer_stats
        .query("BADGE in @above_average()")
        .drop(columns=[
            ('Basic', 'FirstStop'), 
            ('Basic', 'LastStop'), 
        ])
        .apply(lambda x: pd.DataFrame.rank(x, pct=True))
    )


def get_stat_medians():
    return (
        officer_stats
        .drop(columns=[
            ('Basic', 'FirstStop'),
            ('Basic', 'LastStop'),
        ])
        .median()
    )

# Globals
badge_to_name = _get_badge_to_name()
overall_stats = _generate_stats(arrests(), 'dummy').iloc[0]
officer_stats = _generate_stats(arrests().query("BADGE not in @constants.non_badges"), 'BADGE')
medians = get_stat_medians()

officer_zscores = _get_officer_zscores()
officer_percentiles = _get_officer_percentiles()