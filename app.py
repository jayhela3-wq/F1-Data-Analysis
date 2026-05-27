import streamlit as st
import preprocessor
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = preprocessor.preprocess()

st.sidebar.title("Formula-1 Dashboard")
st.sidebar.image('C:/Users/joyhela/F1_DataAnalysis/logo.png',width='stretch')

user_menu = st.sidebar.radio(
    "Select an Option",
    (
        "Home",
        "Top Drivers",
        "Top Constructors",
        "Driver Comparison",
        "Heatmap"
    )
)

if user_menu == "Home" :
    st.title("Formula-1 Data Analysis")

    total_seasons = df['Year'].nunique()
    total_drivers = df['Driver'].nunique()
    total_constructors = df['Constructor'].nunique()
    total_races = df['Race_Name'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("Total Seasons",total_seasons)

    with col2:
        st.metric("Total Drivers",total_drivers)

    with col3:
        st.metric("Total Constructors",total_constructors)

    with col4:
        st.metric("Total Races",total_races)

    races_per_year = df.groupby('Year')['Race_Name'].nunique().reset_index()
    fig1 = px.line(
        races_per_year, x = 'Year', y = 'Race_Name', markers = True, title = 'Number of Races Over Years'
    )
    st.plotly_chart(fig1)

    drivers_per_year = df.groupby('Year')['Driver'].nunique().reset_index()
    fig2 = px.line(
        drivers_per_year, x = 'Year', y = 'Driver', markers = True, title = 'Numbers of Drivers Over Years'
    )
    st.plotly_chart(fig2)

    constructors_per_year = df.groupby('Year')['Constructor'].nunique().reset_index()
    fig3 = px.line(
        constructors_per_year, x = 'Year', y = 'Constructor', markers = True, title = 'Number of Constructors Over Years'
    )
    st.plotly_chart(fig3)




    st.header("Overview")
    st.dataframe(df)

if user_menu == "Top Drivers":
    st.title("Top Drivers by Wins")

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    selected_year = st.sidebar.selectbox("Select Year",years)

    if selected_year == 'Overall':
        filtered_df = df
    else :
        filtered_df = df[df['Year'] == selected_year]

    winners = filtered_df[filtered_df['Position']==1]
    top_drivers = winners['Driver'].value_counts().reset_index()
    top_drivers.columns = ['Driver', 'Wins']
    top10 = top_drivers.head(10)

    st.dataframe(top10)

    fig = px.bar(
        top10, x = 'Driver', y = 'Wins', title = 'Top 10 Drivers by Wins'
    )

    st.plotly_chart(fig)

if user_menu == "Top Constructors":
    st.title("Top Constructors by Wins")

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,"Overall")

    selected_year = st.sidebar.selectbox("Select Year",years)
    
    if selected_year == 'Overall':
        filtered_df = df

    else :
        filtered_df =df[df['Year'] == selected_year]

    winners = filtered_df[filtered_df['Position'] == 1]
    top_constructors = winners['Constructor'].value_counts().reset_index()
    top_constructors.columns = ['Constructor', 'Wins']
    top10 = top_constructors.head(10)

    st.dataframe(top10)

    fig = px.bar(
        top10, x = 'Constructor', y = 'Wins', title = 'Top 10 Constructors by Wins'
    )
    st.plotly_chart(fig)

if user_menu == "Driver Comparison":
    st.title("Driver Comparison")

    drivers_list = df['Driver'].unique().tolist()
    drivers_list.sort()

    selected_drivers = st.multiselect("Select Drivers", drivers_list, default = drivers_list[:2])

    winners = df[df['Position']==1]

    comparison_df = winners[winners['Driver'].isin(selected_drivers)]

    comparison_df = comparison_df.groupby(['Year', 'Driver']).size().reset_index(name='Wins')

    fig = px.line(
        comparison_df, x = 'Year', y = 'Wins', color = 'Driver', markers = True, title = 'Driver Wins Over Years'
    )

    st.plotly_chart(fig)

if user_menu == "Heatmap":
    st.title("Constructor Dominance Heatmap")

    winners = df[df['Position'] == 1]

    latest_year = df['Year'].max()
    winners = winners[winners['Year'] >= latest_year-19]

    top_teams = winners['Constructor'].value_counts().head(10).index
    winners = winners[winners['Constructor'].isin(top_teams)]



    heatmap_data = winners.pivot_table(
        index = 'Constructor',
        columns = 'Year',
        aggfunc = 'size',
        fill_value = 0

    )
    fig, ax = plt.subplots(figsize=(18,6))

    sns.heatmap(
        heatmap_data,
        cmap = 'rocket_r',
        linewidths = 0.5,
        ax = ax
    )


    plt.xticks(rotation = 45)

    st.pyplot(fig)