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
    temp_df = df.dropna(subset=['Medal']) #Remove athletes with no medals
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count' :'Medals'},inplace=True)
    return x


