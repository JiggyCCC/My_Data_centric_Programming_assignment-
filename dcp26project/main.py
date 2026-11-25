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
        print("\nMy Gym Statiistics")
        print("1. See SQl outputs (Questions I asked about my data)")
        print("2. Display Graphs")
        print("3. View Records and add your own")
        print("4. Exit\n")

        choice = input("Enter your choice: ")

        if choice == "1":
            sql_queries()
        elif choice == "2":
            graph_menu()
        elif choice == "3":
            view_records_menu()
        elif choice == "4":
            print("Program exited")
            break
        else:
            print("Invalid choice. Enter number between 1 and 4")




def sql_queries():
    print("\nSQL QUERY RESULTS\n")

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
        if choice == "1":
            graph1()
        elif choice == "2":
            graph2()
        elif choice == "3":
            graph3()
        elif choice == "4":
            graph4()
        elif choice == "5":
            break
        else:
            print("invalid input.")


def graph1():

    df = pd.read_sql("SELECT * FROM gym_statistics", conn)

    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])

    #Workout duration vs modd improvement 
    plt.figure()
    plt.scatter(df['Duration_Minutes'], df['Mood_Improvement'], s=30, alpha=0.5)
    plt.xlabel("Workout Duration (Minutes)")
    plt.ylabel("Mood Improvement")
    plt.title("Woekout Duration vs Mood Improvement")
    plt.show()

    graph_menu()

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

    graph_menu()

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

    graph_menu()

def graph4():
    df = pd.read_sql("SELECT * FROM gym_statistics", conn)
    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])

    plt.figure()
    plt.hist(df['Duration_Minutes'], bins=10, edgecolor='black')
    plt.xlabel("Workout Duration (Minutes)")
    plt.ylabel("Number of Workouts")
    plt.title("Distribution of workout durations")
    plt.show()

    graph_menu()

def view_records_menu():
    while True:
        print("\nRecords menu")
        print("1. Means Max and Mins")
        print("2. Add your workout:")
        print("3. Filter records")
        print("4. return to menu")

        choice = input("select an option: ")
        if choice == "1":
            column_stats()
        elif choice == "2":
            sql_user_queries()
        elif choice == "3":
            filter_records_menu()
        elif choice == "4":
            break
        else:
            print("invalid input.")


def column_stats():

    df = pd.read_sql("SELECT * FROM gym_statistics", conn)

    print("\nColumn stats for Duration_Minutes:\n\n ")
    print("average:", df['Duration_Minutes'].mean())
    print("Max:", df['Duration_Minutes'].max())
    print("Min:", df['Duration_Minutes'].min())

    print("\ncalories Consumed")
    print("average:", df['Calories Consumed'].mean())
    print("Max:", df['Calories Consumed'].max())
    print("min", df['Calories Consumed'].min())

    print("\naverage mood improvment per muscle group")
    df['Mood_Improvement'] = (df['Mood_after(0-5)'] - df['Mood_Before(1-5)'])
    avg = df.groupby('Muscle_group')['Mood_Improvement'].mean()
    print(avg)


def filter_records_menu():

    df = pd.read_sql("SELECT * FROM gym_statistics", conn)

    print("\nFILTER RECORDS")
    print("1. Filter by muscle group")
    print("2. Workouts over 60 minutes")
    print("3. Energy drink consumption")

    choice = input("Select an option: ")

    if choice == "1":
        print("muscle groups = Push, Pull, Legs, ShoulderArm, ChestBack")
        group = input("Enter muscle group: ").strip()
        filtered = df[df['Muscle_group'] == group]

        if filtered.empty:
            print("No matching records found.")
        else:
            print(filtered.to_string(index=False))

    elif choice == "2":
        filtered = df[df['Duration_Minutes'] > 60]
        print(filtered.to_string(index=False))

    elif choice == "3":
        filtered = df[df['EnergyDrink'] == 1]
        print(filtered.to_string(index=False))

    else:
        print("Invalid choice!")



def sql_user_queries():

    print("\nAdd your workout")
    date = input("Enter date (DD/MM/YYYY): ")
    try:
        dt.strptime(date, "%d/%m/%Y")
    except ValueError:
        print("Invlaid Date Format")
        return

    muscle = input("Enter muscle group (Push, Pull, Legs, ShoulderArm, ChestBack): ").strip().title()
    if muscle not in ["Push", "Pull", "Legs", "ShoulderArm", "ChestBack"]:
        print("Invalid")
        return

    try:
        duration = int(input("Enter workout duration in minutes: "))
        mood_before = int(input("Enter mood before (1-5): "))
        mood_after = int(input("Enter mood after (0-5): "))
        calories = int(input("Enter calories consumed: "))
        energy = int(input("Energy drink? (1 = Yes, 0 = No): "))

    except ValueError:
        print("Please enter numbers where required!")
        return
    if duration <= 0 or duration > 130:
        print("Invalid workout duration!")
        return
    if not 1 <= mood_before <= 5:
        print("Mood before must be between 1 and 5!")
        return
    if not 0 <= mood_after <= 5:
        print("Mood after must be between 0 and 5!")
        return
    if calories <= 0:
        print("Calories must be greater than zero!")
        return
    if energy not in [0, 1]:
        print("Energy drink must be 0 or 1!")
        return

    start = input("Enter your start time (HH:MM): ")
    try:
        dt.strptime(start, "%H:%M")
    except ValueError:
        print("Invalid time format!")
        return

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO gym_statistics
        (Date, Muscle_group, Duration_Minutes, start_time, [Mood_Before(1-5)], [Mood_after(0-5)], [Calories Consumed], EnergyDrink)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (date, muscle, duration, start, mood_before,
          mood_after, calories, energy))

    print("workout successfully added!")


menu_interface()