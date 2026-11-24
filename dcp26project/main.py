import os
import sqlite3
from datetime import datetime as dt
import pandas as pd 
import matplotlib.pyplot as plt

CSV = "My_Data.csv"

def data_connect():
    global conn
    conn = sqlite3.connect("gym.db")

    if os.path.exists(CSV):
        df = pd.read_csv(CSV)
        df.to_sql('gym_statisitcs', conn, if_exists='replace', index=False)







