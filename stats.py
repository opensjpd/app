import streamlit as st
import tables
import utilities
import pandas as pd

# Given a column tuple, return a sorted 
# series of that stat for officers above the median stop count
def top_stats(name, column_tuples, percent=True, largest=True):
    s = (
        tables
        .officer_stats
        .loc[tables.above_average()]
        [column_tuples]
        .sort_values(ascending=(not largest))
    )

    # Convert values to integer percents if applicable
    if percent:
        s = (s*100).astype(int)

    # Add officer name with badge number on index
    s.index = s.index.map(
        lambda x: f"{utilities.get_name_from_badge(x).title()} #{x}"
    )

    return s.rename(name)