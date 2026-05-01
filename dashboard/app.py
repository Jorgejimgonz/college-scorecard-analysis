import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def load_data():
    cols = [
        'INSTNM', 'STABBR', 'CONTROL', 'PREDDEG',
        'ADM_RATE', 'SAT_AVG', 'COSTT4_A', 'TUITIONFEE_IN',
        'C150_4', 'MD_EARN_WNE_P10', 'UGDS'
    ]
    df = pd.read_csv('../data/Most-Recent-Cohorts-Institution.csv', usecols=cols)
    df.replace(['PrivacySuppressed', 'NULL', 'None'], np.nan, inplace=True)
    numeric_cols = ['ADM_RATE', 'SAT_AVG', 'COSTT4_A', 'TUITIONFEE_IN', 
                    'C150_4', 'MD_EARN_WNE_P10', 'UGDS']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df = df[df['PREDDEG'] == 3]
    df = df.dropna(subset=['COSTT4_A', 'ADM_RATE', 'C150_4', 'MD_EARN_WNE_P10'])
    df['institution_type'] = df['CONTROL'].map({
        1: 'Public',
        2: 'Private Nonprofit',
        3: 'Private For-Profit'
    })
    df['roi'] = df['MD_EARN_WNE_P10'] / df['COSTT4_A']
    return df

df = load_data()
# ---- PAGE SETUP ----
st.set_page_config(
    page_title="College Scorecard Dashboard",
    layout="wide"
)

# ---- HEADER ----
st.title("College Scorecard: Is Your School Worth It?")
st.markdown("""
This dashboard helps prospective students compare colleges based on cost, 
selectivity, graduation rates, and earnings. Use the filters on the left 
to explore schools by state and institution type.
""")

st.divider()

# ---- SIDEBAR FILTERS ----
st.sidebar.header("Filter Schools")

# State filter
all_states = sorted(df['STABBR'].dropna().unique().tolist())
selected_states = st.sidebar.multiselect(
    "Select State(s)",
    options=all_states,
    default=all_states
)

# Institution type filter
all_types = ['Public', 'Private Nonprofit', 'Private For-Profit']
selected_types = st.sidebar.multiselect(
    "Select Institution Type(s)",
    options=all_types,
    default=all_types
)

# Apply filters to dataframe
filtered_df = df[
    (df['STABBR'].isin(selected_states)) &
    (df['institution_type'].isin(selected_types))
]

# Show how many schools are currently showing
st.sidebar.markdown(f"**Showing {len(filtered_df)} schools**")

# ---- CHART 1: COST VS EARNINGS ----
st.header("Does Paying More Lead to Higher Earnings?")
st.markdown("""
Each dot below represents one school. Move your mouse over any dot to see 
the school name, cost, and earnings. Use the filters on the left to narrow 
down by state or school type.
""")

fig1 = px.scatter(
    filtered_df,
    x='COSTT4_A',
    y='MD_EARN_WNE_P10',
    color='institution_type',
    hover_name='INSTNM',
    trendline='ols',

    hover_data={
        'COSTT4_A': ':$,.0f',
        'MD_EARN_WNE_P10': ':$,.0f',
        'institution_type': False
    },
    labels={
        'COSTT4_A': 'Annual Cost of Attendance ($)',
        'MD_EARN_WNE_P10': 'Median Earnings 10 Years After Enrollment ($)',
        'institution_type': 'Institution Type'
    },
    title='Cost of Attendance vs. Median Earnings',
    color_discrete_map={
        'Public': 'steelblue',
        'Private Nonprofit': 'darkorange',
        'Private For-Profit': 'green'
    }
)

fig1.update_traces(marker=dict(size=7, opacity=0.6))
fig1.update_layout(height=500)

st.plotly_chart(fig1, use_container_width=True)

# ---- CHART 2: ROI BY INSTITUTION TYPE ----
st.header("Which Type of School Gives You the Best Return on Investment?")
st.markdown("""
ROI is calculated as median earnings divided by annual cost of attendance. 
A higher ROI means you're getting more money back relative to what you paid. 
Hover over any bar to see the details.
""")

# Calculate average ROI by institution type
roi_df = filtered_df.groupby('institution_type')['roi'].median().reset_index()
roi_df.columns = ['Institution Type', 'Median ROI']
roi_df = roi_df.sort_values('Median ROI', ascending=False)

fig2 = px.bar(
    roi_df,
    x='Institution Type',
    y='Median ROI',
    color='Institution Type',
    text='Median ROI',
    labels={
        'Institution Type': 'Institution Type',
        'Median ROI': 'Median ROI (Earnings / Cost)'
    },
    title='Median ROI by Institution Type',
    color_discrete_map={
        'Public': 'steelblue',
        'Private Nonprofit': 'darkorange',
        'Private For-Profit': 'green'
    }
)

