import streamlit as st
st.set_page_config(page_title="Officer Lookup - Open SJPD", page_icon=":oncoming_police_car:", layout="wide")

import tables
import insights
import matplotlib.pyplot as plt
import seaborn as sns
import maps
import pydeck as pdk
import utilities

with st.sidebar:
    selected_officer = st.selectbox('Officer', options=utilities.get_all_officer_names())
    if len(utilities.get_badges_by_name(selected_officer)) > 1:
        selected_badge = st.selectbox('Badge', options=utilities.get_badges_by_name(selected_officer))
    else:
        selected_badge = utilities.get_badges_by_name(selected_officer)[0] 

this_officer_stats = tables.officer_stats.loc[selected_badge]

st.markdown(f"# Officer {selected_officer.title()} (#{selected_badge})")

# Metric banner
columns = st.columns(4)
with columns[0]:
    st.metric("Total Arrests", this_officer_stats.Basic.StopCount)
with columns[1]:
    st.metric("Beats Patrolled", this_officer_stats.Basic.UniqueBeats)
with columns[2]:
    st.metric("Booking Rate", f"{this_officer_stats.Status['CHARGED/BOOKED']:.0%}")
with columns[3]:
    st.metric("Median Age", int(this_officer_stats.Basic.MedianAge))


if selected_badge not in tables.officer_percentiles.index:
    st.warning(
        "There aren't enough arrests to compare this officer to others. Only officers with **{} or more arrests** can be compared"
        .format(int(tables.medians.Basic.StopCount))
    )
else:
    insight_list = insights.get_insights(selected_officer, selected_badge)
    st.markdown("## Insights")
    if len(insight_list) == 0:
        st.info(f"**Officer {selected_officer.title()}** is similar to the average officer")
    else:
        for (summary, graph) in insight_list:
            st.info(summary)
            if graph:
                st.pyplot(graph)
            st.markdown("---")

st.markdown("## Top Reasons for Arrest")
st.table(utilities.get_summaries_by_badge(selected_badge))

locations = maps.get_coords(f"BADGE == '{selected_badge}'")

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v10',
    initial_view_state=pdk.ViewState(
        latitude=locations.lat.mean(),
        longitude=locations.lon.mean(),
        zoom=11,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=locations[['lat', 'lon', 'R', 'G', 'B']],
            get_position='[lon, lat]',
            get_color='[R, G, B, 160]',
            get_radius=150,
        ),
    ],
))

st.markdown("## All Arrests")
st.dataframe(utilities.get_arrests_by_badge(selected_badge))