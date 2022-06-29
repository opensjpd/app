import pandas as pd
import constants
import tables
import graphs
from math import floor

# Given a series of stat percentiles, generate relevant text snippets
def get_insights(name, badge):
    upper_bound = constants.anomalous_thresholds['upper']
    lower_bound = constants.anomalous_thresholds['lower']
    this_officer_percentiles = tables.officer_percentiles.loc[badge]
    this_officer_stats = tables.officer_stats.loc[badge]

    p = (
        this_officer_percentiles
        .where(
            (this_officer_percentiles > upper_bound) | 
            (this_officer_percentiles < lower_bound)
        )
        .dropna()
    )

    name = f"Officer {name.title()}"
    insights = []

    if ('Basic', 'MedianAge') in p:
        #sns.kdeplot()
        if p.Basic.MedianAge < lower_bound:
            summary = f"**{name}** tends to arrest **younger** people than other officers"
        elif p.Basic.MedianAge > upper_bound:
            summary = f"**{name}** tends to arrest **older** people than other officers"
        graph = graphs.age_kdeplot(name, badge)
        insights.append((summary, graph))

    if ('Sex', 'F') in p:
        if p.Sex.F < lower_bound:
            summary = f"**{name}** arrested a higher proportion of **males** than **{floor(100*(1 - p.Sex.F))}%** of officers"
        elif p.Sex.F > upper_bound:
            summary = f"**{name}** arrested a higher proportion of **females** than **{floor(p.Sex.F*100)}%** of officers"
        graph = graphs.sex_pie_chart(name, badge)
        insights.append((summary, graph))
    
    if 'Race' in p:
        summary = ""
        if 'AFRICAN AMERICAN' in p.Race and p.Race['AFRICAN AMERICAN'] > upper_bound:
            summary += f"**{name}** arrested more **Black** people than **{floor(p.Race['AFRICAN AMERICAN']*100)}%** of officers\n"
    
        if 'HISPANIC/LATIN/MEXICAN' in p.Race and p.Race['HISPANIC/LATIN/MEXICAN'] > upper_bound:
            summary += f"**{name}** arrested more **Hispanic or Latinx** people than **{floor(p.Race['HISPANIC/LATIN/MEXICAN']*100)}%** of officers\n"
        
        if 'ASIAN/PACIFIC ISLANDER' in p.Race and p.Race['ASIAN/PACIFIC ISLANDER'] > upper_bound:
            summary += f"**{name}** arrested more **Asians or Pacific Islanders** than **{floor(p.Race['ASIAN/PACIFIC ISLANDER']*100)}%** of officers\n"
        
        if 'CAUCASIAN' in p.Race and p.Race['CAUCASIAN'] > upper_bound:
            summary += f"**{name}** arrested more **White** people than **{floor(p.Race['CAUCASIAN']*100)}%** of officers\n"
        
        graph = graphs.race_pie_chart(name, badge)
        insights.append((summary, graph))

    return insights