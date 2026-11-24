import os
import sqlite3
from datetime import datetime as dt
import pandas as pd 
import matplotlib.pyplot as plt

CSV = "My_Data.csv"

#connecting to the database and cleaning values before inserting into a table
def data_connect():
    global conn
    conn = sqlite3.connect("gym.db")

    if os.path.exists(CSV):
        df = pd.read_csv(CSV)

        #cleaning data (missing values, duplicates, and changing data column type)
        df = df.dropna() 
        df = df.drop_duplicates()
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
        df['Duration_Minutes'] = pd.to_numeric(df['Duration_Minutes'], errors='coerce')
        df['CaloriesConsumed'] = pd.to_numeric(df['CaloriesConsumed'], errors='coerce')

        df=df[
            (df['Duration_Minutes'] > 0) &
            (df['Duration_minutes'] <=130) &
            (df['Mood_Before(1-5)'].between(1, 5)) &
            (df['Mood_after(0-5)'].between(0, 5)) &
            (df['EnergyDrink'].isin([0, 1])) &
            (df['Calories Consumed'] > 0)
        ]

        #load data in SQL database
        df.to_sql('gym_statisitcs', conn, if_exists='replace', index=False)
    else:
        print("CSV file not found")




data_connect()









