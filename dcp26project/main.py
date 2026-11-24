import os
import sqlite3 as sql
from datetime import datetime as dt
import pandas as pd 
import matplotlib.pyplot as plt

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "My_Data.csv")

#connecting to the database and cleaning values before inserting into a table
def db_connect():
    global conn
    conn = sql.connect("gym.db")
    
    # Create Database
    if os.path.exists(CSV):
        df = pd.read_csv(CSV)
        df.to_sql('gym_statistics', conn, if_exists='replace', index=False)
    else:
        print("file not found")




def menu_interface():
    db_connect()
    while True:
        print("My Gym Statiistics")
        print("1. See SQl outputs (Questions I asked about my data)")
        print("2. View records")
        print("3. Display graphs")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sql_queries()
        elif choice == "2":
            print("")
        elif choice == "3":
            print("")
        elif choice == "4":
            print("Program exited")
            break
        else:
            print("Invalid choice. Enter number between 1 and 4")




def sql_queries():
    print("SQL QUERY RESULTS")

    print("Question 1: Does workout duration affect how much my mood improves after exercising?")
    query1 = """SELECT Duration_Minutes, [Mood_after(0-5)] - [Mood_Before(1-5)] AS Mood_Improvement
                FROM gym_statistics
                ORDER BY Duration_Minutes ASC""" 
    print(pd.read_sql_query(query1,conn))
    print("\n")

    print("question 2: Does consuming an energy drink affect my workout duration and mood improvement?")
    query2 = """SELECT EnergyDrink, Count(*) as Total_workouts, avg(Duration_Minutes) as Average_Duration, AVG([Mood_after(0-5)] - [Mood_Before(1-5)]) as Average_Mood_improvement
                FROM gym_statistics
                GROUP BY EnergyDrink"""
    print(pd.read_sql_query(query2,conn))
    print("\n")

    print("Question 3: Does the time i start my workout influence my workout duration and mood improvement?")

menu_interface()









