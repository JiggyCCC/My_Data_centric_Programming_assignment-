import sqlite3
import csv
from datetime import datetime

#connecting to the SQL 
connectSQL = sqlite3.connect("gym_data.db")

cursor = connectSQL.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS gym_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    muscle_group TEXT,
    duration INTEGER,
    start_time TEXT,
    mood_before INTEGER,
    mood_after INTEGER,
    calories INTEGER,
    energy_drink INTEGER
)
""")

connectSQL.commit()

with open("My_Data.csv", "r") as file:
    filereader = csv.DictReader(file)
    valid_rows = 0
    invalid_rows = 0

    for row in filereader: 
        try:
            date = row["Date"].strip()
            muscle_group = row["Muscle_group"].strip()
            duration = int(row["Duration_Minutes"])
            start_time = row["start_time"].strip()
            mood_before = int(row["Mood_Before(1-5)"])
            mood_after = int(row["Mood_after(0-5)"])
            calories = int(row["Calories Consumed"])
            energy_drink = int(row["EnergyDrink"])
            datetime.strptime(date, "%d/%m/%Y")
            datetime.strptime(start_time, "%H:%M")

            if muscle_group == " ":
                raise ValueError("Missing muscle group")
            if duration <= 0:
                raise ValueError("invalid Duration")
            if mood_before < 1 or mood_before > 5:
                raise ValueError("Mood before must be 1-5")
            if mood_after < 1 or mood_after > 5:
                raise ValueError("Mood after must be 0-5")
            if calories <= 0:
                raise ValueError("invalid calories")
            if energy_drink not in [0, 1]:
                raise ValueError("Energy Drink must be 0 or 1")

            cursor.execute("""
            INSERT INTO gym_sessions
            (date, muscle_group, duration, start_time, mood_before, mood_after, calories, energy_drink)
            Values (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                date, muscle_group, duration, start_time, mood_before, mood_after, calories, energy_drink
            ))

            valid_rows += 1
        except (ValueError, KeyError) as error:
            print("Invalid row:", row)
            print("Reason:", error)

            invalid_rows += 1   

