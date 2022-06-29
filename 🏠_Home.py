import streamlit as st
st.set_page_config(page_title="Open SJPD", page_icon=":oncoming_police_car:", layout="wide")

import tables
st.markdown("# 🚔 San José Police Open Data")

columns = st.columns(4)

with columns[0]:
    date_range = (tables.overall_stats.Basic.LastStop - tables.overall_stats.Basic.FirstStop).days
    st.metric("Days in Dataset", f"{date_range:,}")

with columns[1]:
    st.metric("Officers", f"{tables.overall_stats.Basic.UniqueOfficers:,}")

with columns[2]:
    st.metric("Arrests", f"{tables.overall_stats.Basic.StopCount:,}")

with columns[3]:
    st.metric("Taxpayer Money", f"${2947905055:,}")

import matplotlib.pyplot as plt

#fig, ax = plt.subplots()
#tables.overall_stats.Race.plot.pie(ylabel='', legend=True, labeldistance=None, ax=ax)
#st.pyplot(fig)

#st.dataframe(tables.overall_stats.index)