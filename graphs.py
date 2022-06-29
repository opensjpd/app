import tables
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import stats
import streamlit as st
import utilities

sns.set_theme()

# Given an officer name and badge number, generate a kdeplot
# comparing the age of their arrest subjects to SJPD's overall
def age_kdeplot(name, badge):
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 5)
    df = (
        tables
        .arrests
        .assign(group=lambda x: x.BADGE == badge)
        .replace({'group': {True: name.title(), False: 'SJPD'}})
    )
    sns.kdeplot(data=df, x='AGE', hue='group', common_norm=False, fill=True, ax=ax)
    return fig

def race_pie_chart(name, badge):
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, sharex=True)
    fig.set_size_inches(12, 10)

    ax[0].set_title('SJPD Average', fontsize=18)
    ax[1].set_title(f"{name.title()} #{badge}", fontsize=18)

    tables.overall_stats.Race.plot.pie(ylabel='', legend=True, labeldistance=None, ax=ax[0])
    tables.officer_stats.loc[badge].Race.plot.pie(subplots=True, labeldistance=None, ax=ax[1])
    ax[0].legend(loc='lower right')

    return fig

def sex_pie_chart(name, badge):
    fig, ax = plt.subplots(nrows=1, ncols=2, sharey=True, sharex=True)
    fig.set_size_inches(12, 10)

    ax[0].set_title('SJPD Average', fontsize=18)
    ax[1].set_title(f"{name.title()} #{badge}", fontsize=18)
    
    tables.overall_stats.Sex.plot.pie(ylabel='', legend=True, labeldistance=None, ax=ax[0])
    tables.officer_stats.loc[badge].Sex.plot.pie(subplots=True, labeldistance=None, ax=ax[1])
    ax[0].legend(loc='lower right')

    return fig

def top_5_kde(name, column_tuple, percent=True, largest=True, pop=None):
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 4)

    series = stats.top_stats(name, column_tuple, percent, largest)
    sns.histplot(
        data=series,
        ax=ax
    )

    ax.set_ylabel('Number of Officers')
    ax.set_xlabel(name)
    if percent:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(100))

    if pop:
        ax.axvline(pop, 0, 1, label='Population', linestyle=':', color='gray', marker=None)

    if largest:
        top_5 = series.nlargest(5)
    else:
        top_5 = series.nsmallest(5)
    for ((officer, value), color) in zip(top_5.iteritems(), sns.color_palette()):
        ax.axvline(value, 1, 0.8, linestyle='-', label=officer, color=color, marker="v")
    ax.legend()

    return (fig, top_5)
