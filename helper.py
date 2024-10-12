import pandas as pd
import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal', 'region'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    
    medal_tally[['Gold', 'Silver', 'Bronze', 'Total']] = medal_tally[['Gold', 'Silver', 'Bronze', 'Total']].apply(lambda x: x.astype(int))
    
    return medal_tally

def country_year_list(df):
    #Create filter for years
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    
    #Create filter for years
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    
    return years,country

#Functions which accepts year and country
def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal', 'region'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == int(year))]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold', ascending=False).reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x[['Gold', 'Silver', 'Bronze', 'Total']] = x[['Gold', 'Silver', 'Bronze', 'Total']].apply(lambda r: r.astype(int))

    return x

def data_vs_time(df,col):
    nations_vs_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_vs_time.rename(columns = {'count' : col},inplace = True)
    return nations_vs_time

#Finding list of most successfull athletes
def most_successful(df,sport):
    # Remove athletes with no medals
    temp_df = df.dropna(subset=['Medal'])
    
    # Filter by sport if specified, otherwise keep all sports
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    # Create a new column for total medals
    temp_df['Total_Medals'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']

    # Group by athlete name and sum their medals
    athlete_medals = temp_df.groupby(['Name'])['Total_Medals'].sum().reset_index()
    # Merge with original df to get 'Sport' and 'region' information
    x = athlete_medals.merge(df[['Name', 'Sport', 'region']].drop_duplicates(), on='Name', how='left')

    # Drop duplicate athlete entries to show unique athletes with their sports
    x = x[['Name', 'Total_Medals', 'Sport', 'region']].drop_duplicates('Name')
    # Sort athletes by total medals in descending order and get the top 15
    x = x.sort_values(by='Total_Medals', ascending=False).head(15)
    
    return x

# Country-wise medal tally per year(lineplot)
def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'], inplace=True)    
    new_temp_df = temp_df[temp_df['region'] == country]
    final_temp_df = new_temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_temp_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'], inplace=True)    
    new_temp_df = temp_df[temp_df['region'] == country]
    pt = new_temp_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')
    return pt

#Top 10 most successfull athletes of a country
def top10_athletes_by_country(df,country):
    temp_df = df.dropna(subset=['Medal'])

    # Filter for the specified country (e.g., 'USA')
    temp_df = temp_df[temp_df['region'] == country]
    
    # Create a new column for total medals
    temp_df['Total_Medals'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    
    # Group by athlete name and sum their medals
    athlete_medals = temp_df.groupby(['Name','Sport'])['Total_Medals'].sum().reset_index()
    
    # Sort athletes by total medals in descending order and get the top 10
    top_10_athletes = athlete_medals.sort_values(by='Total_Medals', ascending=False).head(10)
    return top_10_athletes

