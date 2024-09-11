from nltk.sentiment import SentimentIntensityAnalyzer
import sqlite3
import datetime


def load_chat_history():
    history = []
    time = []
    conn = sqlite3.connect("HISTORY.db")
    cursor = conn.execute("SELECT USER_MESSAGE,TIME FROM HIST;")
    for row in cursor:
        history.append(row[0])
        time.append(row[1])
    conn.close()
    return history,time


history,time = load_chat_history()

def mood_score(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    # Compound score is a normalized score ranging from -1 to 1
    sentiment_score = sentiment["compound"]
    # Convert to mood score (e.g., 1 to 10 scale)
    mood_score = (sentiment_score + 1) * 5  # Scale: 0 to 10
    return mood_score


def save_mood_score():
    id = 0
    conn = sqlite3.connect("mood_tracker.db")
    
    # Check if the MOOD table exists
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='MOOD';")
    result = cursor.fetchone()
    
    if result is None:
        # If the table does not exist, create it
        cur = conn.cursor()
        query = "CREATE TABLE MOOD (ID INTEGER PRIMARY KEY, MESSAGE TEXT, MOOD_SCORE REAL, TIME TEXT)"
        cur.execute(query)
        conn.commit()
    
    # Iterate through history and insert only if no duplicate is found
    for i in range(len(history)):
        if int(mood_score(history[i])) != 5:
            # Check for duplicates based on MESSAGE and TIME
            cursor = conn.execute("SELECT 1 FROM MOOD WHERE MESSAGE = ? AND TIME = ?", (history[i], time[i]))
            duplicate = cursor.fetchone()
            
            if duplicate is None:
                # Insert if no duplicate found
                conn.execute(
                    """
                    INSERT INTO MOOD (MESSAGE, MOOD_SCORE, TIME)
                    VALUES (?, ?, ?)
                    """,
                    (history[i], round(mood_score(history[i]), 2), time[i])
                )
                conn.commit()
    
    conn.close()

