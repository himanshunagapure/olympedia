import pandas as pd

def preprocess(df, regions_df):
    #Merge both datasets
    df = df.merge(regions_df, on='NOC', how='left')
    # Assigning player_id based on player_name
    df['id'] = df.groupby('Name').ngroup() + 1
    #One hot encoding for Medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis = 1)

    return df

