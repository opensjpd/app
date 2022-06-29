import streamlit as st
st.set_page_config(page_title="Unusual Officers - Open SJPD", page_icon=":oncoming_police_car:", layout="wide")

st.markdown("# Unusual Officers")

import stats
import tables
import graphs

st.markdown("## Most Arrests")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde('Total Arrests', ('Basic', 'StopCount'), percent=False)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The median officer has **{} arrests**. **These stats only include officers with at least this many arrests**"
    .format(int(tables.get_stat_medians().Basic.StopCount))
)

st.markdown('---')

st.markdown("## Arrests of Females")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde('% female arrests', ('Sex', 'F'), percent=True, pop=49.4)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The typical officer arrests **{} females per every 100 arrests**"
    .format(int(100*tables.get_stat_medians().Sex.F))
)

st.markdown('---')

st.markdown("## Arrests of Black People")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde('% Black arrests', ('Race', 'AFRICAN AMERICAN'), percent=True, pop=2.9)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The typical officer arrests **{} Black people per every 100 arrests**"
    .format(int(100*tables.get_stat_medians().Race['AFRICAN AMERICAN']))
)

st.markdown('---')

st.markdown("## Arrests of Hispanic and Latinx People")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde('% Hispanic/Latinx arrests', ('Race', 'HISPANIC/LATIN/MEXICAN'), percent=True, pop=31.0)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The typical officer arrests **{} Hispanic or Latinx people per every 100 arrests**"
    .format(int(100*tables.get_stat_medians().Race['HISPANIC/LATIN/MEXICAN']))
)

st.markdown('---')

st.markdown("## Arrests of Asians and Pacific Islanders")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde('% AAPI arrests', ('Race', 'ASIAN/PACIFIC ISLANDER'), percent=True, pop=37.2)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The typical officer arrests **{} Asians or Pacific Islanders per every 100 arrests**"
    .format(int(100*tables.get_stat_medians().Race['ASIAN/PACIFIC ISLANDER']))
)

st.markdown('---')

st.markdown("## Arrests of White people")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde('% white arrests', ('Race', 'CAUCASIAN'), percent=True, pop=25.1)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The typical officer arrests **{} white people per every 100 arrests**"
    .format(int(100*tables.get_stat_medians().Race['CAUCASIAN']))
)

st.markdown('---')

# TODO maybe multiple overlayed KDE plots??
st.markdown("## Arrests of Young People")
columns = st.columns([3,1])
(figure, table) = graphs.top_5_kde(
    'median arrest age', 
    ('Basic', 'MedianAge'), 
    percent=False, 
    largest=False
)
with columns[0]:
    st.pyplot(figure)
with columns[1]:
    st.table(table)
st.info(
    "The typical officer arrests people around **{} years old**"
    .format(int(tables.get_stat_medians().Basic.MedianAge))
)