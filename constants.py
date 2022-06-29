import pandas as pd

non_badges = [
    "BADGE NOT AVAIL IN SOURCE RECORD",
    "FIELD BLANK IN DATA SOURCE",
    "NON SWORN DATA ENTRY, NOT ARRESTING OFCR",
]

non_officer_names = [
    "NON SWORN DATA ENTRY",
    "BADGE NOT AVAIL IN SOURCE RECORD",
]

# Lookup table for RACE and ETHNICITY columns
race_codes = (
    pd.read_csv('datasets/Race_Codes.csv', index_col=0, dtype='category')
)

race_groups = (
    pd.read_csv('datasets/Race_Groups.csv', index_col=0, dtype='category')
)

stat_list = {
    'StopCount': ('AB NO', 'nunique'),
    'FirstStop': ('ARREST DATE', 'min'),
    'LastStop': ('ARREST DATE', 'max'),
    'UniqueStopDays': ('ARREST DATE', 'nunique'),
    'ServiceDuration': ('ARREST DATE', lambda x: (x.max() - x.min()).days + 1),  # Time from earliest to latest stop
    'UniqueBeats': ('BEAT', 'nunique'),

    'MinAge': ('AGE', pd.Series.min),
    'MedianAge': ('AGE', pd.Series.median),

    'UniquePersons': ('PIN', 'nunique'),
    'TopStopReason': ('SUMMARY OF FACTS', pd.Series.mode),
    'UniqueOfficers': ('BADGE', 'nunique'),
}

anomalous_thresholds = {'lower': 0.15, 'upper': 0.85}
