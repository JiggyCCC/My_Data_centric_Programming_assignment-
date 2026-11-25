import os
import sqlite3 as sql
from datetime import datetime as dt
import pandas as pd 
import matplotlib.pyplot as plt

CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "My_Data.csv")

#connecting to the database and replacing table if it already exists
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
        print("2. Display Graphs")
        print("3. View Records")
        print("4. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            sql_queries()
        elif choice == "2":
            graph_menu()
        elif choice == "3":
            print("")
        elif choice == "4":
            print("Program exited")
            break
        else:
            print("Invalid choice. Enter number between 1 and 4")




def sql_queries():
    print("SQL QUERY RESULTS\n")

    print("Question 1: Does workout duration affect how much my mood improves after exercising?")
    query1 = """SELECT Duration_Minutes, [Mood_after(0-5)] - [Mood_Before(1-5)] AS Mood_Improvement
                FROM gym_statistics
                ORDER BY Duration_Minutes ASC""" 
    print(pd.read_sql_query(query1, conn))
    print("\n")

    print("question 2: Does consuming an energy drink affect my workout duration and mood improvement?")
    query2 = """SELECT EnergyDrink, Count(*) as Total_workouts, avg(Duration_Minutes) as Average_Duration, AVG([Mood_after(0-5)] - [Mood_Before(1-5)]) as Average_Mood_improvement
                FROM gym_statistics
                GROUP BY EnergyDrink"""
    print(pd.read_sql_query(query2, conn))
    print("\n")

    print("Question 3: Does the time i start my workout influence my workout duration and mood improvement?")
    query3 = """SELECT start_time, AVG(Duration_Minutes) AS Average_Duration, AVG([Mood_after(0-5)] - [Mood_Before(1-5)]) as Mood_Improvement
                FROM gym_statistics
                GROUP BY start_time
                ORDER BY start_time ASC"""
    print(pd.read_sql_query(query3, conn))



def graph_menu():
    while True: 
        print("\nGRAPH MENU")
        print("1. Workout Duration vs Mood Improvement")
        print("2. Energy Drinks vs Workout Performance")
        print("3. Workout Start Time vs Duration")
        print("4. Workout Start Time vs Mood Improvement")
        print("5. Return to menu")

        choice = input("select a graph: ")
        if choice == 1:
            graph1()
        elif choice == 2:
            graph2()
        elif choice == 3:
            graph3()
        elif choice == 4:
            graph4()
        elif choice == 5:
            menu_interface()
        else:
            print("invalid input.")


def graph1():

    df = pd.read_sql("SELECT * FROM gym_statistics", conn)

    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])

    # Woekout duration vs modd improvement 
    plt.figure()
    plt.scatter(df['Duration_Minutes'], df['Mood_Improvement'], s=30, alpha=0.5)
    plt.xlabel("Workout Duration (Minutes)")
    plt.ylabel("Mood Improvement")
    plt.title("Woekout Duration vs Mood Improvement")
    plt.show()

def graph2():
    df = pd.read_sql("SELECT * FROM gym_statistics", conn)
    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])

    avg = df.groupby('EnergyDrink')[['Duration_Minutes', 'Mood_Improvement']].mean()
    avg.plot(kind='bar')
    plt.xlabel("Energy Drink (0=no, 1 =yes)")
    plt.ylabel("Average Value")
    plt.title("Energy Drinks vs Workout Perfromance")
    plt.legend(["Workout Duration", "Mood Improvement"])
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def graph3():
    df = pd.read_sql("SELECT * FROM gym_statistics", conn)
    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])

    plt.figure()
    plt.scatter(df['start_time'], df['Duration_Minutes'], s=30, alpha=0.5)
    plt.xlabel("Workout Start Time")
    plt.ylabel("Workout Duration (minutes)")
    plt.title("Workout Start Time Vs Workout Duration")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graph4():
    df = pd.read_sql("SELECT * FROM gym_statistics", conn)
    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])

    plt.figure()
    plt.hist(df['Duration_Minutes'], bins=10, edgecolor='black')
    plt.xlabel("Workout Duration (Minutes)")
    plt.ylabel("Number of Workouts")
    plt.title("Distribution of workout durations")
    plt.show()

menu_interface()










