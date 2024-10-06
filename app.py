import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('olympics_dataset.csv')
regions_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, regions_df)

st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select and option',
    ('Medal Tally', 'Overall Analysis','Country-wise','Athlete-wise')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)
    
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in Year " + str(selected_year))
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+" Overall Performance")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title("Performance of "+selected_country+" in Year "+str(selected_year))
    
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] 
    cities = df['City'].unique().shape[0] 
    sports = df['Sport'].unique().shape[0] 
    events = df['Event'].unique().shape[0] 
    athletes = df['Name'].unique().shape[0] 
    nations = df['region'].unique().shape[0]
    
    st.title("Quick Overview")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions) 
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
        
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events) 
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    
    #Line Graphs    
    nations_vs_time = helper.data_vs_time(df,'region')
    st.title('Participating Nations over the Years')
    fig = px.line(nations_vs_time, x='Year', y='region')
    st.plotly_chart(fig)
    
    events_vs_time = helper.data_vs_time(df,'Event')
    st.title('Events over the Years')
    fig = px.line(events_vs_time, x='Year', y='Event')
    st.plotly_chart(fig)
    
    athletes_vs_time = helper.data_vs_time(df,'Name')
    st.title('Athletes over the Years')
    fig = px.line(athletes_vs_time, x='Year', y='Name')
    st.plotly_chart(fig)
    
    #HeatMap
    st.title("No of Events over Time")
    pivot_df = df.drop_duplicates(['Year','Sport','Event'])
    fig,ax = plt.subplots(figsize=(25,25))
    ax = sns.heatmap(pivot_df.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)
    
    #Top 15 Most Successfull Athletes
    st.title('Most Successfull Athletes')
    #create filter
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    
    selected_sport = st.selectbox('Select a Sport', sport_list)
    most_successfull = helper.most_successful(df,selected_sport)
    st.table(most_successfull)