fig2.update_traces(
    texttemplate='%{text:.2f}',     # rounds the number on each bar to 2 decimal places
    textposition='outside',          # puts the number above each bar
    marker_line_width=0
)
fig2.update_layout(
    height=500,
    showlegend=False                 # legend not needed since bars are already labeled
)

st.plotly_chart(fig2, use_container_width=True)

# ---- BOTTOM SUMMARY ----
st.divider()
st.header("Quick Stats for Selected Schools")

# Create 4 columns for key metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Schools",
    value=f"{len(filtered_df):,}"
)

col2.metric(
    label="Avg Annual Cost",
    value=f"${filtered_df['COSTT4_A'].median():,.0f}"
)

col3.metric(
    label="Avg Graduation Rate",
    value=f"{filtered_df['C150_4'].median():.0%}"
)

col4.metric(
    label="Avg Median Earnings",
    value=f"${filtered_df['MD_EARN_WNE_P10'].median():,.0f}"
)


# ---- CHART 3: COST VS GRADUATION RATE ----
st.header("Does Paying More Mean More Students Actually Finish?")
st.markdown("""
This chart compares annual cost against the 6-year graduation rate. 
If expensive schools were truly better, we'd expect to see a clear 
upward trend — more cost, more graduates. Hover over any dot to 
see the school name.
""")

fig3 = px.scatter(
    filtered_df,
    x='COSTT4_A',
    y='C150_4',
    color='institution_type',
    hover_name='INSTNM',
    hover_data={
        'COSTT4_A': ':$,.0f',
        'C150_4': ':.0%',
        'institution_type': False
    },
    labels={
        'COSTT4_A': 'Annual Cost of Attendance ($)',
        'C150_4': '6-Year Graduation Rate',
        'institution_type': 'Institution Type'
    },
    title='Cost of Attendance vs. Graduation Rate',
    color_discrete_map={
        'Public': 'steelblue',
        'Private Nonprofit': 'darkorange',
        'Private For-Profit': 'green'
    }
)

fig3.update_traces(marker=dict(size=7, opacity=0.6))
fig3.update_layout(height=500)
fig3.update_yaxes(tickformat='.0%')

st.plotly_chart(fig3, use_container_width=True)

# ---- CHART 4: SELECTIVITY VS EARNINGS ----
st.header("Do Harder To Get Into Schools Produce Higher Earners?")
st.markdown("""
This chart compares admission rate against median earnings 10 years 
after enrollment. Schools on the LEFT are harder to get into. 
Schools on the RIGHT accept almost everyone. If selectivity drives 
earnings, we'd expect dots on the left to be higher up than dots 
on the right. Hover over any dot to see the school name.
""")

fig4 = px.scatter(
    filtered_df,
    x='ADM_RATE',
    y='MD_EARN_WNE_P10',
    color='institution_type',
    hover_name='INSTNM',
    hover_data={
        'ADM_RATE': ':.0%',
        'MD_EARN_WNE_P10': ':$,.0f',
        'institution_type': False
    },
    labels={
        'ADM_RATE': 'Admission Rate (0% = Most Selective, 100% = Open Admission)',
        'MD_EARN_WNE_P10': 'Median Earnings 10 Years After Enrollment ($)',
        'institution_type': 'Institution Type'
    },
    title='Selectivity vs. Median Earnings',
    color_discrete_map={
        'Public': 'steelblue',
        'Private Nonprofit': 'darkorange',
        'Private For-Profit': 'green'
    }
)

fig4.update_traces(marker=dict(size=7, opacity=0.6))
fig4.update_layout(height=500)
fig4.update_xaxes(tickformat='.0%')

st.plotly_chart(fig4, use_container_width=True)


# ---- RAW DATA TABLE ----
st.divider()
st.header("Explore Individual Schools")
st.markdown("Click any column header to sort. Use filters on the left to narrow down.")

st.dataframe(
    filtered_df[[
        'INSTNM', 'STABBR', 'institution_type',
        'COSTT4_A', 'ADM_RATE', 'C150_4',
        'MD_EARN_WNE_P10', 'roi'
    ]].rename(columns={
        'INSTNM': 'School Name',
        'STABBR': 'State',
        'institution_type': 'Type',
        'COSTT4_A': 'Annual Cost ($)',
        'ADM_RATE': 'Admission Rate',
        'C150_4': 'Graduation Rate',
        'MD_EARN_WNE_P10': 'Median Earnings ($)',
        'roi': 'ROI'
    }),
    use_container_width=True,
    hide_index=True
)