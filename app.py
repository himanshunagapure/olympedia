import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Import styling functions
import styling

# Set page configuration
st.set_page_config(
    page_title="Olympic Data Analysis",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
styling.load_css("styles.css") 

# Define Olympic Colors
cool_palette = ['#EDF8FB', '#B3CDE3', '#8C96C6', '#8856A7', '#810F7C']
custom_cmap = LinearSegmentedColormap.from_list('olympic_cmap', cool_palette, N=100)

# Load and preprocess data
df = pd.read_csv('olympics_dataset.csv')
regions_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, regions_df)

# Setting up Sidebar
st.sidebar.title("🏆 Olympic Analysis")
st.sidebar.image('https://cdn.britannica.com/01/23901-050-33507FA4/flag-Olympic-Games.jpg')
user_menu = st.sidebar.radio(
    'Select and option',
    ('Medal Tally', 'Overall Analysis','Country-wise')
)
# Function to set the main title with custom styling
def set_title(title):
    st.markdown(f"<h1 style='text-align: center; color: #FF5733;'>{title}</h1>", unsafe_allow_html=True)
    
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)
    
    # Determine if flag == 1 (Country-wise over All Years)
    is_country_overall = (selected_year == 'Overall') and (selected_country != 'Overall')
    
    # Determine if both country and year are specific
    is_specific_country_year = (selected_year != 'Overall') and (selected_country != 'Overall')
    
    if is_country_overall:
        # When flag == 1, default sort_by is 'Year' and no sort dropdown is displayed
        sort_by = 'Year'
    else:
        # When flag != 1, provide sort dropdown with options
        sort_options = ['Total', 'Gold', 'Silver', 'Bronze']
        sort_by = st.sidebar.selectbox('Sort By', sort_options, index=0)  # Default to 'Total'
            
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country, sort_by=sort_by)
    
    # Set the title based on selection
    if selected_year=='Overall' and selected_country=='Overall':
        st.title("Overall Tally")
    if selected_year!='Overall' and selected_country=='Overall':
        st.title("Medal Tally in Year " + str(selected_year))
    if selected_year=='Overall' and selected_country!='Overall':
        st.title(selected_country+" Overall Performance")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title("Performance of "+selected_country+" in Year "+str(selected_year))
    
    #st.table(medal_tally.style.set_properties(**{'text-align': 'center'}))
    if medal_tally.empty:
        st.warning("No data available for the selected criteria.")
    else:
        st.table(medal_tally.style.set_properties(**{'text-align': 'center'}))
        
        # Determine the type of visualization based on grouping
        if is_country_overall:
            # Country-wise over All Years: Display Line Chart sorted by 'Year'
            fig = px.line(
                medal_tally, 
                x='Year', 
                y='Total', 
                title=f'Total Medals Over the Years for {selected_country}', 
                markers=True,
                color='Total',
            )
            st.plotly_chart(fig, use_container_width=True)
        elif is_specific_country_year:
            # Specific Country in Specific Year: Display Pie Chart and Bar Chart by Sport
            
            # For the pie chart, we need to sum 'Gold', 'Silver', 'Bronze'
            medal_counts = medal_tally[['Gold', 'Silver', 'Bronze']].sum().reset_index()
            medal_counts.columns = ['Medal', 'Count']
            
            # Pie Chart: Distribution of Medal Types
            fig_pie = px.pie(
                medal_counts, 
                names='Medal', 
                values='Count', 
                title=f'Distribution of Medals for {selected_country} in {selected_year}',
                color='Medal',
                color_discrete_map={'Gold':'gold', 'Silver':'silver', 'Bronze':'#cd7f32'}
            )
            # Display the total number of medals inside the pie chart
            fig_pie.update_traces(
                textinfo='value',  # Show label, percentage, and total count
                textfont_size=14
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        else:
            # Overall Tally or Specific Year: Display Bar Chart sorted by selected criteria
            sort_label = f"{sort_by} Medals"  # For better readability in the title
            if selected_year == 'Overall':
                title = f"{sort_label} by Region"
            else:
                title = f"{sort_label} in {selected_year}"
            
            fig = px.bar(
                medal_tally, 
                x='region', 
                y=sort_by, 
                title=title, 
                color=sort_by, 
                hover_data=['Gold', 'Silver', 'Bronze', 'Total']
            )
            st.plotly_chart(fig, use_container_width=True)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] 
    cities = df['City'].unique().shape[0] 
    sports = df['Sport'].unique().shape[0] 
    events = df['Event'].unique().shape[0] 
    athletes = df['Name'].unique().shape[0] 
    nations = df['region'].unique().shape[0]
    
    st.title("🔍 Quick Overview")
    # First Row of Metrics
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric(label="🏅 Editions", value=editions)
    with col2:
        st.metric(label="🌍 Hosts", value=cities)
    with col3:
        st.metric(label="🤼‍♂️ Sports", value=sports)

    st.markdown("---")  # Horizontal Divider
        
    # Second Row of Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🎯 Events", value=events)
    with col2:
        st.metric(label="🏳️ Nations", value=nations)
    with col3:
        st.metric(label="👥 Athletes", value=athletes)
    
    #Line Graphs    
    st.markdown("<hr>", unsafe_allow_html=True)
    nations_vs_time = helper.data_vs_time(df,'region')
    #st.title('Participating Nations')
    fig = px.line(nations_vs_time, x='Year', y='region', title='Participating Nations over the Years')
    st.plotly_chart(fig, use_container_width=True)
    
    events_vs_time = helper.data_vs_time(df,'Event')
    #st.title('Events')
    fig = px.line(events_vs_time, x='Year', y='Event', title='Events over the Years')
    st.plotly_chart(fig, use_container_width=True)
    
    athletes_vs_time = helper.data_vs_time(df,'Name')
    #st.title('Athletes over the Years')
    fig = px.line(athletes_vs_time, x='Year', y='Name',title='Athletes over the Years')
    st.plotly_chart(fig, use_container_width=True)
    
    # HeatMap
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Number of Events over Time</h3>", unsafe_allow_html=True)
    pivot_df = df.drop_duplicates(['Year', 'Sport', 'Event'])
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(
        pivot_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True,
        fmt="d",
        cmap="YlGnBu",
        ax=ax
    )
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    st.pyplot(fig)
    
    #Top 15 Most Successfull Athletes
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🏅 15 Most Successful Athletes</h2>", unsafe_allow_html=True)
    #create filter
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    
    selected_sport = st.selectbox('Select a Sport', sport_list)
    most_successfull = helper.most_successful(df,selected_sport)
    st.table(most_successfull.style.set_properties(**{'text-align': 'center'}))
    
if user_menu == 'Country-wise':
    st.sidebar.title('🌐 Country-wise Analysis')
    
    #Dropdown to select country
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    
    selected_country = st.sidebar.selectbox('Select Country', country_list)
 
    #Line graph: Country's Medals over year
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal', title=f"{selected_country} Medal Tally over the years")
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap: Medals in Events over the years
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{selected_country} Event Performance </h2>", unsafe_allow_html=True)
    pt = helper.country_event_heatmap(df, selected_country)
    
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, cmap=custom_cmap, ax=ax, linewidths=.5, linecolor='gray')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    st.pyplot(fig)
    
    #Top 10 Most Successfull Athletes of a country
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>🏅 Top 10 Athletes of {selected_country}</h2>", unsafe_allow_html=True)
    top10_athletes = helper.top10_athletes_by_country(df, selected_country)
    st.table(top10_athletes.style.set_properties(**{'text-align': 'center'}))
    