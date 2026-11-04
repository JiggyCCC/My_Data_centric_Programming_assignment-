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
            mood_after


